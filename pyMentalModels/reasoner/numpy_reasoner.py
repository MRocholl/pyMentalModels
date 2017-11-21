#!/usr/bin/python3
""" File that collects numpy logic for mental model reasoner """

import numpy as np
from itertools import product, combinations
from sympy.logic.boolalg import (And, Or, Xor, Not, Implies, Equivalent)
from sympy.core.symbol import Symbol

#######################################################################
#                            Notes to self                            #
#######################################################################

"""

Addinf to models together happens in function of the upper level operator
I.e. And(OR...Or....Xor...) first creates models for OR....Or...and Xor...
before merging them together based on the behavior of the `And`-operator

For And this is a not so interesting case as the all the models have to keep true

For Or, Xor, Imply the case is different as all of them have models where one part of the model
is allowed to be false or not represented


The implementation here for `Or` first adds each model to the merged_model
and adds all the models together like the `And` operator does.
Hence, the `OR` operator acts quite like a combination of both the `Xor`
and And operator for all subexpressions piecewise and total.
    For (A & B) or (C & D) or (E xor F)
    with (A & B):= Arg1, (C & D):=2, etc...

    The Model is:
    -------------
    Arg1 xor Arg2 xor Arg3  // This is just a vstack
    Arg1 & Arg2             // Piecewise addition
    Arg2 & Arg3             //      ""
    Arg1 & Arg2 & Arg3      // Addition of all three
    ========================
    Stacked from top to bottom

The implementation for the material implication `Implies` is not quite clear yet
The staight-forward way would be to duck-type it to the `And` behavior.



The problem child `Not`

The builder catches Nots as not being a symbol and will eventually try to
construct a model of a `Not(Atom)` or `Not(sub_expr)`

Examples of this behaviour would be:

    Not(A) or B             | (A | B) & ~(C | D) // Crete full model
                            |                    // and take complement
    Result should be:       | Result should be:
                            |                            |  C
    ~A                      |   A       ~C  ~D <-- from  |      D
        B                   |       B   ~C  ~D           |  C   D
    ~A  B                   |This does look probelmatic.

Hence, an explicit `Not` in the expression will lead to an explicit `Not`
representation in the final model.
There seems to be a big difference in the semantic importance between the
negation of an atom and the negation of a subexpression.


"""


def mental_model_builder(sympified_expr):
    """
    Builds a mental model representation of the logical expression.

    A Mental model is a mental representation of a logical or indeed any expression.
    An example would be the expression:

        You have either the salad or the soup or the bread

    The mental model representation would then be:

                    Salad
                            Soup
                                    Bread

    `mental_model_builder` recursively builds models of the subexpressions of
    the total expression, merges them and returns the overall mental model
    representation of the expression

    Parameters
    ----------
    sympified_expr: sympy BooleanFunction
        An expression formatted and processed by the `sympy` python module
        Attributes:
            expression.atoms
                Set of all the atoms in the logical expression
            expression.args
                Tuple of arguments the outermost logical operator takes

    Returns
    -------
    Mental model representation of logical expression

    """
    # Extract atoms from sympified expression
    exp_atoms = sympified_expr.atoms()

    # map every atom to its corresponding index in the model
    atom_index_mapping = {atom: i for i, atom in enumerate(sorted(exp_atoms, key=str))}

    return map_instance_to_operation(sympified_expr)(sympified_expr, atom_index_mapping, exp_atoms)


def _merge_models(*sub_models, op):
    """
    Merges the different subexpressions together.
    Implements merging for operator `And`, `Or`, `Xor`

    Parameters
    ----------
    sub_models: List of arbitrary number of sub_models
        subexpressions to be merged together
    """
    assert(len(sub_models)) >= 2

    if op == "And":
        iter_models = iter(sub_models)
        merged_models = next(iter_models)
        for model in iter_models:
            reshaped_merged_models = np.repeat(merged_models, len(model), axis=0)
            reshaped_model2 = np.tile(model, (len(merged_models), 1))
            merged_models = reshaped_merged_models + reshaped_model2
        return merged_models

    if op == "Xor":
        iter_models = iter(sub_models)
        merged_models = next(iter_models)
        for model in iter_models:
            merged_models = np.vstack((merged_models, model))
        return merged_models

    if op == "Or":
        # first xor everything
        xor_models = _merge_models(*sub_models, op="Xor")

        merged_models = xor_models
        # then piecewise and everything
        list_of_piecewise_ands = [
            _merge_models(*comb, op="And")
            for comb in combinations(sub_models, 2)
        ]
        for el in list_of_piecewise_ands:
            merged_models = np.vstack((merged_models, el))

        # then total and everything
        and_everything = _merge_models(*sub_models, op="And")

        merged_models = np.vstack((merged_models, and_everything))

        return merged_models


def map_instance_to_operation(el):
    "maps every instance to its builder function."
    maps = iter((
        (Or, build_or),
        (And, build_and),
        (Xor, build_xor),
        (Not, build_not),
        (Implies, build_and),
        (Equivalent, build_and),
    ))
    try:
        return next(builder for type_, builder in maps if isinstance(el, type_))
    except StopIteration:
        raise ValueError("Not a valid operator")


