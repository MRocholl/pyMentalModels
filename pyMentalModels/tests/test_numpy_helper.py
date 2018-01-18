#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
from sympy import symbols
from pyMentalModels.numpy_reasoner import _merge_models, _complement_array_model

def test_merge_models():
    assert _merge_models(np.array([[1., 1., 0.]]), np.array([[0., 0., 0.], [0., 1., 0.], [0., 0., 1.]]), atom_index_mapping=None, exp_atoms=None, op="And")





# print(_complement_array_model(np.array([[-1., 0.]]), [], exp_atoms=(A, B)))
