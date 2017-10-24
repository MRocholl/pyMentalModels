#!/usr/bin/python3

import unittest

from itertools import product

from sympy import sympify, symbols
from sympy.logic.boolalg import And, Or, Xor, Implies, Equivalent

import pyMentalModels.logical_connectives.operators as op
import pyMentalModels.logical_connectives.custom_logical_classes as clc
import pyMentalModels.parsing.modal_parser as mp
import pyMentalModels.reasoner.sympy_reasoner as sr


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



def _eval_premise(premise_str):
    return sr.generate_possible_models(sympify(mp.sympify_formatter(mp.parse_expr(premise_str), op.intuit_op), locals={"MulXor": clc.MulXor}))


class TestLogicalOperators(unittest.TestCase):

    def test_all_variations_neg_pos_connectives(self):
        """ Test behavior for one junctors"""

        A, B, C = symbols("A B C")  # defining symbols
        print(A)
        for operator in (And, Or, Xor, Implies, Equivalent):
            for valuations in product([0, 1], repeat=2):
                first_arg, sec_arg = [~atom if value == 0 else atom for atom, value in zip([A, B], valuations)]
                log_obj = operator(first_arg, sec_arg)
                print(log_obj)
                print("-------")
                for el in sr.generate_possible_models(log_obj, intuitive=False):
                    print(el)
                print()

    def test_all_dual_variations(self):
        """ Test behavior for combinations of two junctors"""
        A, B, C = symbols("A B C")
        for first, second in product([And, Or, Xor, Implies, Equivalent, clc.MulXor], repeat=2):
            for valuations in product([0, 1], repeat=3):
                first_arg, sec_arg, thrd_arg = [~atom if value == 0 else atom for atom, value in zip([A, B, C], valuations)]
                log_obj = first(first_arg, second(sec_arg, thrd_arg))
                print(log_obj)
                print("-------")
                for el in sr.generate_possible_models(log_obj, intuitive=False):
                    print(el)
                print()

    def test_logical_connectives_implicit(self):
        for premise_pairings in test_premise_pairings:
            for premise in premise_pairings:
                print(premise)
                formatted_prem = mp.sympify_formatter(mp.parse_expr(premise), op.intuit_op)
                sympified_expression = sympify(formatted_prem)
                possible_models = sr.generate_possible_models(sympified_expression, intuitive=True)
                print(possible_models)

    def test_logical_connectives_explicit(self):
        for premise_pairings in test_premise_pairings:
            for premise in premise_pairings:
                print(premise)
                formatted_prem = mp.sympify_formatter(mp.parse_expr(premise), op.explicit_op)
                sympified_expression = sympify(formatted_prem)
                possible_models = sr.generate_possible_models(sympified_expression, intuitive=False)
                print(possible_models)

    # def test_inferences(self):
    # (((If A then B)(A)(not B)) 1)                     ; 1. premise 3 is impossible [inconsistent]
    # (((A)(If A then comma B and C)(A and B and C)) 2) ; 2 [mutually valid]
    # (((A)(if A or B then C)(C)) 3)                    ; 3 premise 3 is true  [valid]
    # (((A or B)(A and B)) 4)                           ; 4 could be TRUE ...  [consistent] prob of 1/3
    # (((A)(A or B)) 5)                                 ; 5 could be true
    # (((A ore B)(C and D)) 6)))                        ; 6. wholly independent [consistent]

