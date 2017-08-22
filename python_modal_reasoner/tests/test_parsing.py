#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import unittest

# Package related imports
from parsing.modal_parser import parse_expr, sympify_formatter
from logical_connectives.operators import op_names

# Sympy imports
from sympy.core.sympify import sympify

from collections import defaultdict

tests = {
                "<>A": ['<>', 'A'],
                "A -> B": ['A', '->', 'B'],
                "A -> <>B": ['A', '->', ['<>', 'B']],
                "[]A": ['[]', 'A'],
                "[]A -> B": [['[]', 'A'], '->', 'B'],
                "<>(A -> B)": ['<>', ['A', '->', 'B']],
                "[](A -> B)": ['[]', ['A', '->', 'B']],
                # further premise pairings to be added here
    }

class TestParse(unittest.TestCase):
    def test_parsing_expressions(self):
        for premise, due in tests.items():
            print(premise)
            parsed_premise = parse_expr(premise).asList()
            self.assertEqual(parsed_premise, due)

if __name__ == "__main__":
    unittest.main()


