#!/usr/bin/python3


def pretty_print_atom_assign(atoms, atom_assignment, mode="intuitive", output="str"):
    """
        Returns a string representation of the atoms
        Atom. Assignment 0 --> "¬atom" if explicit else " "
        Atom. Assignment -1 --> "¬atom" always
        Atom. Assignment 1 --> "atom"

        Parameters
        ----------
        atoms: List,
            Literals/Atoms of the logical expression i.e. the column labels for the model
        atom_assignment: Either 1, 0, -1
            Assignment of the Atoms in the model.
        mode: str, optional
            default is "intuitive" choices are "intuitive", "explicit"
        output: str
            can be either "list" or "str"

    """
    assert mode in ("intuitive", "explicit"), "Provided invalid argument for `mode`"
    assert output in ("list", "str"), "Provided invalid argument for `mode`"

    if mode == "intuitive":
        list_repr = [" {}".format(atom) if value == 1 else "¬{}".format(atom) if value == -2 else "  " for atom, value in zip(atoms, atom_assignment)]
    else:
        list_repr = [" {}".format(atom) if value == 1 else "¬{}".format(atom) for atom, value in zip(atoms, atom_assignment)]

    if output == "list":
        return list_repr
    else:
        return " ".join(list_repr)
