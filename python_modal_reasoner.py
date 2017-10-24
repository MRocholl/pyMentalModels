#! /usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import sympy
# from sympy.logic.boolalg import Not, Or, And, Xor, Implies, BooleanFunction, truth_table
from sympy.logic.boolalg import *
from sympy.core.sympify import sympify


from pyMentalModels.parsing.modal_parser import parse_expr, sympify_formatter
from pyMentalModels.logical_connectives.operators import explicit_op, intuit_op
from pyMentalModels.logical_connectives.custom_logical_classes import MulXor
from pyMentalModels.reasoner.sympy_reasoner import reasoner, satisfiying_variable_assignments, generate_possible_models


premises = ["~A | B"]
explicit = False

if not explicit:
        sympy.boolalg.Implies = sympy.boolalg.And
        operators = intuit_op
else:
    operators = explicit_op
all_possible_models = []
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

    premise_possible_models = generate_possible_models(expr, explicit)
    print(premise_possible_models)
    # print("Extracted possible world for premise {}:\t ".format(i), premise_possible_models, "\n")
    # all_possible_models.append(premise_possible_models)
print("Resulting possible worlds for all premises: ", all_possible_models)

# activate reasoner based on the possible worlds generated based on the premises
conclusion = reasoner(all_atoms, all_possible_models)
if conclusion:
    print("It follows that: ", conclusion)
else:
    print("Nothing follows")
