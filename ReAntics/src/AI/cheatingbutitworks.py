import time
from AIPlayerUtils import *
from GameState import *
from Move import Move
from Ant import UNIT_STATS
from Construction import CONSTR_STATS
from Constants import *
from Player import *
import random
import sys

sys.path.append("..")  # so other modules can be found in parent dir

##
# AIPlayer
# Description: The responsbility of this class is to interact with the game by
# deciding a valid move based on a given game state. This class has methods that
# will be implemented by students in Dr. Nuxoll's AI course.
#
# Variables:
#   playerId - The id of the player.
##

'''
Authors: Joanna, Polina, Hera
'''

class AIPlayer(Player):

    # __init__
    # Description: Creates a new Player
    #
    # Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer, self).__init__(inputPlayerId, "Searcher")

    #############################################################################################
    # getPlacement
    #
    # Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    # Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    # Return: The coordinates of where the construction is to be placed
    #############################################################################################
    def getPlacement(self, currentState):
        numToPlace = 0
        # implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:  # stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    # Choose any x location
                    x = random.randint(0, 9)
                    # Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    # Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        # Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:  # stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    # Choose any x location
                    x = random.randint(0, 9)
                    # Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    # Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        # Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]

    ###########################################################################################
    # getMove
    # Description: Gets the next move from the Player.
    #
    # Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    # Return: The Move to be made
    ###########################################################################################
    def getMove(self, currentState):
        #Defining layers through depth 3 for expansion and evaluation  
        frontier0 = []
        frontier1 = []
        frontier2 = []
        frontier3 = []
        expanded = []

        root = Node(None, currentState,
                    self.heuristicStepsToGoal(currentState), 0, None)
        frontier0.append(root)

        #expand layers
        for i in range(len(frontier0)):
            frontier1 += self.expandNode(frontier0[i])

        for i in range(len(frontier1)):
            frontier2 += self.expandNode(frontier1[i])

        for i in range(len(frontier2)):
            frontier3 += self.expandNode(frontier2[i])

        #evaluate leaves 
        for i in range(len(frontier3)):
            frontier3[i].evaluation = self.heuristicStepsToGoal(
                frontier3[i].state)

        frontier3.sort(key=lambda node: node.evaluation)
        frontier3 = frontier3[:5]

        #go through layer and evaluate best moves 
        if(currentState.whoseTurn == 1):
            self.bestMove(frontier3, currentState, 0)
        else:
            self.bestMove(frontier3, currentState, 1)

        for i in range(len(frontier2)):
            if(frontier2[i].evaluation is None):
                frontier2[i].evaluation = self.heuristicStepsToGoal(frontier2[i].state)

        if(currentState.whoseTurn == 1):
            self.bestMove(frontier2, currentState, 0)
        else:
            self.bestMove(frontier2, currentState, 1)

        for x in frontier1:
            if x.evaluation is None:
                frontier1.remove(x)

        if(currentState.whoseTurn == 1):
            self.bestMove(frontier1, currentState, 0)
        else:
            self.bestMove(frontier1, currentState, 1)

        #averaging evaluations 
        for i in range(len(frontier1)):
            ave = (self.heuristicStepsToGoal(
                frontier1[i].state) + frontier1[i].evaluation) / 2
            frontier1[i].evaluation = ave

        frontier1.sort(key=lambda node: node.evaluation)
        return frontier1[0].move

    ############################################################################################
    # bestMove
    # Parameters:
    #   listOfNodes- takes in a node layer  
    # returns the node with the lowest evaluation
    ###########################################################################################
    def bestMove(self, listOfNodes, state, turn):
        #evaluate decisions based on turn 
        if turn == 1:
            for node in listOfNodes:
                if node.parent.evaluation == None or node.parent.evaluation > node.evaluation:
                    node.parent.evaluation = node.evaluation
        else:
            for node in listOfNodes:
                if node.parent.evaluation == None or node.parent.evaluation > node.evaluation:
                    node.parent.evaluation =  0 - node.evaluation

   ###########################################################################################
    # heuristicStepsToGoal
    # Parameters:
    #   currentState - the state of the game at this point in time.
    # returns number that represents how good the state is
   ###########################################################################################

    def heuristicStepsToGoal(self, state):
        if state.inventories[state.whoseTurn].foodCount == 11:
            return 0
        queen = state.inventories[1-state.whoseTurn].getQueen()
        if not queen:
            return 0
        if state.inventories[1 - state.whoseTurn].getAnthill().captureHealth <= 0:
            return 0

        if len(getAntList(state, state.whoseTurn, (SOLDIER, R_SOLDIER))) != 0:
            return 1000

        turns = 0
        turns += self.foodDistance(state)-30
        turns += self.spawnDrone(state)+40
        turns += self.anthillDistance(state)-20
        # turns += self.queenToAnthill(state)
        turns += self.spawnWorker(state) + 40
        turns += self.noWorkers(state)+40

        if turns < 0:
            return 5
        return turns

        
    ###########################################################################################
    # Helper functions for heuristic function
    # #########################################################################################  
        
    def spawnWorker(self, state):
        workerList = getAntList(state, state.whoseTurn, (WORKER,))
        if len(workerList) != 1:
            return 200

        return -30

    # from the state passed in, it returns the approx number of moves to reach 11 food
    def foodDistance(self, state):

        foodNeeded = 11-getCurrPlayerInventory(state).foodCount

        # get locations of worker ants, food, and anthill/tunnel
        workers = getAntList(state, state.whoseTurn, (WORKER,))
        foodSpots = getCurrPlayerFood(self, state)
        buildings = getConstrList(state, state.whoseTurn, (ANTHILL, TUNNEL))

        # gets the min distance from a food to a building
        foodToDropDist, bestFood, bestBuilding = self.minDistanceToTarget(
            state, buildings, foodSpots)

        # bestFood = foodSpots[0]
        # tunnel = getConstrList(state, state.whoseTurn, (TUNNEL,))[0]
        # foodToDropDist = stepsToReach(state, bestFood.coords, tunnel.coords)
        foodToDropRoundTrip = foodToDropDist*2

        # estimate on how many turns it will take to reach 11 food
        turns = (foodNeeded-1)*foodToDropRoundTrip+2

        # finds turns needed to get next food
        if len(workers) == 0:
            return 75
        ant = workers[0]
        if ant.carrying:
            dist = approxDist(ant.coords, bestBuilding.coords)
        else:
            dist = approxDist(ant.coords, bestFood.coords)+foodToDropDist

        turns += dist
        return turns

    # helper function for foodScore
    # finds the shortest path between either of the food spots and either the tunnel or anthill
    def minDistanceToTarget(self, state, constrs, foodSpots):
        minDist = 30
        for con in constrs:
            dist = approxDist(foodSpots[0].coords, con.coords)
            if dist < minDist:
                minDist = dist
                bestFood = foodSpots[0]
                bestBuild = con

        return minDist, bestFood, bestBuild

    def queenToAnthill(self, state):
        queen = getAntList(state, state.whoseTurn, (QUEEN,))[0]
        if getConstrAt(state, queen.coords):
            return 30
        dist = stepsToReach(state, queen.coords, (5, 1))
        return dist

    def spawnDrone(self, state):
        droneList = getAntList(state, state.whoseTurn, (DRONE,))
        if len(droneList) == 1:
            return -30
        enemyQueen = getEnemyInv(None, state).getQueen()
        if not enemyQueen:
            return -100
        if len(droneList) == 2 and enemyQueen.coords != getEnemyInv(None, state).getAnthill().coords:
            return -50
        return 50

    def anthillDistance(self, state):
        # locations
        enemyTunnel = getEnemyInv(self, state).getTunnels()[0]
        enemyAnthill = getEnemyInv(self, state).getAnthill()
        myAttackList = getAntList(state, state.whoseTurn, (DRONE,))

        turns = 0

        if (len(myAttackList)) == 0:
            return 0

        if (len(myAttackList) == 1):
            # gets the min distance from a drone to enemy anthill
            droneToTunnel = approxDist(
                myAttackList[0].coords, enemyTunnel.coords)
            turns += droneToTunnel
        elif (len(myAttackList) >= 2):
            droneToTunnel = approxDist(
                myAttackList[0].coords, enemyTunnel.coords)
            turns += droneToTunnel
            droneToTunnel = approxDist(
                myAttackList[1].coords, enemyAnthill.coords)
            turns += droneToTunnel
        return turns

    def getAttack(self, currentState, attackingAnt, enemyLocations):
        # Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    def noWorkers(self, state):
        workers = getAntList(state, state.whoseTurn, (WORKER,))
        drones = getAntList(state, state.whoseTurn, (DRONE,))
        enemyAnts = getAntList(state, 1-state.whoseTurn)
        if len(workers) == 0 and len(drones) != 0 and len(enemyAnts) != 0:
            dist = approxDist(drones[0].coords, enemyAnts[0].coords)
            return dist*5
        return 0

    # takes a single node
    # returns all nodes that can be reached from that node
    def expandNode(self, node):
        # gets all legal moves from the state in the node
        moves = listAllLegalMoves(node.state)
        nodes = []
        for move in moves:
            state = getNextStateAdversarial(node.state, move)
            nodes.append(Node(move, state, self.heuristicStepsToGoal(state), node.depth+1, node))

        return nodes

