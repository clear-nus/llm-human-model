from math import sqrt
from numpy import *

class TableFileGenerator:

    def __init__(self):
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
        self.rewardFlag = 'return'
        # self.rewardFlag = 'trust'

        self.trustDyna, self.humanBehav = self.InitTrustDyna()

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


    # Functionality:
    # generate all possible states
    # Format:
    #   object id (0 - 4) + status (on table (0), cleared by the robot(1), dropped by the robot(2), cleared by the human(3)
    # ObjID[object id]ObjStatus[object status]Trust[trust level]
    def StateGen(self):
        objectStates = []
        trustStates = []

        for i0 in range(self.numStatus):
            objectState0 = "ObjStatus0" + str(i0)
            for i1 in range(self.numStatus):
                objectState1 = objectState0  + "ObjStatus1" + str(i1)
                for i2 in range(self.numStatus):
                    objectState2 = objectState1 +  "ObjStatus2" + str(i2)
                    for i3 in range(self.numStatus):
                        objectState3 = objectState2 + "ObjStatus3" + str(i3)
                        for i4 in range(self.numStatus):
                            objectState4 = objectState3 + "ObjStatus4" + str(i4)

                            objectStates.append(objectState4)
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
        actions = ["0", "1", "2", "3", "4"]
        self.actions = actions

    def StartObjBeliefGen(self):
        belief = []
        for i in range(self.numObjStates):
            belief.append(0)
        belief[0] = 1.0
        return belief
    
    def StartTrustBeliefGen(self):
        belief = [0.0, 0.092105263157894732, 0.11842105263157894, 0.17105263157894737, 0.35526315789473684, 0.25, 0.013157894736842105]
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
                            if act < 3:
                                ireward = self.spSuccessBottle
                            elif act == 3:
                                ireward = self.spSuccessCan
                            elif act == 4:
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
            if act < 3:
                newTrustDistri_intervene = self.trustDyna[0, 'Water Bottle'][tr]
            elif act == 3:
                newTrustDistri_intervene = self.trustDyna[0, 'Fish Can'][tr]
            else:
                newTrustDistri_intervene = self.trustDyna[0, 'Glass Cup'][tr]

            newTrustDistri_stay = None
            if act < 3:
                newTrustDistri_stay = self.trustDyna[1, 'Water Bottle'][tr]
            elif act == 3:
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
        if act < 3:
            # water bottle
            dictionary[0] = self.humanBehav['Water Bottle'][tr][0]
        elif act == 3:
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
        return "ObjStatus0" + str(objStatus[0]) + "ObjStatus1" + str(objStatus[1]) + "ObjStatus2" + str(objStatus[2]) + "ObjStatus3" + str(objStatus[3]) + "ObjStatus4" + str(objStatus[4])

def toTrustString(newTrust):
    return "Trust" + str(newTrust)
        
def toString(list):
    s = ""
    for item in list:
        s = s+" "+str(item)

    return s

def toObjState(ss):
    start = ss.find("tus0")
    end = ss.find("ObjStatus1")
    s0 = int(ss[start+4:end])
    start = ss.find("tus1")
    end = ss.find("ObjStatus2")
    s1 = int(ss[start+4:end])
    start = ss.find("tus2")
    end = ss.find("ObjStatus3")
    s2 = int(ss[start+4:end])
    start = ss.find("tus3")
    end = ss.find("ObjStatus4")
    s3 = int(ss[start+4:end])
    start = ss.find("tus4")
    end = len(ss)
    s4 = int(ss[start+4:end])
    return [s0, s1, s2, s3, s4]

def toTrustState(ss):
    start = ss.find('ust')
    end = len(ss)
    return int(ss[start+3:end])

def toAction(ss):
    return int(ss)

xmlTable = TableFileGenerator()
xmlTable.XmlGen("pomdpx/tableClearing.pomdpx")
# xmlTable.XmlGen("pomdpx/tableClearingTrust.pomdpx")
