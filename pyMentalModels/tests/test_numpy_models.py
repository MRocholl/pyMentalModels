#!/usr/bin/python3


import unittest
import numpy as np
import numpy.testing as npt

from sympy import symbols
from sympy.logic.boolalg import And, Or, Xor, Implies, Equivalent, Not
# from itertools import product
from pyMentalModels.reasoner.numpy_reasoner import mental_model_builder


class NotSureThisIsRightError(NotImplementedError):
    """ Error that gets raised when Im not sure result is right"""


class TestNumpySimpleModels(unittest.TestCase):
    """ Class that tests behavior of all numpy model constructors of the logical operators
    """
    alpha_symbols = symbols("A B C D E F G")  # defining symbols

    def test_and(self):
        A, B = self.alpha_symbols[:2]
        expr = And(A, B)
        model = mental_model_builder(expr)
        npt.assert_allclose(model, np.array([[1., 1.]]))

    def test_or(self):
        A, B = self.alpha_symbols[:2]
        expr = Or(A, B)
        model = mental_model_builder(expr)
        npt.assert_allclose(
            model, np.array([[1., 0.],
                             [0., 1.],
                             [1., 1.]]))

    def test_A_or_A(self):
        A, B = self.alpha_symbols[:2]
        expr = Or(A, A)
        model = mental_model_builder(expr)
        npt.assert_allclose(model, np.array([[1.]]))

    def test_implies(self):
        A, B = self.alpha_symbols[:2]
        expr = Implies(A, B)
        model = mental_model_builder(expr)
        npt.assert_allclose(model, np.array([[1., 1.]]))

    def test_xor(self):
        A, B = self.alpha_symbols[:2]
        expr = Xor(A, B)
        model = mental_model_builder(expr)
        npt.assert_allclose(model, np.array([[1., 0.], [0., 1.]]))

    def test_equals(self):
        A, B = self.alpha_symbols[:2]
        expr = Equivalent(A, B)
        model = mental_model_builder(expr)
        npt.assert_allclose(model, np.array([[1., 1.]]))

    def test_not(self):
        A, B = self.alpha_symbols[:2]
        expr = Not(A)
        model = mental_model_builder(expr)
        npt.assert_allclose(model, np.array([[-1.]]))

    def test_not_A_and_B(self):
        A, B = self.alpha_symbols[:2]
        expr = And(Not(A), B)
        model = mental_model_builder(expr)
        npt.assert_allclose(model, np.array([[-1., 1.]]))

    def test_and_negA_negB(self):
        A, B = self.alpha_symbols[:2]
        expr = And(~A, ~B)
        model = mental_model_builder(expr)
        npt.assert_allclose(model, np.array([[-1., -1.]]))


class TestComposedModels(unittest.TestCase):

    alpha_symbols = symbols("A B C D E F G")  # defining symbols

    def test_print_long_example(self):
        A, B, C, D, E, F, G = self.alpha_symbols
        expr = And(A, Or(B, C), Xor(D, E))
        model = mental_model_builder(expr)
        npt.assert_allclose(
            model,
            np.array(
                [[1.0, 1.0, 0.0, 1.0, 0.0],
                 [1.0, 1.0, 0.0, 0.0, 1.0],
                 [1.0, 0.0, 1.0, 1.0, 0.0],
                 [1.0, 0.0, 1.0, 0.0, 1.0],
                 [1.0, 1.0, 1.0, 1.0, 0.0],
                 [1.0, 1.0, 1.0, 0.0, 1.0]]
            )
        )

    def test_B_in_or_xor(self):
        A, B, C, D = symbols("A B C D")
        expr = And(A, Or(B, C), Xor(B, D))
        model = mental_model_builder(expr)
        npt.assert_allclose(
            model,
            np.array([[1.0, 2.0, 0.0, 0.0],
                      [1.0, 2.0, 1.0, 0.0],
                      [1.0, 1.0, 1.0, 0.0],
                      [1.0, 1.0, 0.0, 1.0],
                      [1.0, 0.0, 1.0, 1.0],
                      [1.0, 1.0, 1.0, 1.0]])
        )
        raise NotSureThisIsRightError("Xor and Or might conflict")

    def test_A_and_B_XOR_B_and_C(self):
        A, B, C, D = symbols("A B C D")
        expr = Xor(And(A, B), And(B, C))
        model = mental_model_builder(expr)
        print("this is is the interesting part", model)
        npt.assert_allclose(
            model,
            np.array(
                [[1., 1., 0.],
                 [0., 1., 1.],
                 [1., 2., 1.]]))
        raise NotSureThisIsRightError("Xor and Or might conflict")

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


if __name__ == "__main__":
    unittest.main()
