########################################################
#
# CMPSC 441: Homework 3
#
########################################################


student_name = 'Type your full name here'
student_email = 'Type your email address here'



########################################################
# Import
########################################################

from hw3_utils import *
from collections import deque
import math

# Add your imports here if used






##########################################################
# 1. Best-First, Uniform-Cost, A-Star Search Algorithms
##########################################################


def best_first_search(problem):
    node = Node(problem.init_state, heuristic=problem.h(problem.init_state))
    frontier = deque([node])         # queue: popleft/append-sorted
    explored = [problem.init_state]  # used as "visited"
    while len(frontier) != 0:
        n = frontier.popleft()
        if problem.goal_test(n.state):
            return n
        if n.state not in explored:
            explored.append(n.state)
        for i in n.expand(problem):
            if i.state not in explored:
                x = list()
                for j in frontier:
                    if i.state == j.state:
                        x.append(j)
                if not x:
                    frontier.append(i)
                    frontier = deque(sorted(frontier, key=lambda i: i.heuristic))
                elif i.heuristic < x[0].heuristic:
                    frontier.remove(Node(i.state))
                    frontier.append(i)
                    frontier = deque(sorted(frontier, key=lambda i: i.heuristic))
    return Node(None)




def uniform_cost_search(problem):
    node = Node(problem.init_state)
    frontier = deque([node])         # queue: popleft/append-sorted
    explored = []                    # used as "expanded" (not "visited")
    while len(frontier) != 0:
        n = frontier.popleft()
        if problem.goal_test(n.state):
            return n
        if n.state in explored:
            continue
        explored.append(n.state)
        for i in n.expand(problem):
            if i.state not in explored:
                x = list()
                for j in frontier:
                    if i.state == j.state:
                        x.append(j)
                if not x:
                    frontier.append(i)
                    frontier = deque(sorted(frontier, key = lambda i: i.path_cost))
                elif i.path_cost < x[0].path_cost:
                    frontier.remove(Node(i.state))
                    frontier.append(i)
                    frontier = deque(sorted(frontier, key = lambda i: i.path_cost))
    return Node(None)



    
def a_star_search(problem):
    node = Node(problem.init_state, heuristic=problem.h(problem.init_state))
    frontier = deque([node])         # queue: popleft/append-sorted
    explored = []                    # used as "expanded" (not "visited")
    while len(frontier) != 0:
        n = frontier.popleft()
        if problem.goal_test(n.state):
            return n
        if n.state in explored:
            continue
        explored.append(n.state)
        for i in n.expand(problem):
            if i.state not in explored:
                x = list()
                for j in frontier:
                    if i.state == j.state:
                        x.append(j)
                if not x:
                    frontier.append(i)
                    frontier = deque(sorted(frontier, key = lambda i: i.path_cost + i.heuristic))
                elif i.path_cost + i.heuristic <= x[0].path_cost + x[0].heuristic:
                    frontier.remove(Node(i.state))
                    frontier.append(i)
                    frontier = deque(sorted(frontier, key = lambda i: i.path_cost + i.heuristic))
    return Node(None)




##########################################################
# 2. N-Queens Problem
##########################################################


class NQueensProblem(Problem):
    """
    The implementation of the class NQueensProblem is given
    for those students who were not able to complete it in
    Homework 2.
    
    Note that you do not have to use this implementation.
    Instead, you can use your own implementation from
    Homework 2.

    >>>> USE THIS IMPLEMENTATION AT YOUR OWN RISK <<<<
    >>>> USE THIS IMPLEMENTATION AT YOUR OWN RISK <<<<
    >>>> USE THIS IMPLEMENTATION AT YOUR OWN RISK <<<<
    """
    
    def __init__(self, n):
        super().__init__(tuple([-1] * n))
        self.n = n
        

    def actions(self, state):
        if state[-1] != -1:   # if all columns are filled
            return []         # then no valid actions exist
        
        valid_actions = list(range(self.n))
        col = state.index(-1) # index of leftmost unfilled column
        for row in range(self.n):
            for c, r in enumerate(state[:col]):
                if self.conflict(row, col, r, c) and row in valid_actions:
                    valid_actions.remove(row)
                    
        return valid_actions

        
    def result(self, state, action):
        col = state.index(-1) # leftmost empty column
        new = list(state[:])  
        new[col] = action     # queen's location on that column
        return tuple(new)

    
    def goal_test(self, state):
        if state[-1] == -1:   # if there is an empty column
            return False;     # then, state is not a goal state

        for c1, r1 in enumerate(state):
            for c2, r2 in enumerate(state):
                if (r1, c1) != (r2, c2) and self.conflict(r1, c1, r2, c2):
                    return False
        return True

    
    def conflict(self, row1, col1, row2, col2):
        return row1 == row2 or col1 == col2 or abs(row1-row2) == abs(col1-col2)

    
    def g(self, cost, from_state, action, to_state):
        """
        Return path cost from start state to to_state via from_state.
        The path from start_state to from_state costs the given cost
        and the action that leads from from_state to to_state
        costs 1.
        """
        return cost + 1;


    def h(self, state):
        """
        Returns the heuristic value for the given state.
        Use the total number of conflicts in the given
        state as a heuristic value for the state.
        """
        x = 0;
        for i,item1 in enumerate(state):
            for j,item2 in enumerate(state):
                if i != j and self.conflict(item1, i, item2, j):
                    x+=1
        return x;



