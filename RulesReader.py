
import copy

def rules():
    filename = "rules.txt"

    with open(filename) as f:
        rules = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    rules = [x.strip() for x in rules]


    return rules


rules = rules()
print(len(rules))


def read_sudoku():
    filename = "hardest.txt"
    with open(filename) as f:
        sudoku = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    sudoku = [x.strip() for x in sudoku]

    return sudoku

sudoku = read_sudoku()
print(sudoku)
print(len(sudoku))

vars = {}
clauses = {}
not_vars = []
normal_vars = []

def fill_dictionaries_rules(sudoku_clauses):
    '''
    it fills vars and clauses dictionoaries and return them
    vars is a dictionary with keys strings and values a list of integers,
    for every variable we have the list of caluses that the variable appears.
    clauses is a dictionary with keys integers and values a list of strings,
    for every clause we have the list of variables that appears.

    Output 2 dictionaries

    '''
    for index, line in enumerate(rules):
        # All clauses except first line.
        if index == 0:
            continue
        ind = index - 1
        variables = line.split()
        variables.pop()
        clause_index = sudoku_clauses + ind
        clauses[clause_index] = variables

        for v in variables:

            if v not in vars:
                var_clauses = []
                var_clauses.append(clause_index)
                vars[v] = var_clauses
                if v[0] == '-':
                    not_vars.append(v)
                else:
                    normal_vars.append(v)
            else:
                vars[v].append(clause_index)


def fill_dictionaries_sudoku():
    '''
    it fills vars and clauses dictionoaries with the extra rules of a given sudoku

    Output 2 dictionaries
    '''

    for index, line in enumerate(sudoku):
        # All clauses except first line.

        variables = line.split()
        variables.pop()
        clauses[index] = variables

        for v in variables:

            if v not in vars:
                var_clauses = []
                var_clauses.append(index)
                vars[v] = var_clauses
                if v[0] == '-':
                    not_vars.append(v)
                else:
                    normal_vars.append(v)
            else:
                vars[v].append(index)




fill_dictionaries_sudoku()
print(normal_vars)
print(not_vars)

sudoku_clauses = len(clauses)

fill_dictionaries_rules(sudoku_clauses)
print(len(clauses))
total_clauses = len(clauses)


total_clauses = len(clauses)

print("Clauses length")
print(total_clauses)
print(clauses)
print("Vars length")
print(len(vars))
print(vars)

cnf_solved = False

vars_with_clauses = []
true_clauses = []
pure_literal = []
solution = []
unit_clauses = []

for key in vars:
    if key[0] == '-':
        continue
    else:
        vars_with_clauses.append(key)



print(vars_with_clauses)


def opposite_var(var):
    if var in normal_vars:
        opp_var = '-' + var
    else:
        opp_var = var[1:]

    return opp_var


def remove_tautologies():
    for clause in clauses:
        for var in clauses[clause]:
            opp_var = opposite_var(var)
            if opp_var in clauses[clause]:
                true_clauses.appned(clause)


remove_tautologies()
print("true clauses")
print(true_clauses)


