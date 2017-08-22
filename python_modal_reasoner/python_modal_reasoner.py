#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

import sympy
# from sympy.logic.boolalg import Not, Or, And, Xor, Implies, BooleanFunction, truth_table
from sympy.logic.boolalg import *
from sympy.core.sympify import sympify

from itertools import *
import argparse

from utils.utils import satisfiying_variable_assignments, pretty_print_atom_assign
from parsing.modal_parser import parse_expr, sympify_formatter
from logical_connectives.operators import op_names




#######################################################################
#                            Notes / TODO                             #
#######################################################################
# > Finish implementing reasoner
#
# > Idea: Treat negations in premise differently then negations that arise from parsing


def possible_worlds(atoms, truth_table, explicit=True):
    return [pretty_print_atom_assign(atoms, variable_assignment, explicit) for variable_assignment in satisfiying_variable_assignments(truth_table)]


#######################################################################
#       Analyzing the mental models and making valid inferences       #
#######################################################################


def compare(possible_world_premise1, possible_world_premise2):
    "Yields valid or nill"
    literals1 = possible_world_premise1.split()
    literals2 = possible_world_premise2.split()
    all_literal_pairings = zip_2_lists(literals1, literals2)
    print(all_literal_pairings)


def zip_2_lists(list1, list2):
    """ returns all possible pairings between elements of two different lists"""
    if len(list1) > len(list2):
        longer, len_longer = list1, len(list1)
        shorter = list2
    else:
        longer, len_longer = list2, len(list2)
        shorter = list1
    return [[el for el in zip(x, shorter)] for x in permutations(longer, len_longer)]

def reasoner(all_atoms, all_possible_worlds):
    """
        Modal reasoner. Processes possibilities and returns possible inferences

        Parameters
        ----------
        all_atoms : list of all_atoms
        all_possible_worlds: list of sets of possibilities

        Returns:
        -------
        Possible inference

    """
    # TODO Expand for modal reasoning
    # For instance with numpy that enables vertical and horizontal checking
    # through bitmaps
    """ Checks the possible worlds for contradictions
        and eliminates contradictory models one by one

        Remainding models are then used to formulate a conclusion

        Works for both intuitive and explicit variants
    """
    seen_literals = set().union(*all_possible_worlds)

    possibly = set()  # XXX Not required at the moment
    necessary = set()  # Same applies here
    print(seen_literals)
    pairings_premises = [zip_2_lists(premise1, premise2) for premise1, premise2 in combinations(all_possible_worlds, r=2)]
    print("here goes:", pairings_premises)

    # for atom in seen_literals:
    #    if all(atom in model for model in all_possible_worlds):
    #        return atom

#######################################################################


l1 = ['!B !A', 'B', 'B A']
l2 = ['!B']

def check_pairings(l1, l2):
    for el1 in l1:
        for el2 in l2:
            literals1 = el1.split()
            literals2 = el2.split()
            print(literals1,literals2)





def main():
    parser = argparse.ArgumentParser(description="Please help me")
    parser.add_argument("--explicit", action="store_true", dest="explicit", help="Generate explicit models", default=False)
    parser.add_argument("premises", nargs="+")
    args = parser.parse_args()

    if not args.explicit:
        sympy.boolalg.Implies = sympy.boolalg.And

    all_possible_worlds = []
    all_atoms = []
    for i, premise in enumerate(args.premises):
        # TODO preprocess strings to substitute "<>" biconditional through "&" if intutitive \
        # or "Equals()" if --explicit
        formated_premise = sympify_formatter(parse_expr(premise), op_names)
        expr = sympify(formated_premise, locals={})
        atoms = expr.atoms()
        print("Epression being evaluated is:\t\t", expr)
        premise_possible_worlds = possible_worlds(atoms, truth_table(expr, atoms), args.explicit)
        print("Extracted possible world for premise {}:\t ".format(i), premise_possible_worlds, "\n")
        all_possible_worlds.append(premise_possible_worlds)
    print("Resulting possible worlds for all premises: ", all_possible_worlds)

    # activate reasoner based on the possible worlds generated based on the premises
    conclusion = reasoner(all_atoms, all_possible_worlds)
    if conclusion:
        print("It follows that: ", conclusion)
    else:
        print("Nothing follows")


if __name__ == "__main__":
    main()
