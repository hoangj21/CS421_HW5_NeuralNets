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


class AIPlayer(Player):

    # __init__
    # Description: Creates a new Player
    #
    # Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer, self).__init__(inputPlayerId, "Cheetah")

    ##
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
    # getMove
    # Description: Gets the next move from the Player.
    #
    # Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    # Return: The Move to be made
    ##
    def getMove(self, currentState):
        myId = currentState.whoseTurn
        frontier0 = []
        frontier1 = []
        frontier2 = []
        #frontier3 = []
        #expanded = []
        root = Node(None, currentState,0, 0, None)
        frontier0.extend(self.expandNode(root))
        for node in frontier0:
            node.evaluation = self.heuristicStepsToGoal(node.state)

        for i in range(len(frontier0)):
            if frontier0[i] is None:
                continue
            # Expand the first node in list 1, populate list2 with just the jth batch.
            frontier1.extend(self.expandNode(frontier0[i]))

            # for j in range(len(frontier1)):

            #     # Expand first node in list 2, populate list3 with just the kth batch
            #     frontier2.extend(self.expandNode(frontier1[j]))

            #     for node in frontier2:

            #         if node.parent.depth == -1:
            #             continue
            #         elif node.parent.parent.depth == -1:
            #             node.parent.depth = -1
            #             continue
            #         elif node.evaluation is None:
            #             node.evaluation = self.heuristicStepsToGoal(node.state)

            #         # Pass value ranges up to parent nodes, else delete current node.
            #         if myId == node.parent.state.whoseTurn:
            #             if node.parent.evaluation is None or node.evaluation > node.parent.evaluation:
            #                 node.parent.evaluation = node.evaluation
            #                 #self.pruneParents(myId, node)
            #         else:
            #             if node.parent.evaluation is None or -(node.evaluation) < node.parent.evaluation:
            #                 node.parent.evaluation = -(node.evaluation)
            #                 #self.pruneParents(myId, node)
            #     frontier2 = []
            # frontier1 = []

        for node in frontier0:
            actualEval = self.heuristicStepsToGoal(node.state)
            averageEval = (node.evaluation + actualEval) / 2
            node.evaluation = averageEval

        # Return the best move in list1
        frontier0.sort(key=lambda node: node.evaluation, reverse=True)
        return frontier0[0].move

    # Takes in a list of nodes
    # returns the node with the lowest evaluation

    def bestMove(self, listOfNodes, state, turn):
        bestNode = listOfNodes[0]
        for node in listOfNodes:
            if node.evaluation < bestNode.evaluation:
                bestNode = node
        return bestNode.move

