#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import numpy as np
import logging

# from itertools import product
from functools import reduce

# from pyMentalModels.numpy_reasoner import _merge_models
from pyMentalModels.mental_model import mental_model
from pyMentalModels.constants import EXPL_NEG, POS_VAL, IMPL_NEG

from typing import List
from enum import Enum


class InferenceTask(Enum):
    FOLLOWS = "what_follows?"
    NECESSARY = "necessary?"
    POSSIBLE = "possible?"
    PROBABILITY = "probability?"
    VERIFY = "verify?"
    ONLY_MODELS = "only_models"


def normalize_combined_model_values(model):
    # after adding values can either be 2, -2 , -3 or -4 for the indexes that are active in both models
    # for the other indices values are 0, -1, -2 or 1
    # for the active indices map 4, -2, -3 and -4 to 1, -1, -2

    # XXX with exxxplicit mode, implicit neg == Expl neg
    model[model == POS_VAL + POS_VAL] = POS_VAL
    model[model == POS_VAL + IMPL_NEG] = POS_VAL
    model[model == IMPL_NEG + IMPL_NEG] = IMPL_NEG
    model[model == EXPL_NEG + IMPL_NEG] = EXPL_NEG
    model[model == EXPL_NEG + EXPL_NEG] = EXPL_NEG
    return model


def combine_mental_models(model1, model2, atom_index_mapping, exp_atoms):
    logging.debug("Combining mental models: ")
    logging.debug(str(model1))
    logging.debug(str(model2))

    if not model1.size or not model2.size:
        logging.debug("Either model1 or model2 is the empty model")
        return np.array([])

    """
    pre-process every submodel so that the combinations are allowed
        only compare relevant indices,
     i.e. (A & B) | (B & C)
          1  1  0   0  1  1

    """
    # Gather indices of atoms that are active in the models
    merged_model_active_indices = {i for i, val in enumerate(model1.any(axis=0)) if val}
    model_active_indices = {i for i, val in enumerate(model2.any(axis=0)) if val}

    # single out the overlapping atoms in both models (i.e. (A B) & (B C) -> B)
    atom_indices_to_check = list(merged_model_active_indices & model_active_indices)
    logging.debug("Atoms in both models: {}".format(list(map(lambda x: exp_atoms[x], atom_indices_to_check))))

    if atom_indices_to_check:  # if there are overlapping indices for both models
        sub_models_merged_model = []

        def same_val(val1, val2):
            return (val1 in (EXPL_NEG, IMPL_NEG) and val2 in (IMPL_NEG, EXPL_NEG)) \
                or (val1 in (IMPL_NEG, POS_VAL) and val2 in (IMPL_NEG, POS_VAL))

        for submodel in model1:
            allowed_models = []
            for sub_model_to_check in model2:
                # print(all(same_val(*vals) for vals in zip(submodel[atom_indices_to_check], sub_model_to_check[atom_indices_to_check])))
                if all(same_val(*vals) for vals in zip(submodel[atom_indices_to_check], sub_model_to_check[atom_indices_to_check])):
                    allowed_models.append(sub_model_to_check)
            logging.debug("Allowed models are: {}".format(allowed_models))
            if not allowed_models:
                continue
            allowed_models = np.stack(allowed_models)
            reshaped_submodel = np.repeat(np.atleast_2d(submodel), len(allowed_models), axis=0)
            logging.debug("Reshaped submodel:".format(reshaped_submodel))
            submodel_added_with_allowed_models = reshaped_submodel + allowed_models
            logging.info("SUBMODEL: {}".format(submodel_added_with_allowed_models))
            # after adding values can either be 2, -2 , -3 or -4 for the indexes that are active in both models
            # for the other indices values are 0, -1, -2 or 1
            # for the active indices map 4, -2, -3 and -4 to 1, -1, -2
            submodel_added_with_allowed_models = normalize_combined_model_values(submodel_added_with_allowed_models)
            logging.debug("added submodel with allowed model".format(submodel_added_with_allowed_models))
            sub_models_merged_model.append(submodel_added_with_allowed_models)
            logging.debug("List of valid submodels until now:".format(sub_models_merged_model))

        # finished iterating through all submodels
        # has collected all valid combinations of both the models
        # if there are still no combinations of any submodel with the other model
        # return the empty array
        if sub_models_merged_model:
                merged_models = np.vstack(sub_models_merged_model)
                print("MERGED: ", merged_models)
        else:
            print("The models contradict each other")
            return np.array([[]])
    else:
        reshaped_model1 = np.repeat(model1, len(model2), axis=0)
        reshaped_model2 = np.tile(model2, (len(model1), 1))
        merged_models = reshaped_model1 + reshaped_model2

    logging.info("The combination of both models yields: ")
    logging.info(str(merged_models))
    return merged_models


def resize_model(model, atom_index_mapping_all, all_atoms_in_all_models):
    """
    Resize models so that they all share the same form to be able to compare them

    Parameters
    ----------
    model: MentalModel NamedTuple

    atom_index_mapping_all: Dict
        maps each Atom to its column index in the mental_model.model np.ndarray

    all_atoms_in_all_models

    Returns
    -------

        resized model
    """
    resized_mental_model = np.zeros((len(model.model), len(all_atoms_in_all_models)))
    resized_mental_model[:, list(map(lambda atom: atom_index_mapping_all[atom], model.atoms_model))] = model.model
    logging.debug("Resized model: {}".format(resized_mental_model))
    return resized_mental_model


