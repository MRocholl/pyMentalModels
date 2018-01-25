#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import numpy as np
import logging

from itertools import product

from pyMentalModels.numpy_reasoner import _merge_models
from pyMentalModels.mental_model import mental_model

from typing import List


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

    """
    # first preprocess all mental models to share the same column space
    all_atoms_in_all_models = sorted(set().union(*(set(model.atoms_model) for model in models)), key=str)  # type: List
    atom_index_mapping_all = {atom: i for i, atom in enumerate(all_atoms_in_all_models)}

    resized_mental_models = []

    for model in models:
        resized_mental_model = np.zeros((len(model.model), len(all_atoms_in_all_models)))
        resized_mental_model[:, list(map(lambda atom: atom_index_mapping_all[atom], model.atoms_model))] = model.model
        logging.debug(resized_mental_model)
        resized_mental_models.append(resized_mental_model)
    for i, mod in enumerate(resized_mental_models):
        print("The {}th model is: {}".format(i, mod))

    possible_models = []
    pairings_of_models = list(product(*resized_mental_models))
    for pairing in pairings_of_models:
        possible_model = _merge_models(*pairing, atom_index_mapping=atom_index_mapping_all, exp_atoms=all_atoms_in_all_models, op="And")
        if possible_model.size:
            possible_models.append(possible_model)
            logging.info("Given the models: {}".format(pairing))
            logging.info("The following model is possible: {}".format(possible_model))
    if possible_models:
        possible_models = np.vstack((possible_models))

    return mental_model(tuple(model.expr for model in models), possible_models, all_atoms_in_all_models, atom_index_mapping_all)
