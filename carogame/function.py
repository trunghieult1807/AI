
import multiprocessing
import random
import threading
import numpy as np


def check_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != ".":
                return False
    return True


def BestMove(gird, isMax, depth):
    board = gird.copy()
    best_move = [-1, -1]
    best_value = isMax and -9999 or 9999
    moves = get_top_moves(board, 10, isMax)

    test = list(map(lambda x: x[0], moves))

    test = list(
        map(lambda x: (x, board, isMax, -10e5, 10e5, depth), test))
    p = multiprocessing.Pool()
    result = p.map(getBestMoveThread, test)

    for i in result:
        if ((isMax and i[0] > best_value)
                or (not isMax and i[0] < best_value)):
            best_value = i[0]
            best_move = (i[1], i[2])
    if best_move == [-1, -1]:
        return(moves[0][0])
    print(best_move, best_value)
    return best_move


def getBestMoveThread(a):
    ((x, y), grid, isMax, alpha, beta, depth) = a
    board = grid.copy()
    board[x][y] = 'O'
    value = minimax(board, not isMax, alpha, beta, depth-1)
    board[x][y] = '.'
    return value, x, y


def get_patterns(line, pattern_dic, sym):
    i = 0
    s = ''
    while i < len(line):

        if line[i] == sym:
            if (i != 0 and i != len(line) - 1 and s == '' and line[i-1] != "."):
                s = line[i - 1]
            elif(i == 0):
                s = "b"
            s = s+sym
        if (line[i] != sym) or i == len(line) - 1:
            if i+1 <= len(line) - 1:
                if line[i] == "." and line[i+1] == sym and s != "":
                    s += line[i] + line[i+1]
                    i += 2
                    continue
            if (line[i] != sym and i < len(line) - 1 and line[i] != "." and s != ''):
                s += line[i]
            if(i == len(line)-1 and s != '' and line[i] != "."):
                s += "e"
            if "XXXXX" in s or "OOOOO" in s:
                s = s.replace('e', '')
                s = s.replace('b', '')
            if s in pattern_dic.keys():
                pattern_dic[s] += 1
            else:
                pattern_dic[s] = 1
            s = ''
        i += 1


def get_pattern_for_Row(pattern_dic, B):
    for i in range(B.shape[0]):
        get_patterns(B[i], pattern_dic, 'X')
    for i in range(B.shape[0]):
        get_patterns(B[i], pattern_dic, 'O')


def get_pattern_for_Column(pattern_dic, B):
    T = B.T
    for i in range(T.shape[0]):
        get_patterns(T[i], pattern_dic, 'X')
    for i in range(T.shape[0]):
        get_patterns(T[i], pattern_dic, 'O')


def get_pattern_for_Diagonal(pattern_dic, B):
    for i in range(-B.shape[0]+1, B.shape[0]):
        get_patterns(B.diagonal(i), pattern_dic, 'O')
    A = B[::-1, :]
    for i in range(-A.shape[0]+1, A.shape[0]):
        get_patterns(A.diagonal(i), pattern_dic, 'O')

    for i in range(-B.shape[0]+1, B.shape[0]):
        get_patterns(B.diagonal(i), pattern_dic, 'X')
    A = B[::-1, :]
    for i in range(-A.shape[0]+1, A.shape[0]):
        get_patterns(A.diagonal(i), pattern_dic, 'X')


def get_all_patterns(B):
    pattern_dic = {}
    pattern_dic_remove_reverse = {}
    get_pattern_for_Row(pattern_dic, B)
    get_pattern_for_Column(pattern_dic, B)
    get_pattern_for_Diagonal(pattern_dic, B)
    for i in pattern_dic:
        if (i[::-1] in pattern_dic_remove_reverse):
            pattern_dic_remove_reverse[i[::-1]] += pattern_dic[i]
        elif i not in pattern_dic_remove_reverse:
            pattern_dic_remove_reverse[i.strip()] = pattern_dic[i]
    del pattern_dic_remove_reverse[""]
    return pattern_dic_remove_reverse


