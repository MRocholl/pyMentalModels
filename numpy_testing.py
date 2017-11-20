#!/usr/bin/python3

""" File that collects numpy logic for mental model reasoner """

# XXX Keep track of variable names. i.e. ((A | B) and A)
# XXX Combine functions into recursive structure
# XXX Get rid of boilerplate code


import numpy as np
from itertools import product

from sympy.logic.boolalg import (And, Or, Xor, Implies, Not,
                                 sympify, truth_table)
from sympy.core.symbol import Symbol
from pyMentalModels.reasoner.sympy_reasoner import satisfiying_variable_assignments


ex = sympify("A | Xor(B , C)")
atoms = ex.atoms()

#  Numpy stuff {{{ #


def map_instance_to_operation(el):
    return {
        isinstance(el, Or): build_or,
        isinstance(el, And): build_and,
        isinstance(el, Xor): build_xor,
        isinstance(el, Implies): build_implies,
    }.get(True, ValueError("operator not valid"))


var_ind_map = dict(enumerate(sorted(atoms, key=str)))

#  Or {{{ #


def build_or(array_or_exp):

    if isinstance(array_or_exp, Or):
        if all(isinstance(el, Symbol) for el in array_or_exp.args):
            or_args = array_or_exp.args
            nr_args = len(or_args)
            pos_valuations = [x for x in product(range(2), repeat=nr_args)][1:]
            or_array = np.asarray(sorted(pos_valuations, key=_increasing_ones_first_sort))
            print(or_array)
            return or_array
        else:
            for el in array_or_exp:
                if
            submodel = map_instance_to_operation(el)(el)
            len_submodel = len(submodel)
            or_array = np.asarray([x for x in product(range(2), repeat=2)][1:])

    if isinstance(array_or_exp, np.ndarray):
        or_array = np.ones((len(array_or_exp), len(array_or_exp[0]) + 1))
        or_array[:, :-1] = array_or_exp
        return and_array
#  }}} Or #

#  And {{{ #


def build_and(array_or_exp):
    if isinstance(array_or_exp, np.ndarray):
        and_array = np.ones((len(array_or_exp), len(array_or_exp[0]) + 1))
        and_array[:, :-1] = array_or_exp
        return and_array

    elif isinstance(array_or_exp, And):
        # Check if everything is a Symbol
        arguments = array_or_exp.args
        if all(isinstance(el, Symbol) for el in arguments):
            return np.ones(len(array_or_exp.atoms()))
    else:
        raise ValueError("Never seen this animal before!")
#  }}} And #

#  Xor {{{ #


def build_xor(array_or_exp):
    if isinstance(array_or_exp, np.ndarray):
        print("Looks like an array to me!")

        and_array = np.ones((len(array_or_exp), len(array_or_exp[0]) + 1))
        and_array[:, :-1] = or_array
        return and_array

    elif isinstance(array_or_exp, Xor):
        print("I think not! Its something logical!")
        # Check if everything is a Symbol
        arguments = array_or_exp.args

        seen_not_list = []
        for el in arguments:
            if isinstance(el, Not):
                seen_not_list.append(el)
                return build_not(el)
            elif not isinstance(el, Symbol):
                return map_instance_to_operation(el)(el)

            else:
                pass

        if all(isinstance(el, Symbol) for el in arguments):
            return np.ones(len(array_or_exp.atoms()))
        if any(isinstance(el, Not) for el in arguments):
            return "Witnessed a Not at this place"
    else:
        raise ValueError("Never seen this animal before!")
#  }}} Xor #


def build_implies(array_or_exp):
    raise NotImplementedError


def build_not(array_or_exp):
    if isinstance(array_or_exp, symbol):
        return

#  }}} Numpy stuff #
def _increasing_ones_first_sort(array_slice):
                pos_of_ones = [-array_slice[i] for i, _ in enumerate(array_slice)]
                return array_slice.count(1), pos_of_ones


""" Below lay tests """
# print(np.array(sorted(satisfiying_variable_assignments(truth_table(ex, ex.atoms())), key=_increasing_ones_first_sort)))

or_array = build_or(ex)
print(or_array)
new_array = np.ones((len(or_array), 4))
new_array[:, :-1] = or_array
print(new_array)

#print("Array representation of `A & B`:")
#print(build_and(sympify("A & B")))
print("Array representation of `A | B | C`:")
print(or_array)
print("Array representation of `(A | B | C) & D`:")
print(build_and(or_array))