def build_or(exp, atom_index_mapping, exp_atoms):

    assert(isinstance(exp, Or))

    or_args = exp.args
    nr_args = len(or_args)

    if all(isinstance(el, Symbol) for el in exp.args):
        pos_valuations = [x for x in product(range(2), repeat=nr_args)][1:]
        pos_valuations = sorted(pos_valuations, key=_increasing_ones_first_sort)
        or_model = np.zeros((len(pos_valuations), len(exp_atoms)))
        or_model[
            :, list(map(lambda x: atom_index_mapping[x], or_args))
        ] = pos_valuations
        return or_model
    else:
        symbol_list = []
        subexpression_list = []
        for el in exp.args:
            if isinstance(el, Symbol):
                symbol_list.append(el)
            else:
                subexpression_list.append(el)

        # generate submodels from subexpressions
        modelized_subexpressions = [
            map_instance_to_operation(subexpression)(subexpression, atom_index_mapping, exp_atoms)
            for subexpression in subexpression_list
        ]

        # Create `or` model for the symbols
        if symbol_list:
            pos_valuations = [x for x in product(range(2), repeat=len(symbol_list))][1:]
            pos_valuations = sorted(pos_valuations, key=_increasing_ones_first_sort)
            or_model = np.zeros((len(pos_valuations), len(exp_atoms)))
            or_model[
                :, list(map(lambda x: atom_index_mapping[x], symbol_list))
            ] = pos_valuations
            modelized_subexpressions.append(or_model)

        # merge the generated submodels to an overall model of `And`
        merged_sub_models = _merge_models(*modelized_subexpressions, op="Or")
        return merged_sub_models


def build_and(exp, atom_index_mapping, exp_atoms):

    assert(isinstance(exp, (And, Implies, Equivalent)))

    and_args = exp.args

    if all(isinstance(el, Symbol) for el in and_args):
        and_model = np.zeros((1, len(exp_atoms)))
        and_model[
            :, list(map(lambda x: atom_index_mapping[x], and_args))
        ] = 1.
        return and_model
    else:
        symbol_list = []
        subexpression_list = []
        for el in exp.args:
            if isinstance(el, Symbol):
                symbol_list.append(el)
            else:
                subexpression_list.append(el)
        # generate submodels from subexpressions
        modelized_subexpressions = [
            map_instance_to_operation(subexpression)(subexpression, atom_index_mapping, exp_atoms)
            for subexpression in subexpression_list
        ]
        # Create `and` model for the symbols
        if symbol_list:
            and_model = np.zeros((1, len(exp_atoms)))
            and_model[
                :, list(map(lambda x: atom_index_mapping[x], symbol_list))
            ] = 1.
            modelized_subexpressions.append(and_model)

        # merge the generated submodels to an overall model of `And`
        merged_sub_models = _merge_models(*modelized_subexpressions, op="And")
        return merged_sub_models


def build_xor(exp, atom_index_mapping, exp_atoms):

    assert(isinstance(exp, Xor))

    xor_args = exp.args
    nr_xor_args = len(xor_args)

    if all(isinstance(el, Symbol) for el in exp.args):
        xor_model = np.zeros((nr_xor_args, len(exp_atoms)))
        xor_model[
            :, list(map(lambda x: atom_index_mapping[x], xor_args))
        ] = np.eye(nr_xor_args)
        return xor_model
    else:
        symbol_list = []
        subexpression_list = []
        for el in exp.args:
            if isinstance(el, Symbol):
                symbol_list.append(el)
            else:
                subexpression_list.append(el)

        modelized_subexpressions = [
            map_instance_to_operation(subexpression)(subexpression, atom_index_mapping, exp_atoms)
            for subexpression in subexpression_list
        ]

        if symbol_list:
            xor_model = np.zeros((len(symbol_list), len(exp_atoms)))
            xor_model[
                :, list(map(lambda x: atom_index_mapping[x], symbol_list))
            ] = np.eye(len(symbol_list))
            modelized_subexpressions.append(xor_model)

        # Create `xor` model for the symbols
        merged_sub_models = _merge_models(*modelized_subexpressions, op="Xor")
        return merged_sub_models


def build_not(exp, atom_index_mapping, exp_atoms):
    neg_arg = exp.args[0]
    assert isinstance(exp, Not)
    if isinstance(neg_arg, Symbol):
        not_model = np.zeros([1, len(exp_atoms)])
        not_model[
            0, atom_index_mapping[neg_arg]
        ] = -1.
        return not_model
    else:
        model_positive = map_instance_to_operation(neg_arg)(neg_arg, atom_index_mapping, exp_atoms)
        raise NotImplementedError(
            " Did not implement Negation of sub-expression yet. "
        )


def _increasing_ones_first_sort(array_slice):
                pos_of_ones = [-array_slice[i] for i, _ in enumerate(array_slice)]
                return array_slice.count(1), pos_of_ones
