#!/usr/bin/python2

from math import sqrt
from numpy import *
import json
import sys

class TableFileGenerator:

    def __init__(self, trustdynatype):
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
        self.numStatus = 4
        self.numObjStates = pow(self.numStatus, self.numObjects) + 1

        self.largePenalty = -9999999
        self.rewardFlag = 'return'
        self.trustdynatype = trustdynatype
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
        
        if self.trustdynatype == 'simple':
            path2trustdyna = '../../model_learning/version4/trustdyna/trustdyna_simple.json'
        else:
            path2trustdyna = '../../model_learning/version4/trustdyna/trustdyna_time.json'

        with open(path2trustdyna, 'r') as f:
            trustDyna = json.load(f)

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

    def EarlyStep(self, objstatus):
        count = 0
        for stat in objstatus:
            if stat == 0:
                count += 1
        if count > 3:
            return True
        else:
            return False

    def newTrustStates(self, objStatus, tr, act, trustState):
        t = []
        if objStatus[act] != 0:
            self.addStatetoTrans(t, trustState, 1.0)

        else:
            HumanActionsProb = self.HumanActionsProb(tr, act)

            # intervene
            newTrustDistri_intervene = None
            if act < 3:
                objname = 'Water Bottle'
            elif act == 3:
                objname = 'Fish Can'
            else:
                objname = 'Glass Cup'

            if self.trustdynatype == 'simple':
                key = "(0, '" + objname + "')"
            else:
                if self.EarlyStep(objStatus):
                    key = "(0, 0, '" + objname + "')"
                else:
                    key = "(1, 0, '" + objname + "')"
            newTrustDistri_intervene = self.trustDyna[key][tr]

            newTrustDistri_stay = None

            if self.trustdynatype == 'simple':
                key1 = "(1, '" + objname + "')"
            else:
                if self.EarlyStep(objStatus):
                    key1 = "(0, 1, '" + objname + "')"
                else:
                    key1 = "(1, 1, '" + objname + "')"
            newTrustDistri_stay = self.trustDyna[key1][tr]

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

trustdynatype = sys.argv[1]
xmlTable = TableFileGenerator(trustdynatype)
xmlTable.XmlGen("pomdpx/tableClearingTrustDyna" + trustdynatype + ".pomdpx")
