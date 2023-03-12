#!/usr/bin/python2

from math import sqrt
from numpy import *
import itertools
import sys

class TableFileGenerator:

    def __init__(self, numbottles):
        self.discount = 0.99        #reward discount value
        self.numbottles = numbottles
        self.spSuccessBottle = 1
        self.spSuccessCan = 2
        self.spSuccessGlass = 3
        self.spFailBottle = 0
        self.spFailCan = -4
        self.spFailGlass = -9
        self.intervene = 0

        self.numTrustLevels = 7

        self.numObjects = self.numbottles + 2
        self.numStatus = 4
        self.numObjStates = pow(self.numStatus, self.numObjects) + 1

        self.largePenalty = -9999999
        self.rewardFlag = 'return'
        # self.rewardFlag = 'trust'

        self.trustDyna, self.humanBehav = self.InitTrustDyna()

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


    # Functionality:
    # generate all possible states
    # Format:
    #   object id (0 - 4) + status (on table (0), cleared by the robot(1), dropped by the robot(2), cleared by the human(3)
    # ObjID[object id]ObjStatus[object status]Trust[trust level]
    def StateGen(self):
        objectStates = []
        trustStates = []

        alist = []
        for ind in range(self.numObjects):
            tmp = []
            for j in range(self.numStatus):
                tmp.append("ObjStatus" + str(ind) + str(j))
            alist.append(tmp)

        for element in itertools.product(*alist):
            objectStates.append(''.join(element))

        objectStates.append("END")
        
        for k in range(self.numTrustLevels):
            trustState = "Trust" + str(k)
            trustStates.append(trustState)

        self.objectStates = objectStates
        self.trustStates = trustStates

    # Format
    # Obs[human action]
    def ObservationsGen(self):
        observations = []
        for i in range(2):
            observations.append("Obs" + str(i))
        self.observations = observations

    # to generate all possible actions
    # a list of actions
    def ActionsGen(self):
        actions = []
        for i in range(self.numObjects):
            actions.append(str(i))
        self.actions = actions

    def StartObjBeliefGen(self):
        belief = []
        for i in range(self.numObjStates):
            belief.append(0)
        belief[0] = 1.0
        return belief
    
    def StartTrustBeliefGen(self):
        # belief = [0.0, 0.092105263157894732, 0.11842105263157894, 0.17105263157894737, 0.35526315789473684, 0.25, 0.013157894736842105]
        belief = [1.0 / 7] * 7
        return belief

    def printHeader(self, xmlFile):
        discount = self.discount
        value = "reward"

        self.ActionsGen()
        actions = toString(self.actions)

        self.StateGen()
        objectStates = toString(self.objectStates)
        trustStates = toString(self.trustStates)

        self.ObservationsGen()
        observations = toString(self.observations)

        #real contents
        xmlFile.write("<Discount>"+str(discount)+"</Discount>\n")
	
        xmlFile.write("\n<Variable>\n")

        xmlFile.write("\t<StateVar vnamePrev=\"objState_0\" vnameCurr=\"objState_1\" fullyObs=\"true\">\n\t\t<ValueEnum>" + objectStates + "\n\t\t</ValueEnum>\n\t</StateVar>")
        
        xmlFile.write("\n\n")
        xmlFile.write("\t<StateVar vnamePrev=\"trust_0\" vnameCurr=\"trust_1\" fullyObs=\"false\">\n\t\t<ValueEnum>" + trustStates + "\n\t\t</ValueEnum>\n\t</StateVar>")	
        
        xmlFile.write("\n\n")
        xmlFile.write("\t<ObsVar vname=\"obs_sensor\">\n\t\t<ValueEnum>" + observations + "\n\t\t</ValueEnum>\n\t</ObsVar>")
        
        xmlFile.write("\n\n")
        xmlFile.write("\t<ActionVar vname=\"action_robot\">\n\t\t<ValueEnum>" + actions + "\n\t\t</ValueEnum>\n\t</ActionVar>")	
        
        
        xmlFile.write("\n\n")
        xmlFile.write("\t<RewardVar vname=\"reward_robot\"/>")
        
        xmlFile.write("\n</Variable>\n")

    def printInitialStateBelief(self, xmlFile):
        xmlFile.write("\n<InitialStateBelief>\n")
        self.printInitialObjState(xmlFile)
        xmlFile.write("\n")
        self.printInitialTrustState(xmlFile)
        xmlFile.write("</InitialStateBelief>\n")

    def printStateTransitionFunction(self, xmlFile):
        xmlFile.write("<StateTransitionFunction>")
        self.printObjState(xmlFile)
        self.printTrustState(xmlFile)
        xmlFile.write("</StateTransitionFunction>")

    def printObjState(self, xmlFile):
        xmlFile.write("\t<CondProb>\n")
        xmlFile.write("\t\t<Var>objState_1</Var>")
        xmlFile.write("\t\t<Parent>action_robot objState_0 trust_0</Parent>\n")
        xmlFile.write("\t\t<Parameter type = \"TBL\">\n\n")

        xmlFile.write(self.getStateEntry("*" + " " + "END" + " " + "*" + " " + "END",1.0))

        for objState in self.objectStates:
            for trustState in self.trustStates:
                if objState != "END":
                    for action in self.actions:
                        objStatus = toObjState(objState)
                        # print objStatus
                        tr = toTrustState(trustState)
                        act = toAction(action)

                        t = self.newObjStates(objStatus, tr, act, objState)

                        for i in range(len(t)):
                            if t[i][1] != 0:
                                xmlFile.write(self.getStateEntry(action + " " + objState + " " + trustState + " " + t[i][0], t[i][1]))

	# xmlFile.write("\n")
	xmlFile.write("\t\t</Parameter>\n")
	xmlFile.write("\t</CondProb>\n")

    def printTrustState(self, xmlFile):

        xmlFile.write("\t<CondProb>\n")
        xmlFile.write("\t\t<Var>trust_1</Var>")
        xmlFile.write("\t\t<Parent>action_robot objState_0 trust_0</Parent>\n")
        xmlFile.write("\t\t<Parameter type=\"TBL\">\n\n")


        for objState in self.objectStates:
            for trustState in self.trustStates:
                if objState != "END":
                    for action in self.actions:
                        objStatus = toObjState(objState)
                        tr = toTrustState(trustState)
                        act = toAction(action)

                        t = self.newTrustStates(objStatus, tr, act, trustState)

                        for i in range(len(t)):
                            if t[i][1] != 0:
                                xmlFile.write(self.getStateEntry(action + " " + objState + " " + trustState + " " + t[i][0], t[i][1]))
                else:
                    xmlFile.write(self.getStateEntry("*" + " " + "END" + " " + trustState + " " + trustState,1.0))

	xmlFile.write("\t\t</Parameter>\n")	
        xmlFile.write("\t</CondProb>\n")

    def printReward(self, xmlFile):
	xmlFile.write("<RewardFunction>\n")
        xmlFile.write("<Func>\n")
        xmlFile.write("\t<Var>reward_robot</Var>\n")
	
	xmlFile.write("\t<Parent>action_robot objState_0 trust_0</Parent>\n")
	xmlFile.write("\t<Parameter type = \"TBL\">\n\n")

        for objState in self.objectStates:
            for trustState in self.trustStates:
                if objState == "END":
                    xmlFile.write(self.getRewEntry("*" + " " + objState + " " + "*", 0))
                else:
                    for action in self.actions:
                        objStatus = toObjState(objState)
                        tr = toTrustState(trustState)
                        act = toAction(action)
                        
                        if objStatus[act] != 0:
                            # xmlFile.write(self.getRewEntry(action + " " + objState + " " + "*", self.largePenalty))
                            xmlFile.write(self.getRewEntry(action + " " + objState + " " + trustState, self.largePenalty))
                        else:
                            HumanActionsProb = self.HumanActionsProb(tr, act)
                            ireward = 0
                            if act < self.numbottles:
                                ireward = self.spSuccessBottle
                            elif act == self.numbottles:
                                ireward = self.spSuccessCan
                            else:
                                ireward = self.spSuccessGlass
                            ireward = ireward * HumanActionsProb[1]
                            xmlFile.write(self.getRewEntry(action + " " + objState + " " + trustState, ireward))

	xmlFile.write("\n")
	xmlFile.write("\t</Parameter>\n")
        xmlFile.write("</Func>")
	xmlFile.write("</RewardFunction>\n")

    def printRewardTrust(self, xmlFile):
	xmlFile.write("<RewardFunction>\n")
        xmlFile.write("<Func>\n")
        xmlFile.write("\t<Var>reward_robot</Var>\n")
	
	xmlFile.write("\t<Parent>action_robot objState_0 trust_0</Parent>\n")
	xmlFile.write("\t<Parameter type = \"TBL\">\n\n")

        for objState in self.objectStates:
            for trustState in self.trustStates:
                if objState == "END":
                    xmlFile.write(self.getRewEntry("*" + " " + objState + " " + "*", 0))
                else:
                    for action in self.actions:
                        objStatus = toObjState(objState)
                        tr = toTrustState(trustState)
                        act = toAction(action)
                        
                        if objStatus[act] != 0:
                            xmlFile.write(self.getRewEntry(action + " " + objState + " " + "*", self.largePenalty))
                        else:
                            # HumanActionsProb = self.HumanActionsProb(tr, act)
                            ireward = tr
                            # if act < 3:
                                # ireward = self.spSuccessBottle
                            # elif act == 3:
                                # ireward = self.spSuccessCan
                            # elif act == 4:
                                # ireward = self.spSuccessGlass
                            # ireward = ireward * HumanActionsProb[1]
                            xmlFile.write(self.getRewEntry(action + " " + objState + " " + trustState, ireward))

	xmlFile.write("\n")
	xmlFile.write("\t</Parameter>\n")
        xmlFile.write("</Func>")
	xmlFile.write("</RewardFunction>\n")

    def newTrustStates(self, objStatus, tr, act, trustState):
        t = []
        if objStatus[act] != 0:
            self.addStatetoTrans(t, trustState, 1.0)

        else:
            HumanActionsProb = self.HumanActionsProb(tr, act)

            # intervene
            newTrustDistri_intervene = None
            if act < self.numbottles:
                newTrustDistri_intervene = self.trustDyna[0, 'Water Bottle'][tr]
            elif act == self.numbottles:
                newTrustDistri_intervene = self.trustDyna[0, 'Fish Can'][tr]
            else:
                newTrustDistri_intervene = self.trustDyna[0, 'Glass Cup'][tr]

            newTrustDistri_stay = None
            if act < self.numbottles:
                newTrustDistri_stay = self.trustDyna[1, 'Water Bottle'][tr]
            elif act == self.numbottles:
                newTrustDistri_stay = self.trustDyna[1, 'Fish Can'][tr]
            else:
                newTrustDistri_stay = self.trustDyna[1, 'Glass Cup'][tr]

            for i in range(len(newTrustDistri_intervene)):
                prob_trust_i = HumanActionsProb[0] * newTrustDistri_intervene[i] + HumanActionsProb[1] * newTrustDistri_stay[i];
                newTrustState = toTrustString(i)
                self.addStatetoTrans(t, newTrustState, prob_trust_i)
        return t

    def newObjStates(self, objStatus, tr, act, objState):
        t = []
        if objStatus[act] != 0:
            # newObjState = toObjString(objStatus, -1, -1)
            self.addStatetoTrans(t, objState, 1.0)
        else:
            humanActsProb = self.HumanActionsProb(tr, act)

            ## intervene
            newObjState = toObjString(objStatus, act, 0)
            self.addStatetoTrans(t, newObjState, humanActsProb[0])

            ## stay put
            newObjState = toObjString(objStatus, act, 1)
            self.addStatetoTrans(t, newObjState, humanActsProb[1])

        return t

    def HumanActionsProb(self, tr, act):
        dictionary = {}
        dictionary[0] = 0.0
        dictionary[1] = 0.0
        if act < self.numbottles:
            # water bottle
            dictionary[0] = self.humanBehav['Water Bottle'][tr][0]
        elif act == self.numbottles:
            dictionary[0] = self.humanBehav['Fish Can'][tr][0]
        else:
            dictionary[0] = self.humanBehav['Glass Cup'][tr][0]
        dictionary[1] = 1.0 - dictionary[0]
        return dictionary

    def addStatetoTrans(self, listT, state, prob):
        contains = False
        for i in range(len(listT)):
            if listT[i][0] == state:
                listT[i][1] += prob
                contains = True
        if not contains:
            listT.append([state, prob])


    def getStateEntry(self, instance, prob):
        result = "\t\t\t<Entry>\n"
        result += "\t\t\t\t<Instance>"
        result += instance
        result += "</Instance>\n"
        result += "\t\t\t\t<ProbTable>"
        result += str(prob)
        result += "</ProbTable>\n"
        result += "\t\t\t</Entry>\n\n"
        return result

    def getObsEntry(self, instance, prob):
        result = "\t\t<Entry>\n"
        result += "\t\t\t<Instance>"
        result += instance
        result += "</Instance>\n"
        result += "\t\t\t<ProbTable>"
        result += str(prob)
        result += "</ProbTable>\n"
        result += "\t\t</Entry>\n\n"
        return result    
    
    def getRewEntry(self, instance, prob):
        result = "\t\t<Entry>\n"
        result += "\t\t\t<Instance>"
        result += instance
        result += "</Instance>\n"
        result += "\t\t\t<ValueTable>"
        result += str(prob)
        result += "</ValueTable>\n"
        result += "\t\t</Entry>\n\n"
        return result        

    def printInitialObjState(self, xmlFile):
        objStart = toString(self.StartObjBeliefGen())

        xmlFile.write("\t<CondProb>\n")
        xmlFile.write("\t\t<Var>objState_0</Var>\n")
        xmlFile.write("\t\t\t<Parent>null</Parent>\n")
        xmlFile.write("\t\t\t<Parameter type = \"TBL\">\n")
        xmlFile.write("\t\t\t\t<Entry>\n")
        xmlFile.write("\t\t\t\t\t<Instance>-</Instance>\n")
        xmlFile.write("\t\t\t\t\t<ProbTable>")
        xmlFile.write(objStart)
        xmlFile.write("</ProbTable>\n")
        xmlFile.write("\t\t\t\t</Entry>\n")
        xmlFile.write("\t\t\t</Parameter>\n")		
        xmlFile.write("\t</CondProb>\n")		

    def printInitialTrustState(self, xmlFile):
        trustStart = toString(self.StartTrustBeliefGen())

        xmlFile.write("\t<CondProb>\n")
        xmlFile.write("\t\t<Var>trust_0</Var>\n")
        xmlFile.write("\t\t\t<Parent>null</Parent>\n")
        xmlFile.write("\t\t\t<Parameter type = \"TBL\">\n")
        xmlFile.write("\t\t\t\t<Entry>\n")
        xmlFile.write("\t\t\t\t\t<Instance>-</Instance>\n")
        xmlFile.write("\t\t\t\t\t<ProbTable>")
        xmlFile.write(trustStart)
        xmlFile.write("</ProbTable>\n")
        xmlFile.write("\t\t\t\t</Entry>\n")
        xmlFile.write("\t\t\t</Parameter>\n")		
        xmlFile.write("\t</CondProb>\n")		

    def printObservation(self, xmlFile):

	xmlFile.write("<ObsFunction>")
        xmlFile.write("<CondProb>")
        xmlFile.write("<Var>obs_sensor</Var>\n")
	
	xmlFile.write("\t<Parent>action_robot objState_1 trust_1</Parent>\n")
	xmlFile.write("\t<Parameter type =\"TBL\">\n\n")

        for objState in self.objectStates:
            for trustState in self.trustStates:
                if objState != "END":
                    for action in self.actions:
                        objStatus = toObjState(objState)
                        act = toAction(action)

                        obs = 1
                        if objStatus[act] == 1:
                            obs = 1
                        elif objStatus[act] == 3:
                            obs = 0
                        xmlFile.write(self.getObsEntry(action + " " + objState + " " + trustState + " " + "Obs" + str(obs), 1.0))
                else:
                    xmlFile.write(self.getObsEntry("*" + " " + "END" + " " + trustState + " " + "Obs" + str(1), 1.0))


	xmlFile.write("\n")
	xmlFile.write("\t</Parameter>\n")
        xmlFile.write("</CondProb>")
	xmlFile.write("</ObsFunction>\n")


    def XmlGen(self, outFile):
        xmlFile = open(outFile, 'w')

        xmlFile.write("<?xml version='1.0' encoding='ISO-8859-1'?>\n")
        xmlFile.write("<pomdpx version='0.1' id='tablexmlfac' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='pomdpx.xsd'>\n\n")	

        self.printHeader(xmlFile)

        ############ Robot
            
        self.printInitialStateBelief(xmlFile)
        xmlFile.write("\n")
        
        self.printStateTransitionFunction(xmlFile)
        xmlFile.write("\n")

	##########observations
	self.printObservation(xmlFile)
	xmlFile.write("\n")

	######## rewards
        if self.rewardFlag == "return":
            self.printReward(xmlFile)
        else:
            self.printRewardTrust(xmlFile)
	
        xmlFile.write("</pomdpx>\n")
	
        xmlFile.close


