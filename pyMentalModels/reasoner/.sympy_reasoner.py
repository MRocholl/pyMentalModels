#!/usr/bin/python3

from itertools import permutations, combinations
from sympy.logic.boolalg import truth_table


def satisfiying_variable_assignments(t_table):
    """yields the truth_table entries with valuation True (Principle of Truth)"""
    from collections import namedtuple
    TruthTableEntry = namedtuple("TruthTableEntry", ["assignment", "valuation"])
    yield from (variable_assignment for variable_assignment, _ in filter(
                lambda result: TruthTableEntry(*result).valuation, t_table))


def pretty_print_atom_assign(atoms, atom_assignment, intuitive):
    # TODO These guys need to take into account the possibility of explicitly representing negatives if explicitly given
    """
        Returns a string representation of the atoms
        Atom. Assignment 0 --> "¬atom"
        Atom. Assignment 1 --> "atom"
    """
    if intuitive:
        if any(value for atom, value in zip(atoms, atom_assignment)):
                return [str(atom) if value else " " for atom, value in zip(atoms, atom_assignment)]
        else:
                return ["¬{}".format(atom) for atom in atoms]
    return [str(atom) if value else "¬{}".format(atom) for atom, value in zip(atoms, atom_assignment)]


def generate_possible_models(sympified_expression, intuitive=True):
    # TODO For arguments that are in NOT() find a way to reverse 0 to 1 in truth_table
    # Possibly by post_processing the arguments that are in a Not to look accordingly
    """
        generates all the possible models satisfying `principle of truth`

        Parameters
        ----------
        sympified_expression : BooleanFunction of Sympy logical object
            i.e. sympify("Or(A,B)")

        intuitive : Boolean
           tells the function how to flesh out the models.

        Returns
        -------
        List of strings that each represent a possible world

    """
    def _increasing_ones_first_sort(array_slice):
                pos_of_ones = [-array_slice[i] for i, _ in enumerate(array_slice)]
                return array_slice.count(1), pos_of_ones

    atoms = sorted(sympified_expression.atoms(), key=str)
    t_table = truth_table(sympified_expression, atoms)
    return [pretty_print_atom_assign(atoms, variable_assignment, intuitive) for variable_assignment in sorted(satisfiying_variable_assignments(t_table), key=_increasing_ones_first_sort)]


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
