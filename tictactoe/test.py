from tictactoe import *

board = [[X, EMPTY, EMPTY],
        [EMPTY, X, O],
        [EMPTY, O, EMPTY]]
print(actions(board))
print(board)
print(player(board))
print(result(board, (0,1)))
print(player(board))
print(result(board, (0,2)))
print(player(board))
print(result(board, (2,0)))
print(winner(board))
print(terminal(board))
print(minimax(board))
