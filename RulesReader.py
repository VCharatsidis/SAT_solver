
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

true_clauses = []
defined_variables = []
pure_literal = []
unit_clauses = []
available_vars = []

for key in vars:
    available_vars.append(key)

backtrack = False

def davis_putnam(true_clauses, defined_variables, pure_literal, unit_clauses, available_vars):
    nonlocal backtrack
    dc_true_clauses = []
    dc_true_clauses.deepcopy(true_clauses)

    dc_defined_variables = []
    dc_defined_variables.deepcopy(defined_variables)

    dc_pure_literal = []
    dc_pure_literal.deepcopy(pure_literal)

    dc_unit_clauses = []
    dc_unit_clauses.deepcopy(unit_clauses)

    dc_available_vars = []
    dc_available_vars.deepcopy(available_vars)

    if len(dc_unit_clauses) > 0:
        var = clauses[dc_unit_clauses[0]][0]
        dc_available_vars.remove(var)
        dc_defined_variables.append(var)
        dc_unit_clauses.remove(dc_unit_clauses[0])
        set_variable_true(var, dc_true_clauses, dc_defined_variables, dc_pure_literal, dc_unit_clauses, dc_available_vars)
        davis_putnam(dc_true_clauses, dc_defined_variables, dc_pure_literal, dc_unit_clauses, dc_available_vars)

        if backtrack:
            backtrack = False
            opp_var = opposite_var(var)
            available_vars.remove(opp_var)
            defined_variables.append(opp_var)
            unit_clauses.remove(dc_unit_clauses[0])
            set_variable_true(opp_var, true_clauses, defined_variables, pure_literal, unit_clauses, available_vars)
            davis_putnam(true_clauses, defined_variables, pure_literal, unit_clauses, available_vars)

    if len(dc_pure_literal) > 0:
        var = dc_pure_literal[0]
        dc_available_vars.remove(var)
        dc_defined_variables.append(var)
        dc_pure_literal.remove(dc_pure_literal[0])
        set_variable_true(var, dc_true_clauses, dc_defined_variables, dc_pure_literal, dc_unit_clauses, dc_available_vars)
        davis_putnam(dc_true_clauses, dc_defined_variables, dc_pure_literal, dc_unit_clauses, dc_available_vars)

        if backtrack:
            backtrack = False
            opp_var = opposite_var(var)
            available_vars.remove(opp_var)
            defined_variables.append(var)
            pure_literal.remove(dc_pure_literal[0])
            set_variable_true(opp_var, true_clauses, defined_variables, pure_literal, unit_clauses, available_vars)
            davis_putnam(true_clauses, defined_variables, pure_literal, unit_clauses, available_vars)

    if len(dc_available_vars) > 0:
        var = dc_available_vars[0]
        dc_available_vars.remove(var);
        dc_defined_variables.append(var)
        set_variable_true(var, dc_true_clauses, dc_defined_variables, dc_pure_literal, dc_unit_clauses, dc_available_vars)
        davis_putnam(dc_true_clauses, dc_defined_variables, dc_pure_literal, dc_unit_clauses, dc_available_vars)

        if backtrack:
            backtrack = False
            opp_var = opposite_var(var)
            defined_variables.append(var)
            available_vars.remove(opp_var)
            set_variable_true(opp_var, true_clauses, defined_variables, pure_literal, unit_clauses, available_vars)
            davis_putnam(true_clauses, defined_variables, pure_literal, unit_clauses, available_vars)



def set_variable_true(var, true_clauses, defined_variables, pure_literal, unit_clauses, available_vars):
    for clause in vars[var]:
        true_clauses.append(clause)
        is_solved(true_clauses)

        for variable in clauses[clause]:
            vars[variable].remove(clause)
            if len(vars[variable]) == 0:
                opp_variable = opposite_var(variable)
                pure_literal.append(opp_variable)
                defined_variables.append(variable)

    opp_var = opposite_var(var)
    handle_opposite_var(opp_var)
    defined_variables.append(opp_var)


def handle_opposite_var(opposite_var):
    nonlocal backtrack
    for clause in vars[opposite_var]:
        clauses[clause].remove(opposite_var)

        if not clauses[clause]:
            backtrack = True

        elif len(clauses[clause]) == 1:
            unit_clauses.append(clause)


def opposite_var(var):
    if var in normal_vars:
        opp_var = '-' + var
    else:
        opp_var = var[1:]

    return opp_var


def is_solved(true_clauses):
    if len(true_clauses) == total_clauses:
        print("PROBLEM SOLVED!!!")



