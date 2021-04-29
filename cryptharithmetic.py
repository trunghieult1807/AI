from constraint import *


def cryptarithmetic():
    problem = Problem()

    problem.addVariables(['T', 'W', 'O', 'F', 'U', 'R'], range(10))
    problem.addVariables(['X1', 'X2', 'X3'], [0, 1])

    problem.addConstraint(AllDifferentConstraint(), ['T', 'W', 'O', 'F', 'U', 'R'])
    problem.addConstraint(lambda O, R, X1: (2 * O) == R + (10 * X1), ('O', 'R', 'X1'))
    problem.addConstraint(lambda W, U, X1, X2: X1 + (2 * W) == U + (10 * X2), ('W', 'U', 'X1', 'X2'))
    problem.addConstraint(lambda T, O, X2, X3: X2 + (2 * T) == O + (10 * X3), ('T', 'O', 'X2', 'X3'))
    problem.addConstraint(lambda F, X3: X3 == F, ('F', 'X3'))

    print(problem.getSolutions())


def main():
    cryptarithmetic()


if __name__ == '__main__':
    main()