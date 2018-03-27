#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import numpy as np
import logging

from itertools import product
from functools import reduce

from pyMentalModels.numpy_reasoner import _merge_models
from pyMentalModels.mental_model import mental_model

from typing import List

POS_VAL = 2
IMPL_NEG = -1
EXPL_NEG = -2


def combine_mental_models(model1, model2, atom_index_mapping, exp_atoms):
    logging.info("Combining mental models: ")
    logging.info(model1)
    logging.info(model2)

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
                print(all(same_val(*vals) for vals in zip(submodel[atom_indices_to_check], sub_model_to_check[atom_indices_to_check])))
                if all(same_val(*vals) for vals in zip(submodel[atom_indices_to_check], sub_model_to_check[atom_indices_to_check])):
                    allowed_models.append(sub_model_to_check)
            logging.debug("Allowed models are: {}".format(allowed_models))
            if not allowed_models:
                continue
            allowed_models = np.stack(allowed_models)
            reshaped_submodel = np.repeat(np.atleast_2d(submodel), len(allowed_models), axis=0)
            logging.debug("Reshaped submodel:", reshaped_submodel)
            submodel_added_with_allowed_models = reshaped_submodel + allowed_models
            print("#####################################################################################")
            print("SUBMODEL: ", submodel_added_with_allowed_models)
            # after adding values can either be 2, -2 , -3 or -4 for the indexes that are active in both models
            # for the other indices values are 0, -1, -2 or 1
            # for the active indices map 2, -2, -3 and -4 to 1, -1, -2
            submodel_added_with_allowed_models[submodel_added_with_allowed_models == POS_VAL + POS_VAL] = POS_VAL
            submodel_added_with_allowed_models[submodel_added_with_allowed_models == POS_VAL + IMPL_NEG] = POS_VAL
            submodel_added_with_allowed_models[submodel_added_with_allowed_models == EXPL_NEG + IMPL_NEG] = EXPL_NEG
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


def infer(models: List, task="infer"):
    """
    Parameters
    ----------
    models: List of mental_model NamedTuples with attributes:
        Attributes:
            expression: Logical expression that has been processed (Sympy.object)
            model: The resulting mental model representation (np.ndarry)
            atoms_model: list of atoms in the expression (list)
            atom_index_mapping: mapping of atoms to their column in `model` (Dict)
    Returns
    -------
        if "infer":
            Infer a conclusion based on the premises
        XXX TODO

    """
    # first preprocess all mental models to share the same column space
    all_atoms_in_all_models = sorted(set().union(*(set(model.atoms_model) for model in models)), key=str)  # type: List
    atom_index_mapping_all = {atom: i for i, atom in enumerate(all_atoms_in_all_models)}

    # XXX  CHOOSE: IF contradiction abort early or just remove empty model from model list

    resized_mental_models = [
        resize_model(model, atom_index_mapping_all, all_atoms_in_all_models)
        for model in models
        if model.model.size  # getting rid of contradictions
    ]

    for i, mod in enumerate(resized_mental_models):
        print("The {}th model is: {}".format(i, mod))

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

