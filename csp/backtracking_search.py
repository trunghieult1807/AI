def backtracking_search(csp, assignment):
    return recursive_backtracking(assignment, csp)


def recursive_backtracking(assignment, csp):
    if csp.isComplete(assignment):
        return assignment

    var = csp.selectUnselectedVariable(assignment)
    for val in csp.consistentSuccessor(var, assignment):
        assignment[var] = val
        res = recursive_backtracking(assignment, csp)
        if res:
            return res
        del assignment[var]

    return {}

