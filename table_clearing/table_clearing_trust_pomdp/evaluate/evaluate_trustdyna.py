#!/usr/bin/python2

from math import *
from loadPolicy import *
from numpy import *
import random
import json

class TableClearing:

    def __init__(self, policy, initbel, numruns, trustdynatype):
        self.discount = 0.99        #reward discount value
        self.spSuccessBottle = 1
        self.spSuccessCan = 2
        self.spSuccessGlass = 3
        self.spFailBottle = 0
        self.spFailCan = -4
        self.spFailGlass = -9
        self.intervene = 0

        self.numTrustLevels = 7

        self.numStatus = 4
        self.numObjects = 5
        self.numObjStates = pow(4, 5) + 1

        self.largePenalty = -9999999

        self.trustdynatype = trustdynatype
        self.trustDyna, self.humanBehav = self.InitTrustDyna()

        self.policy = policy
        self.initbel = initbel
        self.numruns = numruns

        self.verbose = 1
        self.bels = {"beliefs": []}
        self.trustdynatype1 = 'time'
        self.path2bel = '../../../journal/Figure-Generation/time-varying/trustdyna'
        if self.trustdynatype1 == 'simple':
            self.path2bel += '_simple.json'
        else:
            self.path2bel += '_time.json'

    def DumpBel(self):
        with open(self.path2bel, 'w') as f:
            json.dump(self.bels, f)

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
        
        if self.trustdynatype == 'simple':
            path2trustdyna = '../../../model_learning/version4/trustdyna/trustdyna_simple.json'
        else:
            path2trustdyna = '../../../model_learning/version4/trustdyna/trustdyna_time.json'

        with open(path2trustdyna, 'r') as f:
            trustDyna = json.load(f)

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

    def step(self):
        # record current belief
        if isinstance(self.bel, list):
            self.bels['beliefs'].append(self.bel)
        else:
            self.bels['beliefs'].append(self.bel.tolist())

        if self.trustdynatype1 == 'time':
            action = self.policy.FindOptimalAction(self.bel, self.state) 
        else:
            action = int(raw_input('Robot Action: '))

        # hact = self.humanAction(action)
        print 'robot action: ', action
        hact = raw_input('input human action: ') 
        hact = int(hact)
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

            if self.verbose > 0:
                print 'state: ', self.state
                print 'trust: ', self.trust
                print 'belief: ', self.bel
            
            if self.end():
                return True, reward
            else:
                return False, reward

    def EarlyStep(self, objstatus):
        count = 0
        for stat in objstatus:
            if stat == 0:
                count += 1
        if count > 3:
            return True
        else:
            return False

    def SelectTrustDistri(self, act, hact, tr):
        if act < 3:
            objname = 'Water Bottle'
        elif act == 3:
            objname = 'Fish Can'
        else:
            objname = 'Glass Cup'
        if self.trustdynatype == 'simple':
            key = "(" + str(hact) + ", '" + objname + "')"
        else:
            if self.EarlyStep(self.state):
                key = "(0, " + str(hact) + ", '" + objname + "')"
            else:
                key = "(1, " + str(hact) + ", '" + objname + "')"
        return self.trustDyna[key][tr]

    def nextTrust(self, act, hact):
        newTrustDistri = self.SelectTrustDistri(act, hact, self.trust) 
        self.trust = self.Sample(newTrustDistri)

    def updateBel(self, act, hact):
        temp_bel = self.bel
        print 'temp_bel: ', temp_bel
    
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

        print 'temp_bel: ', temp_bel
        # evolve trust
        newDistri = zeros(7)
        for tr in range(len(temp_bel)):
            newTrustDistri = self.SelectTrustDistri(act, hact, tr) 
            # if act < 3:
                # newTrustDistri = self.trustDyna[hact, 'Water Bottle'][tr]
            # elif act == 3:
                # newTrustDistri = self.trustDyna[hact, 'Fish Can'][tr]
            # else:
                # newTrustDistri = self.trustDyna[hact, 'Glass Cup'][tr]
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
        print 'discounted return: ', discounted_return
        print 'mean return: ', mean(discounted_return)
        print 'std: ', 1.96 * std(discounted_return) / sqrt(len(discounted_return))

        print '##### intervention ratio #####'
        print 'intervene ratio: ', array([1, 1, 1]) - stayput_count / total_obj_counts

        print '#### trust evolve along time #####'
        trust_evolve = array(trust_evolve)
        for i in range(len(trust_evolve[0])):
            print i, 'th step: '
            mean_trust = mean(trust_evolve[:, i])
            std_err = 1.96 * std(trust_evolve[:, i]) / sqrt(len(trust_evolve[:,i]))
            print 'mean, std err: ', mean_trust, ', ', std_err

if __name__=='__main__':
    policyfile = sys.argv[1]
    trustdynatype = sys.argv[2]
    numruns = 1 
    init_bel = [1.0 / 7.0] * 7
    # init_bel = [0.0, 0.092105263157894732, 0.11842105263157894, 0.17105263157894737, 0.35526315789473684, 0.25, 0.013157894736842105]
    policy = LoadPolicy(policyfile)

    tclear = TableClearing(policy, init_bel, numruns, trustdynatype)

    tclear.runs()
    tclear.DumpBel()
