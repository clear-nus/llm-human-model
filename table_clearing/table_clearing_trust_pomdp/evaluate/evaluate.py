#!/usr/bin/python2
import sys
from math import *
from loadPolicy import *
from numpy import *
import random
from tqdm import tqdm
import numpy as np
import llm_policy
import pandas as pd

class TableClearing:

    def __init__(self, policy, initbel, numruns, llm_q_dict=None):
        self.discount = 0.99        #reward discount value
        self.spSuccessBottle = 1
        self.spSuccessCan = 2
        self.spSuccessGlass = 3
        self.spFailBottle = 0
        self.spFailCan = -4
        self.spFailGlass = -9
        self.intervene = 0

        self.numTrustLevels = 7

        self.numObjects = 5
        self.numObjStates = pow(4, 5) + 1
        self.numStatus = 4

        self.largePenalty = -9999999

        self.trustDyna, self.humanBehav = self.InitTrustDyna()

        self.policy = policy
        self.initbel = initbel
        self.numruns = numruns

        # LLM stuff
        self.history = []
        self.llm_q_dict = llm_q_dict

        self.verbose = 0

    def InitTrustDyna(self):
        hBehav = {'Fish Can': array([[ 0.5       ,  0.5       ],
        [ 0.40196078,  0.59803922],
        [ 0.17213115,  0.82786885],
        [ 0.33443709,  0.66556291],
        [ 0.26821192,  0.73178808],
        [ 0.104811  ,  0.895189  ],
        [ 0.17213115,  0.82786885]]),
 'Glass Cup': array([[ 0.5       ,  0.5       ],
        [ 0.66129032,  0.33870968],
        [ 0.5       ,  0.5       ],
        [ 0.4378882 ,  0.5621118 ],
        [ 0.5       ,  0.5       ],
        [ 0.41408935,  0.58591065],
        [ 0.00617284,  0.99382716]]),
 'Water Bottle': array([[ 0.40196078,  0.59803922],
        [ 0.12732919,  0.87267081],
        [ 0.00819672,  0.99180328],
        [ 0.09510358,  0.90489642],
        [ 0.04991817,  0.95008183],
        [ 0.07746479,  0.92253521],
        [ 0.11538462,  0.88461538]])}

        trustDyna = {(0,
  'Fish Can'): array([[ 0.4       ,  0.1       ,  0.1       ,  0.1       ,  0.1       ,
          0.1       ,  0.1       ],
        [ 0.02      ,  0.48      ,  0.42      ,  0.02      ,  0.02      ,
          0.02      ,  0.02      ],
        [ 0.03333333,  0.03333333,  0.8       ,  0.03333333,  0.03333333,
          0.03333333,  0.03333333],
        [ 0.00909091,  0.00909091,  0.00909091,  0.94545455,  0.00909091,
          0.00909091,  0.00909091],
        [ 0.01111111,  0.01111111,  0.01111111,  0.23333333,  0.71111111,
          0.01111111,  0.01111111],
        [ 0.01428571,  0.01428571,  0.01428571,  0.01428571,  0.3       ,
          0.62857143,  0.01428571],
        [ 0.03333333,  0.03333333,  0.03333333,  0.03333333,  0.03333333,
          0.03333333,  0.8       ]]),
 (0,
  'Glass Cup'): array([[ 0.4       ,  0.1       ,  0.1       ,  0.1       ,  0.1       ,
          0.1       ,  0.1       ],
        [ 0.02      ,  0.88      ,  0.02      ,  0.02      ,  0.02      ,
          0.02      ,  0.02      ],
        [ 0.02      ,  0.02      ,  0.48      ,  0.42      ,  0.02      ,
          0.02      ,  0.02      ],
        [ 0.14      ,  0.00666667,  0.00666667,  0.82666667,  0.00666667,
          0.00666667,  0.00666667],
        [ 0.00588235,  0.00588235,  0.00588235,  0.59411765,  0.25882353,
          0.12352941,  0.00588235],
        [ 0.004     ,  0.004     ,  0.004     ,  0.004     ,  0.324     ,
          0.656     ,  0.004     ],
        [ 0.1       ,  0.1       ,  0.1       ,  0.1       ,  0.1       ,
          0.1       ,  0.4       ]]),
 (0,
  'Water Bottle'): array([[ 0.88      ,  0.02      ,  0.02      ,  0.02      ,  0.02      ,
          0.02      ,  0.02      ],
        [ 0.02      ,  0.88      ,  0.02      ,  0.02      ,  0.02      ,
          0.02      ,  0.02      ],
        [ 0.1       ,  0.1       ,  0.4       ,  0.1       ,  0.1       ,
          0.1       ,  0.1       ],
        [ 0.00909091,  0.19090909,  0.00909091,  0.76363636,  0.00909091,
          0.00909091,  0.00909091],
        [ 0.01428571,  0.01428571,  0.01428571,  0.3       ,  0.62857143,
          0.01428571,  0.01428571],
        [ 0.00769231,  0.00769231,  0.00769231,  0.00769231,  0.31538462,
          0.64615385,  0.00769231],
        [ 0.03333333,  0.03333333,  0.03333333,  0.03333333,  0.03333333,
          0.03333333,  0.8       ]]),
 (1,
  'Fish Can'): array([[ 0.4       ,  0.1       ,  0.1       ,  0.1       ,  0.1       ,
          0.1       ,  0.1       ],
        [ 0.3       ,  0.34285714,  0.3       ,  0.01428571,  0.01428571,
          0.01428571,  0.01428571],
        [ 0.00909091,  0.00909091,  0.03636364,  0.55454545,  0.37272727,
          0.00909091,  0.00909091],
        [ 0.0047619 ,  0.0047619 ,  0.0047619 ,  0.3047619 ,  0.67142857,
          0.0047619 ,  0.0047619 ],
        [ 0.00434783,  0.00434783,  0.00434783,  0.00434783,  0.62608696,
          0.35217391,  0.00434783],
        [ 0.00188679,  0.00188679,  0.00188679,  0.00188679,  0.00188679,
          0.7245283 ,  0.26603774],
        [ 0.00909091,  0.00909091,  0.00909091,  0.00909091,  0.00909091,
          0.00909091,  0.94545455]]),
 (1,
  'Glass Cup'): array([[ 0.4       ,  0.1       ,  0.1       ,  0.1       ,  0.1       ,
          0.1       ,  0.1       ],
        [ 0.03333333,  0.13333333,  0.7       ,  0.03333333,  0.03333333,
          0.03333333,  0.03333333],
        [ 0.02      ,  0.02      ,  0.48      ,  0.42      ,  0.02      ,
          0.02      ,  0.02      ],
        [ 0.00526316,  0.00526316,  0.00526316,  0.54736842,  0.32105263,
          0.11052632,  0.00526316],
        [ 0.00588235,  0.00588235,  0.00588235,  0.00588235,  0.49411765,
          0.47647059,  0.00588235],
        [ 0.00285714,  0.00285714,  0.00285714,  0.00285714,  0.00285714,
          0.69714286,  0.28857143],
        [ 0.00588235,  0.00588235,  0.00588235,  0.00588235,  0.00588235,
          0.00588235,  0.96470588]]),
 (1,
  'Water Bottle'): array([[  5.71428571e-02,   3.00000000e-01,   1.42857143e-02,
           5.85714286e-01,   1.42857143e-02,   1.42857143e-02,
           1.42857143e-02],
        [  3.44827586e-03,   6.34482759e-01,   2.10344828e-01,
           1.41379310e-01,   3.44827586e-03,   3.44827586e-03,
           3.44827586e-03],
        [  7.69230769e-03,   7.69230769e-03,   3.38461538e-01,
           6.23076923e-01,   7.69230769e-03,   7.69230769e-03,
           7.69230769e-03],
        [  2.16494845e-02,   1.03092784e-03,   1.03092784e-03,
           6.84536082e-01,   2.27835052e-01,   6.28865979e-02,
           1.03092784e-03],
        [  8.54700855e-04,   8.54700855e-04,   8.54700855e-04,
           8.54700855e-04,   5.33333333e-01,   4.45299145e-01,
           1.79487179e-02],
        [  6.89655172e-04,   6.89655172e-04,   6.89655172e-04,
           6.89655172e-04,   5.58620690e-02,   8.44137931e-01,
           9.72413793e-02],
        [  5.88235294e-03,   5.88235294e-03,   5.88235294e-03,
           5.88235294e-03,   5.88235294e-03,   5.88235294e-03,
           9.64705882e-01]])}

        return trustDyna, hBehav

    def InitState(self):
        return [0, 0, 0, 0, 0]

    def Sample(self, bel):
        val = random.random()
        temp = 0
        for i in range(len(bel)):
            temp += bel[i]
            if val < temp:
                return i

    def humanAction(self, act):
        prob = [0.0, 0.0]
        if act < 3:
            prob[0] = self.humanBehav['Water Bottle'][self.trust][0]
        elif act == 3:
            prob[0] = self.humanBehav['Fish Can'][self.trust][0]
        else:
            prob[0] = self.humanBehav['Glass Cup'][self.trust][0]

        prob[1] = 1.0 - prob[0]

        return self.Sample(prob)

    def get_llm_action(self):
        assert np.count_nonzero(self.state) == len(self.history)
        found_nodes = []
        for node, q_value in self.llm_q_dict.items():
            if node.history == self.history:
                found_nodes.append(node)
        assert len(found_nodes) == 1
        found_node = found_nodes[0]
        llm_action = max(self.llm_q_dict[found_node], key=self.llm_q_dict[found_node].get)
        action = -1

        if llm_action == 'plastic bottle':
            valid_bottle = False
            for s_idx, s in enumerate(self.state[:3]):
                if s == 0:
                    action = s_idx
                    valid_bottle = True
                    break
            assert valid_bottle
        elif llm_action == 'fish can':
            assert self.state[3] == 0
            action = 3
        else:
            assert llm_action == 'wine glass'
            assert self.state[4] == 0
            action = 4
        assert action != -1
        return action

    def step(self):
        if self.llm_q_dict is not None:
            action = self.get_llm_action()
        else:
            action = self.policy.FindOptimalAction(self.bel, self.state)

        hact = self.humanAction(action)
        robot_action_list = ['plastic bottle', 'plastic bottle', 'plastic bottle', 'fish can', 'wine glass']
        reward = 0

        if self.verbose > 0:
            print 'action: ', action
            print 'human action: ', hact

        if self.state[action] != 0:
            if self.verbose > 0:
                print 'invalid action'
            return False, self.largePenalty

        else:
            if hact == 1:
                # stay put
                self.state[action] = 1
                if action < 3:
                    reward = self.spSuccessBottle
                    self.stay_put_count[0] += 1
                elif action == 3:
                    reward = self.spSuccessCan
                    self.stay_put_count[1] += 1
                else:
                    reward = self.spSuccessGlass
                    self.stay_put_count[2] += 1
            else:
                # intervene
                self.state[action] = 3
            self.nextTrust(action, hact)
            self.updateBel(action, hact)

            self.history.append((robot_action_list[action], hact != 1, True))

            if self.verbose > 0:
                print 'state: ', self.state
                print 'trust: ', self.trust
                print 'belief: ', self.bel

            if self.end():
                return True, reward
            else:
                return False, reward

    def nextTrust(self, act, hact):
        newTrustDistri = None
        if act < 3:
            newTrustDistri = self.trustDyna[hact, 'Water Bottle'][self.trust]
        elif act == 3:
            newTrustDistri = self.trustDyna[hact, 'Fish Can'][self.trust]
        else:
            newTrustDistri = self.trustDyna[hact, 'Glass Cup'][self.trust]
        self.trust = self.Sample(newTrustDistri)

    def get_next_belief(self, cur_belief, robot_action, human_action):
        temp_bel = cur_belief

        obj = None
        if robot_action == 'plastic bottle':
            obj = 'Water Bottle'
        elif robot_action == 'fish can':
            obj = 'Fish Can'
        else:
            assert robot_action == 'wine glass'
            obj = 'Glass Cup'

        weights = []
        for i in range(len(temp_bel)):
            weights.append(temp_bel[i] * self.humanBehav[obj][i][human_action])
        temp_bel = self.normalizeBel(weights)

        # evolve trust
        newDistri = zeros(7)
        for tr in range(len(temp_bel)):
            newTrustDistri = None
            if obj == 'Water Bottle':
                newTrustDistri = self.trustDyna[human_action, 'Water Bottle'][tr]
            elif obj == 'Fish Can':
                newTrustDistri = self.trustDyna[human_action, 'Fish Can'][tr]
            else:
                assert obj == 'Glass Cup'
                newTrustDistri = self.trustDyna[human_action, 'Glass Cup'][tr]
            newTrustDistri = array(newTrustDistri)
            newDistri = newDistri +  newTrustDistri * temp_bel[tr]

        return self.normalizeBel(newDistri)

    def updateBel(self, act, hact):
        temp_bel = self.bel
        # print 'temp_bel: ', temp_bel

        obj = None
        if act < 3:
            obj = 'Water Bottle'
        elif act == 3:
            obj = 'Fish Can'
        else:
            obj = 'Glass Cup'

        weights = []
        for i in range(len(temp_bel)):
            weights.append(temp_bel[i] * self.humanBehav[obj][i][hact])
        temp_bel = self.normalizeBel(weights)

        # print 'temp_bel: ', temp_bel
        # evolve trust
        newDistri = zeros(7)
        for tr in range(len(temp_bel)):
            newTrustDistri = None
            if act < 3:
                newTrustDistri = self.trustDyna[hact, 'Water Bottle'][tr]
            elif act == 3:
                newTrustDistri = self.trustDyna[hact, 'Fish Can'][tr]
            else:
                newTrustDistri = self.trustDyna[hact, 'Glass Cup'][tr]
            newTrustDistri = array(newTrustDistri)
            newDistri = newDistri +  newTrustDistri * temp_bel[tr]

        self.bel = self.normalizeBel(newDistri)

    def normalizeBel(self, bel):
        sum_bel = 0
        nbel = bel
        for i in range(len(bel)):
            sum_bel += bel[i]

        for i in range(len(bel)):
            nbel[i] = bel[i] / sum_bel

        return nbel

    def end(self):
        a = 1
        for i in range(len(self.state)):
            a *= self.state[i]
        if a > 0:
            return True
        else:
            return False

    def run(self):
        self.state = self.InitState()
        self.bel = self.initbel
        self.history = []
        self.trust = self.Sample(self.initbel)
        reward = 0
        terminal = False

        if self.verbose > 0:
            print 'state: ', self.state
            print 'bel: ', self.bel
            print 'trust: ', self.trust

        i = 0
        total_reward = 0
        undis_total_reward = 0
        trust_vec = []
        self.stay_put_count = zeros(3)
        while not terminal:
            if self.verbose > 0:
                print '========= ', i+1, 'the step ============='
            trust_vec.append(self.trust)
            terminal, reward = self.step()
            total_reward += reward * pow(self.discount, i)
            undis_total_reward += reward
            i += 1

        trust_vec.append(self.trust)

        return total_reward, undis_total_reward, trust_vec

    def runs(self):
        discounted_return = []
        undiscounted_return = []
        trust_evolve = []
        stayput_count = zeros(3)
        total_obj_counts = array([self.numruns * 3, self.numruns, self.numruns])
        for i in range(numruns):
            if self.verbose > 0:
                print '######## starting ', i+1, 'th run ################'
            total_reward, undis_total_reward, trust_vec = self.run()
            discounted_return.append(total_reward)
            undiscounted_return.append(undis_total_reward)
            trust_evolve.append(trust_vec)
            stayput_count = stayput_count + self.stay_put_count
            if self.verbose > 0:
                print '######## end ', i+1, 'th run ################'

        print '*************** results ***********************'
        print '#### return #####'
        # print 'discounted return: ', discounted_return
        print 'mean return: ', mean(discounted_return)
        print 'std: ', 1.96 * std(discounted_return) / sqrt(len(discounted_return))

        print '##### intervention ratio #####'
        print 'intervene ratio: ', array([1, 1, 1]) - stayput_count / total_obj_counts

        # print '#### trust evolve along time #####'
        # trust_evolve = array(trust_evolve)
        # for i in range(len(trust_evolve[0])):
        #     print i, 'th step: '
        #     mean_trust = mean(trust_evolve[:, i])
        #     std_err = 1.96 * std(trust_evolve[:, i]) / sqrt(len(trust_evolve[:,i]))
        #     print 'mean, std err: ', mean_trust, ', ', std_err

