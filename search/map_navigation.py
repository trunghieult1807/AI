
import search
import random
import argparse

class Road:
    def __init__(self, city1, city2, cost):
        if city1 == city2:
            raise Exception("Just road between 2 different cities")
        self.city1 = city1
        self.city2 = city2
        self.cost = cost
    
    def __hash__(self):
        c1 = hash(self.city1)
        c2 = hash(self.city2)
        return hash(c1 + c2 + self.cost)
    
    def __eq__(self, other):
        check_city = (self.city1 == other.city1 and self.city2 == other.city2) \
                    or (self.city1 == other.city2 and self.city2 == other.city1)
        return check_city
    
    def __str__(self):
        return f"({self.city1}-{self.city2},{self.cost})"
    
    def connect(self, city):
        return city == self.city1 or city == self.city2

class Map:
    def __init__(self):
        self.roads = []
    
    def containsRoad(self, road):
        return any(road == r for r in self.roads)

    def addRoad(self, road):
        if self.containsRoad(road): return None
        self.roads.append(road)
    
    def getAllRoads(self, city):
        return [road for road in self.roads if road.connect(city)]


class MapNavigationProblem(search.SearchProblem):
    """
    Implement Search problem for Map navigation
    """
    def __init__(self, map, from_city, to_city):
        self.map = map
        self.current_city = from_city
        self.destination = to_city
    
    def getStartState(self):
        return self.current_city
    
    def isGoalState(self, state):
        return state == self.destination
    
    def getSuccessors(self, state):
        for road in self.getActions(state):
            next_state = self.getNextState(state, road)
            yield (next_state, road, self.getActionCost(state, road, next_state))
    
    def getActions(self, state):
        return self.map.getAllRoads(state)
    
    def getActionCost(self, state, action, next_state):
        if not action.connect(state) and not action.connect(next_state):
            raise Exception(f"{Action} not connect {state} with {next_state}")
        return action.cost

    def getNextState(self, state, action):
        return action.city1 if action.city2 == state else action.city2

    def getCostOfActions(self, actions):
        return sum(action.cost for action in actions)
    
    def getNextCity(self, road):
        if not road.connect(self.current_city):
            raise Exception("Invalid solution")
        self.current_city = road.city1 if road.city2 == self.current_city else road.city2
        return self.current_city


def loadMap():
    map = Map()
    map.addRoad(Road('Oradea', 'Zerind', 71))
    map.addRoad(Road('Zerind', 'Arad', 75))
    map.addRoad(Road('Oradea', 'Sibiu', 151))
    map.addRoad(Road('Arad', 'Sibiu', 140))
    map.addRoad(Road('Arad', 'Timisoara', 118))
    map.addRoad(Road('Timisoara', 'Lugoj', 111))
    map.addRoad(Road('Lugoj', ' ', 70))
    map.addRoad(Road('Mehadia', 'Dobreta', 75))
    map.addRoad(Road('Craiova', 'Dobreta', 120))
    map.addRoad(Road('Craiova', 'Rimnicu Vilcea', 146))
    map.addRoad(Road('Craiova', 'Pitesti', 138))
    map.addRoad(Road('Pitesti', 'Rimnicu Vilcea', 97))
    map.addRoad(Road('Sibiu', 'Rimnicu Vilcea', 80))
    map.addRoad(Road('Sibiu', 'Fagaras', 99))
    map.addRoad(Road('Fagaras', 'Bucharest', 211))
    map.addRoad(Road('Pitesti', 'Bucharest', 101))
    map.addRoad(Road('Giurgiu', 'Bucharest', 90))
    map.addRoad(Road('Urziceni', 'Bucharest', 85))
    map.addRoad(Road('Urziceni', 'Hirsova', 98))
    map.addRoad(Road('Eforie', 'Hirsova', 86))
    map.addRoad(Road('Urziceni', 'Vaslui', 142))
    map.addRoad(Road('Lasi', 'Vaslui', 92))
    map.addRoad(Road('Lasi', 'Neamt', 87))
    return map


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('search_type')
    parser.add_argument('from_city')
    parser.add_argument('to_city')

    args = parser.parse_args()

    map = loadMap()

    problem = MapNavigationProblem(map, args.from_city, args.to_city)

    if args.search_type == 'brfs':
        actions = search.brfs(problem)
    elif args.search_type == 'dfs':
        actions = search.dfs(problem)
    elif args.search_type == 'dls':
        actions = search.dls(problem)
    elif args.search_type == 'ids':
        actions = search.dls(problem)
    elif args.search_type == 'ucs':
        actions = search.ucs(problem)
    elif args.search_type == 'bfs':
        actions = search.bfs(problem)
    elif args.search_type == 'astar':
        actions = search.astar(problem)

    cost = problem.getCostOfActions(actions)
    print(f"DFS found a path of {len(actions)} moves with {cost} costs")
    city = [problem.current_city]
    for action in actions:
        city.append(problem.getNextCity(action))
    print('-'.join(city))
