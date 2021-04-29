class CSProblem:
    def __init__(self, v, d, constraintFunc):
        self.variables = v
        self.domains = d
        self.constraintFunc = constraintFunc

    def isComplete(self, assignment):
        return len(assignment) == len(self.variables)

    def selectUnselectedVariable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var

    def consistentSuccessor(self, var, assignment):
        return [val for val in self.domains if self.isConsistent(var, val, assignment)]

    def isConsistent(self, var, val, assignment):
        temp = assignment.copy()
        temp[var] = val
        return self.constraintFunc(temp)