def endState(objStatus):
    a = 1
    for s in objStatus:
        a = a * s
    if a > 0:
        return True
    else:
        return False

def toObjString(objStatus, act, hact):
    if hact == 1:
        # stay put
       objStatus[act] = 1
    elif hact == 0:
        # intervene
       objStatus[act] = 3
    if endState(objStatus):
        return "END"
    else:
        ret = "" 
        for i in range(numobjects):
            ret += "ObjStatus" + str(i) + str(objStatus[i])
        return ret

def toTrustString(newTrust):
    return "Trust" + str(newTrust)
        
def toString(list):
    s = ""
    for item in list:
        s = s+" "+str(item)

    return s

def toObjState(ss):
    objstate = []
    for i in range(numobjects):
        start = ss.find("tus" + str(i))
        if i < numobjects - 1:
            end = ss.find("ObjStatus" + str(i+1))
        else:
            end = len(ss)
        statei = int(ss[start+4:end])
        objstate.append(statei)
    return objstate

def toTrustState(ss):
    start = ss.find('ust')
    end = len(ss)
    return int(ss[start+3:end])

def toAction(ss):
    return int(ss)

numbottles = int(sys.argv[1])
numobjects = numbottles + 2
xmlTable = TableFileGenerator(numbottles)
xmlTable.XmlGen("pomdpx/tableClearing" + str(numbottles) + "Bottles.pomdpx")
