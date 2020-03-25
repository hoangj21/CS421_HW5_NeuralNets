#Joanna and Harry
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

import heapq

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
        super(AIPlayer,self).__init__(inputPlayerId, "Heuristic")
    
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
    #For A* search 
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        us = currentState.whoseTurn

        #frontier nodes = terminal nodes 
        # if terminal node
        #base case, current depth = max depth or if terminal
        #recurse 
        #get all possible actions, for each action, call method 

        #create list of frontier nodes
        #create list of expanded nodes
        frontierNodes = PriorityQueue()
        expandedNodes = []
        root = SearchNode(None, currentState, None)

        frontierNodes.push(root)

        for n in range(3):
            frontier.sort(key=lambda node: node.evaluation)

            bestNode = frontierNodes.pop()

            new_nodes = self.expandNode(bestNode)
            frontierNodes.pushAll(new_nodes)

            expandedNodes.append(bestNode)

        # bestNode = min(frontierNodes, key=lambda node: node.evaluation)
        bestExpanded = min(expandedNodes[1:])
        bestFrontier = frontierNodes.pop()
        bestNode = min(bestExpanded, bestFrontier)

        print("score: " + str(bestNode.evaluation))
        curr = bestNode
        while curr.parent != root:
            curr = curr.parent 
        print("current: " + str(curr.evaluation))
        return curr.move

    #reuse method to get next moves 
    #put a check here for if its our turn
    #pos value if its us, neg val if its enemy 
    def expandNode(self,node):
        allMoves = self.listAllValidMoves(node.state)

        nodes = []
        for move in allMoves:
            state = getNextState(node.state, move)
            if(state.whoseTurn == 1):
                eval = self.hueristicStepsToGoal(state)
            else:
                eval = 1 - self.hueristicStepsToGoal(state)
            nodes.append(SearchNode(move,state,node))

        return nodes

    def listAllValidMoves(self, state):
        legalMoves = listAllLegalMoves(state)

        canMove = False

        for move in legalMoves:
            if move.moveType == MOVE_ANT:
                canMove = True
                break

        #if we can move ant ant, don't list end turn as a valid option
        if canMove:
            #end turn is the back of the list
            legalMoves = legalMoves[:-1]

        return legalMoves

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

#Note to self for changes for part b 
#food needed 
#num workers
#score= steps to food win = steps to collect food * food needed / num workers
#steps to make a food is steps to collect a food /num workers 
#steps to make a drone 2* steps to make a food 
#steps to queen for drone = distance to queen/3 
#steps to attack queen = steps to make drone + steps to queen 
#steps to kill queen = queen's health / 4 * steps to attack queen   


#compute steps to collect food 
def hueristicStepsToGoal(state):
    #return an arbitrarily small score if we're the winner
    if getWinner(state) == state.whoseTurn:
        return -9999

    #get food and food coordinates    
    food = getCurrPlayerFood(None,state)
    foodCoords = food[0].coords

    #Get tunnel coordinates
    tunnelCoords = getConstrList(state,state.whoseTurn,types=(TUNNEL,))[0].coords
    
    #get lists for ants 
    workers = getAntList(state, state.whoseTurn, types=(WORKER,))
    drones = getAntList(state, state.whoseTurn, types=(DRONE,))
    soldiers = getAntList(state, state.whoseTurn, types=(SOLDIER,))
    r_soldiers = getAntList(state, state.whoseTurn, types=(R_SOLDIER,))
    
    #initialize score. Higher score is worse. 
    score = 0

    #If there is no enemy queen, return arbitrarily small score
    if len(getAntList(state, 1-state.whoseTurn, types=(QUEEN,))) == 0:
        return -9999
    
    #Aim to attack workers, if there are no workers, aim to attack queen
    if len(getAntList(state, 1-state.whoseTurn, types=(WORKER,)))!=0:
        targetCoords = getAntList(state, 1-state.whoseTurn, types=(WORKER,))[0].coords
    else:    
        targetCoords = getAntList(state, 1-state.whoseTurn, types=(QUEEN,))[0].coords

    #it's bad if the queen is on the food
    queenCoords = getAntList(state,state.whoseTurn,types=(QUEEN,))[0].coords
    if queenCoords == tunnelCoords or queenCoords == foodCoords:
        score+= 50

    for worker in workers:
        
        #If the worker is carrying food, add the distance to the tunnel to the score
        if worker.carrying == True:
            distanceFromTunnel = approxDist(worker.coords,tunnelCoords)
            score+= distanceFromTunnel

        #if the worker is not carrying food, add the distance from the food and tunnel to the score     
        else:
            distTunnelFood = approxDist(foodCoords,tunnelCoords)
            score+=distTunnelFood 
            distanceFromFood = approxDist(worker.coords, foodCoords)
            score += distanceFromFood

    #Add distance from fighter ants to their targets to score         
    for drone in drones + soldiers + r_soldiers:
        score+= approxDist(drone.coords,targetCoords) 

    #punishment for if the enemy has workers     
    score+=len(getAntList(state, 1-state.whoseTurn, types=(WORKER,)))*7*len(drones)  
    
    #Heavy punishment for not having workers, since workers are needed to win 
    if len(workers) == 0:
        score+=100
    score-= 10* state.inventories[state.whoseTurn].foodCount
    #Reward for building drones 
    score-= len(drones)*30

    return score

