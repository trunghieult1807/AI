from search import Problem

def is_valid(state):
    capacityJug1, totalCapacityJug1, capacityJug2, totalCapacityJug2 = state

    if((capacityJug1 > totalCapacityJug1 or capacityJug1 < 0) or (capacityJug2 > totalCapacityJug2 or capacityJug2 < 0)):
        return False;
    
    return True;

class WaterJugProblem(Problem):

    def result(self, state, action):
        """The result of going to a neighbor is just that neighbor."""
        return action

    def value(self, state):
        pass
    
    def __init__(self, initial, goal):
        self.goal = goal
        self.initial = initial
        self.visited_states = []
        Problem.__init__(self, self.initial, self.goal)

    def __repr__(self):
        return "< State (%s, %s) >" % (self.initial, self.goal)

    def goal_test(self, state):
        return state == self.goal

    def actions(self, cur_state):
        actions = []

        self.visited_states.append(cur_state)

        if(cur_state[0] == 0):

             #Fill the first jug
            new_state = (cur_state[0] + cur_state[1], cur_state[1], cur_state[2], cur_state[3])
            if is_valid(new_state):
                actions.append(new_state)
            
        elif(cur_state[2] == 0):

            #Pour from the first jug into the second one till it's full
            new_state = (cur_state[0] - (cur_state[3] - cur_state[2]), cur_state[1], cur_state[2] + (cur_state[3] - cur_state[2]), cur_state[3])
            if is_valid(new_state):
                actions.append(new_state)

             #Pour from the first jug all the remaining water in the second jar
            new_state = (cur_state[0] - cur_state[0], cur_state[1], cur_state[2] + cur_state[0], cur_state[3])
            if is_valid(new_state):
                actions.append(new_state)

        elif(cur_state[2] == cur_state[3]):

            #Throw the water from the second jug
            new_state = (cur_state[0], cur_state[1], cur_state[2] - cur_state[3], cur_state[3])
            if is_valid(new_state):
                actions.append(new_state)

        elif(cur_state[0] == cur_state[1]):
            
            #Pour from the first jug into the second one till it's full
            new_state = (cur_state[0] - (cur_state[3] - cur_state[2]), cur_state[1], cur_state[2] + (cur_state[3] - cur_state[2]), cur_state[3])
            if is_valid(new_state):
                actions.append(new_state)
      
        return actions
