import time
from search import *
from P1 import *

def main():
    print("The Water Jug Problem - \n")
    problem_waterJug = WaterJugProblem((0, 4, 0, 3), (2, 4, 0, 3))
    path = breadth_first_tree_search(problem_waterJug).solution()
    print('Solution Path: ',path, '\n')


if __name__ == "__main__":
    main()
