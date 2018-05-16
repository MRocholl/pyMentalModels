#!/usr/bin/python3

from pyMentalModels.constants import EXPL_NEG


def pretty_print_atom_assign(atom_assignment, atoms, mode="intuitive", output="str"):
    """
        Returns a string representation of the atoms
        Atom. Assignment IMPL_NEG --> "¬atom" if explicit else " "
        Atom. Assignment EXPL_NEG --> "¬atom" always
        Atom. Assignment POS_VAL --> "atom"

        Parameters
        ----------
        atoms: List,
            Literals/Atoms of the logical expression i.e. the column labels for the model
        atom_assignment: Either EXPL_NEG, POS_VAL, IMPL_NEG

            Assignment of the Atoms in the model.
        mode: str, optional
            default is "intuitive" choices are "intuitive", "explicit"

        Returns
        -------
        output: [List, str]
            can be either "list" or "str"

    """
    assert mode in ("intuitive", "explicit"), "Provided invalid argument for `mode`"
    assert output in ("list", "str"), "Provided invalid argument for `mode`"

    if mode == "intuitive":
        list_repr = [" {}".format(atom) if value > 0 else "¬{}".format(atom) if value == EXPL_NEG else "  " for atom, value in zip(atoms, atom_assignment)]
    else:
        list_repr = [" {}".format(atom) if value > 0 else "¬{}".format(atom) if value < 0 else "  " for atom, value in zip(atoms, atom_assignment)]

    if output == "list":
        return list_repr
    else:
        return " ".join(list_repr)
