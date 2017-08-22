import sympy
import unittest

# Package related imports
from python_modal_reasoner import possible_worlds
from parsing.modal_parser import parse_expr, sympify_formatter

# Sympy imports
# from sympy.logic.boolalg import Not, Or, And, Xor, Implies, BooleanFunction, truth_table
from sympy.logic.boolalg import truth_table
from sympy.core.sympify import sympify



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

class TestParse(unittest.TestCase):
    def test_parsing_expressions(self):
        tests = {





                }

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
            premise_possible_worlds = possible_worlds(atoms, truth_table(expr, atoms), explicit=False)
            print("Extracted possible world for premise {}:\t ".format(inp), premise_possible_worlds, "\n")
            self.assertEqual(make_set_wise(premise_possible_worlds), make_set_wise(soll))



if __name__ == "__main__":
    unittest.main()



"""Collection of iteresting cases to looked at at later points
Raphael is in Tacoma or else Julia is in Atlanta, but not both.
Julia is in Atlanta or else Paul is in Philadelphia, but not both.

A xor B
B xor C

--> A and C or B

# ((ALL A ARE B) (ALL B ARE C))
# [A]  [B]   C
# [A]  [B]   C
# ALL A ARE C  ALL C ARE A
# ADDS
# [A]  [B]   C
# [A]  [B]   C
#            C
# ALL A ARE C  SOME C ARE A
#
# ((ALL A ARE B) (SOME B ARE C))
# [A]   B    C
# [A]   B
#            C
# SOME A ARE C  SOME C ARE A
# BREAKS
# [A]   B
#       B    C
# [A]   B
#            C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((ALL A ARE B) (NO B ARE C))
# [A]  [B]  -C
# [A]  [B]  -C
#           [C]
#           [C]
# NO A ARE C  NO C ARE A
#
# ((ALL A ARE B) (SOME B ARE NOT C))
# [A]   B   -C
# [A]   B   -C
#            C
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
# [A]   B    C
# [A]   B    C
#       B   -C
#       B   -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME A ARE B) (ALL B ARE C))
#  A   [B]   C
#  A
#      [B]   C
# SOME A ARE C  SOME C ARE A
#
# ((SOME A ARE B) (SOME B ARE C))
#  A    B    C
#  A
#       B
#            C
# SOME A ARE C  SOME C ARE A
# BREAKS
#  A    B
#       B    C
#  A
#       B
#            C
# NO VALID CONCLUSION  NO VALID CONCLUSION

# ((SOME A ARE B) (NO B ARE C))
# A   [B]  -C
# A
#     [B]  -C
#          [C]
#          [C]
# NO A ARE C  NO C ARE A
# MOVES
# A        [C]
# A   [B]  -C
#      [B]  -C
#           [C]
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
# A        [C]
# A   [B]  -C
#     [B]  -C
# A        [C]
# SOME A ARE NOT C  NO VALID CONCLUSION
#
# ((SOME A ARE B) (SOME B ARE NOT C))
# A    B   -C
# A
#      B   -C
#           C
#           C
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
# A         C
# A    B    C
#      B   -C
#      B   -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((NO A ARE B) (ALL B ARE C))
# [A]  -B
# [A]  -B
#      [B]   C
#      [B]   C
# NO A ARE C  NO C ARE A
# ADDS-TO-NEGMODEL
# [A]  -B    C
# [A]  -B
#      [B]   C
#      [B]   C
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
# [A]  -B    C
# [A]  -B    C
#      [B]   C
#      [B]   C
# NO VALID CONCLUSION  SOME C ARE NOT A
#
# ((NO A ARE B) (SOME B ARE C))
# [A]  -B
# [A]  -B
#      [B]   C
#      [B]
#            C
# NO A ARE C  NO C ARE A
# ADDS-TO-NEGMODEL
# [A]  -B    C
# [A]  -B
#      [B]   C
#      [B]
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
# [A]  -B    C
# [A]  -B    C
#      [B]   C
#      [B]
#            C
# NO VALID CONCLUSION  SOME C ARE NOT A
#
# ((NO A ARE B) (NO B ARE C))
# [A]  -B
# [A]  -B
#      [B]  -C
#      [B]  -C
#           [C]
#           [C]
# NO A ARE C  NO C ARE A
# MOVES
# [A]  -B   [C]
# [A]  -B   [C]
#      [B]  -C
#      [B]  -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((NO A ARE B) (SOME B ARE NOT C))
# [A]  -B
# [A]  -B
#      [B]  -C
#      [B]  -C
#            C
#            C
# NO A ARE C  NO C ARE A
# MOVES
# [A]  -B    C
# [A]  -B
#      [B]  -C
#      [B]  -C
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
# [A]  -B    C
# [A]  -B    C
#      [B]  -C
#      [B]  -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME A ARE NOT B) (ALL B ARE C))
#  A   -B
#  A   -B
#      [B]   C
#      [B]   C
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
#  A   -B    C
#  A   -B    C
#  A   [B]   C
#  A   [B]   C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME A ARE NOT B) (SOME B ARE C))
#  A   -B
#  A   -B
#       B    C
#       B
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
#  A   -B    C
#  A   -B    C
#  A    B    C
#       B
#  A         C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME A ARE NOT B) (NO B ARE C))
# A   -B
# A   -B
#     [B]  -C
#     [B]  -C
#          [C]
#          [C]
# NO A ARE C  NO C ARE A
# MOVES
# A   -B   [C]
# A   -B
#     [B]  -C
#     [B]  -C
#          [C]
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
# A   -B   [C]
# A   -B   [C]
#     [B]  -C
#     [B]  -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME A ARE NOT B) (SOME B ARE NOT C))
# A   -B
# A   -B
#      B   -C
#      B   -C
#           C
#           C
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
# A   -B    C
# A   -B    C
#      B   -C
#      B   -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((ALL B ARE A) (ALL C ARE B))
# [C]  [B]   A
# [C]  [B]   A
# ALL C ARE A  ALL A ARE C
# ADDS
# [C]  [B]   A
# [C]  [B]   A
#           A
# ALL C ARE A  SOME A ARE C
#
# ((ALL B ARE A) (SOME C ARE B))
# C   [B]   A
# C
#     [B]   A
# SOME C ARE A  SOME A ARE C
#
# ((ALL B ARE A) (NO C ARE B))
# [C]  -B
# [C]  -B
#      [B]   A
#      [B]   A
# NO C ARE A  NO A ARE C
# ADDS-TO-NEGMODEL
# [C]  -B    A
# [C]  -B
#     [B]   A
#     [B]   A
# SOME C ARE NOT A  SOME A ARE NOT C
# ADDS-TO-NEGMODEL
# [C]  -B    A
# [C]  -B    A
#     [B]   A
#     [B]   A
# NO VALID CONCLUSION  SOME A ARE NOT C
#
# ((ALL B ARE A) (SOME C ARE NOT B))
# C   -B
# C   -B
#     [B]   A
#     [B]   A
# SOME C ARE NOT A  SOME A ARE NOT C
# ADDS-TO-NEGMODEL
# C   -B    A
# C   -B    A
# C   [B]   A
# C   [B]   A
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE A) (ALL C ARE B))
# [C]   B    A
# [C]   B
#            A
# SOME C ARE A  SOME A ARE C
# BREAKS
# [C]   B
#       B    A
# [C]   B
#            A
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE A) (SOME C ARE B))
#  C    B    A
#  C
#       B
#            A
# SOME C ARE A  SOME A ARE C
# BREAKS
#  C    B
#       B    A
#  C
#       B
#            A
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE A) (NO C ARE B))
# [C]  -B
# [C]  -B
#      [B]   A
#      [B]
#            A
# NO C ARE A  NO A ARE C
# ADDS-TO-NEGMODEL
# [C]  -B    A
# [C]  -B
#      [B]   A
#      [B]
#            A
# SOME C ARE NOT A  SOME A ARE NOT C
# ADDS-TO-NEGMODEL
# [C]  -B    A
# [C]  -B    A
#      [B]   A
#      [B]
#            A
# NO VALID CONCLUSION  SOME A ARE NOT C
#
# ((SOME B ARE A) (SOME C ARE NOT B))
#  C   -B
#  C   -B
#       B    A
#       B
#            A
# SOME C ARE NOT A  SOME A ARE NOT C
# ADDS-TO-NEGMODEL
#  C   -B    A
#  C   -B    A
#  C    B    A
#       B
#  C         A
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((NO B ARE A) (ALL C ARE B))
# [C]  [B]  -A
# [C]  [B]  -A
#           [A]
#           [A]
# NO C ARE A  NO A ARE C
#
# ((NO B ARE A) (SOME C ARE B))
#  C   [B]  -A
#  C
#      [B]  -A
#           [A]
#           [A]
# NO C ARE A  NO A ARE C
# MOVES
#  C        [A]
#  C   [B]  -A
#      [B]  -A
#           [A]
# SOME C ARE NOT A  SOME A ARE NOT C
# ADDS-TO-NEGMODEL
#  C        [A]
#  C   [B]  -A
#      [B]  -A
#  C        [A]
# SOME C ARE NOT A  NO VALID CONCLUSION
#
# ((NO B ARE A) (NO C ARE B))
# [C]  -B
# [C]  -B
#      [B]  -A
#      [B]  -A
#           [A]
#           [A]
# NO C ARE A  NO A ARE C
# MOVES
# [C]  -B   [A]
# [C]  -B   [A]
#      [B]  -A
#      [B]  -A
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((NO B ARE A) (SOME C ARE NOT B))
#  C   -B
#  C   -B
#      [B]  -A
#      [B]  -A
#           [A]
#           [A]
# NO C ARE A  NO A ARE C
# MOVES
#  C   -B   [A]
#  C   -B
#      [B]  -A
#      [B]  -A
#           [A]
# SOME C ARE NOT A  SOME A ARE NOT C
# MOVES
#  C   -B   [A]
#  C   -B   [A]
#      [B]  -A
#      [B]  -A
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE NOT A) (ALL C ARE B))
# [C]   B   -A
# [C]   B   -A
#            A
#            A
# SOME C ARE NOT A  SOME A ARE NOT C
# MOVES
# [C]   B    A
# [C]   B    A
#       B   -A
#       B   -A
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE NOT A) (SOME C ARE B))
#  C    B   -A
#  C
#       B   -A
#            A
#            A
# SOME C ARE NOT A  SOME A ARE NOT C
# MOVES
#  C         A
#  C    B    A
#       B   -A
#       B   -A
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE NOT A) (NO C ARE B))
# [C]  -B
# [C]  -B
#      [B]  -A
#      [B]  -A
#            A
#            A
# NO C ARE A  NO A ARE C
# MOVES
# [C]  -B    A
# [C]  -B
#      [B]  -A
#      [B]  -A
#            A
# SOME C ARE NOT A  SOME A ARE NOT C
# MOVES
# [C]  -B    A
# [C]  -B    A
#      [B]  -A
#      [B]  -A
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE NOT A) (SOME C ARE NOT B))
#  C   -B
#  C   -B
#       B   -A
#       B   -A
#            A
#            A
# SOME C ARE NOT A  SOME A ARE NOT C
# MOVES
#  C   -B    A
#  C   -B    A
#       B   -A
#       B   -A
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((ALL A ARE B) (ALL C ARE B))
# [A]   B   [C]
# [A]   B   [C]
# ALL A ARE C  ALL C ARE A
# BREAKS
# [A]   B
#       B   [C]
# [A]   B   [C]
# SOME A ARE C  SOME C ARE A
# BREAKS
# [A]   B
#       B   [C]
# [A]   B
#       B   [C]
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((ALL A ARE B) (SOME C ARE B))
# [A]   B    C
# [A]   B
#            C
# SOME A ARE C  SOME C ARE A
# BREAKS
# [A]   B
#       B    C
# [A]   B
#            C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((ALL A ARE B) (NO C ARE B))
# [A]  [B]
# [A]  [B]
#      -B   [C]
#      -B   [C]
# NO A ARE C  NO C ARE A
#
# ((ALL A ARE B) (SOME C ARE NOT B))
# [A]   B
# [A]   B
#      -B    C
#      -B    C
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
# [A]   B    C
# [A]   B    C
#      -B    C
#      -B    C
# NO VALID CONCLUSION  SOME C ARE NOT A
#
# ((SOME A ARE B) (ALL C ARE B))
#  A    B   [C]
#  A
#       B   [C]
# SOME A ARE C  SOME C ARE A
# BREAKS
#  A    B
#       B   [C]
#  A
#       B   [C]
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME A ARE B) (SOME C ARE B))
#  A    B    C
#  A
#       B
#            C
# SOME A ARE C  SOME C ARE A
# BREAKS
#  A    B
#       B    C
#  A
#       B
#            C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME A ARE B) (NO C ARE B))
#  A   [B]
#  A
#      [B]
#      -B   [C]
#      -B   [C]
# NO A ARE C  NO C ARE A
# ADDS-TO-NEGMODEL
#  A   [B]
#  A
#      [B]
#  A   -B   [C]
#      -B   [C]
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
#  A   [B]
#  A
#      [B]
#  A   -B   [C]
#  A   -B   [C]
# SOME A ARE NOT C  NO VALID CONCLUSION
#
# ((SOME A ARE B) (SOME C ARE NOT B))
#  A    B
#  A
#       B
#      -B    C
#      -B    C
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
#  A    B    C
#  A         C
#       B
#  A   -B    C
#  A   -B    C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((NO A ARE B) (ALL C ARE B))
# [A]  -B
# [A]  -B
#      [B]  [C]
#      [B]  [C]
# NO A ARE C  NO C ARE A
#
# ((NO A ARE B) (SOME C ARE B))
# [A]  -B
# [A]  -B
#      [B]   C
#      [B]
#            C
# NO A ARE C  NO C ARE A
# ADDS-TO-NEGMODEL
# [A]  -B    C
# [A]  -B
#      [B]   C
#      [B]
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
# [A]  -B    C
# [A]  -B    C
#      [B]   C
#      [B]
#            C
# NO VALID CONCLUSION  SOME C ARE NOT A
#
# ((NO A ARE B) (NO C ARE B))
# [A]  -B
# [A]  -B
#      [B]
#      [B]
#      -B   [C]
#      -B   [C]
# NO A ARE C  NO C ARE A
# MOVES
# [A]  -B   [C]
# [A]  -B   [C]
#      [B]
#      [B]
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((NO A ARE B) (SOME C ARE NOT B))
# [A]  -B
# [A]  -B
#      [B]
#      [B]
#      -B    C
#      -B    C
# NO A ARE C  NO C ARE A
# MOVES
# [A]  -B    C
# [A]  -B
#      [B]
#      [B]
#      -B    C
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
# [A]  -B    C
# [A]  -B    C
#      [B]
#      [B]
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME A ARE NOT B) (ALL C ARE B))
#  A   -B
#  A   -B
#       B   [C]
#       B   [C]
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
#  A   -B
#  A   -B
#  A    B   [C]
#  A    B   [C]
# SOME A ARE NOT C  NO VALID CONCLUSION
#
# ((SOME A ARE NOT B) (SOME C ARE B))
#  A   -B
#  A   -B
#       B    C
#       B
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
#  A   -B    C
#  A   -B    C
#  A    B    C
#       B
#  A         C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME A ARE NOT B) (NO C ARE B))
#  A   -B
#  A   -B
#      [B]
#      [B]
#      -B   [C]
#      -B   [C]
# NO A ARE C  NO C ARE A
# MOVES
#  A   -B   [C]
#  A   -B
#      [B]
#      [B]
#      -B   [C]
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
#  A   -B   [C]
#  A   -B   [C]
#      [B]
#      [B]
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME A ARE NOT B) (SOME C ARE NOT B))
#  A   -B
#  A   -B
#       B
#       B
#      -B    C
#      -B    C
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
#  A   -B    C
#  A   -B    C
#       B
#       B
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((ALL B ARE A) (ALL B ARE C))
#  A   [B]   C
#  A   [B]   C
# ALL A ARE C  ALL C ARE A
# ADDS
#  A
#  A   [B]   C
#  A   [B]   C
# SOME A ARE C  ALL C ARE A
# ADDS
#  A
#  A   [B]   C
#  A   [B]   C
#            C
# SOME A ARE C  SOME C ARE A
#
# ((ALL B ARE A) (SOME B ARE C))
#  A   [B]   C
#  A   [B]
#            C
# SOME A ARE C  SOME C ARE A
#
# ((ALL B ARE A) (NO B ARE C))
#  A   [B]  -C
#  A   [B]  -C
#           [C]
#           [C]
# NO A ARE C  NO C ARE A
# ADDS-TO-NEGMODEL
#  A   [B]  -C
#  A   [B]  -C
#  A        [C]
#           [C]
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
#  A   [B]  -C
#  A   [B]  -C
#  A        [C]
#  A        [C]
# SOME A ARE NOT C  NO VALID CONCLUSION
#
# ((ALL B ARE A) (SOME B ARE NOT C))
#  A   [B]  -C
#  A   [B]  -C
#            C
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
#  A   [B]  -C
#  A   [B]  -C
#  A         C
#  A         C
# SOME A ARE NOT C  NO VALID CONCLUSION
#
# ((SOME B ARE A) (ALL B ARE C))
#  A   [B]   C
#      [B]   C
#  A
# SOME A ARE C  SOME C ARE A
#
# ((SOME B ARE A) (SOME B ARE C))
#  A    B    C
#       B
#  A
#            C
# SOME A ARE C  SOME C ARE A
# BREAKS
#  A    B
#       B    C
#       B
#  A
#            C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE A) (NO B ARE C))
#  A   [B]  -C
#      [B]  -C
#  A
#           [C]
#           [C]
# NO A ARE C  NO C ARE A
# MOVES
#  A        [C]
#  A   [B]  -C
#      [B]  -C
#           [C]
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
#  A        [C]
#  A   [B]  -C
#      [B]  -C
#  A        [C]
# SOME A ARE NOT C  NO VALID CONCLUSION
#
# ((SOME B ARE A) (SOME B ARE NOT C))
#  A    B   -C
#       B   -C
#  A
#            C
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
#  A         C
#  A    B    C
#       B   -C
#       B   -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((NO B ARE A) (ALL B ARE C))
# -A   [B]   C
# -A   [B]   C
# [A]
# [A]
# NO A ARE C  NO C ARE A
# ADDS-TO-NEGMODEL
# -A   [B]   C
# -A   [B]   C
# [A]        C
# [A]
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
# -A   [B]   C
# -A   [B]   C
# [A]        C
# [A]        C
# NO VALID CONCLUSION  SOME C ARE NOT A
#
# ((NO B ARE A) (SOME B ARE C))
# -A   [B]   C
# -A   [B]
# [A]
# [A]
#            C
# NO A ARE C  NO C ARE A
# MOVES
# [A]        C
# -A   [B]   C
# -A   [B]
# [A]
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
# [A]        C
# -A   [B]   C
# -A   [B]
# [A]        C
# NO VALID CONCLUSION  SOME C ARE NOT A
#
# ((NO B ARE A) (NO B ARE C))
# -A   [B]  -C
# -A   [B]  -C
# [A]
# [A]
#           [C]
#           [C]
# NO A ARE C  NO C ARE A
# MOVES
# [A]       [C]
# [A]       [C]
# -A   [B]  -C
# -A   [B]  -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((NO B ARE A) (SOME B ARE NOT C))
# -A   [B]  -C
# -A   [B]  -C
# [A]
# [A]
#            C
#            C
# NO A ARE C  NO C ARE A
# MOVES
# [A]        C
# -A   [B]  -C
# -A   [B]  -C
# [A]
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
# [A]        C
# [A]        C
# -A   [B]  -C
# -A   [B]  -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE NOT A) (ALL B ARE C))
# -A   [B]   C
# -A   [B]   C
#  A
#  A
# SOME A ARE NOT C  SOME C ARE NOT A
# ADDS-TO-NEGMODEL
# -A   [B]   C
# -A   [B]   C
#  A         C
#  A         C
# NO VALID CONCLUSION  SOME C ARE NOT A
#
# ((SOME B ARE NOT A) (SOME B ARE C))
# -A    B    C
# -A    B
#  A
#  A
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
#  A         C
#  A    B    C
# -A    B
# -A    B
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE NOT A) (NO B ARE C))
# -A   [B]  -C
# -A   [B]  -C
#  A
#  A
#           [C]
#           [C]
# NO A ARE C  NO C ARE A
# MOVES
#  A        [C]
# -A   [B]  -C
# -A   [B]  -C
#  A
#           [C]
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
#  A        [C]
#  A        [C]
# -A   [B]  -C
# -A   [B]  -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
#
# ((SOME B ARE NOT A) (SOME B ARE NOT C))
# -A    B   -C
# -A    B   -C
#  A
#  A
#            C
#            C
# SOME A ARE NOT C  SOME C ARE NOT A
# MOVES
#  A         C
#  A         C
# -A    B   -C
# -A    B   -C
# NO VALID CONCLUSION  NO VALID CONCLUSION
# (T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T T)
"""


