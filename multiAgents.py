# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]


    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        print "new pos:", newPos
        print "new food:", newFood
        print "new Ghost states: ", [state.getPosition() for state in newGhostStates]
        print "newScaredTimes: ", newScaredTimes
        score = successorGameState.getScore()

        weight = 1.0

        # evaluating ghost with respect to ghost
        mindistanceToGhost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
        if mindistanceToGhost > 0:
            if newScaredTimes[0] > 0:                       # move towards this ghost
                score += weight / mindistanceToGhost
            else:                                           # move away from ghost
                score -= weight / mindistanceToGhost

        # evaluating food with respect to food
        foodDistance = [manhattanDistance(newPos, food) for food in newFood.asList()]
        if len(foodDistance):
            score += weight / min(foodDistance)             # move towards nearest food.

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def minMax(self, state, action, agentIndex, totagents, depth):
        scorelist = []                                     #list to store scores for each action
        actions = state.getLegalActions(agentIndex)
        if depth==0 or state.isWin() or state.isLose() or len(actions)==0:
            return self.evaluationFunction(state), None
        successors = [(state.generateSuccessor(agentIndex, action), action) for action in actions]

        if agentIndex==0:                               #for pacman
            score = -99999                              #-ve infinity
            for successor,action in successors:
                v, action = self.minMax(successor, action, 1, totagents, depth)
                scorelist.append(v)
                score = max(score, v)                   #max value

            return score, actions[scorelist.index(score)]

        else :                                          #for ghost
            score = 99999                               #+ve infinity
            for successor, action in successors:
                if agentIndex<totagents-1:
                    v, action = self.minMax(successor, action, agentIndex+1, totagents, depth)  #if not last ghost
                else:
                    v, action = self.minMax(successor, action, 0, totagents, depth - 1)     #if last ghost
                scorelist.append(v)
                score = min(score, v)                  #min value
            return score, actions[scorelist.index(score)]

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        totagents=gameState.getNumAgents()

        score, action= self.minMax(gameState, None, self.index, totagents, self.depth)
        print score
        return action
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def alphaBetaMinMax(self, state, action, agentIndex, totagents, depth, alpha, beta):
        scorelist = []                              #list to store scores for each action
        actions = state.getLegalActions(agentIndex)
        if depth==0 or state.isWin() or state.isLose() or len(actions)==0:
            return self.evaluationFunction(state), None

        if agentIndex==0:                   #if pacman
            score = -99999
            for action in actions:
                successor=state.generateSuccessor(agentIndex, action)
                score = max(score, self.alphaBetaMinMax(successor, action, 1, totagents, depth, alpha, beta)[0])
                alpha = max(alpha, score)
                scorelist.append(score)
                if beta < alpha :                  #pruning
                    break
            return score, actions[scorelist.index(score)]

        else :                          #if ghosts
            score = 99999
            for action in actions:
                successor=state.generateSuccessor(agentIndex, action)
                if agentIndex<totagents-1:
                    score = min(score,self.alphaBetaMinMax(successor, action, agentIndex+1, totagents, depth, alpha, beta)[0])
                else:
                    score = min(score,self.alphaBetaMinMax(successor, action, 0, totagents, depth - 1, alpha, beta)[0])
                beta = min(beta,score)
                scorelist.append(score)
                if beta < alpha :               #pruning
                    break
            return score, actions[scorelist.index(score)]

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        totagents = gameState.getNumAgents()

        score, action = self.alphaBetaMinMax(gameState, None, self.index, totagents, self.depth, -99999, 99999)
        print score
        return action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expectiMax(self, state, action, agentIndex, totagents, depth):
        scorelist = []
        actions = state.getLegalActions(agentIndex)
        if depth == 0 or state.isWin() or state.isLose() or len(actions) == 0:
            return self.evaluationFunction(state), None
        successors = [(state.generateSuccessor(agentIndex, action), action) for action in actions]

        if agentIndex == 0:
            score = -99999
            for successor, action in successors:
                v, action = self.expectiMax(successor, action, 1, totagents, depth)
                scorelist.append(v)
                score = max(score, v)

            return score, actions[scorelist.index(score)]

        else:
            score = 0
            for successor, action in successors:
                if agentIndex < totagents - 1:
                    v, action = self.expectiMax(successor, action, agentIndex + 1, totagents, depth)
                else:
                    v, action = self.expectiMax(successor, action, 0, totagents, depth - 1)
                scorelist.append(v)
                score += 1.0/len(successors)*v          #average the scores of ghosts.
            return score, random.sample(actions,  1)    #randomly take an action for the ghost (chance) so that ghosts can act
                                                        #randomly

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        totagents = gameState.getNumAgents()

        score, action = self.expectiMax(gameState, None, self.index, totagents, self.depth)
        print score
        return action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Inspired by my reflex agent evaluation function.
      I have taken current game state score to start evaluating.
    """
    "*** YOUR CODE HERE ***";
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    weight=1.0

    score = currentGameState.getScore()

    #evaluating ghost with respect to ghost
    mindistanceToGhost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
    if mindistanceToGhost > 0:
        if newScaredTimes[0] > 0:                                   # move towards this ghost
            score += weight / mindistanceToGhost
        else:                                                       # move away from ghost
            score -= weight / mindistanceToGhost

    #evaluating food with respect to food
    foodDistance = [manhattanDistance(newPos, food) for food in newFood.asList()]
    if len(foodDistance):
        score += weight / min(foodDistance)                         #move towards nearest food.

    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

