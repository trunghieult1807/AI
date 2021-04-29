
# lists of states
variables = ["WA", "NT", "SA", "Q", "NSW", "V", "T", ]

# adjacent states of element at matching index of variables in list
constraints = [["NT", "SA"], ["WA", "SA", "Q"], ["WA", "NT", "Q", "NSW", "V"], ["SA", "NT", "NSW"], ["SA", "Q", "V"], ["NSW", "SA"],
               []]

# domains
d = [["red", "green", "blue"], ["red", "green", "blue"], ["red", "green", "blue"], ["red", "green", "blue"],
     ["red", "green", "blue"], ["red", "green", "blue"], ["red", "green", "blue"]]

assignments = {}
arcs = []


def AC3():
    # fill queue with initial arcs
    fillQueue()

    # check if arcs is empty
    while arcs:
        arcVars = arcs.pop(0)
        print("@@@")
        print(arcs)
        if remove_inconsistent_values(arcVars[0], arcVars[1]):

            dIIndex = variables.index(arcVars[0])
            if len(d[dIIndex]) == 0:
                print("No Solution")
                return False

            neighbors = list(constraints[dIIndex])
            neighbors.remove(arcVars[1])

            for xk in neighbors:
                arcs.append([xk, arcVars[0]])

    print(assignments)
    return True


# fill queue with initial arcs
def fillQueue():
    for var in variables:
        varIndex = variables.index(var)
        for arc in constraints[varIndex]:
            arcs.append([var, arc])


def remove_inconsistent_values(Xi, Xj):
    removed = False

    index = variables.index(Xi)

    # for each value in the domain
    for x in d[index]:

        # check if state is adjacent, if not, go to next x
        if Xj not in constraints[index]:
            break

        if Xj not in assignments:
            continue

        # if adjacent state has current assignment of X (same color)
        if x in assignments[Xj]:
            d[index].remove(x)  # remove x from Di
            removed = True

    if not removed and len(d[index]) > 0:
        assignments[Xi] = d[index][0]

    return removed


AC3()
