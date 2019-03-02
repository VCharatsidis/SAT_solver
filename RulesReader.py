
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
    filename = "sudoku.txt"
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

def fill_dictionaries_rules():
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
        clauses[ind] = variables

        for v in variables:

            if v not in vars:
                var_clauses = []
                var_clauses.append(ind)
                vars[v] = var_clauses
                if v[0] == '-':
                    not_vars.append(v)
                else:
                    normal_vars.append(v)
            else:
                vars[v].append(ind)


def fill_dictionaries_sudoku(clauses_number):
    '''
    it fills vars and clauses dictionoaries with the extra rules of a given sudoku

    Output 2 dictionaries
    '''

    for index, line in enumerate(sudoku):
        # All clauses except first line.

        variables = line.split()
        variables.pop()
        clauses[index + clauses_number] = variables

        for v in variables:

            if v not in vars:
                var_clauses = []
                var_clauses.append(index + clauses_number)
                vars[v] = var_clauses
                if v[0] == '-':
                    not_vars.append(v)
                else:
                    normal_vars.append(v)
            else:
                vars[v].append(index + clauses_number)


fill_dictionaries_rules()
print(len(clauses))
total_clauses = len(clauses)

fill_dictionaries_sudoku(total_clauses)
print(normal_vars)
print(not_vars)

total_clauses = len(clauses)

print("Clauses length")
print(total_clauses)
print(clauses)
print("Vars length")
print(len(vars))
print(vars)

cnf_solved = False

true_clauses = []
pure_literal = []
unit_clauses = []
vars_with_clauses = []
solution = []

for key in vars:
    vars_with_clauses.append(key)

backtrack = False


def davis_putnam():
    global backtrack

    vars_changes = {}
    clauses_changes = {}
    pure_literal_changes = []
    vars_with_clauses_changes = []
    unit_clauses_changes = []
    true_clauses_changes = []

    if cnf_solved:
        return

    dc_pure_literal = copy.deepcopy(pure_literal)

    for var in dc_pure_literal:
        print("pure_literal "+var)
        set_variable_true(var, vars_changes, clauses_changes, true_clauses_changes, vars_with_clauses_changes, pure_literal_changes, unit_clauses_changes)
        if is_real_var(var):
            solution.append(var)

        if backtrack:
            backtrack = False
            restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes,
                    unit_clauses_changes, true_clauses_changes)
            if var in solution:
                solution.remove(var)
            set_variable_false(var, vars_changes, clauses_changes, true_clauses_changes, vars_with_clauses_changes, pure_literal_changes, unit_clauses_changes)
            if backtrack:
                restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes,
                        unit_clauses_changes, true_clauses_changes)
                backtrack = False
                return
            else:
                davis_putnam()

                print("unsolvable")
                return

        else:
            delete_var(var, vars_with_clauses_changes, pure_literal_changes)
            davis_putnam()
            restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes,
                    unit_clauses_changes, true_clauses_changes)
            set_variable_false(var, vars_changes, clauses_changes, true_clauses_changes, vars_with_clauses_changes,
                               pure_literal_changes, unit_clauses_changes)
            davis_putnam()
            print("unsolvable")
            return


    dc_unit_clauses = copy.deepcopy(unit_clauses)

    for clause in dc_unit_clauses:
        print("unit_clause " + str(clause))
        var = clauses[clause][0]
        print("unit_clause var clauses" + var)
        set_variable_true(var, vars_changes, clauses_changes, true_clauses_changes, vars_with_clauses_changes, pure_literal_changes, unit_clauses_changes)

        if is_real_var(var):
            solution.append(var)

        if backtrack:
            backtrack = False

            if var in solution:
                solution.remove(var)
            restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes,
                        unit_clauses_changes, true_clauses_changes)
            set_variable_false(var, vars_changes, clauses_changes, true_clauses_changes, vars_with_clauses_changes, pure_literal_changes, unit_clauses_changes)
            if backtrack:
                restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes,
                        unit_clauses_changes, true_clauses_changes)
                backtrack = False
                return
            else:
                davis_putnam()
                restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes,
                        unit_clauses_changes, true_clauses_changes)
        else:
            delete_var(var, vars_with_clauses_changes, pure_literal_changes)
            if clause in unit_clauses:
                unit_clauses.remove(clause)
            davis_putnam()
            restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes,
                    unit_clauses_changes, true_clauses_changes)


    print("vars_with_clauses "+str((len(vars_with_clauses))))
    print(vars_with_clauses)

    for var in vars_with_clauses:

        print("normal " + var)
        set_variable_true(var, vars_changes, clauses_changes, true_clauses_changes, vars_with_clauses_changes, pure_literal_changes, unit_clauses_changes)

        if is_real_var(var):
            solution.append(var)

        if backtrack:
            backtrack = False
            if var in solution:
                solution.remove(var)
            restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes, unit_clauses_changes, true_clauses_changes)
            set_variable_false(var, vars_changes, clauses_changes, true_clauses_changes, vars_with_clauses_changes, pure_literal_changes, unit_clauses_changes)
            if backtrack:
                restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes,
                        unit_clauses_changes, true_clauses_changes)
                backtrack = False
                return
            else:
                davis_putnam()
                restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes,
                        unit_clauses_changes, true_clauses_changes)

        else:
            delete_var(var, vars_with_clauses_changes, pure_literal_changes)
            davis_putnam()
            restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes,
                    unit_clauses_changes, true_clauses_changes)

    print("solution")
    print(solution)


