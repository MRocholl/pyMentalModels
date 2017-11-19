#!/usr/bin/python3
""" File that collects numpy logic for mental model reasoner """

import numpy as np
from itertools import product, combinations
from sympy import symbols
from sympy.logic.boolalg import (And, Or, Xor, Not,
                                 )
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
and And operator for all submodels piecewise and total.
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


"""


def builder(sympified_expr):
    """
    Builds a mental model representation of the logical expression

    Parameters
    ----------
    sympified_expr: sympy BooleanFunction

    Returns
    -------
    Mental model representation of logical expression

    """
    # Extract atoms from sympified expression
    exp_atoms = sympified_expr.atoms()

    # mop every atom to its corresponding index in the model
    var_ind_map = {atom: i for i, atom in enumerate(sorted(exp_atoms, key=str))}

    def _merge_models(*sub_models, op):
        """
        Merges the different submodels together.
        This is a momentary template for the other merging functions
        Implements merging for operator `and`

        Parameters
        ----------
        sub_models: List of arbitrary #sub_models
            submodels to be merged together
        """
        print(sub_models)
        assert(len(sub_models)) >= 2

        if op == "And":
            iter_models = iter(sub_models)
            merged_models = next(iter_models)
            while True:
                try:
                    model2 = next(iter_models)
                except StopIteration:
                    break
                reshaped_merged_models = np.repeat(merged_models, len(model2), axis=0)
                reshaped_model2 = np.vstack((model2, model2))
                merged_models = reshaped_merged_models + reshaped_model2
            return merged_models
        if op == "Xor":
            iter_models = iter(sub_models)
            merged_models = next(iter_models)
            while True:
                try:
                    model2 = next(iter_models)
                except StopIteration:
                    break
                merged_models = np.vstack((merged_models, model2))
            return merged_models

        if op == "Or":

            # first xor everything
            print(len(sub_models))
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
        ))
        try:
            return next(builder for type_, builder in maps if isinstance(el, type_))
        except StopIteration:
            raise ValueError("Not a valid operator")

    def build_or(exp):

        assert(isinstance(exp, Or))

        or_args = exp.args
        nr_args = len(or_args)

        if all(isinstance(el, Symbol) for el in exp.args):
            pos_valuations = [x for x in product(range(2), repeat=nr_args)][1:]
            pos_valuations = sorted(pos_valuations, key=_increasing_ones_first_sort)
            or_model = np.empty((len(pos_valuations), len(exp_atoms)))
            or_model[
                :, list(map(lambda x: var_ind_map[x], or_args))
            ] = pos_valuations
            return or_model
        else:
            symbol_list = []
            submodel_list = []
            for el in exp.args:
                if isinstance(el, Symbol):
                    symbol_list.append(el)
                else:
                    submodel_list.append(el)

            pos_valuations = [x for x in product(range(2), repeat=len(symbol_list))][1:]
            pos_valuations = sorted(pos_valuations, key=_increasing_ones_first_sort)
            or_model = np.empty((len(pos_valuations), len(exp_atoms)))
            or_model[
                :, list(map(lambda x: var_ind_map[x], symbol_list))
            ] = pos_valuations
            # Create `or` model for the symbols
            modelized_submodels = [map_instance_to_operation(el)(el) for submodel in submodel_list]
            modelized_submodels.append(or_model)
            merged_sub_models = _merge_models(*modelized_submodels, op="Or")
            return merged_sub_models
            # len_submodel = len(submodel)
            # get all submodels
            # repeat values for first submodel as often as their are arguments for the operator

            # or_array = np.asarray([x for x in product(range(2), repeat=2)][1:])
            # or_array = np.ones((len(exp), len(exp[0]) + 1))
            # or_array[:, :-1] = exp
            return modelized_submodels

    def build_and(exp):

        assert(isinstance(exp, And))

        and_args = exp.args

        if all(isinstance(el, Symbol) for el in and_args):
            and_model = np.empty((1, len(exp_atoms)))
            and_model[
                :, list(map(lambda x: var_ind_map[x], and_args))
            ] = 1.
            return and_model

    def build_xor(exp):
        if isinstance(exp, np.ndarray):
            xor_array = np.ones((len(exp), len(exp[0]) + 1))
            xor_array[:, :-1] = exp
            return xor_array

        elif isinstance(exp, Xor):
            # Check if everything is a Symbol
            arguments = exp.args
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
                return np.ones(len(exp.atoms()))
            if any(isinstance(el, Not) for el in arguments):
                return "Witnessed a Not at this place"

    def build_not(model):
        pass

    def _increasing_ones_first_sort(array_slice):
                    pos_of_ones = [-array_slice[i] for i, _ in enumerate(array_slice)]
                    return array_slice.count(1), pos_of_ones

    return map_instance_to_operation(sympified_expr)(sympified_expr)


def _merge_models(model1, model2):
        reshaped_model1 = np.repeat(model1, len(model2), axis=0)
        reshaped_model2 = np.vstack(model2, model2)
        merged_models = reshaped_model1 + reshaped_model2
        merged_models[merged_models >= 1] = 1
        return merged_models


def tests():
    A, B, C = symbols("A B C")
    print(builder(Or(A, And(B, C))))
    # print(builder(Or(A, B, C)))


print(tests())


#######################################################################
#              Stuff that i do not need but keep anyways              #
#######################################################################

# XXX The following should never happen.
# if isinstance(exp, np.ndarray):
#     and_array = np.ones((len(exp), len(exp[0]) + 1))
#     and_array[:, :-1] = exp
#     return and_array
