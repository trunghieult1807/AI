import argparse

import search


class WaterJug:
    def __init__(self, capacity, water=0):
        self.water = water
        self.capacity = capacity
    
    def __str__(self):
        return f"({self.water}/{self.capacity})"

    def __hash__(self):
        return hash(self.water + 13 * self.capacity)

    def __eq__(self, other):
        return self.water == other.water and self.capacity == other.capacity

    def isEmpty(self):
        return self.water == 0

    def isFull(self):
        return self.water == self.capacity
    
    def pour_in(self, water):
        remainder = max(self.water + water - self.capacity, 0)
        self.water = min(self.water + water, self.capacity)

        # Return water's remainder
        return remainder
    
    def pour_to(self, other_jug):
        self.water = other_jug.pour_in(self.water)
    
    def copy(self):
        return WaterJug(self.capacity, self.water)

class WaterJugsState:
    def __init__(self):
        self.jugs = [WaterJug(8, 8), WaterJug(5), WaterJug(3)]
    
    def __str__(self):
        return ' - '.join(str(jug) for jug in self.jugs)
    
    def __eq__(self, other):
        return self.jugs == other.jugs
    
    def __hash__(self):
        return sum(hash(jug) for jug in self.jugs)
    
    def isGoal(self):
        return self.jugs == [WaterJug(8, 4), WaterJug(5, 4), WaterJug(3)]
    
    def legalMoves(self):
        # Return a list of states, each state in format (<from_jug_idx>, <to_jug_idx>)
        moves = set()
        for i in range(3):
            if self.jugs[i].isEmpty(): continue
            for j in range(3):
                if i == j or self.jugs[j].isFull(): continue
                moves.add((i, j))
        return moves
    
    def result(self, action):
        from_jug, to_jug = action
        new_state = WaterJugsState()
        new_state.jugs = [jug.copy() for jug in self.jugs]
        new_state.jugs[from_jug].pour_to(new_state.jugs[to_jug])
        return new_state
    
class WaterJugsProblem(search.SearchProblem):
    def __init__(self, water_jugs):
        self.current_state = water_jugs
    
    def getStartState(self):
        return self.current_state

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        for action in self.getActions(state):
            next_state = self.getNextState(state, action)
            yield (next_state, action, self.getActionCost(state, action, next_state))

    def getActions(self, state):
        return state.legalMoves()

    def getActionCost(self, state, action, next_state):
        assert next_state == state.result(action), (
            "getActionCost() called on incorrect next state.")
        return 1

    def getNextState(self, state, action):
        return state.result(action)

    def getCostOfActions(self, actions):
        return len(actions)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('search')
    args = parser.parse_args()
    water_jugs = WaterJugsState()
    
    problem = WaterJugsProblem(water_jugs)
    # actions = search.bfs(problem)
    if args.search == 'brfs':
        actions = search.brfs(problem)
    elif args.search == 'dfs':
        actions = search.dfs(problem)
    elif args.search == 'dls':
        actions = search.dls(problem)
    elif args.search == 'ids':
        actions = search.dls(problem)
    elif args.search == 'ucs':
        actions = search.ucs(problem)
    elif args.search == 'bfs':
        actions = search.bfs(problem)
    elif args.search == 'astar':
        actions = search.astar(problem)
    print('BFS found a path of %d moves: %s' % (len(actions), str(actions)))
    print(f"Start: \t\t {water_jugs}")
    curr = water_jugs
    for action in actions:
        input("Press return for the next state...")  # wait for key stroke
        curr = curr.result(action)
        print(f"Pour {action[0] + 1} to {action[1] + 1}:\t", curr)