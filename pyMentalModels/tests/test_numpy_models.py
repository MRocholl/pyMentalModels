#!/usr/bin/python3


import unittest

from sympy import sympify, symbols
from sympy.logic.boolalg import And, Or, Xor, Implies, Equivalent, Not
from itertools import product
from pyMentalModels.reasoner.numpy_reasoner import builder


class TestNumpyModels(unittest.TestCase):
    """ Class that tests behavior of all numpy model constructors of the logical operators
    """
    alpha_symbols = symbols("A B C D E F G")  # defining symbols

    def test_and(self):
        A, B = self.alpha_symbols[:2]
        expr = And(A, B)
        print(builder(expr))

    def test_or(self):
        A, B = self.alpha_symbols[:2]
        expr = Or(A, B)
        print(builder(expr))

    def test_implies(self):
        A, B = self.alpha_symbols[:2]
        expr = Implies(A, B)
        print(builder(expr))

    def test_xor(self):
        A, B = self.alpha_symbols[:2]
        expr = Xor(A, B)
        print(builder(expr))

    def test_equals(self):
        A, B = self.alpha_symbols[:2]
        expr = Equivalent(A, B)
        print(builder(expr))

    def test_not(self):
        A, B = self.alpha_symbols[:2]
        expr = Not(A)
        print(builder(expr))

    def test_all_variations_neg_pos_connectives_sys1(self):
        """ Test behavior for one junctor"""
        A, B, C, D, E, F, G = symbols("A B C D E F G")  # defining symbols
        print("Testing behavior for one junctor system 1")
        for operator in (And, Or, Xor):
            for valuations in product([0, 1], repeat=2):
                first_arg, sec_arg = [~atom if value == 0 else atom for atom, value in zip([A, B], valuations)]
                log_obj = operator(first_arg, sec_arg)
                print(log_obj)
                print("-------")
                for el in builder(log_obj):
                    print(el)
                print()

    def test(self):
        A, B, C = symbols("A B C")
        exp = Or(A, ~B, C)
        print(exp)
        for model in builder(exp):
            print(list(chr(97 + i) if el == 1. else "" if el == 0 else "-{}".format(chr(97 + i)) if el == -1 else "" for i, el in enumerate(model)))
    # print(builder(Or(A, B, C)))
#    def test_all_variations_neg_pos_connectives_sys2(self):
#        """ Test behavior for one junctor"""
#
#        A, B = symbols("A B")  # defining symbols
#        print("Testing behavior for one junctor system 2")
#        for operator in (And, Or, Xor, Implies, Equivalent):
#            for valuations in product([0, 1], repeat=2):
#                first_arg, sec_arg = [~atom if value == 0 else atom for atom, value in zip([A, B], valuations)]
#                log_obj = operator(first_arg, sec_arg)
#                print(log_obj)
#                print("-------")
#                for el in sr.generate_possible_models(log_obj, intuitive=False):
#                    print(el)
#                print()
#
#    def test_all_dual_variations_sys1(self):
#        """ Test behavior for combinations of two junctors"""
#        A, B, C = symbols("A B C")
#        print("Testing behavior for two junctors system 1")
#        for first, second in product([And, Or, Xor], repeat=2):
#            for valuations in product([0, 1], repeat=3):
#                first_arg, sec_arg, thrd_arg = [~atom if value == 0 else atom for atom, value in zip([A, B, C], valuations)]
#                log_obj = first(first_arg, second(sec_arg, thrd_arg))
#                print(log_obj)
#                print("-------")
#                for el in sr.generate_possible_models(log_obj, intuitive=True):
#                    print(el)
#                print()
#
#    def test_all_dual_variations_sys2(self):
#        """ Test behavior for combinations of two junctors"""
#        A, B, C = symbols("A B C")
#        print("Testing behavior for two junctors system 2")
#        for first, second in product([And, Or, Xor, Implies, Equivalent, clc.MulXor], repeat=2):
#            for valuations in product([0, 1], repeat=3):
#                first_arg, sec_arg, thrd_arg = [~atom if value == 0 else atom for atom, value in zip([A, B, C], valuations)]
#                log_obj = first(first_arg, second(sec_arg, thrd_arg))
#                print(log_obj)
#                print("-------")
#                for el in sr.generate_possible_models(log_obj, intuitive=False):
#                    print(el)
#                print()
#
#    def test_logical_connectives_implicit(self):
#        for premise_pairings in test_premise_pairings:
#            for premise in premise_pairings:
#                print(premise)
#                formatted_prem = mp.sympify_formatter(mp.parse_expr(premise), op.intuit_op)
#                sympified_expression = sympify(formatted_prem)
#                possible_models = sr.generate_possible_models(sympified_expression, intuitive=True)
#                print(possible_models)
#
#    def test_logical_connectives_explicit(self):
#        for premise_pairings in test_premise_pairings:
#            for premise in premise_pairings:
#                print(premise)
#                formatted_prem = mp.sympify_formatter(mp.parse_expr(premise), op.explicit_op)
#                sympified_expression = sympify(formatted_prem)
#                possible_models = sr.generate_possible_models(sympified_expression, intuitive=False)
#                print(possible_models)
#