##########################################################
# 3. Graph Problem
##########################################################



class GraphProblem(Problem):
    """
    The implementation of the class GraphProblem is given
    for those students who were not able to complete it in
    Homework 2.
    
    Note that you do not have to use this implementation.
    Instead, you can use your own implementation from
    Homework 2.

    >>>> USE THIS IMPLEMENTATION AT YOUR OWN RISK <<<<
    >>>> USE THIS IMPLEMENTATION AT YOUR OWN RISK <<<<
    >>>> USE THIS IMPLEMENTATION AT YOUR OWN RISK <<<<
    """
    
    
    def __init__(self, init_state, goal_state, graph):
        super().__init__(init_state, goal_state)
        self.graph = graph

        
    def actions(self, state):
        """Returns the list of adjacent states from the given state."""
        return list(self.graph.get(state).keys())

    
    def result(self, state, action):
        """Returns the resulting state by taking the given action.
            (action is the adjacent state to move to from the given state)"""
        return action

    
    def goal_test(self, state):
        return state == self.goal_state

    
    def g(self, cost, from_state, action, to_state):
        """
        Returns the path cost from root to to_state.
        Note that the path cost from the root to from_state
        is the give cost and the given action taken at from_state
        will lead you to to_state with the cost associated with
        the action.
        """
        return cost + self.graph.get(from_state, to_state)
    

    def h(self, state):
        """
        Returns the heuristic value for the given state. Heuristic
        value of the state is calculated as follows:
        1. if an attribute called 'heuristics' exists:
           - heuristics must be a dictionary of states as keys
             and corresponding heuristic values as values
           - so, return the heuristic value for the given state
        2. else if an attribute called 'locations' exists:
           - locations must be a dictionary of states as keys
             and corresponding GPS coordinates (x, y) as values
           - so, calculate and return the straight-line distance
             (or Euclidean norm) from the given state to the goal
             state
        3. else
           - cannot find nor calculate heuristic value for given state
           - so, just return a large value (i.e., infinity)
        """

        if hasattr(self.graph, 'heuristics'):
            return self.graph.heuristics.get(state)
        elif hasattr(self.graph, 'locations'):
            x = self.graph.locations.get(state)
            y = self.graph.locations.get(self.goal_state)
            return math.hypot(abs(x[0]-y[0]), abs(x[1] - y[1]))
        else:
            return math.inf
        


##########################################################
# 4. Eight Puzzle
##########################################################


class EightPuzzle(Problem):
    def __init__(self, init_state, goal_state=(1,2,3,4,5,6,7,8,0)):
        self.init_state = init_state
        self.goal_state = goal_state
    

    def actions(self, state):
        a = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        if state[0] == 0 or state[1] == 0 or state[2] == 0:
            a.remove('UP')
        if state[0] == 0 or state[3] == 0 or state[6] == 0:
            a.remove('LEFT')
        if state[6] == 0 or state[7] == 0 or state[8] == 0:
            a.remove('DOWN')
        if state[2] == 0 or state[5] == 0 or state[8] == 0:
            a.remove('RIGHT')
        return a

    
    def result(self, state, action):
        i = state.index(0)
        n = list(state)
        if action == 'UP':
            x = i - 3
            y = state[x]
            n[i] = y
            n[x] = 0
        if action == 'DOWN':
            x = i + 3
            y = state[x]
            n[i] = y
            n[x] = 0
        if action == 'LEFT':
            x = i - 1
            y = state[x]
            n[i] = y
            n[x] = 0
        if action == 'RIGHT':
            x = i + 1
            y = state[x]
            n[i] = y
            n[x] = 0
        return tuple(n)
            

    
    def goal_test(self, state):
        return state == self.goal_state
    

    def g(self, cost, from_state, action, to_state):
        """
        Return path cost from root to to_state via from_state.
        The path from root to from_state costs the given cost
        and the action that leads from from_state to to_state
        costs 1.
        """
        return cost + 1
    

    def h(self, state):
        """
        Returns the heuristic value for the given state.
        Use the sum of the Manhattan distances of misplaced
        tiles to their final positions.
        """
        x = 0
        for i, item in enumerate(state):
            if item != 0:
                init_row = int(i/3)
                init_col = i%3
                final_row = int(self.goal_state.index(item)/3)
                final_col = self.goal_state.index(item) % 3
                x += abs(init_row - final_row) + abs(init_col - final_col)
        return x
            
            


