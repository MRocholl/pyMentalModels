#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
import unittest

import numpy as np
import numpy.testing as npt

from pyMentalModels.modal_parser import parse_format
from pyMentalModels.constants import POS_VAL, IMPL_NEG, EXPL_NEG
from pyMentalModels.numpy_reasoner import mental_model_builder, Insight
from pyMentalModels.infer import infer, InferenceTask
from pyMentalModels.pretty_printing import pretty_print_atom_assign


def _infer(expressions, mode):

    sympified_expressions = [
        parse_format(expr)
        for expr in expressions
    ]
    print(sympified_expressions)

    models = []
    for sympified_expression in sympified_expressions:
        print("The expression to be evaluated is: {}".format(sympified_expression))
        model = mental_model_builder(sympified_expression, mode)
        print(model)
        models.append(model)
        print("The mental model that has been created is:")
        for possible_world in model.model:
            print(pretty_print_atom_assign(model.atoms_model, possible_world, mode))

    result = infer(models)
    for possible_world in result.model:
            print(possible_world)
            print(pretty_print_atom_assign(result.atoms_model, possible_world, mode))


def _eval_expr(expressions, mode):
    # Does the right thing
    result = infer([mental_model_builder(parse_format(expr), mode) for expr in expressions], InferenceTask.FOLLOWS)
    return result.model


