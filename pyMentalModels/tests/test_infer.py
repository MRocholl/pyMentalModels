#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-


from pyMentalModels.numpy_reasoner import mental_model_builder
from pyMentalModels.infer import infer

from sympy import symbols
from sympy.logic.boolalg import And, Or, Xor, Implies, Equivalent, Not


def test_infer():
    A, B, C = symbols("A B C")

def test_premise_parirings():
    assert



    test_premise_pairings = [
        ["A & ~A"],                              # 1 above
        ["A | ~A"],                              # 2 above
        ["B", "A -> B"],                         # 3 [consistent]
        ["~A", "A -> B"],                        # 4 [consistent]
        ["A", "A -> B", "B"],                    # 5 [valid]
        ["A", "A -> B", "A & B & C"],            # 6 [consistent]
        ["A", "A -> (B & C)", "A & B & C"],      # 7 [mutually valid]
        ["A", "A -> B", "B & A"],                # 8 [mutually valid]
        ["A -> B", "A & ~B"],                    # 9 false [inconsistent]
        ["A -> B", "A", "~B"],                   # 10 ditto
        ["A | B", "A"],                          # 11 [consistent] probability of 2/3
        ["A | B", "B"],                          # 12 [consistent] probability of 2/3
        ["A | B", "A & B"],                      # 13 [consistent] probability of 1/3
        ["A", "A | B"],                          # 14    "
        ["A | B", "C"],                          # 15 wholly independent [consistent]
        ["A", "A ^ B", "~B"],                    # 16 [valid]
        ["~A", "A ^ B", "B"],                    # 17    "
        ["~A", "A | B", "B"],                   # 18    "
        ["A | B", "~B", "A"],                     # 19    "
        ["A | B", "~A", "~A & B & C"],           # 20 [consistent]
        ["A | B", "~B", "A & ~B"],               # 21 [mutually valid]
        ["A | B", "~A", "~B"],                   # 22 false [inconsistent]
        ["A ^ B", "A | B"],                      # 23 [consistent]
        ["A | B", "A ^ B"],                      # 24 [consistent] probability of 2/3
    ]
