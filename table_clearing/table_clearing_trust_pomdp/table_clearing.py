from math import sqrt

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
                        objectState3 += objectState2 + "ObjStatus3" + str(i3)
                        for i4 in range(self.numStatus):
                            objectState4 += objectState3 + "ObjStatus4" + str(i4)

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
        for i in range(self.numObjects):
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

        xmlFile.write(self.getStateEntry("*" + " " + "*" + " " + "END" + " " + "END",1.0))

        for objState in self.objectStates:
            for trustState in self.trustStates:
                if trustState != "END":
                    for action in self.actions:
                        objStatus = toObjState(objState)
                        tr = toTrustState(trustState)
                        act = toAction(action)

                        t = self.newObjStates(ObjStatus, tr, act, objState)

                        for i in range(len(t)):
                            if t[i][1] != 0:
                                xmlFile.write(self.getStateEntry(action + " " + objState + " " + trustState + " " + t[i][0], t[i][1]))

        
    def newObjStates(objStatus, tr, act, objState):
        t = []
        if objStatus[act] != 0:
            newObjState = toObjString(objStatus, -1, -1)
            self.addStatetoTrans(t, newObjState, 1.0)
        else:
            humanActsProb = self.HumanActionsProb(tr, act)

    def addStatetoTrans(self, listT, state, prob):
        contains = False
        for i in range(len(listT)):
            if listT[i][0] == state:
                listT[i][1] += prob
                contains = True
        if not contains:
            listT.append([state, prob])

    def toObjString(objStatus, act, hact):
        if hact == 0:
            # stay put
           objStatus[act] = 1
        elif hact == 1:
           objStatus[act] = 3
        return "ObjStatus0" + str(objStatus[0]) + "ObjStatus1" + str(objStatus[1]) + "ObjStatus2" + str(objStatus[2]) + "ObjStatus3" + str(objStatus[3]) + "ObjStatus4" + str(objStatus[4])

    def toString(list):
        s = ""
        for item in list:
            s = s+" "+str(item)

        return s

    def toObjState(ss):
        start = ss.find("tus0")
        end = ss.find("ObjStatus1")
        s0 = int(ss[start+3,end])
        start = ss.find("tus1")
        end = ss.find("ObjStatus2")
        s1 = int(ss[start+3,end])
        start = ss.find("tus2")
        end = ss.find("ObjStatus3")
        s2 = int(ss[start+3,end])
        start = ss.find("tus3")
        end = ss.find("ObjStatus4")
        s3 = int(ss[start+3,end])
        start = ss.find("tus4")
        end = len(ss)
        s4 = int(ss[start+3,end])
        return [s0, s1, s2, s3, s4]
    
    def toTrustState(ss):
        start = ss.find('ust')
        end = len(ss)
        return int(ss[start+3, end])

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


xmlTable = TableFileGenerator()
xmlTable.XmlGen("tableClearing.pomdpx")
