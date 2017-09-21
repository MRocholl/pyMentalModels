#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from itertools import permutations, combinations


def satisfiying_variable_assignments(truth_table):
    """yields the truth_table entries with valuation True (Principle of Truth)"""
    from collections import namedtuple
    TruthTableEntry = namedtuple("TruthTableEntry", ["assignment", "valuation"])
    yield from (variable_assignment for variable_assignment, _ in filter(
                lambda result: TruthTableEntry(*result).valuation, truth_table))


def pretty_print_atom_assign(atoms, atom_assignment, explicit):
    """
        Returns a string representation of the atoms
        Atom. Assignment 0 --> "!atom"
        Atom. Assignment 1 --> "atom"
    """
    if not explicit:
        if any(value for atom, value in zip(atoms, atom_assignment)):
            return " ".join(str(atom) for atom, value in zip(atoms, atom_assignment) if value)
        else:
            return " ".join(str(atom) for i, (atom, value) in enumerate(zip(atoms, atom_assignment)) if i == 0)
    return " ".join(str(atom) if value else "!{}".format(atom) for atom, value in zip(atoms, atom_assignment))


def possible_worlds(atoms, truth_table, explicit=True):
    return [pretty_print_atom_assign(atoms, variable_assignment, explicit) for variable_assignment in satisfiying_variable_assignments(truth_table)]


def zip_2_lists(list1, list2):
    """ returns all possible pairings between elements of two different lists"""
    if len(list1) > len(list2):
        longer, len_longer = list1, len(list1)
        shorter = list2
    else:
        longer, len_longer = list2, len(list2)
        shorter = list1
    return [[el for el in zip(x, shorter)] for x in permutations(longer, len_longer)]


def compare(premise_1, premise_2):
    "Yields valid or nill"
    literals_1 = premise_1.split()
    literals_2 = premise_2.split()
    all_literal_pairings = zip_2_lists(literals_1, literals_2)
    print(all_literal_pairings)


def check_pairings(l1, l2):
    for el1 in l1:
        for el2 in l2:
            literals1 = el1.split()
            literals2 = el2.split()
            print(literals1, literals2)


def reasoner(all_atoms, all_possible_worlds):
    # TODO Expand for modal reasoning
    # For instance with numpy that enables vertical and horizontal checking
    # through bitmaps
    """
        Modal reasoner. Processes possibilities and returns possible inferences
        Checks the possible worlds for contradictions
        and eliminates contradictory models one by one

        Remainding models are then used to formulate a conclusion

        Works for both intuitive and explicit variants


        Parameters
        ----------
        all_atoms : list of all_atoms
        all_possible_worlds: list of sets of possibilities

        Returns:
        -------
        Possible inference

    """
    seen_literals = set().union(*all_possible_worlds)
    print(seen_literals)
    pairings_premises = [zip_2_lists(premise1, premise2) for premise1, premise2 in combinations(all_possible_worlds, r=2)]
    print("here goes:", pairings_premises)
