#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from sympy.logic.boolalg import BooleanFunction


class Necessary(BooleanFunction):
    """ Modal logical Operator
        Value of subformula `must` evaluate to `True`:
        i.e. Necessary(False) --> entire formula evaluates to false

        Examples
        ========
        >>> from pyMentalModels.custom_logical_classes import Necessary
        >>> from sympy import symbols
        >>> x, y, z = symbols('x y z')
        >>> Necessary()
        XXX
        >>> Necessary()
        XXX

        Multiple arguments
        >>> Necessary()
        False
        >>> Necessary()
        True

    """


class Possibly(BooleanFunction):
    """ Modal logical Operator
        Arguments `can` evaluate to true.
        This class returns the arguments as are.

        Examples
        ========
        >>> from pyMentalModels.custom_logical_classes import Possibly

    """
