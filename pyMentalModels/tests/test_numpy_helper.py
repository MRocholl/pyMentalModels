#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from sympy import symbols
from pyMentalModels.numpy_reasoner import _merge_models
import numpy as np
import numpy.testing as npt

POS_VAL = 1
IMPL_NEG = -1
EXP_NEG = -2

A, B, C, D = symbols("A B C D")
atom_index_mapping = {A: 0, B: 1, C: 2, D: 3}
exp_atoms = sorted(atom_index_mapping.keys(), key=str)


def test_merge_models():
    npt.assert_array_equal(_merge_models(
        np.array([[POS_VAL, POS_VAL, 0.]]),
        np.array([[0., IMPL_NEG, IMPL_NEG],
                  [0., POS_VAL, IMPL_NEG],
                  [0., IMPL_NEG, POS_VAL]]),
        atom_index_mapping=atom_index_mapping,
        exp_atoms=exp_atoms,
        op="And"), np.array([[POS_VAL, POS_VAL, IMPL_NEG]]))

    npt.assert_array_equal(_merge_models(
        np.array([[0., IMPL_NEG, IMPL_NEG],
                  [0., POS_VAL, IMPL_NEG],
                  [0., IMPL_NEG, POS_VAL]]),
        np.array([[POS_VAL, POS_VAL, 0.]]),
        atom_index_mapping=atom_index_mapping,
        exp_atoms=exp_atoms,
        op="And"), np.array([[POS_VAL, POS_VAL, IMPL_NEG]]))

    npt.assert_array_equal(_merge_models(
        np.array([[POS_VAL, POS_VAL, 0., 0.],
                  [POS_VAL, IMPL_NEG, 0., 0.]]),
        np.array([[0., POS_VAL, POS_VAL, 0.],
                  [0., IMPL_NEG, POS_VAL, 0.]]),
        np.array([[0., 0., POS_VAL, POS_VAL],
                  [0., 0., IMPL_NEG, POS_VAL]]),
        np.array([[IMPL_NEG, 0., POS_VAL, POS_VAL],
                  [POS_VAL, 0., IMPL_NEG, POS_VAL]]),
        atom_index_mapping=atom_index_mapping,
        exp_atoms=exp_atoms,
        op="And"), np.array([[]]))

    npt.assert_array_equal(_merge_models(
        np.array([POS_VAL]),
        np.array([EXP_NEG]),
        atom_index_mapping=atom_index_mapping,
        exp_atoms=exp_atoms,
        op="And"), np.array([[]]))
