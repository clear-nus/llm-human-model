# script to generate tag problem in xml format
# # written by Png Shao Wei
# pngshaowei@gmail.net

# Bugs removed by Zhang Meng
# When Catch happened, the target could not move if it is in
# a different cell than the robot.
# Now if target and robot are not in the same cell and robot's 
# status is not TAG, the target can move freely according to
# the game's rule.


from math import sqrt

class TagFileGenerator:

    def __init__(self):
        self.discount = 0.95        #reward discount value
        self.tagReward = 10
        self.tagPenalty = -10
        self.movePenalty = -1        #penalty for move vertically
	
        self.targetRemainsProb = 0.2 # probability of target remaining


    #*% Functionality:
    #*%     This function reads bit pattern files and generate 2-d array which
    #*%     represents the map, it also returns the height and width of the bitmap
    #*% Argument:
    #*%     fileName: location of bit pattern file to be parsed
    #*% Returns:
    #*%     bitMap: the resulting bitMap (An array of bit strings)
    #               None is returned if file format illegal
    #*%     width: the width of bitMap,
    #               "" is returned if file format illegal
    #*%     height: the height of bitMap,
    #               "" is returned if file format illegal
    #*% Assumptions:
    #*%     the length of each line in bit pattern is the same    
    def ReadBitPattern(self, fileName):
        bitFile = open(fileName,"r")
        bitMap ={}              #array of strings
        i = 0                   #index for line
        commonLength = 0        #standard length of each line, initialized to 0
        for line in bitFile.readlines():        
            line = line.rstrip('\n ')
            length = len(line)  
            #to initialize sLength
            if commonLength==0:
                commonLength = length
            elif length != commonLength:
                if length==0:
                    break
                else:
                    print "Error: length of bit line", i, "not standard"
                    return (None,"","")
            bitMap[i]= line[0:length]
            i = i+1
        bitFile.close
        width = commonLength
        height = i

        return (bitMap, width, height)


    # Functionality:
    #   read bit pattern and save bitMap, width, height
    def ReadBitMap(self, fileName):
        [bitMap, width, height] = self.ReadBitPattern(fileName)
        self.bitMap = bitMap
        self.width = width
        self.height = height
        return [bitMap, width, height]



    # Functionality:
    #   to generate all the possible states
    # Returns:
    #   a list of states
    # Format:
    #   Srv[robot row number]rh[robot column number]tv[target row number]th[target column number] OR
    #   Srv[robot row number]rh[robot column number]tagged
    def StatesGen(self):
        
        robotStates = []
	targetStates = []
	
	numLegalPos = 0
        for i in range(self.height)[::-1]:
            for j in range(self.width):
                if self.bitMap[i][j]=="0":
		    numLegalPos += 1
                    robotState = "Srv"+str(i)+"rh"+str(j)
		    robotStates.append(robotState)
		    targetState = "Ttv"+str(i)+"th"+str(j)
		    targetStates.append(targetState)
	
	targetStates.append("tagged")
        
        self.robotStates = robotStates
	self.targetStates = targetStates
	self.numLegalPos = numLegalPos

    # Functionality:
    #   to generate all the possible observations
    # Returns:
    #   a list of observations
    def ObservationsGen(self):
        observations = []
        #create inview observations
        for i in range(self.height)[::-1]:
            for j in range(self.width):
                if self.bitMap[i][j]=="0":
                    observation = "O" + "rv" + str(i) + "rh" + str(j)
                    observations.append(observation)
	observations.append("yes")
        self.observations = observations

    # Functionality:
    #   to generate all the possible actions
    # Returns:
    #   a list of actions
    def ActionsGen(self):
        actions = ["North","South","East","West","Catch"]
        self.actions = actions


    # Functionality:
    #   generate initial state according to initial prob distribution
    # Returns:
    #   an initial state(string) according to initial prob distribution
    def StartRobotBeliefGen(self):
        belief = []
        #equal probability in any state
        avgProb = 1.0/self.numLegalPos
        for i in range(self.numLegalPos):
            belief.append(str(avgProb))
        return belief

    # Functionality:
    #   generate initial state according to initial prob distribution
    # Returns:
    #   an initial state(string) according to initial prob distribution
    def StartTargetBeliefGen(self):
        belief = []
        #equal probability in any state
        avgProb = 1.0/self.numLegalPos
        for i in range(self.numLegalPos):
            belief.append(str(avgProb))
	belief.append("0") # doesn't start in tagged mode
        return belief

    #function: next
    #Functionality:
    #   get next position when previously in [y, x] and action a is performed
    #Assumption:
    #   previous position is valid 
    def next(self, y, x, a):
	if a == "North":
            newy = y - 1
            newx = x
	if a == "South":
            newy = y + 1
            newx = x
	if a == "West":
            newy = y
            newx = x - 1
	if a == "East":
            newy = y 
            newx = x + 1
	
	if newx < 0 or newx >= self.width:
            return [y,x]
	if newy < 0 or newy >= self.height:
            return [y,x]
	if self.bitMap[newy][newx] != "0":
            return [y,x]
	
	return [newy,newx]


    #function: next
    #Functionality:
    #   get next action and probability of target when robot is previously in [y, x]
    #Assumption:
    #   action of robot does not matter
    def targetActionsProb(self, ry, rx, ty, tx):
	origDist = self.distance(ry,rx,ty,tx)
	
	distNorth = self.distance(ry, rx, ty - 1, tx)
	distSouth = self.distance(ry, rx, ty + 1, tx)
	distWest = self.distance(ry, rx, ty, tx - 1)
	distEast = self.distance(ry, rx, ty, tx + 1)
	
	actionProb = (1 - self.targetRemainsProb) / 4
	
	dictionary = {}
	dictionary["North"] = 0.0
	dictionary["South"] = 0.0
	dictionary["East"] = 0.0
	dictionary["West"] = 0.0
	
	if distNorth > origDist:
            dictionary["North"] += actionProb
	else:
            dictionary["South"] += actionProb
            

	if distSouth > origDist:
            dictionary["South"] += actionProb
	else:
            dictionary["North"] += actionProb
            
	if distWest > origDist:
            dictionary["West"] += actionProb
	else:
            dictionary["East"] += actionProb
            
	if distEast > origDist:
            dictionary["East"] += actionProb
	else:
            dictionary["West"] += actionProb		
            
	return dictionary

    #function: distance
    #Functionality:
    #   get next distance of two points
    def distance(self,y1, x1, y2, x2):
    	distx = abs(x1 - x2)
	disty = abs(y1 - y2)
    	return sqrt(distx*distx + disty*disty)


    def addStatetoTrans(self,listT, state, prob):
	contains = False
	for i in range(len(listT)):
            if listT[i][0] == state:
                listT[i][1] += prob
                contains = True
	if not contains:
            listT.append([state,prob])


    def printHeader(self, xmlFile):
        discount = self.discount
        value = "reward"

        self.ActionsGen()
        actions = toString(self.actions)
	
        self.StatesGen()
        robotStates = toString(self.robotStates)
                
	targetStates = toString(self.targetStates)
	
        self.ObservationsGen()
        observations = toString(self.observations)	

        
	xmlFile.write("<Description>written by Png Shao Wei pngshaowei@gmail.com\n\n")    
        xmlFile.write("\t#This is a XML problem specification file\n\n")    
        xmlFile.write("\t#Environment map width:"+ str(self.width)+"\n")
        xmlFile.write("\t#Environment map height:"+ str(self.height)+"\n")
        xmlFile.write("\t#Total number of cells in map:"+str(self.numLegalPos)+"\n")
        xmlFile.write("\t#Total number of robot states:"+str(len(self.robotStates))+"\n")
	xmlFile.write("\t#Total number of target states:"+str(len(self.targetStates))+"\n")
        xmlFile.write("\t#Total number of observations:"+str(len(self.observations))+"\n\n")
        xmlFile.write("\t#Bug fixed by Zhang Meng dcszhm@nus.edu.sg on 30 May 2014:\n")
        xmlFile.write("\t#Target cannot move when Catch action is executed\n\t#in case that Target and Robot are not in the same cell\n")
        xmlFile.write("</Description>\n\n")
        
        #real contents
        xmlFile.write("<Discount>"+str(discount)+"</Discount>\n")
	
	xmlFile.write("\n<Variable>\n")
	
	xmlFile.write("\t<StateVar vnamePrev=\"robot_0\" vnameCurr=\"robot_1\" fullyObs=\"true\">\n\t\t<ValueEnum>" + robotStates + "\n\t\t</ValueEnum>\n\t</StateVar>")
	
	xmlFile.write("\n\n")
	xmlFile.write("\t<StateVar vnamePrev=\"target_0\" vnameCurr=\"target_1\" fullyObs=\"false\">\n\t\t<ValueEnum>" + targetStates + "\n\t\t</ValueEnum>\n\t</StateVar>")	
	
	xmlFile.write("\n\n")
	xmlFile.write("\t<ObsVar vname=\"obs_sensor\">\n\t\t<ValueEnum>" + observations + "\n\t\t</ValueEnum>\n\t</ObsVar>")
	
	xmlFile.write("\n\n")
	xmlFile.write("\t<ActionVar vname=\"action_robot\">\n\t\t<ValueEnum>" + actions + "\n\t\t</ValueEnum>\n\t</ActionVar>")	
	
	
	xmlFile.write("\n\n")
	xmlFile.write("\t<RewardVar vname=\"reward_robot\"/>")
	
	xmlFile.write("\n</Variable>\n")
    

    def printInitialStateBelief(self,xmlFile):
        xmlFile.write("\n<InitialStateBelief>\n")
        self.printInitialRobotState(xmlFile)
        xmlFile.write("\n")
        self.printInitialTargetState(xmlFile)
        xmlFile.write("</InitialStateBelief>\n")

    def printStateTransitionFunction(self,xmlFile):
        xmlFile.write("<StateTransitionFunction>")
        self.printRobotState(xmlFile)
        self.printTargetState(xmlFile)
        xmlFile.write("</StateTransitionFunction>")
        
    def printInitialRobotState(self, xmlFile):
        robotStart = toString(self.StartRobotBeliefGen())

        xmlFile.write("\t<CondProb>\n")
	xmlFile.write("\t\t<Var>robot_0</Var>\n")
	xmlFile.write("\t\t\t<Parent>null</Parent>\n")
	xmlFile.write("\t\t\t<Parameter type = \"TBL\">\n")
	xmlFile.write("\t\t\t\t<Entry>\n")
	xmlFile.write("\t\t\t\t\t<Instance>-</Instance>\n")
	xmlFile.write("\t\t\t\t\t<ProbTable>")
	xmlFile.write(robotStart)
	xmlFile.write("</ProbTable>\n")
	xmlFile.write("\t\t\t\t</Entry>\n")
	xmlFile.write("\t\t\t</Parameter>\n")		
	xmlFile.write("\t</CondProb>\n")		
	
    def printRobotState(self, xmlFile):
        
	xmlFile.write("\t<CondProb>\n")
        xmlFile.write("\t\t<Var>robot_1</Var>")
	xmlFile.write("\t\t<Parent>action_robot robot_0 target_0</Parent>\n")
	xmlFile.write("\t\t<Parameter type = \"TBL\">\n\n")
	
	for old_state in self.robotStates:
            for action in self.actions:
		if action != "Catch":
                    
                    [ry, rx] = toRobotState(old_state)
                    [new_ry, new_rx] = self.next(ry,rx,action)
                    new_state = toRobotString(new_ry,new_rx)
                    
                    xmlFile.write(self.getStateEntry(action + " " + old_state + " " + "*" + " " + new_state, 1.0))
		
		else: # remains in the same state if the action is catch
                    
                    xmlFile.write(self.getStateEntry(action + " " + old_state + " " + "*" + " " + old_state, 1.0))
	
	# if target is tagged, robot stays in original state
	
	for old_state in self.robotStates:
            xmlFile.write(self.getStateEntry("*" + " " + old_state + " " + "tagged" + " " + "*", 0.0))
            
            xmlFile.write(self.getStateEntry("*" + " " + old_state + " " + "tagged" + " " + old_state, 1.0))



	xmlFile.write("\n")
	xmlFile.write("\t\t</Parameter>\n")
	xmlFile.write("\t</CondProb>\n")


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
    
    def printInitialTargetState(self, xmlFile):

    	targetStart = toString(self.StartTargetBeliefGen())

        xmlFile.write("\t<CondProb>\n")
	xmlFile.write("\t\t<Var>target_0</Var>\n")
	xmlFile.write("\t\t\t<Parent>null</Parent>\n")
	xmlFile.write("\t\t\t<Parameter type = \"TBL\">\n")
	xmlFile.write("\t\t\t\t<Entry>\n")
	xmlFile.write("\t\t\t\t\t<Instance>-</Instance>\n")
	xmlFile.write("\t\t\t\t\t<ProbTable>")
	xmlFile.write(targetStart)
	xmlFile.write("</ProbTable>\n")
	xmlFile.write("\t\t\t\t</Entry>\n")
	xmlFile.write("\t\t\t</Parameter>\n")		
	xmlFile.write("\t</CondProb>\n")		

    def newTargetStates(self, ry, rx, ty, tx, target_state):
        t = []
        actsProb = self.targetActionsProb(ry, rx, ty, tx)

	### remains
        self.addStatetoTrans(t,target_state,self.targetRemainsProb)
	
	### moves north
        (new_ty, new_tx) = self.next(ty, tx, "North")
        new_target_state = toTargetString(new_ty, new_tx)
        self.addStatetoTrans(t,new_target_state,actsProb["North"])
                    
        ### moves south
        (new_ty, new_tx) = self.next(ty, tx, "South")
        new_target_state = toTargetString(new_ty, new_tx)
        self.addStatetoTrans(t,new_target_state,actsProb["South"])
	
	### moves east
        (new_ty, new_tx) = self.next(ty, tx, "East")
        new_target_state = toTargetString(new_ty, new_tx)
        self.addStatetoTrans(t,new_target_state,actsProb["East"])
                    
	### moves west
        (new_ty, new_tx) = self.next(ty, tx, "West")
        new_target_state = toTargetString(new_ty, new_tx)
        self.addStatetoTrans(t,new_target_state,actsProb["West"])

        return t        

    def printTargetState(self, xmlFile):

	xmlFile.write("\t<CondProb>\n")
        xmlFile.write("\t<Var>target_1</Var>")
	xmlFile.write("\t\t<Parent>action_robot robot_0 target_0</Parent>\n")
	xmlFile.write("\t\t<Parameter type=\"TBL\">\n\n")
	
	xmlFile.write(self.getStateEntry("*" + " " + "*" + " " + "tagged" + " " + "tagged",1.0))
	

	### for other actions beside Catch
	for robot_state in self.robotStates:
	    for target_state in	self.targetStates:
		if target_state != "tagged":	
                    [ry,rx] = toRobotState(robot_state)
                    [ty,tx] = toTargetState(target_state)
                   
                    t = self.newTargetStates(ry, rx, ty, tx, target_state)
                   
                    for i in range(len(t)):
                        if t[i][1] != 0 :
                            xmlFile.write(self.getStateEntry("*" + " " + robot_state + " " + target_state + " " + t[i][0], t[i][1]))
                            """
                            xmlFile.write(self.getStateEntry("South" + " " + robot_state + " " + target_state + " " + t[i][0], t[i][1]))
                            xmlFile.write(self.getStateEntry("East" + " " + robot_state + " " + target_state + " " + t[i][0], t[i][1]))
                            xmlFile.write(self.getStateEntry("West" + " " + robot_state + " " + target_state + " " + t[i][0], t[i][1]))
                            """
	### reset Catch
	### xmlFile.write(self.getStateEntry("Catch" + " " + "*" + " " + "*" + " " + "*", 0.0))
	#### for Action Catch
	for robot_state in self.robotStates:
	    for target_state in	self.targetStates:
		if target_state != "tagged":
                    [ry,rx] = toRobotState(robot_state)
                    [ty,tx] = toTargetState(target_state)
                    if ry==ty and rx == tx:
                        xmlFile.write(self.getStateEntry("Catch" + " " + robot_state + " " + target_state + " " + "*", 0))
 
                        xmlFile.write(self.getStateEntry("Catch" + " " + robot_state + " " + target_state + " " + "tagged", 1.0))
                        
	


	xmlFile.write("\t\t</Parameter>\n")	
        xmlFile.write("\t</CondProb>\n")
	

    def printObservation(self, xmlFile):

	xmlFile.write("<ObsFunction>")
        xmlFile.write("<CondProb>")
        xmlFile.write("<Var>obs_sensor</Var>\n")
	
	xmlFile.write("\t<Parent>action_robot robot_1 target_1</Parent>\n")
	xmlFile.write("\t<Parameter type =\"TBL\">\n\n")
	
	for robot_state in self.robotStates:
	    for target_state in	self.targetStates:
		if target_state != "tagged":
                    [ry,rx] = toRobotState(robot_state)
                    [ty,tx] = toTargetState(target_state)
		
                    if ry == ty and rx == tx:
                        obs = "yes"		
                    else:
                        obs = "O" + "rv" + str(ry) + "rh" + str(rx)
			
                    xmlFile.write(self.getObsEntry("*" + " " + robot_state + " " + target_state + " " + obs, 1.0))
		else:
                    [ry,rx] = toRobotState(robot_state)
                    obs = "O" + "rv" + str(ry) + "rh" + str(rx)
                    
                    xmlFile.write(self.getObsEntry("*" + " " + robot_state + " " + target_state + " " + obs, 1.0))
                    
		#catch. a robot always sees itself after it performs catches			
		if target_state != "tagged":
                    [ry,rx] = toRobotState(robot_state)
                    [ty,tx] = toTargetState(target_state)
                    if ry == ty and rx == tx:
                        obs = "yes"
                        xmlFile.write(self.getObsEntry("Catch" + " " + robot_state + " " + target_state + " " + obs, 0.0))
                        
                        obs = "O" + "rv" + str(ry) + "rh" + str(rx)
                        xmlFile.write(self.getObsEntry("Catch" + " " + robot_state + " " + target_state + " " + obs, 1.0))			
			
	
	xmlFile.write("\n")
	xmlFile.write("\t</Parameter>\n")
        xmlFile.write("</CondProb>")
	xmlFile.write("</ObsFunction>\n")
	

    def printReward(self, xmlFile):

	xmlFile.write("<RewardFunction>\n")
        xmlFile.write("<Func>\n")
        xmlFile.write("\t<Var>reward_robot</Var>\n")
	
	xmlFile.write("\t<Parent>action_robot robot_0 target_0</Parent>\n")
	xmlFile.write("\t<Parameter type = \"TBL\">\n\n")
	
	### for all the move actions
	xmlFile.write(self.getRewEntry("*" + " " + "*" + " " + "*", self.movePenalty))
	
	### for all the catch actions
	xmlFile.write(self.getRewEntry("Catch" + " " + "*" + " " + "*", self.tagPenalty))
	
	for robot_state in self.robotStates:
	    for target_state in	self.targetStates:
		if target_state != "tagged":
                    [ry,rx] = toRobotState(robot_state)
                    [ty,tx] = toTargetState(target_state)	
                    if ry==ty and rx ==tx:
                        xmlFile.write(self.getRewEntry("Catch" + " " + robot_state + " " + target_state, self.tagReward))
	
	if ZeroRewardForTagged == 1:
            xmlFile.write(self.getRewEntry("*" + " " + "*" + " " + "tagged", 0))
	else: # follows tagavoid.pomdp in pinneau's paper
            xmlFile.write(self.getRewEntry("Catch" + " " + "*" + " " + "tagged", 0))
            
	xmlFile.write("\n")
	xmlFile.write("\t</Parameter>\n")
        xmlFile.write("</Func>")
	xmlFile.write("</RewardFunction>\n")

    #*% Functionality:
    #*%     To generate the pomdp file
    def XmlGen(self, outFile):
        #init header values

        
        xmlFile = open(outFile,"w")
	
	xmlFile.write("<?xml version='1.0' encoding='ISO-8859-1'?>\n")
	xmlFile.write("<pomdpx version='0.1' id='tagxmlfac' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='pomdpx.xsd'>\n\n")	
	
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
	self.printReward(xmlFile)
	
        xmlFile.write("</pomdpx>\n")
	
        xmlFile.close


