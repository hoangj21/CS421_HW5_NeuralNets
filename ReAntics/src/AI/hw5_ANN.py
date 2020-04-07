import random as rand
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *
import numpy as np
from math import exp
from random import seed
from random import random

##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "Annie")
        self.stateInList = [] #Inputs for ANN
        self.stateOutList = [] #Expected outputs for ANN 
    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = rand.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = rand.randint(0, 3)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = rand.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = rand.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]
    
    ####################################################################################################
    #getMove
    #Description: Gets the next move from the Player.
    # Mapping funtionc called here 
    # States throughout whole game are saved though here     
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ####################################################################################################
    def getMove(self, currentState):
        mapping(currentState)
        allMoves = listAllLegalMoves(currentState)

        nodes = []
        for move in allMoves:
            state = getNextState(currentState, move)

            nodes.append(SearchNode(move,state,parent=None))

        chosenBestNode = bestMove(nodes)
        
        #append a tuple that is the mapped array of the state and the evaluation
        self.stateInList.append(mapping(chosenBestNode.state))
        self.stateOutList.append(chosenBestNode.evaluation)
        #mappedIOTuple = [mapping(chosenBestNode.state), chosenBestNode.evaluation]
        #self.stateIOList.append(mappedIOTuple)
        #print("Mapped best move: " + str(mappedIOTuple))

        return chosenBestNode.move
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        print("Here")
        return enemyLocations[rand.randint(0, len(enemyLocations) - 1)]

   
    ####################################################################################################
    #registerWin
    #
    # ANN Training done here 
    ####################################################################################################
    def registerWin(self, hasWon):
        
        print("\nThe Game Ended!")
       # print("State IO List:")
       # print(self.stateInList)
       # print(self.stateOutList)
        
        #for pair in self.stateIOList:
            #print(pair)
        '''
        seed(1)
        net = initialize_network(18,13,1)
        dataset = self.stateInList
        rand.shuffle(dataset)
        train(net,dataset,.5,1000,1,self.stateOutList)
        #print(net[1])
        
        f= open("out.txt","a")
        for layer in net:
            f.write(str(layer))
        print(net[1])
        f.close()
        '''
        
        
#
#for layer in net:
	#print(layer)

        

# given a list of SearchNodes, return the Move that gives the best evaluation
def bestMove(searchNodes):

    #find the node with the best evaluation
    bestNode = min(searchNodes, key=lambda node: node.evaluation)

    return bestNode

def heuristicStepsToGoal(state):
    
    if getWinner(state) == state.whoseTurn:
        return -999
    food = getCurrPlayerFood(None,state)
    foodCoords = food[0].coords
    tunnelCoords = getConstrList(state,state.whoseTurn,types=(TUNNEL,))[0].coords
    workers = getAntList(state, state.whoseTurn, types=(WORKER,))
    drones = getAntList(state, state.whoseTurn, types=(DRONE,))
    soldiers = getAntList(state, state.whoseTurn, types=(SOLDIER,))
    r_soldiers = getAntList(state, state.whoseTurn, types=(R_SOLDIER,))
    score = 0
    if len(getAntList(state, 1-state.whoseTurn, types=(QUEEN,))) == 0:
        return -999
    queenCoords = getAntList(state, 1-state.whoseTurn, types=(QUEEN,))[0].coords
    
    if len(getAntList(state, 1-state.whoseTurn, types=(WORKER,)))!=0:
        targetCoords = getAntList(state, 1-state.whoseTurn, types=(WORKER,))[0].coords
    else:    
        targetCoords = getAntList(state, 1-state.whoseTurn, types=(QUEEN,))[0].coords
    for worker in workers:
        
        if worker.carrying == True:
            distanceFromTunnel = approxDist(worker.coords,tunnelCoords)
            score+= distanceFromTunnel
        else:
            distTunnelFood = approxDist(foodCoords,tunnelCoords)
            score+=distTunnelFood 
            distanceFromFood = approxDist(worker.coords, foodCoords)
            score += distanceFromFood
    for drone in drones + soldiers + r_soldiers:
        score+= approxDist(drone.coords,targetCoords) 
    score+=len(getAntList(state, 1-state.whoseTurn, types=(WORKER,)))*7*len(drones)  
    if len(workers) == 0:
        score+=100
    #score-=len(workers)*5 
    score-= len(drones)*30
        #add to score 11-how much food we have     
    #print("food " +str(foodCoords))
    #print("tunnel "+str(tunnelCoords))
    #score+=11-(state.inventories[state.whoseTurn].foodCount*7)    
    score = score+80
    score = score/100.0
    print(score)
    return score