def infer(models: List, task: InferenceTask):
    """
    Parameters
    ----------
    models: List of mental_model NamedTuples with attributes:
        Attributes:
            expression: Logical expression that has been processed (Sympy.object)
            model: The resulting mental model representation (np.ndarry)
            atoms_model: list of atoms in the expression (list)
            atom_index_mapping: mapping of atoms to their column in `model` (Dict)
    task: InferenceTask
            One of the InferenceTask.values:
                1. what_follows?:
                    Set task: Infer what follows from all premises
                2. necessary?:
                    Set task: Given all but last premises, infer if last premise necessarily follows
                3. possible?:
                    Set task: Given all but last premises, infer if last premise possibly follows
                4. probability?:
                    Set task: Given all but last premises, infer the probability of last premis
                5. verify?:
                    Set task: Given evidence last premise, verify all but last
                6. only_models
                    Builds models of all the premises

    Returns
    -------
        Returns a conclusion or inference of sort.

    """
    print()
    print("Inference task is: {}".format(task))
    if task == InferenceTask.ONLY_MODELS or len(models) <= 1:
        return models[0]
    # first preprocess all mental models to share the same column space
    all_atoms_in_all_models = sorted(set().union(*(set(model.atoms_model) for model in models)), key=str)  # type: List
    atom_index_mapping_all = {atom: i for i, atom in enumerate(all_atoms_in_all_models)}

    # XXX  CHOOSE: IF contradiction abort early or just remove empty model from model list

    resized_mental_models = [
        resize_model(model, atom_index_mapping_all, all_atoms_in_all_models)
        for model in models
        if model.model.size  # getting rid of contradictions
    ]

    for i, model in enumerate(resized_mental_models):
        logging.debug("The {}th model is: {}".format(i + 1, model))
        print("The {}th model is:".format(i + 1))
        print(model)

    if task == InferenceTask.FOLLOWS:
        print()
        print("Combine mental models...")
        possible_models = reduce(
            lambda model1, model2:
            combine_mental_models(
                model1, model2,
                atom_index_mapping_all, all_atoms_in_all_models
            ),
            resized_mental_models
        )
        return mental_model(tuple(model.expr for model in models), possible_models, all_atoms_in_all_models, atom_index_mapping_all)

    # all the other modes separate the last expression from the first n-1
    *all_but_last_models, last_model = resized_mental_models
    all_but_last_str, last_str = ", ".join(str(model.expr) for model in models[:-1]), models[-1].expr

    # possible models given the first n-1 premises
    print()
    print("Combine all but last mental models...")
    possible_models = reduce(
        lambda model1, model2:
        combine_mental_models(
            model1, model2,
            atom_index_mapping_all, all_atoms_in_all_models
        ), all_but_last_models
    )

    if task == InferenceTask.NECESSARY:

        if not last_model.shape[0] == 1:
            raise ValueError("The last premise should be a simple one that yields a single possible model")

        necessary_atoms = {
            i for i, val in enumerate(
                np.all(possible_models == possible_models[0, :], axis=0)
            )
            if val
        }

        last_model_active_indices = {
            i for i, val in enumerate(
                last_model.all(axis=0)
            )
            if val
        }

        if necessary_atoms.issuperset(last_model_active_indices):
            print("The last premise '{}' necessarily follows from the previous expressions '{}'".format(last_str, all_but_last_str))
        else:
            print("The last premise '{}' does not necessarily follow from the previous expressons '{}'".format(last_str, all_but_last_str))

        return mental_model(tuple(model.expr for model in models), possible_models, all_atoms_in_all_models, atom_index_mapping_all)

    if task == InferenceTask.POSSIBLE:
        if not last_model.shape[0] == 1:
            raise ValueError("The last premise should be a simple one that yields a single possible model")
        print(possible_models.shape, last_model.shape)
        # Get the active indices for the last model to compare agains the different
        # possible_models in the all_but_last model
        last_model_active_indices = list({i for i, val in enumerate(last_model.all(axis=0)) if val})
        values_at_active_indices = last_model[0, last_model_active_indices]
        for possible_model in possible_models:
            if np.equal(  # This will compare the following to arrays elementwise
                values_at_active_indices,
                possible_model[last_model_active_indices]
            ).all():  # And return if all the values where the same
                print("The last premise '{}' possibly follows from the previous expressions '{}'".format(last_str, all_but_last_str))
        print("The last premise '{}' does not possibly follow from the previous expressons '{}'".format(last_str, all_but_last_str))

        return mental_model(tuple(model.expr for model in models), possible_models, all_atoms_in_all_models, atom_index_mapping_all)

    if task == InferenceTask.PROBABILITY:
        raise NotImplementedError("Future work...")  # XXX Requires probabilities based on facts I do not have implemented

    if task == InferenceTask.VERIFY:
        raise NotImplementedError("")
        print()
        print("Combine mental models...")
        possible_models = reduce(lambda model1, model2: combine_mental_models(model1, model2, atom_index_mapping_all, all_atoms_in_all_models), resized_mental_models)
        return mental_model(tuple(model.expr for model in models), possible_models, all_atoms_in_all_models, atom_index_mapping_all)
