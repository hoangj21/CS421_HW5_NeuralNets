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
        print("State IO List:")
        print(self.stateInList)
        print(self.stateOutList)
        
        #for pair in self.stateIOList:
            #print(pair)
        seed(1)
        net = initialize_network(18, 13, 1)
        dataset = self.stateInList
        train(net,dataset,.5,20,1,self.stateOutList)
        print(net[1])
        
        
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
    #print(score)
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
    alliedQueen = getAntList(state, state.whoseTurn, types=(QUEEN,))[0]
    #Enemy Data
    enemyTunnelCoords = getConstrList(state, 1-state.whoseTurn, types=(TUNNEL,))[0].coords
    enemyAnthill = getConstrList(state, 1-state.whoseTurn, types=(ANTHILL,))[0]
    enemyWorkers = getAntList(state, 1-state.whoseTurn, types=(WORKER,))
    enemyFighters = getAntList(state, 1-state.whoseTurn, types=(DRONE,SOLDIER,R_SOLDIER))
    enemyQueen = getAntList(state, 1-state.whoseTurn, types=(QUEEN,))[0]

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
        targetCoords = enemyQueen.coords 

    toAppend = 0.0
    if len(alliedFighters) > 0:
        for fighter in alliedFighters:
            if approxDist(fighter.coords, targetCoords) < 3:
                toAppend = 1.0
    inputs.append(toAppend)

    #8-avg fighter distance method
    if len(alliedFighters) > 0:
           
        
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
    if alliedQueen.health == 10:
        inputs.append(1.0)
    else:
        inputs.append(0.0)

    #12-Queen health %
    inputs.append(alliedQueen.health / 10)

    #13-anthill full health
    if alliedAnthill.captureHealth == 3:
        inputs.append(1.0)
    else:
        inputs.append(0.0)

    #14-anthill health %
    inputs.append(alliedAnthill.captureHealth / 3)

    #15-enemyQueen full health
    if enemyQueen.health == 10:
        inputs.append(1.1)
    else:
        inputs.append(0.0)

    #16-enemyQueen health %
    inputs.append(enemyQueen.health / 10)

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
	hidden = [{'weights':[random() for i in range(num_inputs + 1)]} for i in range(num_hidden)]
	network.append(hidden)
	output = [{'weights':[random() for i in range(num_hidden + 1)]} for i in range(num_outputs)]
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
        self.evaluation = self.depth + heuristicStepsToGoal(self.state)


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
