from math import *
from loadPolicy import *
from numpy import *
import random


class TableClearing:

    def __init__(self, policy, initbel, numruns, \
            numBottle, numCan, numGlass, discount,\
            filename):
        self.discount = discount        #reward discount value
        self.filename = filename
        self.filelog = open(self.filename, 'w')

        self.spSuccessBottle = 1
        self.spSuccessCan = 2
        self.spSuccessGlass = 3
        self.spFailBottle = 0
        self.spFailCan = -4
        self.spFailGlass = -9
        self.intervene = 0

        self.numTrustLevels = 7

        self.numBottle = numBottle
        self.numCan = numCan
        self.numGlass = numGlass

        self.numObjects = self.numBottle + \
                self.numCan + self.numGlass
        self.numStatus = 4
        self.numObjStates = int(pow(self.numStatus, self.numObjects) + 1)

        self.largePenalty = -9999999

        self.trustDyna, self.humanBehav = self.InitTrustDyna()

        self.policy = policy
        self.initbel = initbel
        self.numruns = numruns

        self.verbose = 1

    def InitTrustDyna(self):
        hBehav = {'Fish Can': array([[ 0.41830094,  0.58169906],
            [ 0.3527471 ,  0.6472529 ],
            [ 0.2923042 ,  0.7076958 ],
            [ 0.23840339,  0.76159661],
            [ 0.19174884,  0.80825116],
            [ 0.15239743,  0.84760257],
            [ 0.11992362,  0.88007638]]),
     'Glass Cup': array([[ 0.73957621,  0.26042379],
            [ 0.66677201,  0.33322799],
            [ 0.58503451,  0.41496549],
            [ 0.49833243,  0.50166757],
            [ 0.41173052,  0.58826948],
            [ 0.3302705 ,  0.6697295 ],
            [ 0.25786257,  0.74213743]]),
     'Water Bottle': array([[ 0.19002125,  0.80997875],
            [ 0.15099808,  0.84900192],
            [ 0.11881326,  0.88118674],
            [ 0.09273919,  0.90726081],
            [ 0.07192017,  0.92807983],
            [ 0.05548897,  0.94451103],
            [ 0.04263924,  0.95736076]])}
        
        trustDyna = {(0, 'Fish Can'): array([[  9.18812100e-01,   8.11873725e-02,   5.27455200e-07,
           2.51952099e-16,   8.84882679e-30,   2.28501323e-47,
           4.33837465e-69],
        [  2.04050898e-03,   9.64443541e-01,   3.35158639e-02,
           8.56365845e-08,   1.60880560e-17,   2.22219983e-31,
           2.25682541e-49],
        [  2.08804976e-09,   5.27904858e-03,   9.81309008e-01,
           1.34119283e-02,   1.34775816e-08,   9.95790617e-19,
           5.40952834e-33],
        [  9.98212454e-19,   1.34993954e-08,   1.34227333e-02,
           9.81302522e-01,   5.27472935e-03,   2.08464811e-09,
           6.05760073e-20],
        [  2.22937147e-31,   1.61268776e-17,   8.57735629e-08,
           3.35422292e-02,   9.64418884e-01,   2.03880082e-03,
           3.16897785e-10],
        [  2.29240582e-47,   8.87025021e-30,   2.52357112e-16,
           5.27874324e-07,   8.11859428e-02,   9.18050243e-01,
           7.63286133e-04],
        [  1.04678870e-66,   2.16660585e-45,   3.29713028e-28,
           3.68916105e-15,   3.03497021e-06,   1.83576278e-01,
           8.16420687e-01]]),
 (0,
  'Glass Cup'): array([[  7.51066535e-01,   2.40515396e-01,   8.38621755e-03,
           3.18381729e-05,   1.31610010e-08,   5.92363752e-13,
           2.90299843e-18],
        [  2.46396660e-01,   5.93492703e-01,   1.55652006e-01,
           4.44480620e-03,   1.38200530e-05,   4.67870172e-09,
           1.72464526e-13],
        [  1.59454606e-02,   2.88890814e-01,   5.69887544e-01,
           1.22406187e-01,   2.86270333e-03,   7.28967370e-06,
           2.02115028e-09],
        [  1.66342065e-04,   2.26680857e-02,   3.36346083e-01,
           5.43396296e-01,   9.55885214e-02,   1.83085346e-03,
           3.81821340e-06],
        [  2.76694737e-07,   2.83615363e-04,   3.16531821e-02,
           3.84648259e-01,   5.08942755e-01,   7.33217587e-02,
           1.15015291e-03],
        [  7.34311058e-11,   5.66141533e-07,   4.75257234e-04,
           4.34401410e-02,   4.32327128e-01,   4.68481580e-01,
           5.52753273e-02],
        [  3.23609874e-15,   1.87664795e-10,   1.18495709e-06,
           8.14669034e-04,   6.09843734e-02,   4.97066727e-01,
           4.41133045e-01]]),
 (0,
  'Water Bottle'): array([[  8.66635098e-01,   1.32989543e-01,   3.75339389e-04,
           1.94830174e-08,   1.86000332e-14,   3.26585312e-22,
           1.05464186e-31],
        [  1.20528266e-01,   7.85187465e-01,   9.40769510e-02,
           2.07309181e-04,   8.40193400e-09,   6.26275500e-15,
           8.58572563e-23],
        [  5.50637134e-04,   1.52283613e-01,   7.74579993e-01,
           7.24610805e-02,   1.24671953e-04,   3.94510119e-09,
           2.29600568e-15],
        [  7.48983895e-08,   8.79353271e-04,   1.89880215e-01,
           7.54087033e-01,   5.50793311e-02,   7.39914043e-05,
           1.82809731e-09],
        [  3.03053605e-13,   1.51047516e-07,   1.38462811e-03,
           2.33441535e-01,   7.23849941e-01,   4.12804462e-02,
           4.32977821e-05],
        [  3.64496880e-20,   7.71242892e-13,   3.00133146e-07,
           2.14813798e-03,   2.82771617e-01,   6.84596828e-01,
           3.04831173e-02],
        [  1.33150272e-28,   1.19603157e-19,   1.97591682e-12,
           6.00371544e-07,   3.35503432e-03,   3.44825411e-01,
           6.51818954e-01]]),
 (1, 'Fish Can'): array([[  1.73439171e-01,   7.93448085e-01,   3.31001526e-02,
           1.25916206e-05,   4.36790731e-11,   1.38167326e-18,
           3.98545072e-28],
        [  8.71365075e-04,   2.62120028e-01,   7.19019077e-01,
           1.79854279e-02,   4.10243103e-06,   8.53300412e-12,
           1.61846300e-19],
        [  1.04779947e-07,   2.07255926e-03,   3.73831501e-01,
           6.14872380e-01,   9.22219344e-03,   1.26131518e-06,
           1.57308856e-12],
        [  2.99043373e-13,   3.88948137e-07,   4.61306274e-03,
           4.98915711e-01,   4.92045372e-01,   4.42510190e-03,
           3.62895475e-07],
        [  2.01928604e-20,   1.72696718e-12,   1.34682286e-06,
           9.57804839e-03,   6.21131747e-01,   3.67308163e-01,
           1.98069491e-03],
        [  3.24002765e-29,   1.82206425e-19,   9.34369837e-12,
           4.36932235e-06,   1.86315727e-02,   7.24477824e-01,
           2.56886234e-01],
        [  1.49620136e-39,   5.53265698e-28,   1.86559598e-18,
           5.73642872e-11,   1.60844331e-05,   4.11253938e-02,
           9.58858522e-01]]),
 (1,
  'Glass Cup'): array([[  7.50925537e-02,   7.02874237e-01,   2.19737956e-01,
           2.29445340e-03,   8.00202875e-07,   9.32111098e-12,
           3.62645218e-18],
        [  9.19138129e-04,   1.41810221e-01,   7.30770475e-01,
           1.25776978e-01,   7.23049487e-04,   1.38829447e-07,
           8.90311273e-13],
        [  1.12400520e-06,   2.85851893e-03,   2.42806625e-01,
           6.88853225e-01,   6.52739005e-02,   2.06585169e-04,
           2.18376257e-08],
        [  1.36714799e-10,   5.73105114e-06,   8.02416303e-03,
           3.75242404e-01,   5.86098730e-01,   3.05756963e-02,
           5.32756352e-05],
        [  1.64274208e-15,   1.13510004e-09,   2.61966406e-05,
           2.01931359e-02,   5.19886620e-01,   4.47054239e-01,
           1.28398071e-02],
        [  1.95566291e-21,   2.22743356e-14,   8.47348805e-09,
           1.07662978e-04,   4.56895903e-02,   6.47611933e-01,
           3.06590805e-01],
        [  2.81761662e-28,   5.28979280e-20,   3.31697445e-13,
           6.94691998e-08,   4.85947298e-04,   1.13535781e-01,
           8.85978202e-01]]),
 (1,
  'Water Bottle'): array([[  1.84075573e-01,   7.22940628e-01,   9.25969539e-02,
           3.86792786e-04,   5.26923573e-08,   2.34101657e-13,
           3.39194613e-20],
        [  4.19974015e-03,   2.90773764e-01,   6.56561806e-01,
           4.83485673e-02,   1.16112560e-04,   9.09415575e-09,
           2.32291422e-14],
        [  8.65400115e-06,   1.05627275e-02,   4.20458174e-01,
           5.45829648e-01,   2.31088876e-02,   3.19071899e-05,
           1.43676477e-09],
        [  1.60033361e-09,   3.44346745e-05,   2.41640115e-02,
           5.53005797e-01,   4.12741303e-01,   1.00464766e-02,
           7.97511983e-06],
        [  2.65629845e-14,   1.00760114e-08,   1.24648780e-04,
           5.02892329e-02,   6.61682404e-01,   2.83930311e-01,
           3.97339305e-03],
        [  3.98310616e-20,   2.66354472e-13,   5.80879034e-08,
           4.13141676e-04,   9.58296519e-02,   7.24917211e-01,
           1.78839937e-01],
        [  6.02434880e-27,   7.10189993e-19,   2.73040195e-12,
           3.42346758e-07,   1.39988851e-03,   1.86684508e-01,
           8.11915261e-01]])}

        return trustDyna, hBehav
    
    def InitState(self):
        return [0] * self.numObjects

    def Sample(self, bel):
        val = random.random()
        temp = 0
        for i in range(len(bel)):
            temp += bel[i]
            if val < temp:
                return i

    def humanAction(self, act):
        prob = [0.0, 0.0]
        if act < self.numBottle:
            prob[0] = self.humanBehav['Water Bottle'][self.trust][0]
        elif act < self.numBottle + self.numCan:
            prob[0] = self.humanBehav['Fish Can'][self.trust][0]
        else:
            prob[0] = self.humanBehav['Glass Cup'][self.trust][0]

        prob[1] = 1.0 - prob[0]

        return self.Sample(prob) 

    def step(self):
        action = self.policy.FindOptimalAction(self.bel, self.state) 
        print 'robot action: ', action
        # hact = self.humanAction(action)
        # debug
        # hact = 1 
        hact = int(raw_input('Enter your human action:'))
        reward = 0

        if self.verbose > 0:
            # print 'action: ', action
            print 'human action: ', hact

        if self.state[action] != 0:
            if self.verbose > 0:
                print 'invalid action'
            return False, self.largePenalty
        
        else:
            # save the data
            self.filelog.write(str(self.bel) + '\n')
            self.filelog.write(str(action) + \
                    ' ' + str(hact) + '\n')

            if hact == 1:
                # stay put
                self.state[action] = 1
                if action < self.numBottle:
                    reward = self.spSuccessBottle
                    self.stay_put_count[0] += 1
                elif action < self.numBottle + self.numCan:
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
            self.trust = self.Sample(self.bel)


            if self.verbose > 0:
                print 'state: ', self.state
                print 'trust: ', self.trust
                print 'belief: ', self.bel
                print 'reward: ', reward
            
            if self.end():
                return True, reward
            else:
                return False, reward

    def nextTrust(self, act, hact):
        newTrustDistri = None
        if act < self.numBottle:
            newTrustDistri = self.trustDyna[hact, 'Water Bottle'][self.trust]
        elif act < self.numBottle + self.numCan:
            newTrustDistri = self.trustDyna[hact, 'Fish Can'][self.trust]
        else:
            newTrustDistri = self.trustDyna[hact, 'Glass Cup'][self.trust]

    def updateBel(self, act, hact):
        temp_bel = self.bel
        print 'pre bel: ', temp_bel
    
        obj = None
        if act < self.numBottle:
            obj = 'Water Bottle'
        elif act == self.numBottle + self.numCan:
            obj = 'Fish Can'
        else:
            obj = 'Glass Cup'
        
        weights = []
        for i in range(len(temp_bel)):
            weights.append(temp_bel[i] * self.humanBehav[obj][i][hact])
        temp_bel = self.normalizeBel(weights)

        print 'post bel: ', temp_bel
        # evolve trust
        newDistri = zeros(7)
        for tr in range(len(temp_bel)):
            newTrustDistri = None
            if act < self.numBottle:
                newTrustDistri = self.trustDyna[hact, 'Water Bottle'][tr]
            elif act < self.numBottle + self.numCan:
                newTrustDistri = self.trustDyna[hact, 'Fish Can'][tr]
            else:
                newTrustDistri = self.trustDyna[hact, 'Glass Cup'][tr]
            newTrustDistri = array(newTrustDistri)
            newDistri = newDistri +  newTrustDistri * temp_bel[tr]
            
        self.bel = self.normalizeBel(newDistri).tolist()

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
        total_obj_counts = array([self.numruns * self.numBottle, self.numruns * self.numCan, self.numruns * self.numGlass])
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
    if len(sys.argv) != 8:
        print 'Usage: python table_clearing.py policyfile num-bottle num-can num-glass discount intervene savefile'
        sys.exit(0)

    policyfile = sys.argv[1]

    numBottle = int(sys.argv[2])
    numCan = int(sys.argv[3])
    numGlass = int(sys.argv[4])
    discount = float(sys.argv[5])
    savefile = int(sys.argv[7])

    if savefile == 0:
        filename = 'test.txt'
    else:
        filename = 'plots/' + str(numBottle) + 'bottle-' + str(numCan) + \
                'can-' + str(numGlass) + 'glass-' + str(discount) + '-' + \
                sys.argv[6] + '.txt'

    numruns = 1

    # init_bel = [0.0, 0.092105263157894732, 0.11842105263157894, 0.17105263157894737, 0.35526315789473684, 0.25, 0.013157894736842105]
    init_bel = [1.0/7.0] * 7

    policy = LoadPolicy(policyfile, numBottle, \
            numCan, numGlass)
    tclear = TableClearing(policy, init_bel, numruns, numBottle, numCan, numGlass, \
            discount, filename)

    tclear.runs()
    tclear.filelog.close()
