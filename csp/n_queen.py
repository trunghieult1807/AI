import numpy as np


def isViolateRow(matrix, row):
    for i in range(matrix.shape[0]):
        if matrix[row][i] == 1:
            return True
    return False


def isViolateDiagonal(matrix, row, col):
    i = 0
    while row + i < matrix.shape[0] or row - i >= 0 or col + i < matrix.shape[0] or col - i >= 0:
        if row + i < matrix.shape[0] and col + i < matrix.shape[0] and matrix[row + i][col + i] == 1:
            return True
        if row + i < matrix.shape[0] and col - i >= 0 and matrix[row + i][col - i] == 1:
            return True
        if row - i >= 0 and col + i < matrix.shape[0] and matrix[row - i][col + i] == 1:
            return True
        if row - i >= 0 and col - i >= 0 and matrix[row - i][col - i] == 1:
            return True
        i += 1
    return False


def nqueens(matrix, col=0):
    for row in range(matrix.shape[0]):
        if not isViolateRow(matrix, row) and not isViolateDiagonal(matrix, row, col):
            matrix[row][col] = 1
            if col == matrix.shape[0] - 1:
                return True
            flag = nqueens(matrix, col + 1)
            if not flag:
                matrix[row][col] = 0
            else:
                return True

    return False


def main():
    n = int(input("Enter n(greater than 3) : "))
    matrix = np.zeros([n, n], dtype=int)
    if nqueens(matrix):
        print(matrix)
    else:
        print("No solution")


if __name__ == "__main__":
    main()