def davis_putnam(vars_with_clauses, true_clauses, pure_literal, unit_clauses, vars, clauses):
    global cnf_solved

    print(solution)
    if cnf_solved:
        return

    var = vars_with_clauses[0]

    dc_vars_with_clauses = copy.deepcopy(vars_with_clauses)
    dc_vars_with_clauses.remove(var)

    solution.append(var)
    dc_true_clauses = copy.deepcopy(true_clauses)
    dc_pure_literal = copy.deepcopy(pure_literal)
    dc_unit_clauses = copy.deepcopy(unit_clauses)
    dc_vars = copy.deepcopy(vars)
    dc_clauses = copy.deepcopy(clauses)

    backtrack = case_true(var, dc_true_clauses, dc_pure_literal, dc_unit_clauses, dc_vars, dc_clauses)

    if backtrack:

        #restore(var, vars_changes, clauses_changes, True)
        solution.remove(var)
        dc_true_clauses = copy.deepcopy(true_clauses)
        dc_pure_literal = copy.deepcopy(pure_literal)
        dc_unit_clauses = copy.deepcopy(unit_clauses)
        dc_vars = copy.deepcopy(vars)
        dc_clauses = copy.deepcopy(clauses)

        backtrack = case_false(var, dc_true_clauses, dc_unit_clauses, dc_vars, dc_clauses)

        if backtrack:
            #restore(var, vars_changes, clauses_changes, False)
            return True

        davis_putnam(dc_vars_with_clauses, dc_true_clauses, dc_pure_literal, dc_unit_clauses, dc_vars, dc_clauses)

    else:
        backtrack = davis_putnam(dc_vars_with_clauses, dc_true_clauses, dc_pure_literal, dc_unit_clauses, dc_vars, dc_clauses)

        if backtrack:
            #restore(var, vars_changes, clauses_changes, True)
            solution.remove(var)
            dc_true_clauses = copy.deepcopy(true_clauses)
            dc_pure_literal = copy.deepcopy(pure_literal)
            dc_unit_clauses = copy.deepcopy(unit_clauses)
            dc_vars = copy.deepcopy(vars)
            dc_clauses = copy.deepcopy(clauses)

            backtrack = case_false(var, dc_true_clauses, dc_unit_clauses, dc_vars, dc_clauses)

            if backtrack:
                #restore(var, vars_changes, clauses_changes, False)
                return True

            backtrack = davis_putnam(dc_vars_with_clauses, dc_true_clauses, dc_pure_literal, dc_unit_clauses, dc_vars, dc_clauses)
            print("UNSOLVED")
            return backtrack

    return True


# def restore(var, vars_changes, clauses_changes, opposite):
#     # print("restore")
#     # print(clauses_changes)
#     # print(vars_changes)
#     for vari in vars_changes:
#         for c in vars_changes[vari]:
#             vars[vari].append(c)
#
#     if opposite:
#         opp = opposite_var(var)
#     else:
#         opp = var
#
#     for clause in clauses_changes:
#         clauses[clause].append(opp)


def case_false(var, dc_true_clauses, unit_clauses, dc_vars, dc_clauses):
    var_clauses = dc_vars[var]

    for clause in var_clauses:
        if clause not in dc_true_clauses:
            dc_clauses[clause].remove(var)

            if len(clauses[clause]) == 1:
                unit_clauses.append(clause)

            elif len(clauses[clause]) == 0:
                backtrack = True
                return backtrack

    opp_var = opposite_var(var)
    var_clauses = dc_vars[opp_var]

    for clause in var_clauses:
        if clause not in dc_true_clauses:

            dc_true_clauses.append(clause)

            clause_variables = dc_clauses[clause]
            for variable in clause_variables:
                dc_vars[variable].remove(clause)

    is_solved(dc_true_clauses)

    backtrack = False
    return backtrack


def case_true(var, dc_true_clauses, dc_pure_literal, unit_clauses, dc_vars, dc_clauses):

    var_clauses = dc_vars[var]

    for clause in var_clauses:
        if clause not in dc_true_clauses:
            dc_true_clauses.append(clause)

            clause_variables = dc_clauses[clause]
            for variable in clause_variables:
                dc_vars[variable].remove(clause)

                if len(dc_vars[variable]):
                    opp_var = opposite_var(variable)
                    dc_pure_literal.append(opp_var)

    is_solved(dc_true_clauses)

    opp_var = opposite_var(var)
    clauses_opp_var = dc_vars[opp_var]

    for clause in clauses_opp_var:
        if clause not in dc_true_clauses:

            dc_clauses[clause].remove(opp_var)

            if len(dc_clauses[clause]) == 1:
                unit_clauses.append(clause)

            elif len(dc_clauses[clause]) == 0:
                backtrack = True
                return backtrack

    is_solved(dc_true_clauses)
    backtrack = False
    return backtrack


def is_real_var(var):
    if var[0] == '-':
        return False
    else:
        return True


def is_solved(true_clauses):
    global cnf_solved
    if len(true_clauses) == total_clauses:
        cnf_solved = True
        print(len(solution))
        print("PROBLEM SOLVED!!!")


davis_putnam(vars_with_clauses, true_clauses, pure_literal, unit_clauses, vars, clauses)