def check_full(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == ".":
                return False
    return True


def checkState(board):
    pattern_dic = get_all_patterns(board)
    if 'XXXXX' in pattern_dic or 'OXXXXX' in pattern_dic or 'XXXXXO' in pattern_dic:
        return 100000
    elif 'OOOOO' in pattern_dic or 'XOOOOO' in pattern_dic or 'OOOOOX' in pattern_dic:
        return -100000
    else:
        if check_full(board):
            return "tie"
        return 0


def score_parttern(pattern, block, is_curent, space=False):

    if block == 2:
        return 0
    if pattern >= 5:
        if space:
            return 8000
        return 100000
    consec_score = (2, 5, 1000, 10000)
    block_count_score = (0.5, 0.6, 0.01, 0.25)
    not_current_score = (1, 1, 0.2, 0.15)
    empty_space_score = (1, 1.2, 0.9, 0.4)
    if pattern == 4 and block == 0 and is_curent == False:
        return 10000
    if pattern == 4 and block == 1 and is_curent == False:
        return 10000
    consec_idx = pattern - 1
    value = consec_score[consec_idx]
    if block == 1:
        value *= block_count_score[consec_idx]
    if not is_curent:
        value *= not_current_score[consec_idx]
    if space:
        value *= empty_space_score[consec_idx]
    return int(value)


def score(a, isMax):
    all_parttern = get_all_patterns(a)
    all_parttern['X'] = 1
    all_parttern['O'] = 1
    score = 0
    for i in all_parttern:
        countX = i.count("X")
        countO = i.count("O")
        countDot = i.count('.')
        countWall = len(i) - countO - countDot - countX
        current = False
        space = '.' in i
        if(countX >= countO):
            current = True == isMax
            consec = countX
            block = countO + countWall
            if countX == 5 and countO == 1:
                block = 1
            score += score_parttern(consec, block, current,
                                    space) * all_parttern[i]

        else:
            consec = countO
            current = False == isMax
            block = countX + countWall
            if countO == 5 and countX == 1:
                block = 1
            score -= score_parttern(consec, block, current,
                                    space) * all_parttern[i]
    return score


def isMoveLeft(game_board):
    for i in range(12):
        for j in range(12):
            if(game_board[i][j] == '.'):
                return True
    return False


def is_end(game_board):
    is_win, turn = check_win(game_board)
    if(is_win and turn == 'X'):
        return True, "X"
    if(is_win and turn == 'O'):
        return True, "O"
    return False, ""


# This is the minimax function. It considers all
#  the possible ways the game can go and returns
#  the value of the board


def minimax(game_board, isMax, alpha, beta, depth):
    iswin, winner = is_end(game_board)
    if(depth == 0 or iswin):
        if winner == "X":
            return 100000
        if winner == "O":
            return -100000
        return score(game_board, not isMax)

    moves = list(dict.fromkeys(possible_moves(game_board)))

    # if maximizer's move
    if(isMax):
        value = -9999
        # Traversal all cells
        for i, j in moves:
            if(game_board[i][j] == '.'):

                game_board[i][j] = "X"
                # call minimax rescursively and choose max value
                value = max(value, minimax(
                    game_board, False, alpha, beta, depth-1))
                # undo the move
                game_board[i][j] = '.'

                alpha = max(value, alpha)
                # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                if(alpha >= beta):
                    break
        return value
    else:
        value = 9999
        for i, j in moves:
            if(game_board[i][j] == '.'):

                game_board[i][j] = "O"
                value = min(value, minimax(
                    game_board, True, alpha, beta,  depth-1))
                game_board[i][j] = '.'

                beta = min(value, beta)
                if(alpha >= beta):
                    break
        return value


def possible_moves(board, expand=[1]):
    taken = []
    # mảng directions lưu hướng đi (8 hướng)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (-1, -1), (-1, 1), (1, -1)]
    move_left = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != '.':
                taken.append((i, j))
    for direction in directions:
        dx, dy = direction
        for x, y in taken:
            for length in expand:
                xf = x + length*dx
                yf = y + length*dy
                # chừng nào yf,xf không có trong board
                while not (0 <= xf < len(board) and 0 <= yf < len(board)):
                    xf -= dx
                    yf -= dy
                move = xf, yf
                if move not in taken:
                    move_left.append(move)
    return move_left


def get_top_moves(board, n, isMax):
    top_moves = []
    move_left = list(dict.fromkeys(possible_moves(board)))

    for move in move_left:
        x, y = move
        board[x][y] = isMax and 'X' or 'O'
        score_move = score(board, isMax)
        board[x][y] = '.'
        top_moves.append((move, score_move))
    return sorted(top_moves, key=lambda x: x[1], reverse=isMax)[:n]


def get_best_move(game_board, isMax, depth):
    best_move = [-1, -1]
    best_value = isMax and -9999 or 9999
    moves = get_top_moves(game_board, 10, isMax)

    for move_and_score in moves:
        x, y = move_and_score[0]
        game_board[x][y] = isMax and 'X' or 'O'
        value = minimax(game_board, not isMax, -10e5, 10e5, depth-1)
        game_board[x][y] = '.'

        if ((isMax and value > best_value)
                or (not isMax and value < best_value)):
            best_value = value
            best_move = move_and_score[0]
    if best_move == [-1, -1]:
        return moves[0][0]
    return best_move


def check_win(board_game):
    win = checkState(board_game)
    if win == 100000:
        return True, "X"
    if win == -100000:
        return True, "O"
    return False, ""