# Functionality:
#   to generate a string representation of the list
# Returns:
#   a string composed of 'list' items interleaved by " "
# Assumption:
#   'list' is a list of strings
def toString(list):
    s = ""
    for item in list:
        s = s+" "+str(item)

    return s

def toRobotState(ss):
    
    start = ss.find("rv")
    end = ss.find("rh")
    ry = int(ss[start+2:end])
    start = end
    end = len(ss)
    rx = int(ss[start+2:end])
    
    return [ry, rx]

def toRobotString(ry, rx):
    return "Srv" + str(ry) + "rh" + str(rx)


def toTargetState(ss):
    
    start = ss.find("tv")
    end = ss.find("th")
    ty = int(ss[start+2:end])
    start = end
    end = len(ss)
    tx = int(ss[start+2:end])
    
    return [ty, tx]

def toTargetString(ty, tx):
    return "Ttv" + str(ty) + "th" + str(tx)


#*% Testing Area...

# All actions should have zero at end states
# set it to O to follow TagAvoid.pomdp mentioned in Pinneau's paper
ZeroRewardForTagged = 1

xmlFG = TagFileGenerator()
[b, w, h] = xmlFG.ReadBitMap("tagsmall.txt")
xmlFG.XmlGen("tagsmallTerm.pomdpx")
print "Bit map:", b
print w, " ", h
