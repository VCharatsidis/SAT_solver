
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

backtrack = False

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


def davis_putnam(vars_with_clauses, true_clauses, pure_literal, unit_clauses):
    global backtrack
    global cnf_solved

    if cnf_solved:
        return

    var = vars_with_clauses[0]

    print("")
    print("var " + str(var))
    #print("len(solution) " + str(len(solution)))
    print("solution " + str(solution))
    print("")

    if var == '-111':
        print(vars[var])

    dc_vars_with_clauses = copy.deepcopy(vars_with_clauses)

    dc_vars_with_clauses.remove(var)
    solution.append(var)
    dc_true_clauses = copy.deepcopy(true_clauses)
    dc_pure_literal = copy.deepcopy(pure_literal)
    dc_unit_clauses = copy.deepcopy(unit_clauses)
    vars_changes = {}
    clauses_changes = []

    case_true(var, dc_true_clauses, vars_changes, dc_pure_literal, clauses_changes, dc_unit_clauses)

    if backtrack:
        print("backtrack")
        restore(var, vars_changes, clauses_changes)
        solution.remove(var)
        backtrack = False

        dc_true_clauses = copy.deepcopy(true_clauses)
        dc_pure_literal = copy.deepcopy(pure_literal)
        dc_unit_clauses = copy.deepcopy(unit_clauses)
        vars_changes = {}
        clauses_changes = []

        case_false(var, dc_true_clauses, vars_changes, clauses_changes, dc_unit_clauses)
        print("vars_changes " + str(vars_changes) + " " )
        print("clauses_changes " + str(clauses_changes) + " ")

        if backtrack:
            backtrack = False
            restore(var, vars_changes, clauses_changes)
            return

        davis_putnam(dc_vars_with_clauses, dc_true_clauses, dc_pure_literal, dc_unit_clauses)

    else:
        davis_putnam(dc_vars_with_clauses, dc_true_clauses, dc_pure_literal, dc_unit_clauses)
        print("after dp " +str(var))

        restore(var, vars_changes, clauses_changes)
        solution.remove(var)
        backtrack = False

        dc_true_clauses = copy.deepcopy(true_clauses)
        dc_pure_literal = copy.deepcopy(pure_literal)
        dc_unit_clauses = copy.deepcopy(unit_clauses)
        vars_changes = {}
        clauses_changes = []

        case_false(var, dc_true_clauses, vars_changes, clauses_changes, dc_unit_clauses)

        if backtrack:
            backtrack = False
            restore(var, vars_changes, clauses_changes)
            return

        davis_putnam(dc_vars_with_clauses, dc_true_clauses, dc_pure_literal, dc_unit_clauses)

        backtrack = True
        print("UNSOLVED")
        return


def restore(var, vars_changes, clauses_changes):
    # print("restore")
    # print(clauses_changes)
    # print(vars_changes)
    for vari in vars_changes:
        for c in vars_changes[vari]:
            vars[vari].append(c)

    opp = opposite_var(var)
    for clause in clauses_changes:
        clauses[clause].append(opp)


def case_false(var, dc_true_clauses, vars_changes, clauses_changes, unit_clauses):
    global backtrack
    var_clauses = vars[var]

    print("Case False")

    print("var_clauses " + str(var_clauses))

    for clause in var_clauses:
        if clause not in dc_true_clauses:

            # print(clause)
            # print(clauses[clause])
            clauses[clause].remove(var)
            clauses_changes.append(clause)

            if var == '118':
                print("clause of 118 " + str(clause))
                print("len clause " + str(len(clauses[clause])))

            if len(clauses[clause]) == 1:
                unit_clauses.append(clause)

            elif len(clauses[clause]) == 0:
                backtrack = True
                return

    opp_var = opposite_var(var)
    var_clauses = vars[opp_var]

    for clause in var_clauses:
        if clause not in dc_true_clauses:

            dc_true_clauses.append(clause)

            clause_variables = clauses[clause]
            for variable in clause_variables:
                # if variable == '-112':
                #     print("vars[variable] of -112 "+str(vars[variable]) +" "+str(clause))
                vars[variable].remove(clause)

                if variable not in vars_changes:
                    var_clau = []
                    var_clau.append(clause)
                    vars_changes[variable] = var_clau
                else:
                    vars_changes[variable].append(clause)

    is_solved(dc_true_clauses)



def case_true(var, dc_true_clauses, vars_changes, dc_pure_literal, clauses_changes, unit_clauses):
    global backtrack
    var_clauses = vars[var]

    for clause in var_clauses:
        if clause not in dc_true_clauses:
            dc_true_clauses.append(clause)

            clause_variables = clauses[clause]
            for variable in clause_variables:
                vars[variable].remove(clause)

                if variable not in vars_changes:
                    var_clau = []
                    var_clau.append(clause)
                    vars_changes[variable] = var_clau
                else:
                    vars_changes[variable].append(clause)

                if len(vars[variable]):
                    opp_var = opposite_var(variable)
                    dc_pure_literal.append(opp_var)

    is_solved(dc_true_clauses)

    opp_var = opposite_var(var)
    clauses_opp_var = vars[opp_var]
    print("opp_var "+str(opp_var))
    print("clauses_opp_var "+str(clauses_opp_var))

    for clause in clauses_opp_var:
        if clause not in dc_true_clauses:
            print("clause "+str(clause))
            print("clauses[clause] "+str(clauses[clause]))
            clauses[clause].remove(opp_var)
            clauses_changes.append(clause)

            if len(clauses[clause]) == 1:
                unit_clauses.append(clause)

            elif len(clauses[clause]) == 0:
                backtrack = True
                return


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


davis_putnam(vars_with_clauses, true_clauses, pure_literal, unit_clauses)