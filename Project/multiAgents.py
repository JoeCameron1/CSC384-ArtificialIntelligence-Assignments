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

#Solution by Joseph Manfredi Cameron


from util import manhattanDistance
from game import Directions
import random, util
import datetime

from game import Agent

def scoreEvaluationFunction(currentGameState):
   """
     This default evaluation function just returns the score of the state.
     The score is the same one displayed in the Pacman GUI.

     This evaluation function is meant for use with adversarial search agents
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
        
        value = float('-inf')
	action = Directions.STOP
	
	for legalAction in gameState.getLegalActions(0):
		temp = self.minValue(0, 1, gameState.generateSuccessor(0, legalAction))
		if temp > value and legalAction != Directions.STOP:
			value = temp
			action = legalAction

	return action

    

    def maxValue(self, depth, agent, state):

		if depth == self.depth:
			return self.evaluationFunction(state)

		else:
			
			if len(state.getLegalActions(agent)) > 0:
				maximumValue = float('-inf')
			else:
				maximumValue = self.evaluationFunction(state)

			for legalAction in state.getLegalActions(agent):
				successor = self.minValue(depth, agent+1, state.generateSuccessor(agent, legalAction))
				if successor > maximumValue:
					maximumValue = successor

			return maximumValue

    

    def minValue(self, depth, agent, state):

		if depth == self.depth:
			return self.evaluationFunction(state)

		else:

			if len(state.getLegalActions(agent)) > 0:
				minimumValue = float('inf')
			else:
				minimumValue = self.evaluationFunction(state)

			for legalAction in state.getLegalActions(agent):
				if agent == state.getNumAgents() - 1:
					successor = self.maxValue(depth+1, 0, state.generateSuccessor(agent, legalAction))
					if successor < minimumValue:
						minimumValue = successor
				else:
					successor = self.minValue(depth, agent+1, state.generateSuccessor(agent, legalAction))
					if successor < minimumValue:
						minimumValue = successor

			return minimumValue




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        alpha = float("-inf")
	beta = float("inf")

	
        # Select either max or min value.
       	def minimaxValue(agent, depth, state, alpha, beta):

		if depth == self.depth:
			return [self.evaluationFunction(state), 0]
		elif agent == 0:
			return maxValue(agent, depth, state, alpha, beta)
		else:
			return minValue(agent, depth, state, alpha, beta)


        # PacMan is the Maximizing Agent, so we want to pick the best action available.
	def maxValue(agent, depth, state, alpha, beta):

		if state.isWin() or state.isLose():
			return [self.evaluationFunction(state), 0]

		value = float("-inf")
		action = 0

		for legalAction in state.getLegalActions(agent):
			successor = state.generateSuccessor(agent, legalAction)
			value_of_action = minimaxValue(agent+1, depth, successor, alpha, beta)
			
			if value_of_action[0] > value:
				value = value_of_action[0]
				action = legalAction
				
			if value > beta:
                                return (value, action)

			alpha = max(alpha, value)

		return (value, action)


        # Ghosts are the Minimizing Agents, so we want to pick the worst action available with respect to Pacman.
	def minValue(agent, depth, state, alpha, beta):

		value = float("inf")
		action = 0

		if state.isWin() or state.isLose():	
			return [self.evaluationFunction(state), 0]

		if not state.getLegalActions(agent):
			return [self.evaluationFunction(state), 0]

		for legalAction in state.getLegalActions(agent):

			successor = state.generateSuccessor(agent, legalAction)

			if agent == gameState.getNumAgents() - 1:
		    		value_of_action = minimaxValue(0, depth+1, successor, alpha, beta)

		    		if value_of_action[0] < value:
					value = value_of_action[0]
					action = legalAction

		    		if value < alpha:
					return (value, action)

		    		beta = min(beta, value)

			else:		
		    		value_of_action = minimaxValue(agent+1, depth, successor, alpha, beta)

		    		if value_of_action[0] < value:
					value = value_of_action[0]
					action = legalAction

		    		if value < alpha:
					return (value, action)

		    		beta = min(beta, value)

		return (value, action)

	return minimaxValue(0, 0, gameState, alpha, beta)[1]





class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        value = float('-inf')
	action = Directions.STOP
	
	for legalAction in gameState.getLegalActions(0):
		temp = self.expValue(0, 1, gameState.generateSuccessor(0, legalAction))
		if temp > value and legalAction != Directions.STOP:
			value = temp
			action = legalAction

	return action


    def maxValue(self, depth, agent, state):

		if depth == self.depth:
			return self.evaluationFunction(state)

		else:

			if len(state.getLegalActions(agent)) > 0:
				maximumValue = float('-inf')
			else:
				maximumValue = self.evaluationFunction(state)

			for legalAction in state.getLegalActions(agent):
				maximumValue = max(maximumValue, self.expValue(depth, agent+1, state.generateSuccessor(agent, legalAction)))
					
			return maximumValue


    def expValue(self, depth, agent, state):

		if depth == self.depth:
			return self.evaluationFunction(state)

		else:
			expectedValue = 0

			for legalAction in state.getLegalActions(agent):
				if agent == state.getNumAgents() - 1:
					expectedValue = expectedValue + self.maxValue(depth+1, 0, state.generateSuccessor(agent, legalAction))
				else:
					expectedValue = expectedValue + self.expValue(depth, agent+1, state.generateSuccessor(agent, legalAction))

			if len(state.getLegalActions(agent)) != 0:
				return expectedValue / len(state.getLegalActions(agent))
			else:
				return self.evaluationFunction(state)




class MonteCarloAgent(MultiAgentSearchAgent):
    """
        Your monte-carlo agent (question 5)
        ***UCT = MCTS + UBC1***
        TODO:
        1) Complete getAction to return the best action based on UCT.
        2) Complete runSimulation to simulate moves using UCT.
        3) Complete final, which updates the value of each of the states visited during a play of the game.

        * If you want to add more functions to further modularize your implementation, feel free to.
        * Make sure that your dictionaries are implemented in the following way:
            -> Keys are game states.
            -> Value are integers. When performing division (i.e. wins/plays) don't forget to convert to float.
      """

    def __init__(self, evalFn='mctsEvalFunction', depth='-1', timeout='40', numTraining=100, C='2', Q=None):
        # This is where you set C, the depth, and the evaluation function for the section "Enhancements for MCTS agent".
        if Q:
            if Q == 'minimaxClassic':
                pass
            elif Q == 'testClassic':
                pass
            elif Q == 'smallClassic':
                pass
            else: # Q == 'contestClassic'
                assert( Q == 'contestClassic' )
                pass
        # Otherwise, your agent will default to these values.
        else:
            self.C = int(C)
            # If using depth-limited UCT, need to set a heuristic evaluation function.
            if int(depth) > 0:
                evalFn = 'scoreEvaluationFunction'
        self.states = []
        self.plays = dict()
        self.wins = dict()
        self.calculation_time = datetime.timedelta(milliseconds=int(timeout))

        self.numTraining = numTraining

        "*** YOUR CODE HERE ***"

        MultiAgentSearchAgent.__init__(self, evalFn, depth)

    def update(self, state):
        """
        You do not need to modify this function. This function is called every time an agent makes a move.
        """
        self.states.append(state)

    def getAction(self, gameState):
        """
        Returns the best action using UCT. Calls runSimulation to update nodes
        in its wins and plays dictionary, and returns best successor of gameState.
        """
        "*** YOUR CODE HERE ***"
        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation(gameState)
            games += 1
        


    def run_simulation(self, state):
        """
        Simulates moves based on MCTS.
        1) (Selection) While not at a leaf node, traverse tree using UCB1.
        2) (Expansion) When reach a leaf node, expand.
        4) (Simulation) Select random moves until terminal state is reached.
        3) (Backpropapgation) Update all nodes visited in search tree with appropriate values.
        * Remember to limit the depth of the search only in the expansion phase!
        Updates values of appropriate states in search with with evaluation function.
        """
        "*** YOUR CODE HERE ***"
        
        visited_states = set()
        player = 0
        actionInfo = True

        while True:
           
            for legalAction in state.getLegalActions(0):
                successor = state.generateSuccessor(0, legalAction)
                if successor not in self.plays and self.wins:
                    actionInfo = False
            print actionInfo
            if actionInfo:
                values = []
                for legalAction in state.getLegalActions(0):
                    state = state.generateSuccessor(0, legalAction)
                    #UCB

            if not actionInfo:
                new = state.generateSuccessor(0, action)
                self.plays[new] = 0
                self.wins[new] = 0
                break
               
            

        
                 
        

        

    def final(self, state):
        """
        Called by Pacman game at the terminal state.
        Updates search tree values of states that were visited during an actual game of pacman.
        """
        "*** YOUR CODE HERE ***"
        pass



def mctsEvalFunction(state):
    """
    Evaluates state reached at the end of the expansion phase.
    """
    return 1 if state.isWin() else 0


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (to help improve your UCT MCTS).
    """
    "*** YOUR CODE HERE ***"

    value = 0
    distance_to_food = 0
    score_of_ghost = 0
    
    if len(currentGameState.getFood().asList()) == 0:
        value = 1000000000000000000

    for food in currentGameState.getFood().asList():
        distance = manhattanDistance(food, currentGameState.getPacmanPosition())
        distance_to_food = distance_to_food + distance

    times = []
    for state_of_ghost in currentGameState.getGhostStates():
        times.append(state_of_ghost.scaredTimer)
	
    if len(times) > 0 and times[0] > 0:
        score_of_ghost = score_of_ghost + 100.0
	
    value = value + (1.0 / (1 + len(currentGameState.getFood().asList())) + 1.0 / (1 + distance_to_food) + score_of_ghost + currentGameState.getScore())
	
    return value

# Abbreviation
better = betterEvaluationFunction
