from __future__ import print_function
import random

#initial state
chess_board = [0, 0, 0, 0, 0, 0, 0, 0]
initial_chess_board = chess_board

#function to print current state of the chess_board
def show_chess_board(chess_board_p):

    new_chess_board = []
    for i in range(len(chess_board)):
        new_chess_board.append([i, chess_board_p[i]])

    print(new_chess_board)

    for i in range(len(chess_board)):
        for j in range(len(chess_board)):
            if [j, i] in new_chess_board:
                print("Q", end=" ")
            else:
                print("*", end=" ")
        print()
    print()

#heuristic cost = no of queens attacking one another
#function to determine the heuristic cost of the chess_board
def determine_heuristic_cost(chess_board):
    h = 0

    # check all queens
    for i in range(len(chess_board)):
        # check interaction with remaining queens
        for j in range(i + 1, len(chess_board)):
            # if queen in same column
            if chess_board[i] == chess_board[j]:
                h += 1

            # get offset
            offset = i - j

            # check if there is diagonal interaction
            if chess_board[i] == chess_board[j] + offset or chess_board[i] == chess_board[j] - offset:
                h += 1
    return h

#there are 56(8*7) neighbouring states
#function to determine the next best move based on the h cost of all neighbouring states
def best_move(chess_board):
    moves = []
    moves.append([chess_board, determine_heuristic_cost(chess_board)])

    for col in range(len(chess_board)):
        for row in range(len(chess_board)):
            chess_board_copy = list(chess_board)
            if chess_board[col] == row:
                continue
            chess_board_copy[col] = row
            cost_of_state = determine_heuristic_cost(chess_board_copy)
            moves.append([chess_board_copy, cost_of_state])

    current = determine_heuristic_cost(chess_board)

    for row in moves:
        if row[1] < current:
            current = row[1]

    #there can be more than 1 best neighbouring state due to same h values
    best_moves = []
    for row in moves:
        if row[1] == current:
            best_moves.append(row[0])

    #randomly select one move out of all the best moves
    next_move = random.choice(best_moves)

    return next_move

#show initial state of the chess_board and its h cost
show_chess_board(chess_board)
print("h = " + str(determine_heuristic_cost(chess_board)))
print()

action_sequence = []

heuristic_cost = determine_heuristic_cost(chess_board)
action_sequence.append([chess_board, heuristic_cost])

#loop through until the minimum h cost state is achieved
no_of_steps = 0
state = 1
while (state == 1):

    chess_board_next_state = best_move(chess_board)

    #if the next best state is the current state, it has reached a maximum state
    if chess_board == chess_board_next_state or heuristic_cost == determine_heuristic_cost(chess_board_next_state):
        state = 0
        show_chess_board(chess_board)
        cost = determine_heuristic_cost(chess_board)
        print("h = " + str(cost))
        if cost == 0:
            print("Reached the Global Maximum!")
            print()
        else:
            print("Stuck in a Local Maximum")
            print()

            # if the result is a local minimum, then reinitialize the chess_board and try again
            state = 1
            chess_board = initial_chess_board
    else:
        chess_board = chess_board_next_state
        state = 1
        heuristic_cost = determine_heuristic_cost(chess_board)
        action_sequence.append([chess_board, heuristic_cost])
        no_of_steps += 1
        # show_chess_board(chess_board)

print("Steps taken: ")
for row in action_sequence:
    print(row)

print()
print("No.of steps: " + str(no_of_steps))
print()

print("The Final solution for 8-Queen Problem:")
print()
show_chess_board(chess_board)
