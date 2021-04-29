import argparse

import search
import random


class BoardState:
    """
    Implement 8x8 Board for 8 queens
    """
    def __init__(self, size=8):
        self.size = size
        self.queens = set()
    
    def __str__(self):
        s = []
        for i in range(self.size):
            line = '|'
            line += '|'.join('Q' if (i, j) in self.queens else ' ' for j in range(self.size))
            line += '|'
            s.append('-' * (self.size * 2 + 1))
            s.append(line)
        s.append('-' * (self.size * 2 + 1))
        return '\n'.join(s)
    
    def __eq__(self, other):
        return self.size == other.size and self.queens == other.queens

    def __hash__(self):
        return hash(str(self.queens))
    
    def isGoal(self):
        return len(self.queens) == self.size
    
    def addQueen(self, queen_pos):
        x, y = queen_pos
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            raise Exception("Queen out of board")
        if self.isSafe(queen_pos):
            self.queens.add(queen_pos)

    def result(self, queen_pos):
        new_board = BoardState(self.size)
        queens = self.queens.copy()
        [new_board.addQueen(queen) for queen in self.queens]
        new_board.addQueen(queen_pos)
        return new_board

    def addRandomQueens(self):
        THRESH_HOLD = 50
        counter = 0
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.isSafe((x, y)):
                self.queens.add((x, y))
                return (x, y)
            counter += 1
            if counter == THRESH_HOLD:
                return None
    
    def isSafe(self, queen_pos):
        x, y = queen_pos
        for queen in self.queens:
            if x == queen[0] or y == queen[1] or abs(x - queen[0]) == abs(y - queen[1]):
                return False
        return True
    
    def legalMoves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.isSafe((i, j)):
                    moves.append((i, j))
        return moves


class EightQueensProblem(search.SearchProblem):
    """
    Implement 8 queens search problem
    """
    def __init__(self, board):
        self.board = board

    def getStartState(self):
        return self.board

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        for queen_pos in self.getActions(state):
            next_state = self.getNextState(state, queen_pos)
            yield (next_state, queen_pos, self.getActionCost(state, queen_pos, next_state))

    def getActions(self, state):
        return state.legalMoves()

    def getActionCost(self, state, action, next_state):
        return 1

    def getNextState(self, state, action):
        return state.result(action)

    def getCostOfActions(self, actions):
        return len(actions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('search_type')
    args = parser.parse_args()
    board = BoardState()
    board.addRandomQueens()
    print('Add a random queen:')
    print(board)
    
    problem = EightQueensProblem(board)

    if args.search_type == 'brfs':
        actions = search.brfs(problem)
    elif args.search_type == 'dfs':
        actions = search.dfs(problem)
    elif args.search_type == 'dls':
        actions = search.dls(problem)
    elif args.search_type == 'ids':
        actions = search.dls(problem)
    elif args.search_type == 'ucs':
        actions = search.ucs(problem)
    elif args.search_type == 'bfs':
        actions = search.bfs(problem)
    elif args.search_type == 'astar':
        actions = search.astar(problem)

    print('DFS found a path of %d moves: %s' % (len(actions), str(actions)))
    curr = board
    for queen_pos in actions:
        input("Press return for the next state...")   # wait for key stroke
        curr = curr.result(queen_pos)
        print(curr)