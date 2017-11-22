#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import unittest

# Package related imports
from pyMentalModels.parsing.modal_parser import parse_expr, sympify_formatter
from pyMentalModels.logical_connectives.operators import explicit_op, intuit_op


expressions = [
    "(<> Hund | <> Katze) -> ([] Tier & [] Lebewesen)",
    "Bread ^ Butter ^ Salad",
]  # To be exported to own submodule at later point /tests

parsed_expressions = [
    [[['<>', 'Hund'], '|', ['<>', 'Katze']], '->', [['[]', 'Tier'], '&', ['[]', 'Lebewesen']]],
    ['Bread', '^', 'Butter', '^', 'Salad'],
    # other parsed expressions to be added here
]

premise_pairs = [
    "<> A, A -> B",
    "A, A -> <> B",
    "<> C, A -> B",
    "[] A, A -> B",
    "A, A -> B",
    "[]A -> B",
    "A, <>(A -> B)",
    "<>A, <>(A -> B)",
    "C, <>(A -> B)",
    "A, [](A -> B)",
    "[]A, [](A -> B)",
    "C, [](A -> B)",
    # further premise pairings to be added here
]

tests_parsing = {
    "<>A": ['<>', 'A'],
    "A -> B": ['A', '->', 'B'],
    "A -> <>B": ['A', '->', ['<>', 'B']],
    "[]A": ['[]', 'A'],
    "[]A -> B": [['[]', 'A'], '->', 'B'],
    "<>(A -> B)": ['<>', ['A', '->', 'B']],
    "[](A -> B)": ['[]', ['A', '->', 'B']],
    # further premise pairings to be added here
    "(<> Hund | <> Katze) -> ([] Tier & [] Lebewesen)": [[['<>', 'Hund'], '|', ['<>', 'Katze']], '->', [['[]', 'Tier'], '&', ['[]', 'Lebewesen']]],
    "Bread ^ Butter ^ Salad": ['Bread', '^', 'Butter', '^', 'Salad'],

}


tests_parsing_non_dyadic = {
    "A | B | C | D": ['A', '|', 'B', '|', 'C', '|', 'D'],
    "(A ^ B) & C": [['A', '^', 'B'], '&', 'C'],
    # further premise pairings to be added here
}

test_formatting_expr_R_full = {
    "Possibly(A)": ['<>', 'A'],
    "Implies(A, B)": ['A', '->', 'B'],
    "Implies(A, Possibly(B))": ['A', '->', ['<>', 'B']],
    "Necessary(A)": ['[]', 'A'],
    "Implies(Necessary(A), B)": [['[]', 'A'], '->', 'B'],
    "Possibly(Implies(A, B))": ['<>', ['A', '->', 'B']],
    "Necessary(Implies(A, B))": ['[]', ['A', '->', 'B']],
    # further premise pairings to be added here
}

test_formatting_expr_R_intuit = {
    "Possibly(A)": ['<>', 'A'],
    "And(A, B)": ['A', '->', 'B'],
    "And(A, Possibly(B))": ['A', '->', ['<>', 'B']],
    "Necessary(A)": ['[]', 'A'],
    "And(Necessary(A), B)": [['[]', 'A'], '->', 'B'],
    "Possibly(And(A, B))": ['<>', ['A', '->', 'B']],
    "Necessary(And(A, B))": ['[]', ['A', '->', 'B']],
    # further premise pairings to be added here
}


class TestParse(unittest.TestCase):

    def test_parsing_modal_expressions(self):
        for premise, due in tests_parsing.items():
            parsed_premise = parse_expr(premise).asList()
            self.assertEqual(parsed_premise, due)

    def test_parsing_logical_expression_non_dyadic(self):
        for premise, due in tests_parsing_non_dyadic.items():
            parsed_premise = parse_expr(premise).asList()
            self.assertEqual(parsed_premise, due)

    def test_A_and_BorC_and_DxorE(self):
        parsed_premise = parse_expr("A & (B | C) & (D ^ E)").asList()
        self.assertEqual(parsed_premise, ['A', '&', ['B', '|', 'C'], '&', ['D', '^', 'E']])


class TestFormatter(unittest.TestCase):

    def test_formatting_expression_R_full(self):
        for due, parsed_expr in test_formatting_expr_R_full.items():
            self.assertEqual(sympify_formatter(parsed_expr, explicit_op), due)

    def test_formatting_expression_R_intuit(self):
        for due, parsed_expr in test_formatting_expr_R_intuit.items():
            self.assertEqual(sympify_formatter(parsed_expr, intuit_op), due)


if __name__ == "__main__":
    unittest.main()
