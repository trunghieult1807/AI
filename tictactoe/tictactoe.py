"""
Tic Tac Toe Player
"""

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                countX += 1
            if board[i][j] == O:
                countO += 1
    if countX == countO:
        return X
    else:
        return O

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    setOfActions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                setOfActions.add((i,j))

    # for action in setOfActions:
    #     print(action)
    return setOfActions
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardcopy = copy.deepcopy(board)
    try:
        if boardcopy[action[0]][action[1]] != EMPTY:
            raise IndexError
        else:
            boardcopy[action[0]][action[1]] = player(boardcopy)
            return boardcopy
    except IndexError:
        print('Spot already occupied')



    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    countX = 0
    countO = 0
    # Check for row
    for i in range(3):
        countX = 0
        countO = 0
        for j in range(3):
            if board[i][j] == X:
                countX += 1
            elif board[i][j] == O:
                countO += 1
        if countX == 3:
            return X
        elif countO == 3:
            return O
    # Check for column
    countX = 0
    countO = 0
    for j in range(3):
        countX = 0
        countO = 0
        for i in range(3):
            if board[i][j] == X:
                countX += 1
            elif board[i][j] == O:
                countO += 1
        if countX == 3:
            return X
        elif countO == 3:
            return O
    # Check for downwards diagonal
    countX = 0
    countO = 0
    for i in range(3):
        if board[i][i] == X:
            countX += 1
        elif board[i][i] == O:
            countO += 1
    if countX == 3:
        return X
    elif countO == 3:
        return O
    # Check for upwards diagonal
    countX = 0
    countO = 0
    for i in range(3):
        if board[i][2 - i] == X:
            countX += 1
        elif board[i][2 - i] == O:
            countO += 1
    if countX == 3:
        return X
    elif countO == 3:
        return O

    return EMPTY
    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    countNone = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                countNone += 1
    if countNone == 0 or winner(board) != EMPTY:
        return True
    else:
        return False
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    #raise NotImplementedError
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Make a random move at begin
    if board == initial_state():
        return random.randint(0, 2), random.randint(0, 2)

    current_player = player(board)
    base = -math.inf if current_player == X else math.inf

    for action in actions(board):
        value = minimax_value(result(board, action), base)

        if current_player == X:
            value = max(base, value)

        if current_player == O:
            value = min(base, value)

        if value != base:
            base = value
            best_action = action

    return best_action


def minimax_value(board, best_value):
    """
    Returns the best value for each recursive minimax iteration.
    Optimized using Alpha-Beta Pruning: If the new value found is better
    than the best value then return without checking the others.
    """
    if terminal(board):
        return utility(board)

    current_player = player(board)
    base = -math.inf if current_player == X else math.inf

    for action in actions(board):
        value = minimax_value(result(board, action), base)

        if current_player == X:
            if value > best_value:
                return value
            base = max(base, value)

        if current_player == O:
            if value < best_value:
                return value
            base = min(base, value)

    return base
