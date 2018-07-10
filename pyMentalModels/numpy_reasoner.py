#!/usr/bin/python3
""" File that collects numpy logic for mental model reasoner """

import numpy as np
from itertools import product, combinations
from sympy.logic.boolalg import (And, Or, Xor, Not, Implies, Equivalent)
from sympy.core.symbol import Symbol
from enum import Enum
import logging

from pyMentalModels.mental_model import mental_model
from pyMentalModels.custom_logical_classes import Necessary, Possibly
from pyMentalModels.constants import EXPL_NEG, POS_VAL, IMPL_NEG


#######################################################################
#                            Notes to self                            #
#######################################################################
#
# Also does not care how many arguments Xor takes (psychologically viable)
#
#
# Proposed solution:
#

# The sentence               The mental                The fully explicit models
#                            models of its
#                            possibilities
# ==========================|=========================|================================
# A And B                   |       A   B             |              A   B
# --------------------------|-------------------------|--------------------------------
# Neither A nor B           |      ~A  ~B             |             ~A  ~B
# --------------------------|-------------------------|--------------------------------
#                           |                         |
#                           |                         |
#                           |                         |
#                           |                         |
# A or else B, but not both |       A                 |              A  ~B
#                           |           B             |             ~A   B
# --------------------------|-------------------------|--------------------------------
# A or B or both            |       A                 |              A  ~B
#                           |           B             |             ~A   B
#                           |       A   B             |              A   B
# --------------------------|-------------------------|--------------------------------
# If A then B               |       A   B             |              A   B
#                           |        ...              |             ~A  ~B
#                           |                         |             ~A   B
# --------------------------|-------------------------|--------------------------------
# If and only if A then B   |       A   B             |              A   B
#                           |        ...              |             ~A  ~B

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
    with (A & B)=: Arg1, (C & D)=:Arg2, etc...

    The Model is:
    -------------
    Arg1 xor Arg2 xor Arg3  // This is just a vstack
    Arg1 & Arg2             // Piecewise concatenation
    Arg2 & Arg3             //      ""
    Arg1 & Arg2 & Arg3      // Addition of all three
    ========================
    Stacked from top to bottom

The implementation for the material implication `Implies` is not quite clear yet
The straight-forward way would be to duck-type it to the `And` behavior.


           +--------------------------+--------------+------------+
           |The sentence              |The mental    |  The fully |
           |                          |models of its |  explicit  |
           |                          |possibilities |  models    |
           +==========================+==============+============+
           |A And B                   |    A   B     |    A   B   |
           +--------------------------+--------------+------------+
           |Neither A nor B           |   ~A  ~B     |   ~A  ~B   |
           +--------------------------+--------------+------------+
           |A or else B, but not both |    A         |    A  ~B   |
           |                          |        B     |   ~A   B   |
           +--------------------------+--------------+------------+
           |A or B or both            |    A         |    A  ~B   |
           |                          |        B     |   ~A   B   |
           |                          |    A   B     |    A   B   |
           +--------------------------+--------------+------------+
           |If A then B               |    A   B     |    A   B   |
           |                          |     ...      |   ~A  ~B   |
           |                          |              |   ~A   B   |
           +--------------------------+--------------+------------+
           |If and only if A then B   |    A   B     |    A   B   |
           |                          |     ...      |   ~A  ~B   |
           +--------------------------+--------------+------------+


`Not`

The builder catches Nots as not being a symbol and will eventually try to
construct a model of a `Not(Atom)` or `Not(sub_expr)`

Examples of this behaviour would be:

    Not(A) or B             | (A | B) & ~(C | D) // Crete full model
                            |                    // and take complement
    Result should be:       | Result should be:
                            |                            |  C
    ~A                      |   A       ~C  ~D <-- from  |      D
        B                   |       B   ~C  ~D           |  C   D
    ~A  B                   |

Hence, an explicit `Not` in the expression will lead to an explicit `Not`
representation in the final model.
There seems to be a big difference in the semantic importance between the
negation of an atom and the negation of a subexpression.


