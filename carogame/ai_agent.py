import Caro

# Minimax with alpha-beta pruning
def minimax(state):
    actions = state.actions()

    alpha, beta = -1000000, 1000000
    if state.player() == Caro.X:
        scores = [min_value(state.result(action), alpha, beta) for action in actions]
        return actions[scores.index(max(scores))]
    else:
        scores = [max_value(state.result(action), alpha, beta) for action in actions]
        return actions[scores.index(min(scores))]

# Score function for seeking optimality
def max_value(state, alpha, beta):
    if state.terminal():
        return state.utility()
    
    v = -10000
    for action in state.actions():
        v = max(v, min_value(state.result(action), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(state, alpha, beta):
    if state.terminal():
        return state.utility()
    
    v = 10000
    for action in state.actions():
        v = min(v, max_value(state.result(action), alpha, beta))
        if v <= alpha:
            return v
        beta = min(v, beta)
    return v

######################### Cut-off search #############################################
def minimax_cutoff(state):
    actions = state.localActions()

    alpha, beta = -1000000, 1000000
    depth = 3
    if state.player() == Caro.X:
        scores = [min_value_eval(state.result(action), alpha, beta, depth) for action in actions]
        return actions[scores.index(max(scores))]
    else:
        scores = [max_value_eval(state.result(action), alpha, beta, depth) for action in actions]
        return actions[scores.index(min(scores))]
    
def max_value_eval(state, alpha, beta, depth):
    if depth == 0:
        return state.eval()
    
    v = -10000
    for action in state.localActions():
        v = max(v, min_value_eval(state.result(action), alpha, beta, depth - 1))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value_eval(state, alpha, beta, depth):
    if depth == 0:
        return state.eval()
    
    v = 10000
    for action in state.localActions():
        v = min(v, max_value_eval(state.result(action), alpha, beta, depth - 1))
        if v <= alpha:
            return v
        beta = min(v, beta)
    return v