# def test_illusions(
#      ((if there is a king then there is an ace ore if not there is a king then there is an ace)(there is an ace))
#      ((you have the bread ore comma you have the soup ore you have the salad)(you have the bread)
#       (you have the soup ore you have the salad))
#      ((albert is here or betty is here ore comma charlie is here or betty is here)
#       (not albert is here and not charlie is here)(betty is here))
#      ((king or ace ore comma queen or ace)(ace))
#      ((iff jack ore not queen then jack))
#      ((there is a nail or there is a bolt ore comma there is a bolt and there is a wrench)
#       (there is a nail and there is a bolt and there is a wrench))
#      ((red and square ore red))))
#
# (defvar *eight-cases* '(((if louvre in paris then he is married)         a) ; a. fact yields MP inference
#                       ((if not he is married then not louvre in paris) a) ; a. fact yield MT inference
#                       ((if wearing a shirt then wearing pants) b)         ; b. contingent
#                       ((if pouring then raining) c)                       ; c. true a priori
#                       ((if raining then pouring) d)                       ; d. modulated to biconditional but contingent
#                       ((not raining or not pouring) d)                    ; d. modulated to exclusve disjn but contingent
#                       ((if god exists then atheism is wrong) e)            ; e. modulated but true a priori
#                       ((iff god exists then atheism is right) f)          ; f. false a priori
#                        ))
#
# (defvar *disjunctions* '(
#                        ((louvre in paris or interested) a)                 ; a. fact
#                        ((not louvre in paris or interested) a)             ; a. fact yields inference
#                        ((interested or louvre in paris) a)                 ; a. fact
#                        ((interested or not louvre in paris) a)             ; a. fact yields inference
#                        ((trousers or shirts) b)                            ; b. contingent
#                        ((not trousers or shirts) b)                        ; b. contingent
#                        ((not interested or raining) b)                     ; b. contingent
#                        ((not interested or not raining) b)                 ; b. contingent
#                        ((not pouring or raining) c)                        ; c. true a priori
#                        ((not pouring or raining) c)                        ; c. true a priori
#                        ((not raining or pouring) d)                        ; d. modulated (iff rain pour) contingent
#                        ((not raining or not pouring) d)                    ; d. modulated contingent
#                        ((not pouring or not raining) d)                    ; d. modulated contingent
#                        ((not close or not near) d)                         ; d. modulated referring to -c & -n
#                        ((not close or near) e)                             ; e. modulated true a priori  (close v - close)
#                        ((god exists ore atheism is wrong) f)               ; f. false a priori
#                         ))
#
# (defvar *conditionals* '(
#                         ((if louvre in paris then shirts) a)         ; a. fact yields MP
#                         ((if not louvre in paris then interested) a) ; a. fact
#                         ((if interested then not louvre in Paris) a) ; a. fact yields MT
#                         ((if interested then louvre in Paris) a)     ; a. fact
#                         ((if trousers then shirts) b)                ; b. contingent
#                         ((if interested then raining) b)             ; b. contingent
#                         ((if interested then not raining) b)         ; b. contingent
#                         ((if pouring then raining) c)                ; c. true a priori
#                         ((iff god exists then atheism is wrong) e)   ; e. modulated but true a priori
#                         ((if raining then pouring) d)                ; d. modulated but contingent
#                         ((if raining then not pouring) d)            ; d. modulated but contingent
#                         ((if pouring then not raining) d)            ; d. modulated contingent refers to -p -r, and -p r
#                         ((if close then not near) d)                 ; d. modulated contingent refers to -close -near
#                         ((if close then near) e)                     ; e. modulated true a priori
#                         ((if god exists then atheism is wrong) e)    ; e. modulated but true a priori
#                         ((iff god exists then atheism is right) f)   ; f. false a priori
#                         ((iff close then not near) f)                ; f. false a priori
#                         ))
#
# (defvar *def-examples* '(
#    ((if poisonous snake bites then dies)(poisonous snake bites)(not dies))
#    ((if pull trigger then gun fires)(pull trigger)(not gun fires))))
#test_premise_pairings = [
#    ["A & ~A", []],
#    ["A | ~A", [['A'], ['¬A']]],
#    ["B", [['B']]],
#    ["A -> B", [['A', 'B']]],
#    ["~A", [['¬A']]],
#    ["A & B & C", [['A', 'B', 'C']]],
#    ["A -> (B & C)", [['A', 'B', 'C']]],
#    ["A & ~B", []],
#    ["A -> B", []],
#    ["A", []],
#    ["~B", []],
#    ["A | B", []],
#    ["A", []],
#    ["A | B", []],
#    ["B", []],
#    ["A | B", []],
#    ["A & B", []],
#    ["A", []],
#    ["A | B", []],
#    ["A | B", []],
#    ["C", []],
#    ["A", []],
#    ["A ^ B", []],
#    ["~B", []],
#    ["~A", []],
#    ["A ^ B", []],
#    ["B", []],
#    ["~A", []],
#    ["A | B", []],
#    ["B", []],
#    ["A | B", []],
#    ["~B", []],
#    ["A", []],
#    ["A | B", []],
#    ["~A", []],
#    ["~A & B & C", []],
#    ["A | B", []],
#    ["~B", []],
#    ["A & ~B", []],
#    ["A | B", []],
#    ["~A", []],
#    ["~B", []],
#    ["A ^ B", []],
#    ["A | B", []],
#    ["A | B", []],
#    ["A ^ B", []],
#]




if __name__ == "__main__":
    unittest.main()
