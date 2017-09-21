#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

""" File that collects numpy logic for mental model reasoner """

# XXX Keep track of variable names. i.e. ((A | B) and A)
# XXX Combine functions into recursive structure
# XXX Get rid of boilerplate code


import numpy as np

from sympy.logic.boolalg import And, Or, sympify, truth_table
from sympy.core.symbol import Symbol

from parsing.modal_parser import parse_expr
from itertools import product
from pyMentalModels.utils.utils import satisfiying_variable_assignments

# In case I will not use sympy at all and work directly on the parse_array
or_example = parse_expr("(A ^ B ^ C) & D")
print(or_example)


ex = sympify("A|B|C")
atoms = ex.atoms()

#  Numpy stuff {{{ #

var_ind_map = dict(enumerate(sorted(atoms, key=str)))
print(var_ind_map)


def build_or(array_or_exp):
    if isinstance(array_or_exp, Or):
        if all(isinstance(el, Symbol) for el in array_or_exp.args):
            or_args = array_or_exp.args
            print("These are the arguments:", or_args)
            nr_args = len(or_args)
            pos_valuations = [x for x in product(range(2), repeat=nr_args)][1:]
            or_array = np.asarray(sorted(pos_valuations, key=_increasing_ones_first_sort))
            return or_array

    if isinstance(array_or_exp, np.ndarray):
        print("Looks like an array to me!")

        and_array = np.ones((len(array_or_exp), len(array_or_exp[0]) + 1))
        and_array[:, :-1] = or_array
        return and_array


def build_and(array_or_exp):
    if isinstance(array_or_exp, np.ndarray):
        print("Looks like an array to me!")

        and_array = np.ones((len(array_or_exp), len(array_or_exp[0]) + 1))
        and_array[:, :-1] = or_array
        return and_array

    elif isinstance(array_or_exp, And):
        print("I think not! Its something logical!")
        # Check if everything is a Symbol
        arguments = array_or_exp.args
        if all(isinstance(el, Symbol) for el in arguments):
            return np.ones(len(array_or_exp.atoms()))
    else:
        raise ValueError("Never seen this animal before!")


def build_xor(array_or_exp):
    if isinstance(array_or_exp, np.ndarray):
        print("Looks like an array to me!")

        and_array = np.ones((len(array_or_exp), len(array_or_exp[0]) + 1))
        and_array[:, :-1] = or_array
        return and_array

    elif isinstance(array_or_exp, And):
        print("I think not! Its something logical!")
        # Check if everything is a Symbol
        arguments = array_or_exp.args
        if all(isinstance(el, Symbol) for el in arguments):
            return np.ones(len(array_or_exp.atoms()))
    else:
        raise ValueError("Never seen this animal before!")


#  }}} Numpy stuff #
def _increasing_ones_first_sort(array_slice):
                pos_of_ones = [-array_slice[i] for i, _ in enumerate(array_slice)]
                return array_slice.count(1), pos_of_ones



""" Below lay tests """
print(np.array(sorted(satisfiying_variable_assignments(truth_table(ex, ex.atoms())), key=_increasing_ones_first_sort)))

or_array = build_or(ex)

new_array = np.ones((len(or_array), 4))
new_array[:, :-1] = or_array
print(new_array)
print(build_and(sympify("A & B")))
print(build_and(or_array))
