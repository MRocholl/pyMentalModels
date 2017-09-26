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

from sympy.logic.boolalg import And, Xor, Implies, Or
from sympy.core.symbol import Symbol

import numpy as np


def populate_np_array(sympified_expr):
    # XXX might not be necessary anymore if sympy takes care of this
    # XXX Need to fuse this function with the different logical
    #     numpy constructurs
    """ Takes sympified expression and populates n-dimensional array

        initialize numpy array of right dimensionality D = |Atoms|

    Idea: Traverse sympy expression recursively and broadcast model
          according to the logical rule

    Parameters
    ----------
    sympified_expr : Logical Instance of the usual logical operators


    Example
    -------
    >>> populate_np_array()


    Returns
    -------
    possible_models: n-dimensional array

    """

    sorted_atoms = list(sympified_expr.atoms())
    nr_atoms = len(sorted_atoms)

    if isinstance(sympified_expr, Xor):
        if all(isinstance(arg, Symbol) for arg in sympified_expr.args):
            possible_models = np.identity(nr_atoms, dtype=np.int8)

    if isinstance(sympified_expr, And):
        if all(isinstance(arg, Symbol) for arg in sympified_expr.args):
            possible_models = np.array([1 for _ in range(nr_atoms)])

    if isinstance(sympified_expr, Or):
        if all(isinstance(arg, Symbol) for arg in sympified_expr.args):
            possible_models = np.identity(nr_atoms, dtype=np.int8)

    if isinstance(sympified_expr, Implies):
        if all(isinstance(arg, Symbol) for arg in sympified_expr.args):
            raise NotImplementedError("Did not implement `Implies` yet")

    modal_possible = dict(zip(sorted_atoms, np.any(possible_models, axis=1)))
    modal_necessary = dict(zip(sorted_atoms, np.all(possible_models, axis=1)))
    return modal_possible, modal_necessary, possible_models