"""


class Insight(Enum):

    """Enum for the diferent insight modes intuitive and full"""
    INTUITIVE = "intuitive"
    EXPLICIT = "explicit"


#######################################################################
#   Functions to introduce probabilistic behavior for Insight Level   #
#######################################################################


def probability_intuititive_explicit(mode, depth, depth_threshold=4):
    if mode == Insight.INTUITIVE:
        return Insight.INTUITIVE
    else:
        # Dependent on the recursion depth change mode of Insight.
        # XXX Set level to 4 for now ....
        return Insight.INTUITIVE if depth <= depth_threshold else Insight.EXPLICIT

#######################################################################
#                Main Function `mental_model_builder`                 #
#######################################################################


def mental_model_builder(sympified_expr, mode):
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
    mode: Insight
        Insight can be either Insight.INTUITIVE or Insight.FULL

    Returns
    -------
    Mental model representation of logical expression

    """
    # Extract atoms from sympified expression
    exp_atoms = sorted(sympified_expr.atoms(), key=str)

    # map every atom to its corresponding index in the model
    atom_index_mapping = {atom: i for i, atom in enumerate(exp_atoms)}

    return mental_model(sympified_expr, map_instance_to_operation(sympified_expr, mode)(sympified_expr, atom_index_mapping, exp_atoms, mode), exp_atoms, atom_index_mapping)


def map_instance_to_operation(el, mode):
    "maps every logical instance to its builder function."
    inst_op_mapping_explicit = (
        (Or, build_or),
        (And, build_and),
        (Xor, build_xor), # XXX This is a non-dyadic implementation of the Xor for arbitrary many arguments
        (Implies, build_implication),
        (Equivalent, build_equals),
        (Not, build_not),
        (Necessary, build_necessary),
        (Possibly, build_possibly),
        (Symbol, lambda *_: np.array([[POS_VAL]])),
    )
    inst_op_mapping_implicit = (
        (Or, build_or),
        (And, build_and),
        (Xor, build_xor),  # XXX Maybe change this to `Or`
        (Implies, build_and),
        (Equivalent, build_and),
        (Not, build_not),
        (Necessary, build_necessary),
        (Possibly, build_possibly),
        (Symbol, lambda *_: np.array([[POS_VAL]])),
    )
    if mode == Insight.INTUITIVE:
        maps = iter(inst_op_mapping_implicit)
    elif mode == Insight.EXPLICIT:
        maps = iter(inst_op_mapping_explicit)
    else:
        raise ValueError("Not a valid Insight `mode`")
    try:
        return next(builder for type_, builder in maps if isinstance(el, type_))
    except StopIteration:
        raise ValueError("Not a valid operator")

#######################################################################
#        Builder functions for the different logical operators        #
#######################################################################


def build_or(exp, atom_index_mapping, exp_atoms, mode):
    """
    Builds model of `Or` expression.

    Parameters
    ----------
    exp:
        expression with outer-most logical operator being `Or`

    atom_index_mapping: Dict
        mapping from all the atoms to their index in the model/array

    exp_atoms: List
        List of all the Atoms of the mental_model

    Returns
    -------
        Model: np.ndarray
    """

    assert(isinstance(exp, Or))

    or_args = exp.args
    nr_args = len(or_args)

    if all(isinstance(el, Symbol) for el in exp.args):
        pos_valuations = [x for x in product([IMPL_NEG, POS_VAL], repeat=nr_args)][1:]
        pos_valuations = sorted(pos_valuations, key=_sort_by_pos_vals)
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
            map_instance_to_operation(subexpression, mode)(subexpression, atom_index_mapping, exp_atoms, mode)
            for subexpression in subexpression_list
        ]

        # Create `or` model for the symbols
        if symbol_list:
            pos_valuations = [x for x in product([IMPL_NEG, POS_VAL], repeat=len(symbol_list))][1:]
            pos_valuations = sorted(pos_valuations, key=_sort_by_pos_vals)
            or_model = np.zeros((len(pos_valuations), len(exp_atoms)))
            or_model[
                :, list(map(lambda x: atom_index_mapping[x], symbol_list))
            ] = pos_valuations
            modelized_subexpressions.append(or_model)

        # merge the generated submodels to an overall model of `And`
        merged_sub_models = _merge_or(*modelized_subexpressions, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)
        print(merged_sub_models)
        return np.array(sorted(np.unique(merged_sub_models, axis=0), key=_sort_by_pos_vals))


