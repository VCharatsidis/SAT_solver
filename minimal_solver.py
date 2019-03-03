import time
from collections import Counter


def __select_literal(cnf):
    # if exists unit clause use this
    unit_clauses = [c for c in cnf if len(c) == 1]

    for c in unit_clauses:
        for literal in c:
            return literal[0]

    #Check for pure literals
    var_counts = Counter()
    for c in cnf:
        for pred in c:
            if pred[1]:
                var_counts[pred[0]] += 1
            else:
                var_counts[-pred[0]] += 1

    for v in variables:
        if v in var_counts and (var_counts[v] == 0 or var_counts[-v] == 0):
            return v


    # find most constrained variable heuristic
    var = max(variables, key=lambda x: var_counts[x])
    return var

    # clause length heuristic
    unit_clauses = [c for c in cnf if len(c) == 3]

    for c in unit_clauses:
        for literal in c:
            return literal[0]

    # find biggest clause and use this
    unit_clauses = max(cnf, key=len)
    for c in unit_clauses:
        return c[0]

    for c in cnf:
        for literal in c:
            return literal[0]

rec_calls = 0
min_clauses_left = 1E6


def dpll(cnf, assignments={}):
    global rec_calls
    global min_clauses_left
    rec_calls += 1
    min_clauses_left = min(min_clauses_left, len(cnf))
    if rec_calls % 1000 == 0:
        print(str(rec_calls) + ' ' + str(len(assignments)) + ' clauses_left: ' + str(len(cnf)) + ' min_clauses_left: ' + str(min_clauses_left))

    if len(cnf) == 0:
        return True, assignments

    if any([len(c) == 0 for c in cnf]):
        return False, None

    literal = __select_literal(cnf)

    new_cnf = [c for c in cnf if (literal, True) not in c]
    new_cnf = [c.difference({(literal, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{literal: True}})
    if sat:
        return sat, vals

    new_cnf = [c for c in cnf if (literal, False) not in c]
    new_cnf = [c.difference({(literal, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{literal: False}})
    if sat:
        return sat, vals

    return False, None


def read_sudoku(filename):
    with open(filename) as f:
        sudoku = f.readlines()
    return [x.strip() for x in sudoku]


def read_rules(filename):
    with open(filename) as f:
        rules = f.readlines()
    rules = rules[1:]
    return [x.strip() for x in rules]


def make_cnf(rules):
    cnf = []
    for rule in rules:
        clause = set()
        rule_preds = rule.split(' ')[:-1]
        for pred in rule_preds:
            if pred.startswith('-'):
                tup = (int(pred[1:]), False)
                clause.add(tup)
            else:
                tup = (int(pred), True)
                clause.add(tup)
        cnf.append(clause)
    return cnf


def draw_sudoku(solution):
    simplified_sol = []
    for key in solution:
        if solution[key] == True:
            simplified_sol.append(key)

    one = []
    two = []
    three = []
    four = []
    five = []
    six = []
    seven = []
    eight = []
    nine = []
    print(simplified_sol)
    simplified_sol.sort
    for square in simplified_sol:
        if str(square)[0] == '1':
            one.append(str(square))
        elif str(square)[0] == '2':
            two.append(str(square))
        elif str(square)[0] == '3':
            three.append(str(square))
        elif str(square)[0] == '4':
            four.append(str(square))
        elif str(square)[0] == '5':
            five.append(str(square))
        elif str(square)[0] == '6':
            six.append(str(square))
        elif str(square)[0] == '7':
            seven.append(str(square))
        elif str(square)[0] == '8':
            eight.append(str(square))
        elif str(square)[0] == '9':
            nine.append(str(square))

    print(one)
    print(two)
    print(three)
    print(four)
    print(five)
    print(six)
    print(seven)
    print(eight)
    print(nine)




# rules = read_rules("biggerTest.txt")
rules = read_rules("rules.txt")
rules = read_sudoku("hardest.txt") + rules
print(len(rules))

print(rules)
cnf = make_cnf(rules)
variables = set(p[0] for c in cnf for p in c)
print(cnf)

start = time.time()
solved, solution = dpll(cnf)
print('\nsolution: ' + str(solved))
stop = time.time()
time_taken = stop - start
print(time_taken)

draw_sudoku(solution)