# class that represents a Node for heuristic search
# contains a parent node, a move, a state, and an evaluation
class SearchNode:

    #given a parent SearchNode and a Move, create a new SearchNode
    def __init__(self, move, state, parent):
        self.parent = parent
        self.move = move
        if self.parent == None:
            self.depth = 0
        else:
            if move.moveType == MOVE_ANT:
                moveCost = 1
            elif move.buildType == WORKER:
                moveCost = 100
            else:
                moveCost = 1

            self.depth = parent.depth + moveCost

        self.state = state
        self.evaluation = self.depth + hueristicStepsToGoal(self.state)

    def __str__(self):
        return '<{} {} {}>'.format(self.move, self.evaluation, self.depth)

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.evaluation < other.evaluation

# class PriorityQueue:
#     def __init__(self):
#         self.heap = []
#
#     def push(self, elem):
#         heapq.heappush(self.heap, elem)
#
#     def pushAll(self, elems):
#         for elem in elems:
#             self.push(elem)
#
#     def pop(self):
#         return heapq.heappop(self.heap)

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, elem):
        self.heap.append(elem)

    def pushAll(self, elems):
        self.heap+= elems

    def pop(self):
        best = min(self.heap)
        self.heap.remove(best)
        return best

#Copy and pasted from AIPlayerUtils.py
#Commented out lines that changes state of ant.carrying to prevent a glitch 
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

#Unit tests

#Make a player and make them move, and test getMove()
def getMoveTest():
    state = getGameState()
    player = AIPlayer(0)
    playerMove = player.getMove(state)
    move = Move(MOVE_ANT,[(9,0),(8,0),(8,1)],None)
    if move.moveType != playerMove.moveType:
        print("Move type not the same")
    if move.coordList != playerMove.coordList:    
        print("Coord list not the same")

#make nodes and moves and test bestmove()    
def bestMoveTest():
    state = getGameState()
    move1 = Move(None,None,None)
    node1 = SearchNode(move1,state,None)
    node1.evaluation = 10

    move2 = Move(None,None,None)
    node2 = SearchNode(move2,state,None)
    node2.evaluation = 5
    actualMove = bestMove([node1, node2])

    if actualMove is not move2:
        print("Best Move Test error")

#Make a simple game state, and test the scores
def hueristicStepsToGoalTest():
    #get game state
    state = getGameState()
    myAnt = Ant((0,6), DRONE, 0)
    enemyAnt = Ant((0,3), WORKER, 1)
    state.inventories[state.whoseTurn].ants.append(myAnt)
    state.inventories[1-state.whoseTurn].ants.append(enemyAnt)
    
    #dist to enemy + round trip for worker to get food 
    #+punishment for enemy having 2 workers - we have 1 drone
    #equals 5
    score = 3+18+14-30
    testScore = hueristicStepsToGoal(state)
    if(score !=testScore):
        print("Scores do not match")    

      
#get a game state with some food and a worker on the tunnel
def getGameState():
    state = GameState.getBasicState()

    playerInventory = state.inventories[state.whoseTurn]
    enemyInventory = state.inventories[1-state.whoseTurn]

    playerInventory.constrs.append(Construction((1,1),FOOD))
    enemyInventory.constrs.append(Construction((2,2),FOOD))

    enemyInventory.constrs.append(Construction((8,8), FOOD))
    enemyInventory.constrs.append(Construction((7,7), FOOD))

    playerTunnel = playerInventory.getTunnels()[0].coords
    enemyTunnel = enemyInventory.getTunnels()[0].coords

    playerInventory.ants.append(Ant(playerTunnel,WORKER,state.whoseTurn))
    enemyInventory.ants.append(Ant(enemyTunnel,WORKER,1-state.whoseTurn))

    state.inventories[2].constrs = playerInventory.constrs + enemyInventory.constrs
    state.inventories[2].ants = playerInventory.ants + enemyInventory.ants

    return state

if __name__ == "__main__":
    getMoveTest()
    bestMoveTest()
    hueristicStepsToGoalTest()