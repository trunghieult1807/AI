import Caro
import ai_agent as AI

# state = Caro.CaroState.loadState((12, 12), {(3,4), (3,5), (4,5)}, {(3,3), (3,2)})

# Xs = {(1,1), (1,2), (1,3), (1,4), (1,5)}
# Os = {(0,1), (1,0), (1,7), (4,4), (5,5)}
# x_win_state = Caro.CaroState.loadState((12, 12), Xs, Os)
# game = Caro.CaroGame.loadState(x_win_state)
# game.checkWinner()

# x_win_state.printBoard()
# # print(game.winner())

# game2 = Caro.CaroGame((12, 12))
# for X, O in zip(Xs, Os):
#     game2.makeMove(X)
#     if game2.terminal():
#         print(game2.winner())
#         continue
#     game2.makeMove(O)
#     if game2.terminal():
#         print(game2.winner())
#         continue

Xs = {(2,2), (3,2), (4,2), (3,3)}
Os = {(1,3), (3,4), (4,4)}
gameState = Caro.CaroState.loadState((7, 7), Xs, Os)
# print(gameState.localActions())

# gameState.printBoard()
# print()
# newState.printBoard()

while not gameState.terminal():
    move = AI.minimax_cutoff(gameState)
    print(gameState.player(), "make move", move)
    gameState = gameState.result(move)
    gameState.printBoard()
    input()
# move = AI.minimax_cutoff(gameState)
# print(move)
# gameState = gameState.result(move)