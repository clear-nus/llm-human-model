#!/usr/bin/python2

import xml.etree.ElementTree
import sys
import ast

class LoadPolicy:
    def __init__(self, policyfile):
        self.policy = xml.etree.ElementTree.parse(policyfile).getroot()
        # for bottles and glass
        self.numstates = 5

    def FindOptimalAction(self, bel, obs_state):
        opt_value = -999999
        opt_action = -1
        for neighbor in self.policy.iter('Vector'):
            action = int(neighbor.attrib['action'])
            obsValue = int(neighbor.attrib['obsValue'])
            avec =  self.line2list(neighbor.text)
            value = 0
            if self.obsStateMatch(obs_state, obsValue):
                for i in range(len(avec)):
                    value += avec[i] * bel[i]
                if value > opt_value:
                    opt_value = value
                    opt_action = action

        if opt_action == -1:
            # print 'did not find the action!'
            # sys.exit(0)
            pass

        return opt_action
    
    def obsStateMatch(self, state, value):
        temp = 0
        for i in range(len(state)):
            # temp += state[i] * pow(4, 4 - i)
            temp += state[i] * pow(4, self.numstates - i - 1)

        return temp == value

    def line2list(self, ss):
        vec1 = ss.split(' ')
        vec = []
        for i in range(7):
            vec.append(float(vec1[i]))
        return vec

if __name__ == "__main__":
    policyfile = sys.argv[1]
    policy = LoadPolicy(policyfile)
    bel = [0.0, 0.092105263157894732, 0.11842105263157894, 0.17105263157894737, 0.35526315789473684, 0.25, 0.013157894736842105]
    # model trust
    # print policy.FindOptimalAction(bel, [0, 0, 0, 0, 0])
    # print policy.FindOptimalAction(bel, [1, 0, 0, 0, 0])
    # print policy.FindOptimalAction(bel, [1, 1, 0, 0, 0])
    # print policy.FindOptimalAction(bel, [1, 1, 1, 0, 0])
    # print policy.FindOptimalAction(bel, [1, 1, 1, 1, 0])

    # baseline
    # print policy.FindOptimalAction(bel, [0, 0, 0, 0, 0])
    # print policy.FindOptimalAction(bel, [0, 0, 0, 0, 1])

    # trust maximize
    print policy.FindOptimalAction(bel, [0, 0, 0, 0, 0])
    print policy.FindOptimalAction(bel, [0, 0, 1, 0, 0])
    # print policy.FindOptimalAction(bel, [0, 1, 1, 0, 0])
    print policy.FindOptimalAction(bel, [1, 0, 1, 0, 0])
    print policy.FindOptimalAction(bel, [1, 1, 1, 0, 0])
    # print policy.FindOptimalAction(bel, [1, 1, 1, 1, 0])

    # print policy.FindOptimalAction(bel, [0, 0, 0, 0, 0])
