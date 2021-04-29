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
import sys


class Node:
    def __init__(self, state, parent, action, depth=0, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost


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

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    @Return
        actions: a list of actions to reach solution
    """
    "*** YOUR CODE HERE ***"
    model = GenericSearch(problem, util.Stack())
    actions = model.search()
    return actions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    model = GenericSearch(problem, util.Queue())
    actions = model.search()
    return actions


def uniformCostSearch(problem):
    model = GenericSearch(problem, util.PriorityQueue())
    actions = model.search()
    return actions


def depthLimitSearch(problem, limit=100):
    model = GenericSearch(problem, util.Stack())
    actions = model.search(limit)
    return actions


def iterativeDeepeningSearch(problem, max_depth=1000):
    for depth in range(max_depth):
        model = GenericSearch(problem, util.Stack())
        actions = model.search(depth)
        if actions:
            return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    model = GenericSearch(problem, util.PriorityQueue(), heuristic)
    actions = model.aStarSearch()
    return actions


def bestFirstSearch(problem, heuristic=nullHeuristic):
    model = GenericSearch(problem, util.PriorityQueue(), heuristic)
    actions = model.bestFirstSearch()
    return actions


# def depthFirstSearch(problem):
#     """
#     Search the deepest nodes in the search tree first.
#
#     Your search algorithm needs to return a list of actions that reaches the
#     goal. Make sure to implement a graph search algorithm.
#
#     To get started, you might want to try some of these simple commands to
#     understand the search problem that is being passed in:
#
#     print("Start:", problem.getStartState())
#     print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
#     @Return
#         actions: a list of actions to reach solution
#     """
#     "*** YOUR CODE HERE ***"
#     start_node = Node(state=problem.getStartState(), parent=None, action=None)
#     frontier = util.Stack()
#     frontier.push(start_node)
#     explored = set()
#
#     while not frontier.isEmpty():
#         node = frontier.pop()
#
#         if problem.isGoalState(node.state):
#             actions = []
#             while node.parent is not None:
#                 actions.append(node.action)
#                 node = node.parent
#             actions.reverse()
#             return actions
#
#         explored.add(node.state)
#
#         for child, action, cost in problem.getSuccessors(node.state):
#             if child not in explored:
#                 child_node = Node(state=child, parent=node, action=action, depth=node.depth + 1, cost=node.cost + cost)
#                 frontier.push(child_node)
#
#     return []
#
#
# def breadthFirstSearch(problem):
#     """Search the shallowest nodes in the search tree first."""
#     "*** YOUR CODE HERE ***"
#     start_node = Node(state=problem.getStartState(), parent=None, action=None)
#     frontier = util.Queue()
#     frontier.push(start_node)
#     explored = set()
#
#     while not frontier.isEmpty():
#         node = frontier.pop()
#
#         if problem.isGoalState(node.state):
#
#             actions = []
#             while node.parent is not None:
#
#                 actions.append(node.action)
#                 node = node.parent
#
#             actions.reverse()
#             return actions
#
#         explored.add(node.state)
#         for child, action, cost in problem.getSuccessors(node.state):
#             if child not in explored:
#                 child_node = Node(state=child, parent=node, action=action, depth=node.depth + 1, cost=node.cost + cost)
#                 frontier.push(child_node)
#
#     return []
#
#
# def uniformCostSearch(problem):
#     explored = set()
#     start_node = Node(state=problem.getStartState(), parent=None, action=None)
#     frontier = util.PriorityQueue()
#     frontier.push(start_node, start_node.cost)
#
#     while not frontier.isEmpty():
#         node = frontier.pop()
#         if problem.isGoalState(node.state):
#             actions = []
#             while node.parent is not None:
#                 actions.append(node.action)
#                 node = node.parent
#
#             actions.reverse()
#             return actions
#
#         explored.add(node.state)
#         for child, action, cost in problem.getSuccessors(node.state):
#             if child not in explored:
#                 child_node = Node(state=child, parent=node, action=action, depth=node.depth + 1, cost=node.cost + cost)
#                 frontier.push(child_node, child_node.cost)
#     return []
#
#
# def deepLimitedSearch(problem, limit=30):
#
#     explored = set()
#     start_node = Node(state=problem.getStartState(), parent=None, action=None)
#     frontier = util.Stack()
#     frontier.push(start_node)
#
#     while not frontier.isEmpty():
#         node = frontier.pop()
#
#         if problem.isGoalState(node.state):
#             actions = []
#             while node.parent is not None:
#                 actions.append(node.action)
#                 node = node.parent
#             actions.reverse()
#             return actions
#
#         elif limit >= 0 and limit == node.depth:
#             explored.add(node.state)
#             continue
#
#         explored.add(node.state)
#         for child, action, cost in problem.getSuccessors(node.state):
#             if child not in explored:
#                 child_node = Node(state=child, parent=node, action=action, depth=node.depth + 1, cost=node.cost + cost)
#                 frontier.push(child_node)
#     return []
#
#
# def iterativeDeepeningSearch(problem, max_depth=sys.maxsize):
#     for depth in range(max_depth):
#         actions = deepLimitedSearch(problem, depth)
#         if actions:
#             return []
#
#
# def nullHeuristic(state, problem=None):
#     """
#     A heuristic function estimates the cost from the current state to the nearest
#     goal in the provided SearchProblem.  This heuristic is trivial.
#     """
#     return 0


# def bestFirstSearch(problem, heuristic=nullHeuristic):
#     explored = set()
#     frontier = util.PriorityQueue()
#     start_node = Node(state=problem.getStartState(), parent=None, action=None)
#     frontier.push(start_node, heuristic(start_node.state, problem))
#
#     while not frontier.isEmpty():
#         node = frontier.pop()
#         if problem.isGoalState(node.state):
#             actions = []
#             while node.parent is not None:
#                 actions.append(node.action)
#                 node = node.parent
#             actions.reverse()
#             return actions
#         explored.add(node.state)
#         for child, action, cost in problem.getSuccessors(node.state):
#             if child not in explored:
#                 child_node = Node(state=child, parent=node, action=action, depth=node.depth + 1, cost=node.cost + cost)
#                 frontier.push(child_node, heuristic(child_node.state, problem))
#     return []
#
#
# def aStarSearch(problem, heuristic=nullHeuristic):
#     """Search the node that has the lowest combined cost and heuristic first."""
#     "*** YOUR CODE HERE ***"
#     start_node = Node(state=problem.getStartState(), parent=None, action=None)
#     explored = set()
#     frontier = util.PriorityQueue()
#
#     frontier.update(start_node, start_node.cost + heuristic(start_node.state, problem))
#
#     while not frontier.isEmpty():
#         node = frontier.pop()
#         if problem.isGoalState(node.state):
#             actions = []
#             while node.parent is not None:
#                 actions.append(node.action)
#                 node = node.parent
#             actions.reverse()
#             return actions
#
#         explored.add(node.state)
#         for child, action, cost in problem.getSuccessors(node.state):
#             if child not in explored:
#                 child_node = Node(state=child, parent=node, action=action, depth=node.depth + 1, cost=node.cost + cost)
#                 frontier.update(child_node, child_node.cost + heuristic(child_node.state, problem))
#     return []


# Generic graph search


class GenericSearch:
    def __init__(self, problem, fringe, heuristic=nullHeuristic):
        self.problem = problem
        self.fringe = fringe
        self.explored = set()
        self.heuristic = heuristic
        self.algorithm = None

    def search(self, limit=-1):
        start_node = Node(state=self.problem.getStartState(), parent=None, action=None)
        self.pushFringe(start_node)

        while not self.fringe.isEmpty():
            node = self.fringe.pop()

            if self.problem.isGoalState(node.state):
                actions = []
                while node.parent is not None:
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                return actions
            elif limit >= 0 and node.depth >= limit:  # Cutoff
                self.explored.add(node.state)
                continue

            if node.state not in self.explored:
                self.explored.add(node.state)
                for child, action, cost in self.problem.getSuccessors(node.state):
                    if child not in self.explored:
                        child_node = Node(state=child, parent=node, action=action,
                                          depth=node.depth + 1, cost=node.cost + cost)
                        self.pushFringe(child_node)
        return []

    def pushFringe(self, node):
        if isinstance(self.fringe, util.PriorityQueue):
            if self.algorithm == 'aStar':
                self.fringe.push(node, node.cost + self.heuristic(node.state, self.problem))
            elif self.algorithm == 'bfs':
                self.fringe.push(node, self.heuristic(node.state, self.problem))
            else:
                self.fringe.push(node, node.cost)
        else:
            self.fringe.push(node)

    def bestFirstSearch(self):
        self.algorithm = 'bfs'
        return self.search()

    def aStarSearch(self):
        self.algorithm = 'aStar'
        return self.search()


brfs = breadthFirstSearch
dfs = depthFirstSearch
dls = depthLimitSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
bfs = bestFirstSearch
astar = aStarSearch
