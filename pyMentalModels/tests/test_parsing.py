#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import unittest

# Package related imports
from pyMentalModels.parsing.modal_parser import parse_expr, sympify_formatter
from pyMentalModels.logical_connectives.operators import op_names, intuit_op


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


class TestFormatter(unittest.TestCase):

    def test_formatting_expression_R_full(self):
        for due, parsed_expr in test_formatting_expr_R_full.items():
            self.assertEqual(sympify_formatter(parsed_expr, op_names), due)

    def test_formatting_expression_R_intuit(self):
        for due, parsed_expr in test_formatting_expr_R_intuit.items():
            self.assertEqual(sympify_formatter(parsed_expr, intuit_op), due)


from sympy.logic.boolalg import And, Or, Xor, Implies, sympify
# from pyMentalModels.parsing.modal_parser import parse_expr, sympify_formatter
# from pyMentalModels.reasoner.reasoner import populate_np_array
# from pyMentalModels.data.expressions import expressions, parsed_expressions
# from pyMentalModels.logical_connectives.operators import op_names

DEBUG = True

cat_dog_expr, triv_ragni_ex = parsed_expressions


#  Sympify formatter (transforms list to string that is sympify-readable) {{{ #



sympify_ready_triv_expr = sympify_formatter(triv_ragni_ex, op_names)
sympify_ready_cat_dog_expr = sympify_formatter(cat_dog_expr, op_names)
sympified_expr_triv = sympify(sympify_ready_triv_expr)
sympified_expr_pars = sympify(sympify_ready_cat_dog_expr)
#  }}} Sympify formatter (transforms list to string that is sympify-readable) #


if DEBUG:
    print("sympify_ready_triv_expr\t", sympify_ready_triv_expr)
    print("sympify_ready_cat_dog_expr\t", sympify_ready_cat_dog_expr)
    print()
    print("The outer-most junctor is of type: ", type(sympified_expr_triv))
    print("The atoms are: ", sympified_expr_triv.atoms())
    print("The outer-most junctor is of type: ", type(sympified_expr_pars))
    print("The atoms are: ", sympified_expr_pars.atoms())

    """
    print(combs)
    for combination in combs:
        for term, value in truth_table(sympified_expr, combination):
            print(term, value)
    """

possible, necessary, possible_models = populate_np_array(sympified_expr_triv)

if DEBUG:
    print()
    print("The modal possible valuations of the atoms are: ", possible)
    print("The modal necessary valuations of the atoms are: ", necessary)
    print("The possible worlds are: \n", possible_models)






if __name__ == "__main__":
    unittest.main()
