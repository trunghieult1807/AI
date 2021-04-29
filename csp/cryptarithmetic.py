from backtracking_search import *
from csp import *


def cryptarithmeticConstraints(assignment):
    """
    @Return:
        True: if satisfy constraints
    """
    unique = set()
    for var, val in assignment.items():
        if var in ['X1', 'X2', 'X3']:
            continue
        if val in unique:
            return False
        else:
            unique.add(val)
    if 'T' in assignment and assignment['T'] == 0:
        return False
    if 'F' in assignment and assignment['F'] == 0:
        return False
    if 'O' in assignment and 'R' in assignment and 'X1' in assignment and \
            assignment['O'] * 2 != assignment['R'] + 10 * assignment['X1']:
        return False
    if 'W' in assignment and 'U' in assignment and \
            'X1' in assignment and 'X2' in assignment and \
            assignment['W'] * 2 + assignment['X1'] != assignment['U'] + 10 * assignment['X2']:
        return False
    if 'T' in assignment and 'O' in assignment and \
            'X2' in assignment and 'X3' in assignment and\
            assignment['T'] * 2 + assignment['X2'] != assignment['O'] + 10 * assignment['X3']:
        return False
    if 'F' in assignment and 'X3' in assignment and assignment['F'] != assignment['X3']:
        return False
    return True
    

def main():
    variables = ['T', 'W', 'O', 'F', 'U', 'R', 'X1', 'X2', 'X3']
    domains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    cryptarithmetic = CSProblem(variables, domains, cryptarithmeticConstraints)
    assignment = {}
    result = backtracking_search(cryptarithmetic, assignment)
    print(result)


if __name__ == "__main__":
    main()