class TestLispCases(unittest.TestCase):
    def test_basic_cases(self):
        """
        1 A AND NOT A.

        This premise is a self-contradiction.
        The models of premise 1 represent:  Null model.
        Number of models constructed equals 0
        """
        npt.assert_array_equal(mental_model_builder(parse_format("a & ~a"), Insight.INTUITIVE).model, np.array([[]]))

        """
        2 A OR NOT A.

        The models of premise 1 represent:
            A {T2 (((A)))}
          ¬ A {T1 (((- A)))}
        Number of models constructed equals 2

        """
        npt.assert_array_equal(mental_model_builder(parse_format("a | ~a"), Insight.INTUITIVE).model, np.array([[POS_VAL], [EXPL_NEG]]))

        """
        3 B. IF A THEN B.

        The models of premise 1 represent:
            B
        The models of premise 2 represent:
            A    B
                   {T3 (((- A)))}
        Premise 2 is POSSIBLE given previous premise or premises, and vice versa [consistent].  Premises so far yield models of only one possible outcome:-
          B, and  A.
        Number of models constructed equals 3

        """
        npt.assert_array_equal(_eval_expr(["b", "a -> b"], Insight.INTUITIVE), np.array([[POS_VAL, POS_VAL]]))

        """

        4 NOT A. IF A THEN B.

        The models of premise 1 represent:
          ¬ A
        The models of premise 2 represent:
            A    B
                   {T4 (((- A)))}
        Premise 2 suggests no intuitive conclusion. Premises so far yield models of only one possible outcome:-
         NOT A, and  T4.
        Number of models constructed equals 3

        """

        npt.assert_array_equal(_eval_expr(["~a", "a -> b"], Insight.INTUITIVE), np.array([[]]))

        """

        5 A. IF A THEN B. B.

        The models of premise 1 represent:
            A
        The models of premise 2 represent:
            A    B
                   {T5 (((- A)))}
        Premise 2 is POSSIBLE given previous premise or premises, and vice versa [consistent].  Premises so far yield models of only one possible outcome:-
          A, and  B.
        The models of premise 3 represent:
            B
        Premise 3 FOLLOWS from previous premise or premises [valid].  Premises so far yield models of only one possible outcome:-
          A, and  B.
        Number of models constructed equals 5

        """
        npt.assert_array_equal(_eval_expr(["a", "a -> b", "b"], Insight.INTUITIVE), np.array([[POS_VAL, POS_VAL]]))
        """

        6 A. IF A THEN B. A AND B AND C.

        The models of premise 1 represent:
            A
        The models of premise 2 represent:
            A    B
                   {T6 (((- A)))}
        Premise 2 is POSSIBLE given previous premise or premises, and vice versa [consistent].  Premises so far yield models of only one possible outcome:-
          A, and  B.
        The models of premise 3 represent:
            A    B    C
        Premise 3 is POSSIBLE given previous premise or premises, and vice versa [consistent].  Premises so far yield models of only one possible outcome:-
          A,  B, and  C.
        Number of models constructed equals 5

        """

        npt.assert_array_equal(_eval_expr(["a", "a -> b", "a & b & c"], Insight.INTUITIVE), np.array([[POS_VAL, POS_VAL, POS_VAL]]))

        """

        7 A. IF A THEN COMMA B AND C. A AND B AND C.

        The models of premise 1 represent:
            A
        The models of premise 2 represent:
            A    B    C
                        {T7 (((- A)))}
        Premise 2 is POSSIBLE given previous premise or premises, and vice versa [consistent].  Premises so far yield models of only one possible outcome:-
          A,  B, and  C.
        The models of premise 3 represent:
            A    B    C
        Premise 3 FOLLOWS from previous premise or premises, and vice versa [mutually valid].  Premises so far yield models of only one possible outcome:-
          A,  B, and  C.
        Number of models constructed equals 5

        """
        npt.assert_array_equal(_eval_expr(["a", "a -> (b & c)", "a & b & c"], Insight.INTUITIVE), np.array([[POS_VAL, POS_VAL, POS_VAL]]))
        """

        8 A. IF A THEN B. B AND A.

        The models of premise 1 represent:
            A
        The models of premise 2 represent:
            A    B
                   {T8 (((- A)))}
        Premise 2 is POSSIBLE given previous premise or premises, and vice versa [consistent].  Premises so far yield models of only one possible outcome:-
          A, and  B.
        The models of premise 3 represent:
            B    A
        Premise 3 FOLLOWS from previous premise or premises, and vice versa [mutually valid].  Premises so far yield models of only one possible outcome:-
          A, and  B.
        Number of models constructed equals 5

        """

        npt.assert_array_equal(_eval_expr(["a", "a -> b", "b & a"], Insight.INTUITIVE), np.array([[POS_VAL, POS_VAL]]))
        """

        9 IF A THEN B. A AND NOT B.

        The models of premise 1 represent:
            A    B
                   {T9 (((- A)))}
        The models of premise 2 represent:
            A  ¬ B
        Premise 2 is IMPOSSIBLE given the previous premise or premises, and vice versa [inconsistent].  Premises so far yield models of 0 possibilities:- Null model.
        Number of models constructed equals 2

        """

        """

        10 IF A THEN B. A. NOT B.

        The models of premise 1 represent:
            A    B
                   {T10 (((- A)))}
        The models of premise 2 represent:
            A
        Premise 2 is CONSISTENT with previous premise or premises, and vice versa. Premises so far yield models of only one possible outcome:-
          A, and  B.
        The models of premise 3 represent:
          ¬ B
        Premise 3 is IMPOSSIBLE given the previous premise or premises, and vice versa [inconsistent].  Premises so far yield models of 0 possibilities:- Null model.
        Number of models constructed equals 4

        """

        """

        11 A OR B. A.

        The models of premise 1 represent:
            A      {T12 (((- B)))}
                 B {T11 (((- A)))}
            A    B
        The models of premise 2 represent:
            A
        Premise 2 is CONSISTENT with previous premise or premises, and vice versa. Premises so far yield models of 3 possibilities:-
            A      {T12 (((- B)))}
            A    B {T11 (((- A)))}
            A    B
        Number of models constructed equals 7

        """

        """

        12 A OR B. B.

        The models of premise 1 represent:
            A      {T14 (((- B)))}
                 B {T13 (((- A)))}
            A    B
        The models of premise 2 represent:
            B
        Premise 2 is CONSISTENT with previous premise or premises, and vice versa. Premises so far yield models of 3 possibilities:-
            A    B {T14 (((- B)))}
                 B {T13 (((- A)))}
            A    B
        Number of models constructed equals 7

        """

        """

        13 A OR B. A AND B.

        The models of premise 1 represent:
            A      {T16 (((- B)))}
                 B {T15 (((- A)))}
            A    B
        The models of premise 2 represent:
            A    B
        Premise 2 is CONSISTENT with previous premise or premises, and vice versa. Premises so far yield models of 3 possibilities:-
            A    B {T16 (((- B)))}
            A    B {T15 (((- A)))}
            A    B
        Number of models constructed equals 7

        """

        """

        14 A. A OR B.

        The models of premise 1 represent:
            A
        The models of premise 2 represent:
            A      {T18 (((- B)))}
                 B {T17 (((- A)))}
            A    B
        Premise 2 is POSSIBLE given previous premise or premises, and vice versa [consistent].  Premises so far yield models of 3 possibilities:-
            A      {T18 (((- B)))}
            A    B {T17 (((- A)))}
            A    B
        Number of models constructed equals 7

        """

        """

        15 A OR B. C.

        The models of premise 1 represent:
            A      {T20 (((- B)))}
                 B {T19 (((- A)))}
            A    B
        The models of premise 2 represent:
            C
        Premise 2 is wholly independent of previous premises [consistent].  Premises so far yield models of 3 possibilities:-
            A    C      {T20 (((- B)))}
                 C    B {T19 (((- A)))}
            A    C    B
        Number of models constructed equals 7

        """

        """

        16 A. A ORE B. NOT B.

        The models of premise 1 represent:
            A
        The models of premise 2 represent:
            A      {T22 (((- B)))}
                 B {T21 (((- A)))}
        Premise 2 is POSSIBLE given previous premise or premises, and vice versa [consistent].  Premises so far yield models of 2 possibilities:-
            A      {T22 (((- B)))}
            A    B {T21 (((- A)))}
        The models of premise 3 represent:
          ¬ B
        Premise 3 suggests no intuitive conclusion. Premises so far yield models of only one possible outcome:-
          A,  T22, and NOT B.
        Number of models constructed equals 7

        """

        """

        17 NOT A. A ORE B. B.

        The models of premise 1 represent:
          ¬ A
        The models of premise 2 represent:
            A      {T24 (((- B)))}
                 B {T23 (((- A)))}
        Premise 2 suggests no intuitive conclusion. Premises so far yield models of only one possible outcome:-
         NOT A,  B, and  T23.
        The models of premise 3 represent:
            B
        Premise 3 FOLLOWS from previous premise or premises [valid].  Premises so far yield models of only one possible outcome:-
         NOT A,  B, and  T23.
        Number of models constructed equals 6

        """

        """

        18 NOT A. A OR B. B.

        The models of premise 1 represent:
          ¬ A
        The models of premise 2 represent:
            A      {T26 (((- B)))}
                 B {T25 (((- A)))}
            A    B
        Premise 2 suggests no intuitive conclusion. Premises so far yield models of only one possible outcome:-
         NOT A,  B, and  T25.
        The models of premise 3 represent:
            B
        Premise 3 FOLLOWS from previous premise or premises [valid].  Premises so far yield models of only one possible outcome:-
         NOT A,  B, and  T25.
        Number of models constructed equals 7

        """


        """

        19 A OR B. NOT B. A.

        The models of premise 1 represent:
            A      {T28 (((- B)))}
                 B {T27 (((- A)))}
            A    B
        The models of premise 2 represent:
          ¬ B
        Premise 2 suggests no intuitive conclusion. Premises so far yield models of only one possible outcome:-
          A,  T28, and NOT B.
        The models of premise 3 represent:
            A
        Premise 3 FOLLOWS from previous premise or premises [valid].  Premises so far yield models of only one possible outcome:-
          A,  T28, and NOT B.
        Number of models constructed equals 7

        """

        """

        20 A OR B. NOT A. NOT A AND B AND C.

        The models of premise 1 represent:
            A      {T30 (((- B)))}
                 B {T29 (((- A)))}
            A    B
        The models of premise 2 represent:
          ¬ A
        Premise 2 suggests no intuitive conclusion. Premises so far yield models of only one possible outcome:-
          B,  T29, and NOT A.
        The models of premise 3 represent:
          ¬ A    B    C
        Premise 3 suggests no intuitive conclusion. Premises so far yield models of only one possible outcome:-
          B,  T29, NOT A, and  C.
        Number of models constructed equals 7

        """

        """

        21 A OR B. NOT B. A AND NOT B.

        The models of premise 1 represent:
            A      {T32 (((- B)))}
                 B {T31 (((- A)))}
            A    B
        The models of premise 2 represent:
          ¬ B
        Premise 2 suggests no intuitive conclusion. Premises so far yield models of only one possible outcome:-
          A,  T32, and NOT B.
        The models of premise 3 represent:
            A  ¬ B
        Premise 3 FOLLOWS from previous premise or premises [valid].  Premises so far yield models of only one possible outcome:-
          A,  T32, and NOT B.
        Number of models constructed equals 7

        """

        """

        22 A OR B. NOT A. NOT B.

        The models of premise 1 represent:
            A      {T34 (((- B)))}
                 B {T33 (((- A)))}
            A    B
        The models of premise 2 represent:
          ¬ A
        Premise 2 suggests no intuitive conclusion. Premises so far yield models of only one possible outcome:-
          B,  T33, and NOT A.
        The models of premise 3 represent:
          ¬ B
        Premise 3 is IMPOSSIBLE given the previous premise or premises, and vice versa [inconsistent].  Premises so far yield models of 0 possibilities:- Null model.
        Number of models constructed equals 6

        """

        """

        23 A ORE B. A OR B.

        The models of premise 1 represent:
            A      {T36 (((- B)))}
                 B {T35 (((- A)))}
        The models of premise 2 represent:
            A      {T38 (((- B)))}
                 B {T37 (((- A)))}
            A    B
        Premise 2 suggests no intuitive conclusion. Premises so far yield models of 6 possibilities:-
            A      {T36 (((- B)))} {T38 (((- B)))}
            A    B {T37 (((- A)))} {T36 (((- B)))}
            A    B {T36 (((- B)))}
            A    B {T35 (((- A)))} {T38 (((- B)))}
                 B {T37 (((- A)))} {T35 (((- A)))}
            A    B {T35 (((- A)))}
        Number of models constructed equals 11

        """

        """

        24 A OR B. A ORE B.

        The models of premise 1 represent:
            A      {T40 (((- B)))}
                 B {T39 (((- A)))}
            A    B
        The models of premise 2 represent:
            A      {T42 (((- B)))}
                 B {T41 (((- A)))}
        Premise 2 suggests no intuitive conclusion. Premises so far yield models of 6 possibilities:-
            A      {T40 (((- B)))} {T42 (((- B)))}
            A    B {T41 (((- A)))} {T40 (((- B)))}
            A    B {T39 (((- A)))} {T42 (((- B)))}
                 B {T41 (((- A)))} {T39 (((- A)))}
            A    B {T42 (((- B)))}
            A    B {T41 (((- A)))}
        Number of models constructed equals 11
        """