def build_and(exp, atom_index_mapping, exp_atoms, mode):
    """
    Builds model of `And` expression.

    Parameters
    ----------
    exp:
        expression with outer-most logical operator being `And`

    atom_index_mapping: Dict
        mapping from all the atoms to their index in the model/array

    exp_atoms: List
        List of all the Atoms of the mental_model

    Returns
    -------
        Model: np.ndarray
    """

    assert(isinstance(exp, (And, Implies, Equivalent)))

    and_args = exp.args

    if all(isinstance(el, Symbol) for el in and_args):
        and_model = np.zeros((1, len(exp_atoms)))
        and_model[
            :, list(map(lambda x: atom_index_mapping[x], and_args))
        ] = POS_VAL
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
            map_instance_to_operation(subexpression, mode)(subexpression, atom_index_mapping, exp_atoms, mode)
            for subexpression in subexpression_list
        ]
        # Create `and` model for the symbols
        if symbol_list:
            and_model = np.zeros((1, len(exp_atoms)))
            and_model[
                :, list(map(lambda x: atom_index_mapping[x], symbol_list))
            ] = POS_VAL
            modelized_subexpressions.append(and_model)

        # merge the generated submodels to an overall model of `And`
        merged_sub_models = _merge_and(*modelized_subexpressions, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)
        if merged_sub_models.size:
            return np.array(sorted(np.unique(merged_sub_models, axis=0), key=_sort_by_pos_vals))
        else:
            return merged_sub_models


def build_xor(exp, atom_index_mapping, exp_atoms, mode):
    """
    Builds model of `Xor` expression.

    Parameters
    ----------
    exp:
        expression with outer-most logical operator being `Xor`

    atom_index_mapping: Dict
        mapping from all the atoms to their index in the model/array

    exp_atoms: List
        List of all the Atoms of the mental_model

    Returns
    -------
        Model: np.ndarray
    """
    assert(isinstance(exp, Xor))

    xor_args = exp.args
    nr_xor_args = len(xor_args)

    if all(isinstance(el, Symbol) for el in exp.args):
        xor_model = np.zeros((nr_xor_args, len(exp_atoms)))
        all_combinations = np.eye(nr_xor_args) * POS_VAL
        all_combinations[np.where(all_combinations != POS_VAL)] = IMPL_NEG
        xor_model[
            :, list(map(lambda x: atom_index_mapping[x], xor_args))
        ] = all_combinations
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
            map_instance_to_operation(subexpression, mode)(subexpression, atom_index_mapping, exp_atoms, mode)
            for subexpression in subexpression_list
        ]

        if symbol_list:
            xor_model = np.zeros((len(symbol_list), len(exp_atoms)))
            all_combinations = np.eye(len(symbol_list)) * POS_VAL
            all_combinations[np.where(all_combinations != POS_VAL)] = IMPL_NEG
            xor_model[
                :, list(map(lambda x: atom_index_mapping[x], symbol_list))
            ] = all_combinations
            modelized_subexpressions.append(xor_model)

        # Create `xor` model for the symbols
        merged_sub_models = _merge_xor(
            *modelized_subexpressions, atom_index_mapping=atom_index_mapping,
            exp_atoms=exp_atoms)
        return np.array(sorted(np.unique(merged_sub_models, axis=0), key=_sort_by_pos_vals))


