# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from sre_constants import FAILURE
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    #Set of states already checked as not GoalStates
    expanded = set()

    #Stack of states to be examined
    frontier = util.Stack()

    #So that <problem.getStartState()> doesn't need to be called again in line #113
    startState = problem.getStartState()
    
    #node = (state,action,parentNode)
    #action = action required to reach state in node[0]
    #parentNode: current state was accessed by applying current action to parentNode's state: parentNode[0] ------(node[1])-------> node[0]
    node = (startState,"",(tuple))
    frontier.push(node)

    while not (frontier.isEmpty()):
        node = frontier.pop()
        state = node[0]
        if (problem.isGoalState(state)):
            actions = []
            #The first node contains no useful information as to the path.
            while (node[0] != startState):
                actions.append(node[1])
                node = node[2]
            actions.reverse()
            return actions
        
        if (state not in expanded):
            action = node[1]
            parent = node[2]
            successors = problem.getSuccessors(state)
            expanded.add(state)
            for s in successors:
                if (s[0] not in expanded):
                    new_state = s[0]
                    action = s[1]
                    new_node = (new_state,action,node)
                    frontier.push(new_node)
    return FAILURE

    util.raiseNotDefined()

#Completely identical, only difference is frontier is a queue
def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    expanded = set()
    frontier = util.Queue()
    startState = problem.getStartState()
    
    node = (startState,"",(tuple))
    frontier.push(node)

    while not (frontier.isEmpty()):
        node = frontier.pop()
        state = node[0]
        if (problem.isGoalState(state)):
            actions = []
            while (node[0] != startState):
                actions.append(node[1])
                node = node[2]
            actions.reverse()
            return actions
        
        if (state not in expanded):
            action = node[1]
            parent = node[2]
            successors = problem.getSuccessors(state)
            expanded.add(state)
            for s in successors:
                if (s[0] not in expanded):
                    new_state = s[0]
                    action = s[1]
                    new_node = (new_state,action,node)
                    frontier.push(new_node)
    return FAILURE

    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    expanded = set()
    frontier = util.PriorityQueue()
    startState = problem.getStartState()

    #node = (state,action,pathCost,parentNode)
    node = (startState,"",0,(tuple))
    frontier.push(node,0)

    while (not frontier.isEmpty()):
        node = frontier.pop()
        state = node[0]
        if (problem.isGoalState(state)):
            actions = []
            while (node[0] != startState):
                actions.append(node[1])
                node = node[3]
            actions.reverse()
            return actions
        if state not in expanded:
            expanded.add(state)
            successors = problem.getSuccessors(state)
            for s in successors:
                if (s not in expanded):
                    new_state = s[0]
                    action = s[1]
                    cost = node[2] + s[2]
                    new_node = (new_state,action,cost,node)
                    frontier.update(new_node,cost)
        
    return FAILURE
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    expanded = set()
    frontier = util.PriorityQueue()
    startState = problem.getStartState()

    #node = (state,action,pathCost,parentNode)
    node = (startState,"",0,(tuple))
    frontier.push(node,0)

    while (not frontier.isEmpty()):
        node = frontier.pop()
        state = node[0]
        if (problem.isGoalState(state)):
            actions = []
            while (node[0] != startState):
                actions.append(node[1])
                node = node[3]
            actions.reverse()
            return actions
        if state not in expanded:
            expanded.add(state)
            successors = problem.getSuccessors(state)
            for s in successors:
                if (s not in expanded):
                    new_state = s[0]
                    action = s[1]
                    gn = node[2] + s[2]
                    fn = gn + heuristic(new_state,problem)
                    new_node = (new_state,action,gn,node)
                    frontier.update(new_node,fn)
        
    return FAILURE
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
