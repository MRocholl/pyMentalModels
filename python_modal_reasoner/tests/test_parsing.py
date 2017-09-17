#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import unittest

# Package related imports
from parsing.modal_parser import parse_expr, sympify_formatter
from logical_connectives.operators import op_names, intuit_op


tests_parsing = {
    "<>A": ['<>', 'A'],
    "A -> B": ['A', '->', 'B'],
    "A -> <>B": ['A', '->', ['<>', 'B']],
    "[]A": ['[]', 'A'],
    "[]A -> B": [['[]', 'A'], '->', 'B'],
    "<>(A -> B)": ['<>', ['A', '->', 'B']],
    "[](A -> B)": ['[]', ['A', '->', 'B']],
    # further premise pairings to be added here

}

tests_parsing_non_dyadic = {
    "A | B | C | D": ['A', '|', 'B', '|', 'C', '|', 'D'],
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


class TestFormatter(unittest.TestCase):

    def test_formatting_expression_R_full(self):
        for due, parsed_expr in test_formatting_expr_R_full.items():
            self.assertEqual(sympify_formatter(parsed_expr, op_names), due)

    def test_formatting_expression_R_intuit(self):
        for due, parsed_expr in test_formatting_expr_R_intuit.items():
            self.assertEqual(sympify_formatter(parsed_expr, intuit_op), due)


if __name__ == "__main__":
    unittest.main()