###########################################################################################
# Node Class
###########################################################################################
class Node:
    def __init__(self, move, state, eval, depth=0, parent=None, child=None):
        self.move = move
        self.state = state
        self.depth = depth
        self.evaluation = eval
        self.parent = parent
        self.child = child

###########################################################################################
# Unit Tests
###########################################################################################

# tests for heuristic steps to goal functions
ai = AIPlayer(random)
state = GameState(None, None, None, None)
state = state.getBasicState()


# test for spawnWorker
# assert ai.spawnWorker(state) == 200

# adds a worker to player 0 inventory
worker = Ant((1, 1), WORKER, 0)
state.inventories[0].ants.append(worker)

# test for spawning worker
# returns -50 if you have 1 worker
assert ai.spawnWorker(state) == -30


assert ai.anthillDistance(state) == 0

# test for spawnDrone
assert ai.spawnDrone(state) == 50

drone = Ant((3, 3), DRONE, 0)
state.inventories[0].ants.append(drone)
assert ai.spawnDrone(state) == -30

# checks if function returns distance greater than zero
assert ai.anthillDistance(state) > 0

drone2 = Ant((3, 4), DRONE, 0)
state.inventories[0].ants.append(drone2)
assert ai.spawnDrone(state) == 50

food = Construction((1, 4), FOOD)
state.inventories[2].constrs.append(food)


assert ai.minDistanceToTarget(state, [state.inventories[0].getAnthill()],
                              getConstrList(state, 2, (FOOD,)))[0] < 30
assert ai.minDistanceToTarget(state, [state.inventories[0].getAnthill()],
                              getConstrList(state, 2, (FOOD,)))[1] == getConstrList(state, 2, (FOOD,))[0]


food2 = Construction((2, 3), FOOD)
food3 = Construction((6, 8), FOOD)
food4 = Construction((7, 5), FOOD)
state.inventories[2].constrs.append(food2)
state.inventories[2].constrs.append(food3)
state.inventories[2].constrs.append(food4)
# foodDistance
assert ai.foodDistance(state) > 0

assert ai.heuristicStepsToGoal(state) > 0

# tests the bestMove method, returns node with smallest eval
node1 = Node(None, None, 50)
node2 = Node(None, None, 25)
nodes = [node1, node2]
# assert ai.bestMove(nodes) == node2
