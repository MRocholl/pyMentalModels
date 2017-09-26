import sympy
import unittest

# Package related imports
from pyMentalModels.reasoner.sympy_reasoner import generate_possible_models

# Sympy imports
# from sympy.logic.boolalg import Not, Or, And, Xor, Implies, BooleanFunction, truth_table
from sympy.logic.boolalg import truth_table
from sympy.core.sympify import sympify


class TestSimple(unittest.TestCase):
    def test_simple_implicit_cases(self):

        # Configuring boolean operators to behave intuitively
        sympy.boolalg.Implies = sympy.boolalg.And

        tests = {
            "Implies(Or(A, B), C)": ['C A', 'B C', 'B C A'],
            # XXX More inputs
        }

        def make_set_wise(models):
            return {frozenset(el.split()) for el in models}

        for inp, soll in tests.items():
            expr = sympify(inp, locals={})
            print(expr)
            atoms = expr.atoms()
            premise_possible_models = generate_possible_models(atoms, truth_table(expr, atoms), explicit=False)
            print("Extracted possible world for premise {}:\t ".format(inp), premise_possible_models, "\n")
            self.assertEqual(make_set_wise(premise_possible_models), make_set_wise(soll))


if __name__ == "__main__":
    unittest.main()
