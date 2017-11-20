#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import unittest

from pyMentalModels.logical_connectives.custom_logical_classes import (
    MulXor,
    ModalAnd, ModalOr, ModalImplies, ModalEquivalent,
    Possibly, Necessary
)

from sympy import symbols
A, B, C = symbols("A B C")

locals = {
    "Possibly": Possibly,
    "Necessary": Necessary,
    "ModalAnd": ModalAnd,
    "ModalOr": ModalOr,
    "MulXor": MulXor,
    "ModalImplies": ModalImplies,
    "ModalEquivalent": ModalEquivalent,
}

list_modal_expressions = [
    ModalAnd(A, Possibly(B & C)),
    ModalAnd(A, Possibly(B | C)),
    ModalAnd(A, Necessary(ModalAnd(B, C))),
]


class TestModalLogicalOperators(unittest.TestCase):
    """ Class that tests behavior of all modal logical variants
        of the logical operators
    """

    def test_modal_and(self):
        pass

    def test_modal_or(self):
        pass

    def test_modal_implies(self):
        pass

    def test_modal_xor(self):
        pass

    def test_modal_equals(self):
        pass

    def test_modal_not(self):
        pass