####################################################################################################
# 
# mapping 
# maps a state to input values for ANN
# 18 total inputs, most of which are binary      
#    
####################################################################################################    
def mapping(state):
    inputs = [] #array of floats that are between positive (1) or negative (0)
    #Allied Data
    foods = getCurrPlayerFood(None,state)
    alliedTunnelCoords = getConstrList(state, state.whoseTurn, types=(TUNNEL,))[0].coords
    alliedAnthill = getConstrList(state, state.whoseTurn, types=(ANTHILL,))[0]
    alliedWorkers = getAntList(state, state.whoseTurn, types=(WORKER,))
    alliedFighters = getAntList(state, state.whoseTurn, types=(DRONE,SOLDIER,R_SOLDIER))
    QL = getAntList(state, state.whoseTurn, types=(QUEEN,)) #temp queenlist variable
    if (len(QL) > 0):
        alliedQueen = QL[0]
    else:
        alliedQueen = None
    #Enemy Data
    enemyTunnelCoords = getConstrList(state, 1-state.whoseTurn, types=(TUNNEL,))[0].coords
    enemyAnthill = getConstrList(state, 1-state.whoseTurn, types=(ANTHILL,))[0]
    enemyWorkers = getAntList(state, 1-state.whoseTurn, types=(WORKER,))
    enemyFighters = getAntList(state, 1-state.whoseTurn, types=(DRONE,SOLDIER,R_SOLDIER))
    QL = getAntList(state, 1-state.whoseTurn, types=(QUEEN,))
    if(len(QL) > 0):
        enemyQueen = QL[0]
    else:
        enemyQueen = None

    #1-have I won
    if getWinner(state) == state.whoseTurn:
        inputs.append(1.0)
    else:
        inputs.append(0.0)

    #2-Food %
    foodPercent = state.inventories[state.whoseTurn].foodCount/11
    inputs.append(foodPercent)

    #3-do our fighters outnumber their fighters
    if (len(alliedFighters) > len(enemyFighters)):
        inputs.append(1.0)
    else:
        inputs.append(0.0)

    #4-do their fighters outnumber our fighters
    if (len(alliedFighters) < len(enemyFighters)):
        inputs.append(1.0)
    else:
        inputs.append(0.0)

    #5-do our workers outnumber their workers
    if (len(alliedWorkers) > len(enemyWorkers)):
        inputs.append(1.0)
    else:
        inputs.append(0.0)

    #6-do their workers outnumber our workers
    if (len(alliedWorkers) < len(enemyWorkers)):
        inputs.append(1.0)
    else:
        inputs.append(0.0)

    #7-do we have a fighter close to our target
    if len(enemyWorkers)!=0:
        targetCoords = enemyWorkers[0].coords
    else:
        if (enemyQueen != None) :    
            targetCoords = enemyQueen.coords
        else:
            targetCoords = enemyAnthill.coords

    toAppend = 0.0
    if len(alliedFighters) > 0:
        for fighter in alliedFighters:
            if approxDist(fighter.coords, targetCoords) < 3:
                toAppend = 1.0
    inputs.append(toAppend)

    #8-avg fighter distance method
    if len(alliedFighters) > 0 or alliedQueen == None or enemyQueen == None:
           
        
        dist = 0
        for drone in alliedFighters:
            dist += approxDist(drone.coords,targetCoords)

        avgDist = dist / len(alliedFighters)

            #takes the distance between queens and the distance between anthills and averages them
            #intended to give an approximate "battlefield" distance to compare the numbers to
        queensDist = approxDist(alliedQueen.coords, enemyQueen.coords)
        antHillsDist = approxDist(alliedAnthill.coords, enemyAnthill.coords)
        offenceDist = (queensDist + antHillsDist) / 2

        fighterDistPerc = 1 - (avgDist / offenceDist)  #inverts the percentage to make 1 = very close to enemy valuables

            #check to see its not under 0
        if fighterDistPerc < 0:
            fighterDistPerc = 0.0
        
        inputs.append(fighterDistPerc)
    else:
        inputs.append(0.0)

    #9-a carrying worker is close to delivering food
    toAppend = 0.0

    if len(alliedWorkers) > 0:
        for worker in alliedWorkers:
            if worker.carrying == True and approxDist(worker.coords,alliedTunnelCoords) < 2:
                toAppend = 1.0

    inputs.append(toAppend)

    #10-worker distance from food avg smthd
    distSum = 0
    if len(alliedWorkers) > 0:
        for worker in alliedWorkers:
            if worker.carrying == True:
                distSum += approxDist(worker.coords,alliedTunnelCoords)
            else:
                distSum += approxDist(foods[0].coords,alliedTunnelCoords)
                distSum += approxDist(worker.coords, foods[0].coords)
            
        distAvg = distSum / len(alliedWorkers) # the average distance a worker is from delivering a food

            #will be compared with about the total distance of a trip to food
        foodToTunnelDist = 0
        for food in foods:
            foodToTunnelDist += approxDist(food.coords,alliedTunnelCoords)

        workerDistPerc = 1 - (distAvg / foodToTunnelDist) #inverts the percentage to make 1 = food delivered

            #check to see its not under 0
        if workerDistPerc < 0:
            workerDistPerc = 0.0
        
        inputs.append(workerDistPerc)
    else:
        inputs.append(0.0)
    
    #11-queen full health
    if (alliedQueen != None):
        if alliedQueen.health == 10:
            inputs.append(1.0)
        else:
            inputs.append(0.0)
    else:
        inputs.append(0.0)

    #12-Queen health %
    if (alliedQueen != None):
        inputs.append(alliedQueen.health / 10)
    else:
        inputs.append(0.0)

    #13-anthill full health
    if alliedAnthill.captureHealth == 3:
        inputs.append(1.0)
    else:
        inputs.append(0.0)

    #14-anthill health %
    inputs.append(alliedAnthill.captureHealth / 3)

    #15-enemyQueen full health
    if(enemyQueen != None):
        if enemyQueen.health == 10:
            inputs.append(1.0)
        else:
            inputs.append(0.0)
    else:
        inputs.append(0.0)

    #16-enemyQueen health %
    if (enemyQueen != None):
        inputs.append(enemyQueen.health / 10)
    else:
        inputs.append(0.0)

    #17-enemyAnthill full health
    if enemyAnthill.captureHealth == 3:
        inputs.append(1.0)
    else:
        inputs.append(0.0)

    #18-Enemy Anthill health %
    inputs.append(enemyAnthill.captureHealth / 3)

    #check that the correct amounts of inputs have been added
    if len(inputs) != 18:
        print("length of inputs was not 18!")


    return inputs


 ####################################################################################################
