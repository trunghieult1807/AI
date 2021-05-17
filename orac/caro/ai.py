from . import palette


def minimax_cutoff(state, current_player):
    actions = state.top_actions(current_player)

    alpha, beta = -1000000, 1000000
    depth = 1
    if current_player == palette.ai:
        scores = [min_value_eval(state.result(action, current_player), alpha, beta, depth, current_player) for action in actions]
        print(scores)
        return actions[scores.index(max(scores))]
    else:
        scores = [max_value_eval(state.result(action, current_player), alpha, beta, depth, current_player) for action in actions]
        return actions[scores.index(min(scores))]


def max_value_eval(state, alpha, beta, depth, current_player):
    if depth == 0:
        return state.evaluate()

    v = -1000000
    for action in state.top_actions(current_player):
        v = max(v, min_value_eval(state.result(action, current_player), alpha, beta, depth - 1, current_player))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value_eval(state, alpha, beta, depth, current_player):
    if depth == 0:
        return state.evaluate()

    v = 1000000
    for action in state.top_actions(current_player):
        v = min(v, max_value_eval(state.result(action, current_player), alpha, beta, depth - 1, current_player))
        if v <= alpha:
            return v
        beta = min(v, beta)
    return v
