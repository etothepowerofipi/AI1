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

    #set of states already checked as not goal states
    expanded = set()

    #list of actions made to reach current state ----(becomes)------> list of actions necessary to reach goal state from starting state
    actions = []
    
    #list of states required to reach the goal state, in order. Useful for backtracking
    path = [] 

    #stack of nodes. 
    frontier = util.Stack()

    #set of states that have been added to the frontier at some point. Prevents multiple additions of the same state
    visited = set()

    #stack of states that added more than one new successors to the frontier. In case of a dead end, we backtrack until reaching the last state that did so
    expandable = util.Stack()

    #a tuple.first element is the state(also a tuple), and second is the required action(string) needed to reach said state
    node = (problem.getStartState(),'Stop')

    expanded.add(node[0])
    expandable.push(node[0])
    visited.add(node[0])
    path.append(node[0])
    successors = problem.getSuccessors(node[0])

    for s in successors:
        frontier.push(s)
        visited.add(s)


    while not frontier.isEmpty():
        node = frontier.pop()
        path.append(node[0])
        actions.append(node[1])

        if (problem.isGoalState(node[0])):
            print("path =",path)
            print("actions =",actions)
            return actions
        

        if (node[0] not in expanded):
            successors = problem.getSuccessors(node[0])
            expanded.add(node[0])

            #Used to save time and mainly space by preventing already expanded nodes to be added to the frontier
            added = 0
            for s in successors:
                if (s[0] not in expanded): #node is unsearched
                    frontier.push(s[0:2])
                    added += 1
            if added>1:
                expandable.push(node[0])
            elif added == 0:
                last = expandable.pop()
                while last != node[0]:
                    path.pop()
                    actions.pop()
                    node = (path[-1],node[1])

            # from helpfulFunctions import helpfulFunctions

            # #If we reach a state all of whose successors have already been expanded (eg (5,4) in the tinyMaze problem), continuing would result in a loop.
            # #Therefore, we backtrack until we reach a state that has non-expanded successors
            # # while helpfulFunctions.explored(successors,visited):           
            # #     actions.pop()
            # #     path.pop()
            # #     node = (path[-1],node[1])
            # #     ###Εδώ είναι το πρόβλημα, ότι ξαναπαίρνω τους successors του 'A'
            # #     ###λύση: χρήση dictionary node->true/false με όνομα "visited" και ανάθεση visited[s] = true στη γραμμή 134. Ο έλεγχος στην 132 θα γίνει "not visited s[0]"
            # #     ###λύση: χρήση set visited
            # #     successors = problem.getSuccessors(node[0])
            # while (helpfulFunctions.explored(successors,expanded)):
            #     actions.pop()
            #     path.pop()
            #     node = (path[-1],node[1])
            #     successors = problem.getSuccessors(node[0])
        
        else:
            last = expandable.pop()
            while last != node[0]:
                path.pop()
                actions.pop()
                node = (path[-1],node[1])    
        #     print(node[0], "in expanded")
        #     # ###Αυτό πάντα σε γυρνάει στην αρχή και μετά κάνει actions.pop() σε κενό actions, γιατί προφανώς όλα τα προηγούμενα στο path είναι expanded, ηλίθιε
        #     # # while node[0] in expanded:
        #     # #     print(node[0]," in expanded")
        #     # #     actions.pop()
        #     # #     path.pop()
        #     # #     node = (path[-1],node[1])
        #     # successors = problem.getSuccessors(node[0])
        #     # while helpfulFunctions.explored(successors,visited):           
        #     #     actions.pop()
        #     #     path.pop()
        #     #     node = (path[-1],node[1])
        #     #     ###Εδώ είναι το πρόβλημα, ότι ξαναπαίρνω τους successors του 'A'
        #     #     ###λύση: χρήση dictionary node->true/false με όνομα "visited" και ανάθεση visited[s] = true στη γραμμή 134. Ο έλεγχος στην 132 θα γίνει "not visited s[0]"
        #     #     ###λύση: χρήση set visited
        #     #     successors = problem.getSuccessors(node[0])
        #     actions.pop()
        #     path.pop()
        #     node = (path[-1],node[1])


            
    return actions

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
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
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