def build_implication(exp, atom_index_mapping, exp_atoms, mode):
    """
    Builds numpy representation of implication

    Behaves differently depending on if it is called with parameter Insight.Intuitive
    or Insight.Full

    "A -> B"

    Should yield model

    1 1     mode = INTUITIVE
    ---
    0 1     mode = FULL
    0 0

    Parameters
    ----------
    exp: symbolic expression
        Expression with only symbols or symbols and logical arguments
    atom_index_mapping:
    exp_atoms: TODO
    mode: TODO, optional

    Returns
    -------

    """
    assert(isinstance(exp, Implies))
    assert len(exp.args) == 2

    antecedent, consequent = exp.args

    if all(isinstance(el, Symbol) for el in exp.args):
        pos_valuations = [(POS_VAL, POS_VAL), (IMPL_NEG, POS_VAL), (IMPL_NEG, IMPL_NEG)]
        implication_model = np.zeros((len(pos_valuations), len(exp_atoms)))
        implication_model[
            :, list(map(lambda x: atom_index_mapping[x], [antecedent, consequent]))
        ] = pos_valuations
        return implication_model
    else:
        if not isinstance(antecedent, Symbol) and not isinstance(consequent, Symbol):
            modelized_antecedent = map_instance_to_operation(antecedent, mode)(antecedent, atom_index_mapping, exp_atoms, mode)
            modelized_consequent = map_instance_to_operation(consequent, mode)(consequent, atom_index_mapping, exp_atoms, mode)

        elif not isinstance(consequent, Symbol):
            modelized_antecedent = np.zeros((1, len(exp_atoms)))
            modelized_antecedent[:, atom_index_mapping[antecedent]] = POS_VAL
            modelized_consequent = map_instance_to_operation(consequent, mode)(consequent, atom_index_mapping, exp_atoms, mode)
        else:
            modelized_antecedent = map_instance_to_operation(antecedent, mode)(antecedent, atom_index_mapping, exp_atoms, mode)
            modelized_consequent = np.zeros((1, len(exp_atoms)))
            modelized_consequent[:, atom_index_mapping[consequent]] = POS_VAL

        merged_sub_models = _merge_implication(
            modelized_antecedent, modelized_consequent, atom_index_mapping=atom_index_mapping,
            exp_atoms=exp_atoms)
        return np.array(sorted(np.unique(merged_sub_models, axis=0), key=_sort_by_pos_vals))


def build_equals(exp, atom_index_mapping, exp_atoms, mode):
    """
    Builds numpy representation of implication

    Behaves differently depending on if it is called with parameter Insight.Intuitive
    or Insight.Full

    "A -> B"
    Should yield model
    1 1     mode = INTUITIVE
    ---
    0 1     mode = FULL
    0 0

    Parameters
    ----------
    exp: symbolic expression
        Expression with only symbols or symbols and logical arguments
    atom_index_mapping:
    exp_atoms: TODO
    mode: TODO, optional

    Returns
    -------

    """
    assert(isinstance(exp, Equivalent))
    assert len(exp.args) == 2

    antecedent, consequent = exp.args

    if all(isinstance(el, Symbol) for el in exp.args):
        pos_valuations = [(POS_VAL, POS_VAL), (IMPL_NEG, IMPL_NEG)]
        bi_implication_model = np.zeros((len(pos_valuations), len(exp_atoms)))
        bi_implication_model[
            :, list(map(lambda x: atom_index_mapping[x], [antecedent, consequent]))
        ] = pos_valuations
        return bi_implication_model
    else:
        if not isinstance(antecedent, Symbol) and not isinstance(consequent, Symbol):
            modelized_antecedent = map_instance_to_operation(antecedent, mode)(antecedent, atom_index_mapping, exp_atoms, mode)
            modelized_consequent = map_instance_to_operation(consequent, mode)(consequent, atom_index_mapping, exp_atoms, mode)

        elif not isinstance(consequent, Symbol):
            modelized_antecedent = np.zeros((1, len(exp_atoms)))
            modelized_antecedent[:, atom_index_mapping[antecedent]] = 1
            modelized_consequent = map_instance_to_operation(consequent, mode)(consequent, atom_index_mapping, exp_atoms, mode)
        else:
            modelized_antecedent = map_instance_to_operation(antecedent, mode)(antecedent, atom_index_mapping, exp_atoms, mode)
            modelized_consequent = np.zeros((1, len(exp_atoms)))
            modelized_consequent[:, atom_index_mapping[consequent]] = 1

        merged_sub_models = _merge_equivalent(
            modelized_antecedent, modelized_consequent, atom_index_mapping=atom_index_mapping,
            exp_atoms=exp_atoms)

        return np.array(sorted(np.unique(merged_sub_models, axis=0), key=_sort_by_pos_vals))


def build_not(exp, atom_index_mapping, exp_atoms, mode):
    """
    Builds model of expression with outer-most argument being Not
    """
    assert isinstance(exp, Not)
    neg_arg = exp.args[0]
    if isinstance(neg_arg, Symbol):
        not_model = np.zeros([1, len(exp_atoms)])
        not_model[
            0, atom_index_mapping[neg_arg]
        ] = EXPL_NEG
        return not_model
    else:
        # First build model of the model to be negated
        # then get the complement of that model and return it
        model_positive = map_instance_to_operation(neg_arg, mode)(neg_arg, atom_index_mapping, exp_atoms, mode)
        neg_model = _complement_array_model(model_positive, atom_index_mapping, exp_atoms)
        return neg_model


