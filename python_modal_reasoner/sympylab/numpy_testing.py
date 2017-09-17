#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from sympy.logic.boolalg import And, Or, Xor, sympify, truth_table
from sympy.core.symbol import Symbol
import numpy as np
from itertools import product

or_example = sympify("Xor(A, B) | C")


print(type(or_example))
print(or_example.args)
for el in or_example.args:
    a = type(el)
    print(type(el) == a)


def satisfiying_variable_assignments(truth_table):
    """yields the truth_table entries with valuation True (Principle of Truth)"""
    from collections import namedtuple
    TruthTableEntry = namedtuple("TruthTableEntry", ["assignment", "valuation"])
    yield from (variable_assignment for variable_assignment, _ in filter(lambda result: TruthTableEntry(*result).valuation, truth_table))


def build_or(or_exp):
    or_args = or_exp.args
    print("These are the arguments:", or_args)
    nr_args = len(or_args)

    def increasing_ones_first_sort(array_slice):
        pos_of_ones = [-array_slice[i] for i in range(nr_args)]
        return array_slice.count(1), pos_of_ones

    pos_valuations = [x for x in product(range(2), repeat=nr_args)][1:]

    or_array = np.asarray(sorted(pos_valuations, key=increasing_ones_first_sort))
    return or_array


a = sympify("A|B|C")


print(list(satisfiying_variable_assignments(truth_table(a, a.atoms()))))
or_array = build_or(a)


def build_and(array_or_exp):
    if isinstance(array_or_exp, np.array):
        print("Looks like an array to me!")
        and_array = np.ones((len(or_array), 4))
        and_array[:, :-1] = or_array
        return and_array

    elif isinstance(array_or_exp, (And, Or, Xor)):
        print("I think not! Its something logical!")
        # Check if everything is a Symbol
        if all(isinstance(el, Symbol) for el in array_or_exp):
            return np.ones(len(array_or_exp.atoms()))
    else:
        raise ValueError("Never seen this animal before!")


new_array = np.ones((len(or_array), 4))
new_array[:, :-1] = or_array
print(new_array)

for line in or_array:
    print(line)