if __name__=='__main__':
    policyfile = sys.argv[1]

    numruns = 10000
    init_bel = [0.0, 0.092105263157894732, 0.11842105263157894, 0.17105263157894737, 0.35526315789473684, 0.25, 0.013157894736842105]
    policy = LoadPolicy(policyfile)
    llm_q_dict = None

    if len(sys.argv) > 2:
        llm_result_file = sys.argv[2]
        remaining_objects = {'plastic bottle': 3, 'fish can': 1, 'wine glass': 1}

        robot_action_list = ['plastic bottle', 'plastic bottle', 'plastic bottle', 'fish can', 'wine glass']

        # Load the LLM policy
        llm_root_node = llm_policy.Node(remaining_objects, [], include_trust_change=True)

        llm_policy.expand_interaction_tree(llm_root_node)
        all_llm_nodes = llm_root_node.traverse()

        llm_result_df = pd.read_csv(llm_result_file)
        # Get the probs
        s = set()
        for node in all_llm_nodes:
            probs = []
            if len(llm_result_df[llm_result_df['history'] == str(node.history)]) == 0:
                assert len(node.children) == 0
            else:
                assert len(node.children) == len(llm_result_df[llm_result_df['history'] == str(node.history)]) * 2
                rows = llm_result_df[llm_result_df['history'] == str(node.history)]
                for row_idx, row in rows.iterrows():
                    probs.append(row['A'] / (row['A'] + row['B']))
                    probs.append(row['B'] / (row['A'] + row['B']))
            node.probs = probs

        llm_q_dict = llm_policy.get_policy(llm_root_node, all_llm_nodes)

    init_bel = [0.0, 0.092105263157894732, 0.11842105263157894, 0.17105263157894737, 0.35526315789473684, 0.25, 0.013157894736842105]


    tclear = TableClearing(policy, init_bel, numruns, llm_q_dict=llm_q_dict)
    tclear.verbose = 0


    tclear.runs()

    print(llm_result_file)