def build_necessary(exp, atom_index_mapping, exp_atoms, mode):
    # XXX NOT being used right now. Also functionality questionable
    """
    Builds model of `necessary` expression

    1. Models represent possibilities (J-L & Byrne, 1991)

    2. Compounds of alternatives refer by default to exhaustive conjunctions of
    possibilities, e.g.: A or else B, but not both
    has two mental models (system 1):
    A
        B
    (J-L, Khemlani, & Goodwin, 2015.)

    Fully explicit models (system 2) also represent what’s impossible.

    3. A conjunction, A and B, makes a factual claim: both propositions hold in
    all possibilities.

    4. Parsimony: possible that A and possible that B has a mental model of a
    single possibility:

    A   B


    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    (2) Necessary
    The problem is that the truth value of A does not determine the truth value for []A. For example, when A is ‘Dogs are dogs’, []A is true, but when A is ‘Dogs are pets’, []A is false

    (3) Possible

    Rules for the modal logical system:
    ==================================

    (~) v(~A, w)=T iff v(A, w)=F.

    (->) v(A -> B, w)=T iff v(A, w)=F or v(B, w)=T. !!!!! Implication is AND in implicit mode

    (5) v([]A, w)=T iff for every world w′ in W, v(A, w′)=T.

    Furthermore, [](A&B) entails []A&[]B and vice versa; while []A|[]B entails [](A|B), but not vice versa. This reflects the patterns exhibited by the universal quantifier: ∀x(A&B) entails ∀xA&∀xB and vice versa, while ∀xA ∨ ∀xB entails ∀x(A ∨ B) but not vice versa
"""
    assert isinstance(exp, Necessary)
    # necessary
    # necessar -- AND
    # possible -- OR
    return map_instance_to_operation(exp.args[0])(exp.args[0], atom_index_mapping, exp_atoms, mode)


def build_possibly(exp, atom_index_mapping, exp_atoms, mode):
    """
    Builds model of `possibly` expression
    """
    assert isinstance(exp, Possibly)
    return map_instance_to_operation(exp.args[0], mode)(exp.args[0], atom_index_mapping, exp_atoms, mode)

###############################################################################
#         functions that work directly on np.ndarray models                   #
#         `_merge_[and|or|xor|implication|equals]`, `_complement_array_model` #
###############################################################################


