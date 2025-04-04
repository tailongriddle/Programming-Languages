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


def depthFirstSearch(problem):
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

    #PRINTING SUCCESSORS COUNTS AS EXPANDING
 
    stack = util.Stack()
    visited = set() # set of visited nodes
             
    start_state = problem.getStartState() # push the start state with an empty path
    stack.push((start_state, []))  # (current state, path to reach it)
    
    while not stack.isEmpty(): # while stack is not empty
        current_state, path = stack.pop()  # get the current state and the path to it             

        if current_state not in visited: # if current state not in visited
            visited.add(current_state) #take top item of stack and add to visited
            
            if problem.isGoalState(current_state): # if it is the goal state...
                return directions; # return that path
        
            for next_state, action, _ in problem.getSuccessors(current_state):
                if next_state not in visited:
                    directions = path + [action]  # add action to the current path
                    stack.push((next_state, directions))  # push the successor onto the stack
    return [];



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"  

    queue = util.Queue()
    visited = set() # set of visited nodes
             
    start_state = problem.getStartState() # push the start state with an empty path
    queue.push((start_state, []))  # (current state, path to reach it)
    
    while not queue.isEmpty(): # while queue is not empty
        current_state, path = queue.pop()  # get the current state and the path to it   
        
        if current_state not in visited: # if node is not visited....
            visited.add(current_state) # mark current state as visited
            
            if problem.isGoalState(current_state): # if it is the goal state
                return path; # return the path to the goal state
            
            for next_state, action, _ in problem.getSuccessors(current_state): # for each successor
                if next_state not in visited:
                    directions = path + [action]  # add action to the current path
                    queue.push((next_state, directions))  # put the successor onto the queue

    return []  # return an empty list if no path is found
       

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueue()
    visited = set() # set of visited nodes
             
    start_state = problem.getStartState() # push the start state with an empty path
    queue.push((start_state, [], 0), 0)  # (current state, path to reach it, cost)
    
    while not queue.isEmpty(): # while queue is not empty...
        current_state, path, cost = queue.pop()  # get the current state, the path to it, and the cost
        if problem.isGoalState(current_state): # if it is the goal state
            return path  # return path to goal state
        
        if current_state not in visited: # if node is not visited...
            visited.add(current_state) # mark current state as visited

            for next_state, action, step_cost in problem.getSuccessors(current_state): # for each successor
                if next_state not in visited:
                    directions = path + [action]  # add action to the current path
                    total_cost = cost + step_cost  # calculate the total cost
                    queue.push((next_state, directions, total_cost), total_cost)  # put the successor onto the queue with its total cost

    return []  # return an empty list if no path is found
       
   
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0 

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueue()
    visited = set() # set of visited nodes
             
    start_state = problem.getStartState() # push the start state with an empty path
    queue.push((start_state, [], 0), 0)  # (current state, path to reach it, cost)
    
    while not queue.isEmpty(): # while queue is not empty...
        current_state, path, cost = queue.pop()  # get the current state, the path to it, and the cost
        
           
        if problem.isGoalState(current_state): # if it is the goal state
            return path  # return path to goal state
        
        if current_state not in visited: # if node is not visited...
            visited.add(current_state) # mark current state as visited

            for next_state, action, step_cost in problem.getSuccessors(current_state): # for each successor
                if next_state not in visited:
                    new_cost = cost + step_cost  # calculate the value of g (cost + step cost)
                    h = heuristic(next_state, problem)  # calculate the value of h (heuristic function)
                    directions = path + [action]  # add action to the current path
                    total_cost = new_cost + h  # calculate the total cost
                    queue.push((next_state, directions, new_cost), total_cost)  # put the successor onto the queue with its new cost and total cost
                
    return []  # return an empty list if no path is found
       

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