##
    # heuristicStepsToGoal
    # Parameters:
    #   currentState - the state of the game at this point in time.
    # returns number that represents how good the state is
    #
    def heuristicStepsToGoal(self, currentState):
        myState = currentState
        steps = 0

        #it's me!
        me = myState.whoseTurn
        enemy = 1-me

        #fetching constructions
        tunnels = getConstrList(myState, types = (TUNNEL,))
        hills = getConstrList(myState, types = (ANTHILL,))
        allFoods = getConstrList(myState, None, (FOOD,))


        #finding out what belongs to whom
        myInv = getCurrPlayerInventory(myState)
        myFoodCount = myInv.foodCount
        # my items/constructs/ants
        myTunnel = myInv.getTunnels()[0]
        myHill = getConstrList(currentState, me, (ANTHILL,))[0]
        myWorkers = getAntList(myState, me, (WORKER,))
        mySoldiers = getAntList(myState, me, (SOLDIER,))
        myRSoldiers = getAntList(myState, me, (R_SOLDIER,))
        myDrones = getAntList(myState, me, (DRONE,))
        myQueen = myInv.getQueen()
        myAnts = myInv.ants
        # enemy items/constructs/ants
        enemyInv = getEnemyInv(self, myState)
        enemyTunnel = enemyInv.getTunnels()[0]
        enemyHill = getConstrList(currentState, enemy, (ANTHILL,))[0]
        enemyWorkers = getAntList(myState, enemy, (WORKER,))
        ememySoldiers = getAntList(myState, enemy, (SOLDIER,))
        enemyRSoldiers = getAntList(myState, enemy, (R_SOLDIER,))
        enemyDrones = getAntList(myState, enemy, (DRONE,))
        enemyQueen = enemyInv.getQueen()
        #arbitrary food distance value for workers to work around
        foodDist = 9999999
        foodTurns = 0
        isTunnel = False

        # If-statements intended to punish or reward the agent based upon the status of the environment
        if enemyWorkers == None or enemyWorkers == []:
            steps -=1000
        if len(enemyWorkers) > 0:
            steps += 150
        if enemyQueen == None:
            steps -= 10000
        if len(myWorkers) < 1:
            steps += 150
        if myQueen.health == 0:
            steps += 999999999
        if myQueen.coords == myHill.coords:
            steps += 50
        for food in allFoods:
            if myQueen.coords == food.coords:
                steps += 20
        if len(myDrones) < 1:
            steps += 350
        elif len(myDrones) < 2:
            steps += 40
        elif len(myDrones) > 4:
            steps += 20
        if len(mySoldiers) < 1:
            steps += 25
        
        # iteration through worker array to 
        for worker in myWorkers: 
            if worker.carrying: #worker has food; go to the hill
                distToTunnel = approxDist(worker.coords, myTunnel.coords)
                distToHill = approxDist(worker.coords, myHill.coords)
                foodDist = min(distToTunnel, distToHill) - 0.2
                if worker.coords == myHill.coords or worker.coords == myTunnel.coords:
                    foodDist = 0.2 #scalar for good food retrieval
            else: # Otherwise, we want to move toward the food
                if worker.coords == myHill.coords or worker.coords == myTunnel.coords:
                    foodDist = 0.2 #scalar for good food retrieval
                closestFoodDist = 99999
                bestFood = None
                for food in allFoods:
                    distToCurrFood = approxDist(worker.coords, food.coords)
                    if worker.coords == food.coords:
                        bestFood = food
                        closestFoodDist = 0.01 #scalar for good food retrieval
                        break
                    if distToCurrFood <= closestFoodDist:
                        closestFoodDist = distToCurrFood
                        bestFood = food
                foodDist = closestFoodDist
                if approxDist(myQueen.coords, bestFood.coords) <= approxDist(worker.coords, bestFood.coords):
                    steps += 75  
            steps += foodDist * (11 - myInv.foodCount)

        #aiming for a win through offense
        attackDist = 999999
        for drone in myDrones:
            # primary target for drones is enemy queen
            if enemyQueen != None:            
                steps += approxDist(drone.coords, enemyQueen.coords)
            else:
                attackDist = approxDist(drone.coords, enemyHill.coords)
            steps += attackDist
                

        # # Target enemy workers with soldiers, then move to the anthill
        for soldier in mySoldiers:
            if len(enemyWorkers) > 0:
                for worker in enemyWorkers:
                    stepsToWorker = approxDist(soldier.coords, worker.coords) + 1
                    stepsToHill = approxDist(soldier.coords, enemyHill.coords) + 1
                    if stepsToWorker <= stepsToHill:
                        steps += stepsToWorker
                    else: steps += stepsToHill
            else:
                stepsToHill = approxDist(soldier.coords, enemyHill.coords) + 1
                steps += stepsToHill
            if soldier.coords == enemyHill.coords:
                steps -= 200
        # this is intended to keep an ant on the enemy hill if it happens to make its way there
        for ant in myAnts:
            if ant.coords == enemyHill.coords:
                steps -= 100000
        if len(myWorkers) >= 2:
            steps -= 1000
        return steps 

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
        moves = listAllLegalMoves(node.state)
        listOfNodes = []
        # myInv = node["state"].inventories[myId]
        myId = node.state.whoseTurn
        myDrones = getAntList(node.state, myId, (DRONE,))
        for move in moves:
            if len(myDrones) > 0 and "<Move: BUILD DRONE" in str(move):
                continue
            if "<Move: BUILD WORKER" in str(move):
                continue
            if "<Move: BUILD RANGED" in str(move):
                continue
            if "<Move: BUILD SOLDIER" in str(move):
                continue
            nextState = getNextStateAdversarial(node.state, move)
            curNode = Node(move, nextState, node.depth+1, 0, node)
            listOfNodes.append(curNode)
        return listOfNodes


class Node:
    def __init__(self, move, state, depth, steps, parent):
        self.move = move
        self.state = state
        self.depth = depth
        self.evaluation = None
        self.parent = parent


# # tests for heuristic steps to goal functions
# ai = AIPlayer(random)
# state = GameState(None, None, None, None)
# state = state.getBasicState()

# # test for spawnWorker
# # assert ai.spawnWorker(state) == 200

# # adds a worker to player 0 inventory
# worker = Ant((1, 1), WORKER, 0)
# state.inventories[0].ants.append(worker)

# # test for spawning worker
# # returns -50 if you have 1 worker
# assert ai.spawnWorker(state) == -30


# assert ai.anthillDistance(state) == 0

# # test for spawnDrone
# assert ai.spawnDrone(state) == 50

# drone = Ant((3, 3), DRONE, 0)
# state.inventories[0].ants.append(drone)
# assert ai.spawnDrone(state) == -30

# # checks if function returns distance greater than zero
# assert ai.anthillDistance(state) > 0

# drone2 = Ant((3, 4), DRONE, 0)
# state.inventories[0].ants.append(drone2)
# assert ai.spawnDrone(state) == 50

# food = Construction((1, 4), FOOD)
# state.inventories[2].constrs.append(food)


# assert ai.minDistanceToTarget(state, [state.inventories[0].getAnthill()],
#                               getConstrList(state, 2, (FOOD,)))[0] < 30
# assert ai.minDistanceToTarget(state, [state.inventories[0].getAnthill()],
#                               getConstrList(state, 2, (FOOD,)))[1] == getConstrList(state, 2, (FOOD,))[0]


# food2 = Construction((2, 3), FOOD)
# food3 = Construction((6, 8), FOOD)
# food4 = Construction((7, 5), FOOD)
# state.inventories[2].constrs.append(food2)
# state.inventories[2].constrs.append(food3)
# state.inventories[2].constrs.append(food4)
# # foodDistance
# assert ai.foodDistance(state) > 0

# assert ai.heuristicStepsToGoal(state) > 0

# # tests the bestMove method, returns node with smallest eval
# #node1 = Node(None, None, 50)
# #node2 = Node(None, None, 25)
# #nodes = [node1, node2]
# # assert ai.bestMove(nodes) == node2
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