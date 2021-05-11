# from caro import Caro
#
# game = Caro()
# def minimax_cutoff():
#     actions = game.local_successor()
#
#     alpha, beta = -1000000, 1000000
#     depth = 3
#     if state.player() == game.:
#         scores = [min_value_eval(state.result(action), alpha, beta, depth) for action in actions]
#         return actions[scores.index(max(scores))]
#     else:
#         scores = [max_value_eval(state.result(action), alpha, beta, depth) for action in actions]
#         return actions[scores.index(min(scores))]
#
#
# def max_value_eval(state, alpha, beta, depth):
#     if depth == 0:
#         return state.eval()
#
#     v = -10000
#     for action in state.localActions():
#         v = max(v, min_value_eval(state.result(action), alpha, beta, depth - 1))
#         if v >= beta:
#             return v
#         alpha = max(alpha, v)
#     return v
#
#
# def min_value_eval(state, alpha, beta, depth):
#     if depth == 0:
#         return state.eval()
#
#     v = 10000
#     for action in state.localActions():
#         v = min(v, max_value_eval(state.result(action), alpha, beta, depth - 1))
#         if v <= alpha:
#             return v
#         beta = min(v, beta)
#     return v