def restore(vars_changes, clauses_changes, pure_literal_changes, vars_with_clauses_changes, unit_clauses_changes, true_clauses_changes):
    for var in vars_changes:
        for clause in vars_changes[var]:
            vars[var].append(clause)

    for clause in clauses_changes:
        for var in clauses_changes[clause]:
            clauses[clause].append(var)

    for var in pure_literal_changes:
        pure_literal.remove(var)

    for clause in unit_clauses_changes:
        unit_clauses.remove(clause)

    for var in vars_with_clauses_changes:
        vars_with_clauses.append(var)

    for clause in true_clauses_changes:
        true_clauses.remove(clause)



def set_variable_false(var, vars_changes, clauses_changes, true_clauses_changes, vars_with_clauses_changes, pure_literal_changes, unit_clauses_changes):
    global backtrack
    for clause in vars[var]:
        if len(clauses[clause]) == 1:
            backtrack = True
            return

    opp_var = opposite_var(var)
    delete_var(opp_var, vars_with_clauses_changes, pure_literal_changes)
    delete_var(var, vars_with_clauses_changes, pure_literal_changes)

    for clause in vars[var]:

        clauses[clause].remove(var)
        if clause not in clauses_changes:
            clause_vars = []
            clause_vars.append(var)
            clauses_changes[clause] = clause_vars
        else:
             clauses_changes[clause].appned(var)

        if len(clauses[clause]) == 1:

            unit_clauses.append(clause)
            unit_clauses_changes.append(clause)

    handle_true_opposite_var(opp_var, vars_changes, clauses_changes, true_clauses_changes, vars_with_clauses_changes, pure_literal_changes, unit_clauses_changes)


def handle_true_opposite_var(opposite_var, vars_changes, true_clauses_changes, vars_with_clauses_changes, pure_literal_changes):
    for clause in vars[opposite_var]:

        true_clauses.append(clause)
        true_clauses_changes.append(clause)

        is_solved(true_clauses)

        for variable in clauses[clause]:

            vars[variable].remove(clause)
            if variable not in vars_changes:
                var_clauses = []
                var_clauses.append(clause)
                vars_changes[variable] = var_clauses
            else:
                vars_changes[variable].append(clause)

            if len(vars[variable]) == 0:

                vars_with_clauses.remove(var)

                vars_with_clauses_changes.add(var)

                var = opposite_var(variable)

                pure_literal.append(var)
                pure_literal_changes.append(var)


def set_variable_true(var, vars_changes, clauses_changes, true_clauses_changes, vars_with_clauses_changes, pure_literal_changes, unit_clauses_changes):
    global backtrack
    opp_var = opposite_var(var)
    handle_false_opposite_var(opp_var, clauses_changes, unit_clauses_changes)

    if backtrack:
        return

    delete_var(opp_var, vars_with_clauses_changes, pure_literal_changes)
    delete_var(var, vars_with_clauses_changes, pure_literal_changes)

    for clause in vars[var]:
        true_clauses.append(clause)
        is_solved(true_clauses)

        clauses[clause].remove(var)
        if clause not in clauses_changes:
            clause_vars = []
            clause_vars.append(var)
            clauses_changes[clause] = clause_vars
        else:
            clauses_changes[clause].appned(var)

        for variable in clauses[clause]:

            vars[variable].remove(clause)
            if variable not in vars_changes:
                var_clauses = []
                var_clauses.append(clause)
                vars_changes[variable] = var_clauses
            else:
                vars_changes[variable].append(clause)

            if len(vars[variable]) == 0:
                delete_var(variable, vars_with_clauses_changes, pure_literal_changes)
                opp_variable = opposite_var(variable)

                if opp_variable in vars_with_clauses:
                    pure_literal.append(opp_variable)
                    pure_literal_changes.append(opp_variable)


def delete_var(var, vars_with_clauses_changes, pure_literal_changes):
    if var in vars_with_clauses:
        vars_with_clauses.remove(var)
        vars_with_clauses_changes.append(var)
    if var in pure_literal:
        pure_literal.remove(var)


def handle_false_opposite_var(opposite_var, clauses_changes, unit_clauses_changes):
    global backtrack
    print("opposite_var : "+opposite_var)
    var_clauses = vars[opposite_var]
    print(var_clauses)
    for clause in var_clauses:
        if len(clauses[clause]) == 1:
            print(clauses[clause])
            print("BACKTRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACK-------------------------")
            backtrack = True
            return

    for clause in var_clauses:
        print("clause " + str(clause))
        print(clauses[clause])
        if opposite_var in clauses[clause]:

            clauses[clause].remove(opposite_var)

            if clause not in clauses_changes:
                clause_vars = []
                clause_vars.append(opposite_var)
                clauses_changes[clause] = clause_vars
            else:
                clauses_changes[clause].append(opposite_var)

        print(clauses[clause])
        if len(clauses[clause]) == 1:

            unit_clauses.append(clause)
            unit_clauses_changes.append(clause)


def opposite_var(var):
    if var in normal_vars:
        opp_var = '-' + var
    else:
        opp_var = var[1:]

    return opp_var


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


davis_putnam()
