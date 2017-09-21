#! /usr/bin/python3
# -*- coding: iso-8859-15 -*-

import numpy as np
import sympy
# from sympy.logic.boolalg import Not, Or, And, Xor, Implies, BooleanFunction, truth_table
from sympy.logic.boolalg import *
from sympy.core.sympify import sympify


from pyMentalModels.parsing.modal_parser import parse_expr, sympify_formatter
from pyMentalModels.logical_connectives.operators import op_names, intuit_op
from pyMentalModels.logical_connectives.custom_logical_classes import MyXor
from pyMentalModels.reasoner.sympy_reasoner import reasoner, satisfiying_variable_assignments, possible_worlds


premises = ["A -> (B | C)"]
explicit = False

if not explicit:
        sympy.boolalg.Implies = sympy.boolalg.And
        operators = intuit_op
else:
    operators = op_names
all_possible_worlds = []
all_atoms = []
for i, premise in enumerate(premises):
    # XXX preprocess strings to substitute "<>" biconditional through "&" if intutitive \
    # or "Equals()" if --explicit

    formated_premise = sympify_formatter(parse_expr(premise), operators)
    print(formated_premise)
    expr = sympify(formated_premise, locals={})
    atoms = sorted(expr.atoms(), key=str)
    print("Epression being evaluated is:\t\t", expr)
    print(atoms)
    print(np.asarray(list(satisfiying_variable_assignments(truth_table(expr, atoms)))))
    premise_possible_worlds = possible_worlds(atoms, truth_table(expr, atoms), explicit)
    print(premise_possible_worlds)
    # print("Extracted possible world for premise {}:\t ".format(i), premise_possible_worlds, "\n")
    # all_possible_worlds.append(premise_possible_worlds)
print("Resulting possible worlds for all premises: ", all_possible_worlds)

# activate reasoner based on the possible worlds generated based on the premises
conclusion = reasoner(all_atoms, all_possible_worlds)
if conclusion:
    print("It follows that: ", conclusion)
else:
    print("Nothing follows")