# 
# NEURAL NET CODE HERE
# reference: https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/
#    
####################################################################################################

def initialize_network(num_inputs, num_hidden, num_outputs):
    network = list()
    #hidden = [{'weights':[random() for i in range(num_inputs + 1)]} for i in range(num_hidden)]
    hidden = [{'weights': [0.13436424411240122, 0.8474097315830905, 0.7638093917793238, 0.2550690257394217, 0.4954361803051495, 0.4497007764674338, 0.6515953839185775, 0.7887368967179484, 0.09403693684603721, 0.02824277425990609, 0.8355015639813508, 0.43250352796653657, 0.7620165425194231, 0.001842513412591753, 0.44512365411628463, 0.7212764924022637, 0.22849868133193368, 0.9452706955539223, 0.9011639176729647], 'output': 0.9892228477286135, 'delta': -1.6825434875842683e-07},\
    {'weights': [0.030589983033553536, 0.02541360613234625, 0.5422371547737498, 0.9391491627785106, 0.38124904569264273, 0.21856150894027337, 0.4223472267146733, 0.0294046237517661, 0.22305974723439514, 0.4384152645000383, 0.4960219718107253, 0.23329418068644764, 0.2310762719698593, 0.21899076776656362, 0.45981319616660826, 0.28999134501936025, 0.021699435694783893, 0.8375779756625729, 0.5566640530813044], 'output': 0.9607123589943041, 'delta': -9.637780765255275e-07},\
    {'weights': [0.6422943629324456, 0.18589722041063397, 0.9925463573556511, 0.8599465287952899, 0.12088994892829469, 0.332711297134966, 0.7214834555569934, 0.7111926461652107, 0.936452801368433, 0.4220503547008479, 0.8299365859700412, 0.6702064591097852, 0.3032694036286425, 0.5874814988392736, 0.8823798935275718, 0.8460983111240269, 0.5051847132753146, 0.5890022579825517, 0.03442672284706424], 'output': 0.9972016670616342, 'delta': -3.570086662153543e-08},\
    {'weights': [0.24273997354306764, 0.7973544110085867, 0.4137183342528891, 0.17300740157905092, 0.5487648343811973, 0.7021929221429732, 0.674236908060768, 0.37442065182916723, 0.4384605327282245, 0.5076433246874894, 0.7773826626762185, 0.5198784652892179, 0.39219514264029764, 0.4886335681383298, 0.028515011642980027, 0.04242733803260026, 0.7023221362799087, 0.9831877173096739, 0.5921237780561303], 'output': 0.9866903066254826, 'delta': 4.197790873629822e-07},\
    {'weights': [0.393599686377914, 0.17033010009452454, 0.502126441392316, 0.9820766375385342, 0.770518918886093, 0.5394622688190822, 0.8602499492655924, 0.23212475202134047, 0.5136887709431504, 0.952259177197171, 0.5774863708047885, 0.458823294914252, 0.26897104044500486, 0.5476878724698343, 0.9568078444638123, 0.005400692453977797, 0.7833467956189752, 0.8204859119254819, 0.8858711438295936], 'output': 0.9941940038578502, 'delta': 4.935654745622513e-08},\
    {'weights': [0.7405034118331963, 0.8090577800661256, 0.5181966456302747, 0.561357864778379, 0.4260739433287067, 0.05494087564307365, 0.8698993232770905, 0.5697937959876884, 0.19902780429265465, 0.503726472935183, 0.4836761902056211, 0.35554104252284263, 0.3448289969960418, 0.5372298737157345, 0.6222405307753953, 0.6112035427606158, 0.45689787807761134, 0.027974984083842358, 0.22835610925491232], 'output': 0.9915492694585938, 'delta': 2.8878982557752504e-07},\
    {'weights': [0.1772112589385827, 0.5843368482093461, 0.8607044869955086, 0.798438940577426, 0.7970791666610791, 0.8160369656947133, 0.2551119792044804, 0.84158722113462, 0.6728354335477179, 0.08215753230826896, 0.015066954103834799, 0.012936298913087592, 0.7539630992404692, 0.24793554964169648, 0.1078649512826353, 0.6231784081407473, 0.3427991880847666, 0.06951537853084733, 0.15800184868212117], 'output': 0.9609285832941976, 'delta': 3.620790384242358e-08},\
    {'weights': [0.5273803990480128, 0.1681156980495527, 0.27292304784298793, 0.7115899271852729, 0.4547006349632926, 0.3220938771100938, 0.47375165860606727, 0.023633194947728534, 0.3866212488957183, 0.42073738326880905, 0.18771238740782184, 0.10843477510192513, 0.8994915830125372, 0.5097890635851934, 0.20876407520827903, 0.6053217226905335, 0.8167127510344039, 0.020818108509287336, 0.017537603484306375], 'output': 0.9899018447244947, 'delta': -1.192503138907864e-07},\
    {'weights': [0.146461740399346, 0.7187902823418941, 0.15952991700494054, 0.7046056278520025, 0.6781377663370582, 0.5439507923547997, 0.22028239075115355, 0.9752577485135293, 0.7974398048352865, 0.5158171908868521, 0.22206318016447607, 0.6473738180170622, 0.3937654097761033, 0.5747133627058625, 0.32011320926292897, 0.6298152611891528, 0.057652516124296845, 0.29860594962301334, 0.966770710068695], 'output': 0.9851881503175585, 'delta': 3.5822922217598145e-07},\
    {'weights': [0.8755342442351592, 0.30637399466412424, 0.858439572970525, 0.31036362735313405, 0.9392850324832898, 0.743688655115742, 0.41613646247583985, 0.25232149286749034, 0.0083658320091399, 0.878564659538084, 0.037722208214595744, 0.8192197882288087, 0.9620068027968295, 0.5700862478611917, 0.17132277279373373, 0.8675867420510048, 0.9735809137757031, 0.7040231423300713, 0.508679423693902], 'output': 0.9973152220500147, 'delta': 7.335702280048217e-08},\
    {'weights': [0.37796883434360806, 0.34692584436743706, 0.20600998559130435, 0.6741530142468641, 0.43296421604752167, 0.19458553993641767, 0.10450498330736364, 0.6660696860398193, 0.296372100203628, 0.4999681941734316, 0.3254836079899736, 0.8717594605375326, 0.8998162227487586, 0.018230936754449298, 0.20099096455473775, 0.3278786582102448, 0.9871876710420036, 0.7827003757293756, 0.339233600964911], 'output': 0.9929007893004994, 'delta': -2.179512887310704e-07},\
    {'weights': [0.21302979638081376, 0.6744317215576591, 0.8375493591072714, 0.9321874718936273, 0.3438380678132884, 0.882199943325432, 0.6870364140174546, 0.48442423668109363, 0.9853929135952564, 0.23437016327867644, 0.7250761543689697, 0.08429119854417748, 0.16930510992207878, 0.9105987516357651, 0.21257916311911537, 0.7587271508441374, 0.5998197982599468, 0.8411321957058551, 0.36771896753334266], 'output': 0.9905468991637405, 'delta': 1.509255552973914e-07},\
    {'weights': [0.34028523500198804, 0.2912039332343983, 0.8674596653842154, 0.6039825288917112, 0.9543096361262692, 0.8873973369231172, 0.13536410399873855, 0.5511897519485157, 0.10438551502674127, 0.03910851165607476, 0.07308727625395271, 0.8660622147881832, 0.7880103061468375, 0.8283998288907247, 0.34079132153818453, 0.6150798899806478, 0.7817974590543659, 0.3780396288383874, 0.5706753830206345], 'output': 0.9952338020348437, 'delta': -1.2007476310865499e-07}]
    network.append(hidden)
    #output = [{'weights':[random() for i in range(num_hidden + 1)]} for i in range(num_outputs)]
    output = [{'weights': [-0.22031273942448423, -0.35647337460255635, -0.17858741072236195, 0.4463212557398392, 0.11941742231963302, 0.48122333875728024, 0.013499042401971322, -0.16652299236565513, 0.3427824166401582, 0.38254517195334825, -0.4316671953001151, 0.22507289751351217, -0.35338819967170226, -0.3303080811576219], 'output': 0.8394685112727266, 'delta': 7.162402139217288e-05}]
    network.append(output)
    return network

