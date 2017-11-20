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
negation of an atom and the negation of a submodel.


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
        print("Merging models")
        assert(len(sub_models)) >= 2

        if op == "And":
            iter_models = iter(sub_models)
            merged_models = next(iter_models)
            print("merged model")
            print(merged_models, merged_models.shape)
            while True:
                try:
                    model2 = next(iter_models)
                    print(model2, model2.shape)
                except StopIteration:
                    break
                reshaped_merged_models = np.repeat(merged_models, len(model2), axis=0)
                reshaped_model2 = np.tile(model2, (len(merged_models), 1))
                print(reshaped_merged_models)
                print(reshaped_model2)
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

            # Create `or` model for the symbols
            pos_valuations = [x for x in product(range(2), repeat=len(symbol_list))][1:]
            pos_valuations = sorted(pos_valuations, key=_increasing_ones_first_sort)
            or_model = np.empty((len(pos_valuations), len(exp_atoms)))
            or_model[
                :, list(map(lambda x: var_ind_map[x], symbol_list))
            ] = pos_valuations
            # create submodels for every submodel in submodel_list
            modelized_submodels = [map_instance_to_operation(el)(el) for submodel in submodel_list]
            modelized_submodels.append(or_model)
            merged_sub_models = _merge_models(*modelized_submodels, op="Or")
            return merged_sub_models

    def build_and(exp):

        assert(isinstance(exp, And))

        and_args = exp.args

        if all(isinstance(el, Symbol) for el in and_args):
            and_model = np.empty((1, len(exp_atoms)))
            and_model[
                :, list(map(lambda x: var_ind_map[x], and_args))
            ] = 1.
            return and_model
        else:
            symbol_list = []
            submodel_list = []
            for el in exp.args:
                if isinstance(el, Symbol):
                    symbol_list.append(el)
                else:
                    submodel_list.append(el)

            # Create `and` model for the symbols
            and_model = np.empty((1, len(exp_atoms)))
            and_model[
                :, list(map(lambda x: var_ind_map[x], symbol_list))
            ] = 1.
            # create submodels for every submodel in submodel_list
            modelized_submodels = [map_instance_to_operation(el)(el) for submodel in submodel_list]
            modelized_submodels.append(and_model)
            merged_sub_models = _merge_models(*modelized_submodels, op="And")
            return merged_sub_models

    def build_xor(exp):

        assert(isinstance(exp, Xor))

        xor_args = exp.args
        nr_args = len(xor_args)

        if all(isinstance(el, Symbol) for el in exp.args):
            xor_model = np.empty((nr_args, len(exp_atoms)))
            xor_model[
                :, list(map(lambda x: var_ind_map[x], xor_args))
            ] = np.eye(nr_args)
            return xor_model
        else:
            symbol_list = []
            submodel_list = []
            for el in exp.args:
                if isinstance(el, Symbol):
                    symbol_list.append(el)
                else:
                    submodel_list.append(el)

            xor_model = np.empty((symbol_list, len(exp_atoms)))
            xor_model[
                :, list(map(lambda x: var_ind_map[x], symbol_list))
            ] = np.eye(len(symbol_list))
            # Create `or` model for the symbols
            modelized_submodels = [map_instance_to_operation(el)(el) for submodel in submodel_list]
            modelized_submodels.append(xor_model)
            merged_sub_models = _merge_models(*modelized_submodels, op="Xor")
            return merged_sub_models

    def build_not(exp):
        arg = exp.args[0]
        assert isinstance(exp, Not)
        if isinstance(arg, Symbol):
            not_model = np.empty((1, len(exp_atoms)))
            not_model[
                :, var_ind_map[arg]
            ] = -1.
            return not_model
        else:
            model_positive = map_instance_to_operation(arg)(arg)
            print(model_positive)

    def _increasing_ones_first_sort(array_slice):
                    pos_of_ones = [-array_slice[i] for i, _ in enumerate(array_slice)]
                    return array_slice.count(1), pos_of_ones

    return map_instance_to_operation(sympified_expr)(sympified_expr)


def tests():
    A, B, C = symbols("A B C")
    exp = Or(A, ~B, C)
    print(exp)
    for model in builder(exp):
        print(list(chr(97 + i) if el == 1. else "" if el == 0 else "-{}".format(chr(97 + i)) if el == -1 else "" for i, el in enumerate(model)))
    # print(builder(Or(A, B, C)))


print(tests())


#######################################################################
#              Stuff that i do not need but keep anyways              #
#######################################################################

# XXX The following should never happen. Input should never be an array
# if isinstance(exp, np.ndarray):
#     and_array = np.ones((len(exp), len(exp[0]) + 1))
#     and_array[:, :-1] = exp
#     return and_array

# XXX Stuff from Xor
# if all(isinstance(el, Symbol) for el in arguments):
#             return np.ones(len(exp.atoms()))
#
#         # Check if everything is a Symbol
#         for el in arguments:
#             if isinstance(el, Not):
#                 seen_not_list.append(el)
#                 return build_not(el)
#             elif not isinstance(el, Symbol):
#                 return map_instance_to_operation(el)(el)
#             else:
#                 pass
#         if any(isinstance(el, Not) for el in arguments):
#             return "Witnessed a Not at this place"
#
