#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-


def satisfiying_variable_assignments(truth_table):
    """yields the truth_table entries with valuation True (Principle of Truth)"""
    from collections import namedtuple
    TruthTableEntry = namedtuple("TruthTableEntry", ["assignment", "valuation"])
    yield from (variable_assignment for variable_assignment, _ in filter(lambda result: TruthTableEntry(*result).valuation, truth_table))


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

    """
    if explicit:
        return {str(atom) if value else "!{}".format(atom) for atom, value in zip(atoms, atom_assignment)}
    else:
        if not any(value for atom, value in zip(atoms, atom_assignment)):
            return {str(atom) if value else "!{}".format(atom) for atom, value in zip(atoms, atom_assignment)}
        return {str(atom) for atom, value in zip(atoms, atom_assignment) if value}
    """
