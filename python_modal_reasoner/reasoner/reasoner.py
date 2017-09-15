#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

"""
    Different approaches to the modal reasoning problem

    1) Populate numpy dependent on logical rules given.
       This does not use the in-build functionality of sympy to evaluate logical
       connectives when substituting symboloics by valuations

    2) Populate numpy arrays on the basis of the truth table results returned
       by the sympy function `truth_table`

    3) ...

"""


from sympy.logic.boolalg import And, Xor, Implies, Or, sympify
from itertools import combinations

import numpy as np

def populate_np_array(sympified_expr):
    # XXX might not be necessary anymore if sympy takes care of this
    """ Takes sympified expression and populates n-dimensional array

        initialize numpy array of right dimensionality D = |Atoms|

    Idea: Traverse sympy expression recursively and broadcast model according to the logical rule

    Parameters
    ----------
    sympified_expr : Logical Instance of the usual logical operators


    Example
    -------

    >>> populate_np_array()


    Returns
    -------
    possible_worlds: n-dimensional array

    """
    sorted_atoms = list(sympified_expr.atoms())
    nr_atoms = len(sorted_atoms)
    print(type(sympified_expr))
    if isinstance(sympified_expr, Xor):
        possible_worlds = np.identity(nr_atoms, dtype=np.int8)
        print(sorted_atoms)
        combs = list(combinations(range(nr_atoms), 2))

        # The following will only work for symmetric relations
        for first_at, second_at in combs:

            """Do bit by bit combinations of the logical xor operation"""
            possible_worlds[first_at, second_at] = np.bitwise_xor(possible_worlds[first_at, first_at],
                                                                  possible_worlds[second_at, second_at])
    if isinstance(sympified_expr, And):
        possible_worlds = np.array([1 for _ in range(nr_atoms)])

    if isinstance(sympified_expr, Or):
        possible_worlds = np.identity(nr_atoms, dtype=np.int8)
        combs = list(combinations(range(nr_atoms), 2))

        # The following will only work for symmetric relations
        for first_at, second_at in combs:
            """Do bit by bit combinations of the logical or operation"""
            possible_worlds[first_at, second_at] = np.bitwise_or(possible_worlds[first_at, first_at],
                                                                 possible_worlds[second_at, second_at])
    if isinstance(sympified_expr, Implies):
        raise NotImplementedError("Did not implement `Implies` yet")


    modal_possible = dict(zip(sorted_atoms, np.any(possible_worlds, axis=1)))
    modal_necessary = dict(zip(sorted_atoms, np.all(possible_worlds, axis=1)))
    return modal_possible, modal_necessary, possible_worlds


def OR():
    """TODO: Docstring for OR.
    Returns
    -------
    TODO

    """
    pass


_, _, possible_world = populate_np_array(sympify("Or(A, B, C)"))

print(possible_world)