#activate and sigmoid are helper functions for forward prop
def activate(inputs, weights):
   activation = weights[-1]
   for i in range(len(weights)-1):
       activation += weights[i] * inputs[i]
   return activation

def sigmoid(x):
    return 1/(1 + np.exp(-x)) 

def forward_prop(network, inputs):
	for layer in network:
		new_inputs = []
		for neuron in layer:
			activation = activate(neuron['weights'], inputs)
			neuron['output'] = sigmoid(activation)
			new_inputs.append(neuron['output'])
		inputs = new_inputs
	return inputs

#helper function for back propogation 
def transfer_derivative(output):
	return output * (1.0 - output)
def back_prop(network, expected):
	for i in reversed(range(len(network))):
		layer = network[i]
		errors = list()
		if i != len(network)-1:
			for j in range(len(layer)):
				error = 0.0
				for neuron in network[i + 1]:
					error += (neuron['weights'][j] * neuron['delta'])
				errors.append(error)
		else:
			for j in range(len(layer)):
				neuron = layer[j]
				errors.append(expected[j] - neuron['output'])
		for j in range(len(layer)):
			neuron = layer[j]
			neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])
	#f= open("error.txt","a")
	#f.write(str(network[1][0]['delta']))
       

# Update network weights with error
def update_weights(network, row, l_rate):
	for i in range(len(network)):
		inputs = row[:-1]
		if i != 0:
			inputs = [neuron['output'] for neuron in network[i - 1]]
		for neuron in network[i]:
			for j in range(len(inputs)):
				neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
			neuron['weights'][-1] += l_rate * neuron['delta']
