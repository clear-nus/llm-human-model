#!/usr/bin/python2

from math import *
from loadPolicy import *
from numpy import *
import random
import sys
sys.path.insert(0, '../')
from init_trust_model import *
from copy import *


class TableClearing:

    def __init__(self, policy, initbel, numruns, discount):
        self.discount = discount        #reward discount value
        self.spSuccessBottle = 1
        self.spSuccessGlass = 3
        self.spFailBottle = 0
        self.spFailGlass = -9
        self.intervene = 0

        self.numTrustLevels = 10

        self.numObjects = 4
        self.numStatus = 4
        self.numObjStates = pow(self.numStatus, self.numObjects) + 1

        self.largePenalty = -9999999

        self.trustDyna, self.humanBehav = InitTrustDynaNoTransfer('../trust_models/trust_dynamics_no_transfer.json')

        self.policy = policy
        self.initbel = initbel
        self.numruns = numruns

        self.verbose = 1


    def InitState(self):
        return [0, 0, 0, 0]


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
        else:
            prob[0] = self.humanBehav['Glass Cup'][self.trust][0]

        prob[1] = 1.0 - prob[0]

        return self.Sample(prob) 

    def step(self):
        action = self.policy.FindOptimalAction(self.bel, self.state) 
        if self.verbose > 0:
            print 'robot action: ', RobotAction[action]
        # hact = self.humanAction(action)
        hact = int(raw_input('Human Action: '))
        reward = 0

        if self.verbose > 0:
            # print 'robot action: ', RobotAction[action]
            print 'human action: ', HumanAction[hact]

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
                else:
                    reward = self.spSuccessGlass
                    self.stay_put_count[2] += 1
            else:
                # intervene
                self.state[action] = 3
            self.nextTrust(action, hact)
            self.updateBel(action, hact)

            if self.verbose > 0:
                print 'state: ', self.state
                print 'reward : ', reward 
                # print 'trust: ', self.trust
                print 'belief: ', [round(x, 2) for x in self.bel]
            
            if self.end():
                return True, reward
            else:
                return False, reward

    def nextTrust(self, act, hact):
        newTrustDistri = None
        if act < 3:
            newTrustDistri = self.trustDyna[hact, 'Water Bottle'][self.trust]
        else:
            newTrustDistri = self.trustDyna[hact, 'Glass Cup'][self.trust]
        self.trust = self.Sample(newTrustDistri)


    def UpdateBelPre(self, ptask):
        # evolve trust
        newDistri = zeros(self.numTrustLevels)
        for tr in range(len(self.initbel)):
            newTrustDistri = None
            newTrustDistri = self.trustDyna[1, ptask][tr]
            newTrustDistri = array(newTrustDistri)
            newDistri = newDistri +  newTrustDistri * self.initbel[tr]
            
        self.initbel = self.normalizeBel(newDistri)

    def updateBel(self, act, hact):
        temp_bel = copy(self.bel)
        # print 'temp_bel: ', temp_bel
    
        obj = None
        if act < 3:
            obj = 'Water Bottle'
        else:
            obj = 'Glass Cup'
        
        weights = []
        for i in range(len(temp_bel)):
            weights.append(temp_bel[i] * self.humanBehav[obj][i][hact])
        temp_bel = self.normalizeBel(weights)

        # print 'temp_bel: ', temp_bel
        # evolve trust
        newDistri = zeros(self.numTrustLevels)
        for tr in range(len(temp_bel)):
            newTrustDistri = None
            if act < 3:
                newTrustDistri = self.trustDyna[hact, 'Water Bottle'][tr]
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
        self.trust = self.Sample(self.initbel)
        reward = 0
        terminal = False
        
        if self.verbose > 0:
            print 'state: ', self.state
            print 'bel: ', self.bel
            # print 'trust: ', self.trust
        
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
        print 'discounted return: ', discounted_return
        print 'mean return: ', mean(discounted_return)
        print 'std: ', 1.96 * std(discounted_return) / sqrt(len(discounted_return))

        # print '##### intervention ratio #####'
        # print 'intervene ratio: ', array([1, 1, 1]) - stayput_count / total_obj_counts

        # print '#### trust evolve along time #####'
        # trust_evolve = array(trust_evolve)
        # for i in range(len(trust_evolve[0])):
            # print i, 'th step: '
            # mean_trust = mean(trust_evolve[:, i])
            # std_err = 1.96 * std(trust_evolve[:, i]) / sqrt(len(trust_evolve[:,i]))
            # print 'mean, std err: ', mean_trust, ', ', std_err



if __name__=='__main__':
    policyfile = sys.argv[1]
    discount = float(sys.argv[2])
    numruns = 1 
    # init_bel = [0.0, 0.092105263157894732, 0.11842105263157894, 0.17105263157894737, 0.35526315789473684, 0.25, 0.013157894736842105]
    init_bel = [0.1] * 10
    policy = LoadPolicy(policyfile)

    tclear = TableClearing(policy, init_bel, numruns, discount)
    tclear.UpdateBelPre('Navigation')

    tclear.runs()
