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


def combine_mental_models(model1, model2, atom_index_mapping, exp_atoms):
    logging.debug("Combining mental models: ")
    logging.debug(model1)
    logging.debug(model2)

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
            logging.debug("Reshaped submodel:", reshaped_submodel)
            submodel_added_with_allowed_models = reshaped_submodel + allowed_models
            logging.info("SUBMODEL: {}".format(submodel_added_with_allowed_models))
            # after adding values can either be 2, -2 , -3 or -4 for the indexes that are active in both models
            # for the other indices values are 0, -1, -2 or 1
            # for the active indices map 4, -2, -3 and -4 to 1, -1, -2
            submodel_added_with_allowed_models[submodel_added_with_allowed_models == POS_VAL + POS_VAL] = POS_VAL
            submodel_added_with_allowed_models[submodel_added_with_allowed_models == POS_VAL + IMPL_NEG] = POS_VAL
            submodel_added_with_allowed_models[submodel_added_with_allowed_models == IMPL_NEG + IMPL_NEG] = IMPL_NEG
            submodel_added_with_allowed_models[submodel_added_with_allowed_models == EXPL_NEG + IMPL_NEG] = EXPL_NEG
            submodel_added_with_allowed_models[submodel_added_with_allowed_models == EXPL_NEG + EXPL_NEG] = EXPL_NEG
            logging.debug("added submodel with allowed model", submodel_added_with_allowed_models)
            sub_models_merged_model.append(submodel_added_with_allowed_models)
            logging.debug("List of valid submodels until now:", sub_models_merged_model)

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
    logging.info(merged_models)
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
    logging.debug(resized_mental_model)
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
                6. Otherwise
                    No task specified and so builds models of all the premises

    Returns
    -------
        if "infer":
            Infer a conclusion based on the premises

    """
    print()
    print("Inference task is: {}".format(task))
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
        logging.debug("The {}th model is: {}".format(i, model))
        print("The {}th model is:".format(i))
        print(model)

    print()
    print("Combine mental models...")
    possible_models = reduce(lambda model1, model2: combine_mental_models(model1, model2, atom_index_mapping_all, all_atoms_in_all_models), resized_mental_models)
    return mental_model(tuple(model.expr for model in models), possible_models, all_atoms_in_all_models, atom_index_mapping_all)


"""
    pairings_of_models = list(product(*resized_mental_models))

    for pairing in pairings_of_models:
        possible_model = _merge_models(*pairing, atom_index_mapping=atom_index_mapping_all, exp_atoms=all_atoms_in_all_models, op="And")
        if possible_model.size:
            possible_models.append(possible_model)
            logging.info("Given the models: {}".format(pairing))
            logging.info("The following model is possible: {}".format(possible_model))
    """
