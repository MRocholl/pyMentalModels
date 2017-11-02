#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-


# TODO Time to wrap the following into a class
"""
    Different approaches to the modal reasoning problem

    1) Populate numpy dependent on logical rules given.
       This does not use the in-build functionality of sympy to evaluate logical
       connectives when substituting symboloics by valuations

    2) Populate numpy arrays on the basis of the truth table results returned
       by the sympy function `truth_table`

    3) ...

"""

from sympy.logic.boolalg import And, Xor, Implies, Or, Not, sympify
from sympy.core.symbol import Symbol

import numpy as np

explicit_negated_atoms = set([])

# def sympify_formatter(args, rules):
#     """
#     Formatting function to make the parsed list sympify-readable
#     For sympify refer to:  http://docs.sympy.org/latest/modules/core.html
#
#     """
#     if len(args) == 1 or isinstance(args, str):
#         return "{}".format(args)
#     if len(args) == 2:
#         op, arg = args
#         return "{}({})".format(rules[op], sympify_formatter(arg, rules))
#     if len(args) >= 3:
#         op = rules[args[1]]
#         arguments = (sympify_formatter(expr, rules) for expr in args[::2])
#         # Sympify takes general form of Operator(#args > 2)
#         return "{operator}({f_args})".format(operator=op,
#                                              f_args=", ".join(arguments))


def populate_np_array(sympified_expr, logical_connective):
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

    print(logical_connective)
    sorted_atoms = list(sympified_expr.atoms())
    nr_atoms = len(sympified_expr.args)
    var_ind_map = {atom: i for i, atom in enumerate(sorted(sympified_expr.atoms(), key=str))}
    ind_var_map = dict(enumerate(sorted(sympified_expr.atoms(), key=str)))

    def _preprocessed_args(argumentlist):
        all_symbols = True
        out_arg_list = []
        for arg in argumentlist:
            if not isinstance(arg, Symbol) and not isinstance(arg, Not):
                all_symbols = False
            if isinstance(arg, Not):
                if isinstance(arg.args[0], Symbol):
                    explicit_negated_atoms.add(arg.args[0])
                    out_arg_list.append(arg.args[0])
            else:
                out_arg_list.append(arg)

        return all_symbols, out_arg_list

    def _replace_expl_neg(possible_models):
                for el in explicit_negated_atoms:
                    possible_models[:, var_ind_map[el]] = 2
                return possible_models

    if not isinstance(sympified_expr, np.ndarray):
        all_symbols, arguments = _preprocessed_args(sympified_expr.args)
        if isinstance(sympified_expr, Not):
            if isinstance(sympified_expr.args[0], Symbol):
                explicit_negated_atoms.add(sympified_expr.args[0])
                possible_models = sympified_expr.args[0]
                return possible_models

        if isinstance(sympified_expr, Xor):
            if all_symbols:
                possible_models = np.identity(nr_atoms, dtype=np.int8)
                return _replace_expl_neg(possible_models)

        if isinstance(sympified_expr, And):
            if all_symbols:
                possible_models = np.array([[1 for _ in range(nr_atoms)]])
                return _replace_expl_neg(possible_models)

        if isinstance(sympified_expr, Or):
            if all_symbols:
                possible_models = np.identity(nr_atoms, dtype=np.int8)
                return _replace_expl_neg(possible_models)

        if isinstance(sympified_expr, Implies):
            if all(isinstance(arg, Symbol) for arg in sympified_expr.args):
                raise NotImplementedError("Did not implement `Implies` yet")
    if isinstance(sympified_expr, np.ndarray):
        pass


def test_example(expression):
    sympified_expr = sympify(expression)
    print(sympify(expression).args)
    raw_numeric_model = populate_np_array(sympified_expr, type(sympified_expr)).tolist()
    print(raw_numeric_model)
    def str_model(raw_numeric_model):
        ind_var_map = dict(enumerate(sorted(sympified_expr.atoms(), key=str)))
        pretty_model = []
        for model in raw_numeric_model:
            new_model = []
            for i, value in enumerate(model):
                new_model.append(str(ind_var_map[i])) if value == 1 else new_model.append("~{}".format(ind_var_map[i])) if value == 2 else new_model.append("")
            pretty_model.append(new_model)
        return pretty_model
    print(str_model(raw_numeric_model))

test_example("A | ~A")
# modal_possible = dict(zip(sorted_atoms, np.any(possible_models, axis=1)))
# modal_necessary = dict(zip(sorted_atoms, np.all(possible_models, axis=1)))
