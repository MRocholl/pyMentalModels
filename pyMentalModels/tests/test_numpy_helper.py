#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from sympy import symbols
from pyMentalModels.numpy_reasoner import (
    _merge_and, _merge_or,
    _merge_equivalent, _merge_implication,
    _merge_xor)

import numpy as np
import numpy.testing as npt
from pyMentalModels.constants import POS_VAL, IMPL_NEG, EXPL_NEG


A, B, C, D = symbols("A B C D")
atom_index_mapping = {A: 0, B: 1, C: 2, D: 3}
exp_atoms = sorted(atom_index_mapping.keys(), key=str)


def test_merge_and():
    npt.assert_array_equal(_merge_and(
        np.array([[POS_VAL, POS_VAL, 0.]]),
        np.array([[0., IMPL_NEG, IMPL_NEG],
                  [0., POS_VAL, IMPL_NEG],
                  [0., IMPL_NEG, POS_VAL]]),
        atom_index_mapping=atom_index_mapping,
        exp_atoms=exp_atoms,),
        np.array([[POS_VAL, POS_VAL, IMPL_NEG]]))

    npt.assert_array_equal(_merge_and(
        np.array([[0., IMPL_NEG, IMPL_NEG],
                  [0., POS_VAL, IMPL_NEG],
                  [0., IMPL_NEG, POS_VAL]]),
        np.array([[POS_VAL, POS_VAL, 0.]]),
        atom_index_mapping=atom_index_mapping,
        exp_atoms=exp_atoms,),
        np.array([[POS_VAL, POS_VAL, IMPL_NEG]]))

    npt.assert_array_equal(_merge_and(
        np.array([[POS_VAL, POS_VAL, 0., 0.],
                  [POS_VAL, IMPL_NEG, 0., 0.]]),
        np.array([[0., POS_VAL, POS_VAL, 0.],
                  [0., IMPL_NEG, POS_VAL, 0.]]),
        np.array([[0., 0., POS_VAL, POS_VAL],
                  [0., 0., IMPL_NEG, POS_VAL]]),
        np.array([[IMPL_NEG, 0., POS_VAL, POS_VAL],
                  [POS_VAL, 0., IMPL_NEG, POS_VAL]]),
        atom_index_mapping=atom_index_mapping,
        exp_atoms=exp_atoms,),
        np.array([[]]))

    npt.assert_array_equal(_merge_and(
        np.array([POS_VAL]),
        np.array([EXPL_NEG]),
        atom_index_mapping=atom_index_mapping,
        exp_atoms=exp_atoms,),
        np.array([[]]))

    def test_merge_or():
        pass
        npt.assert_array_equal(_merge_or(
            np.array([[]])))

    def test_merge_equivalent():
        pass
        npt.assert_array_equal(_merge_equivalent(
            np.array([[]])))

    def test_merge_implication():
        pass
        npt.assert_array_equal(_merge_implication(
            np.array([[]])))

    def test_merge_xor():
        pass
        npt.assert_array_equal(_merge_xor(
            np.array([[]])))