def _merge_and(*sub_models, atom_index_mapping, exp_atoms):
    """
    Merges the different subexpressions together.
    Implements merging for operator `And`

    Parameters
    ----------
    sub_models: List[np.ndarray]
        List of arbitrary number of sub_models subexpressions to be merged together

    atom_index_mapping: Dict
        Mapping of atom to its index in np.ndarray representation of a mental model

    Returns
    -------
    np.ndarray
        Merged `submodels` as `merged_models`

    """
    assert(len(sub_models)) >= 2

    sub_models = tuple(np.atleast_2d(model) for model in sub_models)

    logging.debug("Arguments for `And` merge: ")
    logging.debug(sub_models)
    print(sub_models)

    iter_models = iter(sub_models)
    merged_models = next(iter_models)
    for model in iter_models:
        """
        pre-process every submodel so that the combinations are allowed
            only compare relevant indices,
         i.e. (A & B) | (B & C)
              1  1  0   0  1  1

        """
        # Gather indices of atoms that are active in the models
        merged_model_active_indices = {i for i, val in enumerate(merged_models.any(axis=0)) if val}
        model_active_indices = {i for i, val in enumerate(model.any(axis=0)) if val}

        # single out the overlapping atoms in both models (i.e. (A B) , (B C) -> B)
        atom_indices_to_check = list(merged_model_active_indices & model_active_indices)
        logging.debug("Atoms in both models: {}".format(list(map(lambda x: exp_atoms[x], atom_indices_to_check))))

        if atom_indices_to_check:  # if there are overlapping indices for both models
            sub_models_merged_model = []

            def same_val(val1, val2):
                return (val1 == POS_VAL and val2 == POS_VAL) \
                    or (val1 in (IMPL_NEG, EXPL_NEG) and val2 in (IMPL_NEG, EXPL_NEG))
            for submodel in merged_models:
                allowed_models = []
                for sub_model_to_check in model:  # loop through all the possible submodels
                    if all(                       # for the second model and compare to current submodel
                        same_val(*vals)  # Checks if the values for the same active atom
                        for vals in zip(  # in the two possible models are compatible
                            submodel[atom_indices_to_check],
                            sub_model_to_check[atom_indices_to_check]
                        )
                    ):
                        allowed_models.append(sub_model_to_check)  # if yes: append
                logging.debug("Allowed models are: {}".format(allowed_models))
                if not allowed_models:
                    logging.debug("No allowed submodels")
                    continue
                elif len(allowed_models) >= 2:
                    allowed_models = np.stack(allowed_models)
                else:
                    allowed_models = np.atleast_2d(allowed_models)
                reshaped_submodel = np.repeat(np.atleast_2d(submodel),
                                              len(allowed_models),
                                              axis=0)
                submodel_added_with_allowed_models = reshaped_submodel + allowed_models

                # normalize values for Pos, impl and expl values
                submodel_added_with_allowed_models[submodel_added_with_allowed_models == POS_VAL + POS_VAL] = POS_VAL
                submodel_added_with_allowed_models[submodel_added_with_allowed_models == IMPL_NEG + IMPL_NEG] = IMPL_NEG
                submodel_added_with_allowed_models[submodel_added_with_allowed_models == EXPL_NEG + IMPL_NEG] = EXPL_NEG
                submodel_added_with_allowed_models[submodel_added_with_allowed_models == EXPL_NEG + EXPL_NEG] = EXPL_NEG

                logging.debug("added submodel with allowed model {}".format(submodel_added_with_allowed_models))
                sub_models_merged_model.append(submodel_added_with_allowed_models)
                logging.debug("List of valid submodels until now: {}".format(sub_models_merged_model))

            # finished iterating through all submodels
            # has collected all valid combinations of both the models
            # if there are still no combinations of any submodel with the other model
            # return the empty array
            if sub_models_merged_model:
                iter_models = iter(sub_models_merged_model)
                merged_models = next(iter_models)
                for sub_model in iter_models:
                    merged_models = np.vstack((merged_models, sub_model))
            else:
                logging.info("AND yields the empty array")
                return np.array([[]])
        else:
            reshaped_merged_models = np.repeat(merged_models, len(model), axis=0)
            reshaped_model2 = np.tile(model, (len(merged_models), 1))
            merged_models = reshaped_merged_models + reshaped_model2

    logging.debug("Merged `AND`: ")
    logging.debug(merged_models)
    return merged_models


def _merge_xor(*sub_models, atom_index_mapping, exp_atoms):
    """
    Takes complement of one model and the other model and adds them together

    generate complement for each model
          0  0  0
          0  1  0  ...
          1  0  0

          combine for all models in merged_models
          and check if models to be added are compatible with preexisting
          merged models

        i.e. Model1 & ~Model2
            ~Model1 &  Model2
    """
    logging.debug(str(sub_models))
    negated_models = [
        _complement_array_model(model, atom_index_mapping, exp_atoms)
        for model in sub_models
    ]
    # for each model in sub_models add the model
    # with the complements of all other submodels
    pos_neg_combinations = [
        _merge_and(
            model,
            *(neg_model for j, neg_model in enumerate(negated_models) if j != i),
            atom_index_mapping=atom_index_mapping,
            exp_atoms=exp_atoms
        )
        for i, model in enumerate(sub_models)
    ]
    iter_models = iter(pos_neg_combinations)
    merged_models = next(iter_models)
    for model in iter_models:
        merged_models = np.vstack((merged_models, model))
    return merged_models


def _merge_or(*sub_models, atom_index_mapping, exp_atoms):
        # first xor everything
        print(sub_models)
        xor_models = _merge_xor(*sub_models, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)
        merged_models = xor_models
        # then piecewise and everything
        list_of_piecewise_ands = [
            _merge_and(*comb, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)
            for comb in combinations(sub_models, 2)
        ]

        if len(list_of_piecewise_ands) > 1:
            for el in list_of_piecewise_ands:
                merged_models = np.vstack((merged_models, el))
        # then total and everything
        and_everything = _merge_and(*sub_models, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)

        print(merged_models, and_everything)
        print(merged_models.shape, and_everything.shape)
        if and_everything.size:
            merged_models = np.vstack((merged_models, and_everything))
        return merged_models


