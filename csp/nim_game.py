import math
import time
import random
import itertools

def successors(s):
    player = s[1]
    piles = s[0]
    successor_states = []
    successors = []
    if player == 1:
        player = 2
    if player == 2:
        player == 1
    for i, pile in enumerate(piles):
        for remove in range(1, pile + 1):
            result = pile - remove
            if result != 0:
                next_piles = sorted(piles[:i] + [result] + piles[i + 1:])
            else:
                next_piles = sorted(piles[:i] + piles[i + 1:])
            successor_states.append(next_piles)

    successor_states.sort()
    successor_states = list(successor_states for successor_states, _ in itertools.groupby(successor_states))
    print(successor_states)
    for i in range(len(successor_states)):
        successors.append([successor_states[i], player])
    return successors


def terminal_test(state):
    if state in [([1], 1), ([], 2)]:
        terminal_state = True
    elif state in [([1], 2), ([], 1)]:
        terminal_state = True
    else:
        terminal_state = False
    return terminal_state


def utility_test(state):
    if state in [([1], 1), ([], 2)]:
        utility = 1
    elif state in [([1], 2), ([], 1)]:
        utility = -1
    else:
        if state[1] == -1:
            utility = 1
        else:
            utility = -1
    return utility


def max_value(max_state):
    v = math.inf
    terminal_state, utility = terminal_test(max_state)
    if not terminal_state:
        for s in successors(max_state):
            v = min(v, min_value(s))
        return v
    else:
        return terminal_test(max_state)


def min_value(min_state):
    v = -math.inf
    terminal_state, utility = terminal_test(min_state)
    if not terminal_state:
        for s in successors(min_state):
            v = max(v, max_value(s))
        return v
    else:
        return terminal_test(min_state)


def min_max(state):
    if state[1] == 1:
        utility = max_value(state)
    else:
        utility = min_value(state)
    if utility == 1:
        print("Win for Max!")
    if utility == -1:
        print("Win for Min!")
    return utility


def max_value_ab(min_state, a, b):
    v = 1
    terminal_state = terminal_test(min_state)
    utility = utility_test(min_state)
    if not terminal_state:

        for s in successors(min_state):

            if v > utility:
                utility = v
            if v >= b:
                return utility
            if v > a:
                a = v
        v = min(v, min_value_ab(min_state, a, b))
    return utility


def min_value_ab(max_state, a, b):
    v = -1
    terminal_state = terminal_test(max_state)
    utility = utility_test(max_state)
    if not terminal_state:

        for s in successors(max_state):

            if v < utility:
                utility = v
            if v <= a:
                return utility
            if v < b:
                b = v
        v = max(v, max_value_ab(max_state, a, b))
    return utility


def minimax_ab(state):
    start = time.time()
    alpha = 0
    beta = 0
    if state[1] == 1:
        utility_value = min_value_ab(state, alpha, beta)
    else:
        utility_value = max_value_ab(state, alpha, beta)
    end = time.time()
    return utility_value


def minimax_game():
    number_of_piles = int(input("Number of piles: "))
    maximum_pile_size = int(input("Maximum number of sticks: "))
    first_player = int(input("First player: 1 for computer, 2 for human: "))
    initial_piles = []
    for pile in range(0, number_of_piles):
        pile_size = random.randrange(1, maximum_pile_size + 1)
        initial_piles.append(pile_size)
    state = (sorted(initial_piles), first_player)
    while True:
        # Print game state
        print("state", state)
        if state[1] == 2:
            piles = state[0]
            pile_number = (int(input("Enter the number of pile to remove sticks from: ")) - 1)
            pile = piles[pile_number]
            pick = int(input("Number of sticks to remove: "))
            if pick <= pile:
                result = pile - pick
                if result == 0:
                    new_piles = sorted(piles[:pile_number] + piles[pile_number + 1:])
                else:
                    new_piles = sorted(piles[:pile_number] + [result] + piles[pile_number + 1:])
                state = (new_piles, 1)
            else:
                print("out of bound")
                break
        elif state[1] == 1:
            list_of_successors = successors(state)
            number_of_next_states = len(list_of_successors)
            for s, next_state in enumerate(list_of_successors):
                utility_value = minimax_ab(next_state)
                if utility_value == -1:
                    state = next_state
                elif utility_value == 1:
                    state = list_of_successors[random.randrange(0, number_of_next_states)]
                    state = next_state
        if state in [([1], 1), ([], 2), ([1], 2), ([], 1)]:
            util = utility_test(state)
            if util == -1:
                print("You lost")
                break
            elif util == 1:
                print("You won")
                break


minimax_game()