def train(network, train, learning_rate, num_epoch, num_outputs, exp):
	for epoch in range(num_epoch):
		sum_error = 0
		for row in train:
			outputs = forward_prop(network, row)
			expected = exp
			#expected[row[-1]] = 1
			sum_error = 0#sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
			back_prop(network, expected)
			update_weights(network, row, learning_rate)            
            
def run_ANN(state):
    seed(1)
    network = initialize_network(18,13,1)
    inputs = mapping(state)
    #print(inputs)
    out = forward_prop(network, inputs)
    #print(out)
    return out[0]
    
####################################################################################################        
# Class SearchNode            
# class that represents a Node for heuristic search
# contains a parent node, a move, a state, and an evaluation
####################################################################################################            
class SearchNode:

    #given a parent SearchNode and a Move, create a new SearchNode
    def __init__(self, move, state, parent):
        self.parent = parent
        self.move = move
        self.depth = 0
        self.state = state
        #self.evaluation = self.depth + heuristicStepsToGoal(self.state)
        self.evaluation = self.depth + run_ANN(self.state)


####################################################################################################        
# getNextState         
# 
# Copy and pasted from AIPlayerUtils.py
# Commented out lines that changes state of ant.carrying to prevent a glitch h
# 
####################################################################################################            
def getNextState(currentState, move):
    # variables I will need
    myGameState = currentState.fastclone()
    myInv = getCurrPlayerInventory(myGameState)
    me = myGameState.whoseTurn
    myAnts = myInv.ants
    myTunnels = myInv.getTunnels()
    myAntHill = myInv.getAnthill()

    # If enemy ant is on my anthill or tunnel update capture health
    ant = getAntAt(myGameState, myAntHill.coords)
    if ant is not None:
        if ant.player != me:
            myAntHill.captureHealth -= 1

    # If an ant is built update list of ants
    antTypes = [WORKER, DRONE, SOLDIER, R_SOLDIER]
    if move.moveType == BUILD:
        if move.buildType in antTypes:
            ant = Ant(myInv.getAnthill().coords, move.buildType, me)
            myInv.ants.append(ant)
            # Update food count depending on ant built
            myInv.foodCount -= UNIT_STATS[move.buildType][COST]
        # ants are no longer allowed to build tunnels, so this is an error
        elif move.buildType == TUNNEL:
            print("Attempted tunnel build in getNextState()")
            return currentState

    # If an ant is moved update their coordinates and has moved
    elif move.moveType == MOVE_ANT:
        newCoord = move.coordList[-1]
        startingCoord = move.coordList[0]
        for ant in myAnts:
            if ant.coords == startingCoord:
                ant.coords = newCoord
                # TODO: should this be set true? Design decision
                ant.hasMoved = False
                # If an ant is carrying food and ends on the anthill or tunnel drop the food
                if ant.carrying and ant.coords == myInv.getAnthill().coords:
                    myInv.foodCount += 1
                    #ant.carrying = False
                for tunnels in myTunnels:
                    if ant.carrying and (ant.coords == tunnels.coords):
                        myInv.foodCount += 1
                        #ant.carrying = False
                # If an ant doesn't have food and ends on the food grab food
                if not ant.carrying and ant.type == WORKER:
                    foods = getConstrList(myGameState, 2, [FOOD])
                    for food in foods:
                        if food.coords == ant.coords:
                            pass    
                         #   ant.carrying = True
                # If my ant is close to an enemy ant attack it
                attackable = listAttackable(ant.coords, UNIT_STATS[ant.type][RANGE])
                for coord in attackable:
                    foundAnt = getAntAt(myGameState, coord)
                    if foundAnt is not None:  # If ant is adjacent my ant
                        if foundAnt.player != me:  # if the ant is not me
                            foundAnt.health = foundAnt.health - UNIT_STATS[ant.type][ATTACK]  # attack
                            # If an enemy is attacked and looses all its health remove it from the other players
                            # inventory
                            if foundAnt.health <= 0:
                                myGameState.inventories[1 - me].ants.remove(foundAnt)
                            # If attacked an ant already don't attack any more
                            break
    return myGameState        