def _merge_implication(*sub_models, atom_index_mapping, exp_atoms):
        """ get 1 1
                0 1
                0 0 combination"""
        antecedent, consequent = sub_models
        complement_antecedent = _complement_array_model(antecedent, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)
        logging.debug("complement_antecedent")
        logging.debug(str(complement_antecedent))
        complement_consequent = _complement_array_model(consequent, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)

        logging.debug("complement_consequent")
        logging.debug(str(complement_consequent))

        list_of_combinations = []

        # antecedent and conseqent together
        antecedent_consequent = _merge_and(antecedent, consequent, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)

        if antecedent_consequent.size:
            list_of_combinations.append(antecedent_consequent)

        logging.debug("Combination 1 1")
        logging.debug(str(antecedent_consequent))

        # complement of ante and consequent
        comp_antecedent_consequent = _merge_and(complement_antecedent, consequent, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)

        if comp_antecedent_consequent.size:
            list_of_combinations.append(comp_antecedent_consequent)

        logging.debug("Combination 0 1")
        logging.debug(str(comp_antecedent_consequent))

        # ante and complement of consequent
        comp_antecedent_comp_consequent = _merge_and(complement_antecedent, complement_consequent, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)

        if comp_antecedent_comp_consequent.size:
            list_of_combinations.append(comp_antecedent_comp_consequent)

        logging.debug("Combination 0 0")
        logging.debug(str(comp_antecedent_comp_consequent))

        # complement of ante and complement of consequent
        merged_models = np.vstack(list_of_combinations)
        logging.debug("Total merged `Implication` model: ")
        logging.debug(str(merged_models))
        return merged_models


def _merge_equivalent(*sub_models, atom_index_mapping, exp_atoms):
        """ get 1 1
                0 1
                0 0 combination"""
        antecedent, consequent = sub_models
        complement_antecedent = _complement_array_model(antecedent, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)
        logging.debug("complement_antecedent")
        logging.debug(str(complement_antecedent))
        complement_consequent = _complement_array_model(consequent, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)

        logging.debug("complement_consequent")
        logging.debug(str(complement_consequent))

        merged_models = _merge_and(antecedent, consequent, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)
        logging.debug("Combination 1 1")
        logging.debug(str(merged_models))

        comp_antecedent_comp_consequent = _merge_and(complement_antecedent, complement_consequent, atom_index_mapping=atom_index_mapping, exp_atoms=exp_atoms)
        logging.debug("Combination 0 0")
        logging.debug(str(comp_antecedent_comp_consequent))

        merged_models = np.vstack((merged_models, comp_antecedent_comp_consequent))
        logging.debug("Total merged `Implication` model: ")
        logging.debug(str(merged_models))
        return merged_models


def _complement_array_model(model, atom_index_mapping, exp_atoms):
    model_arg_indices = [i for i, val in enumerate(model.any(axis=0)) if val]
    nr_args = len(model_arg_indices)
    all_combinations = [list(el) for el in product([IMPL_NEG, POS_VAL], repeat=nr_args)]
    # generate all combinations
    model_copy = model.copy()
    all_possible_models = np.zeros((len(all_combinations), len(exp_atoms)))
    all_possible_models[:, model_arg_indices] = all_combinations
    set_all_possible_models = {tuple(el) for el in all_possible_models}
    model_copy[model_copy < 0] = 0
    set_model = {tuple(el) for el in model_copy}
    complement_as_set = set_all_possible_models.difference(set_model)
    return np.array(sorted(complement_as_set, key=_sort_by_pos_vals))


def _sort_by_pos_vals(array_slice):
    """ Helper function to sort models by atom"""
    # this negates all the values as sorted will sort from smallest to biggest
    first_positive_then_neg = [-val for val in array_slice]
    # first sorts after number of positive values and then after the order in the array
    return list(array_slice).count(POS_VAL) == 0, list(array_slice).count(POS_VAL), first_positive_then_neg
