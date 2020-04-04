import random
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
                    x = random.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = random.randint(0, 3)
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
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        allMoves = listAllLegalMoves(currentState)

        nodes = []
        for move in allMoves:
            state = getNextState(currentState, move)

            nodes.append(SearchNode(move,state,parent=None))

        return bestMove(nodes)
    
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
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]


    ##
    #registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass

# given a list of SearchNodes, return the Move that gives the best evaluation
def bestMove(searchNodes):

    #find the node with the best evaluation
    bestNode = min(searchNodes, key=lambda node: node.evaluation)

    return bestNode.move

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
    
def mapping(state):
    inputs = [] #array of inputs that are either positive (1) or negative (0)
    antCoordList = []
    allAnts = getAntList(state)
    for ant in allAnts:
        antCoordList.append(ant.coords)
    
    foods = getCurrPlayerFood(None,state)

    #Allied Data
    alliedTunnelCoords = getConstrList(state, state.whoseTurn, types=(TUNNEL,))[0].coords
    alliedAnthillCoords = getConstrList(state, state.whoseTurn, types=(ANTHILL,))[0].coords
    alliedWorkers = getAntList(state, state.whoseTurn, types=(WORKER,))
    alliedFighters = getAntList(state, state.whoseTurn, types=(DRONE,SOLDIER,R_SOLDIER))
    alliedQueen = getAntList(state, state.whoseTurn, types=(QUEEN,))[0]
    allAlliedUnits = alliedWorkers + alliedFighters
    allAlliedUnits.append(alliedQueen)
    
    #Enemy Data
    enemyTunnelCoords = getConstrList(state, 1-state.whoseTurn, types=(TUNNEL,))[0].coords
    enemyAnthillCoords = getConstrList(state, 1-state.whoseTurn, types=(ANTHILL,))[0].coords
    enemyWorkers = getAntList(state, 1-state.whoseTurn, types=(WORKER,))
    enemyFighters = getAntList(state, 1-state.whoseTurn, types=(DRONE,SOLDIER,R_SOLDIER))
    enemyQueen = getAntList(state, 1-state.whoseTurn, types=(QUEEN,))[0]
    allEnemyUnits = enemyWorkers + enemyFighters
    allAlliedUnits.append(alliedQueen)

    #1-Worker in danger
    toAppend = 0
    for worker in alliedWorkers:
        if self.checkIfInAttackRange(worker.coord, enemyFighters):
            toAppend = 1
            break
    inputs.append(toAppend)

    #2-Fighter in danger
    toAppend = 0
    for fighter in alliedFighters:
        if self.checkIfInAttackRange(fighter.coord, enemyFighters):
            toAppend = 1
            break
    inputs.append(toAppend)

    #3-Queen in danger
    if self.checkIfInAttackRange(alliedQueen.coord, enemyFighters):
        inputs.append(1)
    else:
        inputs.append(0)

    #4-worker can deposit food
    workersCarrying = []
    workersEmpty = []
    for worker in alliedWorkers:
        if worker.carrying:
            workersCarrying.append(worker)
        else:
            workersEmpty.append(worker)

    #check if there are ants in tunnel
    if alliedTunnelCoords in antCoordList:
        antOnTunnel = True
    if alliedAnthillCoords in antCoordList:
        antOnAnthill = True

    #check if workers with food can move to 
    if antOnTunnel == False and antOnAnthill == False:
        if self.canMoveToCoord(workersCarrying, alliedAnthillCoords) or self.canMoveToCoord(workersCarrying, alliedTunnelCoords):
            inputs.append(1)
        else:
            inputs.append(0)
    else:
        inputs.append(0)

    #5-worker can pick up food
    #get list of unoccupied food
    freeFood = []
    for food in foods:
        if not food.coords in antCoordList:
            freeFood.append(food)
    
    toAppend = 0

    #check if unoccupied food is within the movement range of all empty workers
    for food in freeFood:
        if self.canMoveToCoord(workersEmpty, food.coords):
            toAppend = 1

    inputs.append(toAppend)

    #6-fighter can occupy enemy anthill
    if self.canMoveToCoord(alliedFighters, enemyAnthillCoords):
        inputs.append(1)
    else:
        inputs.append(0)

    #7-fighter can occupy enemy tunnel
    if self.canMoveToCoord(alliedFighters, enemyTunnelCoords):
        inputs.append(1)
    else:
        inputs.append(0)

    #8-unit not on allied tunnel
    if antOnTunnel == None :
        inputs.append(1)
    else:
        inputs.append(0)

    #9 - unit not on allied anthill
    antOnHill = getAntAt(state, alliedAnthillCoords)
    if antOnHill == None :
        inputs.append(1)
    else:
        inputs.append(0)

    #10-enemy unit in allied territory
    if self.checkIfInAlliedTerr(allEnemyUnits):
        inputs.append(1)
    else:
        inputs.append(0)


    #11-allied unit in enemy territory
    if self.checkIfInEnemyTerr(allAlliedUnits):
        inputs.append(1)
    else:
        inputs.append(0)


    #12-more fighters than opponent
    if alliedFighters.len() > enemyFighters.len() :
        inputs.append(1)
    else:
        inputs.append(0)

    #13-more workers than opponent
    if alliedWorkers.len() > enemyWorkers.len() :
        inputs.append(1)
    else:
        inputs.append(0)

    food = getCurrPlayerFood(None,state)
    #14-can purchace worker
    if food >= 1:
        inputs.append(1)
    else:
        inputs.append(0)

    #15-can purchace soldier
    if food >= 2:
        inputs.append(1)
    else:
        inputs.append(0)

    #16-have I won
    if getWinner(state) == state.whoseTurn or len(getAntList(state, 1-state.whoseTurn, types=(QUEEN,))) == 0:
        inputs.append(1)
    else:
        input.append(0)

    #check that the correct amounts of inputs have been added
    if inputs.len != 16:
        print("length of inputs was not 16!")

    return inputs

#Helper coordinateds should all return bools
#check if a coordinate is within range of any of the list ants' attack
def checkIfInAttackRange(self, coord, ants):
    return False

#check if any units in list are in enemy territory
def checkIfInEnemyTerr(self, units):
    for unit in units:
        if unit.coords[1] > 3: #check if y coord is below 3
            return True
    return False

#check if any units in list are in allied territory
def checkIfInAlliedTerr(self, units):
    for unit in units:
        if unit.coords[1] <= 3: #check if y coord is above or equal to 3
            return True
    return False

#check if any units can move to a certain coordinate
def canMoveToCoord(self, units, coord):
    return False

def out():

    return
    
def sigmoid(x):
    return 1/(1 + np.exp(-x)) 
    
def backprop():

    return    

# class that represents a Node for heuristic search
# contains a parent node, a move, a state, and an evaluation
class SearchNode:

    #given a parent SearchNode and a Move, create a new SearchNode
    def __init__(self, move, state, parent):
        self.parent = parent
        self.move = move
        self.depth = 0
        self.state = state
        self.evaluation = self.depth + heuristicStepsToGoal(self.state)

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

    """
    Inputs
    1-Worker in danger
    2-Fighter in danger
    3-Queen in danger
    4-fighter can attack
    5-queen can attack
    6-worker can deposit food
    7-worker can pick up food
    8-fighter can destroy enemy
    9-fighter can occupy anthill
    10-fighter can occupy tunnel
    11-unit on allied tunnel
    12-enemy unit in allied territory
    13-allied unit in enemy territory
    14-less fighters than opponent
    15-less workers than opponent
    16-can purchace unit
    17-have I won
    """