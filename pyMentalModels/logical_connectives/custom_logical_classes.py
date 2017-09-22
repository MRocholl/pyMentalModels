#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

"""
    Implementation of Custom logical connectives:
    (1) Xor: Takes multiple arguments instead of 2
    (2) Necessary
    (3) Possible


    """
# XXX Will probalby need to subclass all operators to ensure modal logical behavior

#  Imports {{{ #
from sympy.logic.boolalg import Xor


from collections import defaultdict
from itertools import combinations, product

from sympy.core.basic import Basic
from sympy.core.cache import cacheit
from sympy.core.numbers import Number
from sympy.core.operations import LatticeOp
from sympy.core.function import Application, Derivative
from sympy.core.compatibility import ordered, range, with_metaclass, as_int
from sympy.core.sympify import converter, _sympify, sympify
from sympy.core.singleton import Singleton, S

from sympy.logic.boolalg import *
from sympy import Eq

#  }}} Imports #


class MulXor(BooleanFunction):
    """
        Intuitive Xor that behaves slightly differently to the normal xor
        Normal Xor is a binary operator.
        i.e. Xor(a, b, c) ~  Xor(Xor(a, b), c)
        In natural language Xor may take more than two arguments resulting in different behavior

        Examples
        ========
        >>> from alternative_operators import MulXor
        >>> from sympy import symbols
        >>> x, y, z = symbols('x y z')
        >>> MulXor(True, False)
        True
        >>> MulXor(True, True)
        False

        Multiple arguments are not evaluated in a dyadic manner but as one
        >>> MulXor(True, True, False)
        False
        >>> MulXor(True, False, False, False)
        True

        MulXor uses xreplace or subs to give symbolic variables values
        >>> MulXor(Or(x, y), And(x,y)).xreplace({x:True, y:False})
        True

    """

    def __new__(cls, *args, **kwargs):
        argset = set([])
        obj = super(Xor, cls).__new__(cls, *args, **kwargs)
        counts = Counter(obj._args)
        if counts[True] > 1:
            return false
        blackset = {el for el in counts if counts[el] > 1}
        for arg in obj._args:
            if isinstance(arg, Number) or arg in (True, False):
                if arg:
                    arg = true
                else:
                    continue
            if isinstance(arg, Xor):
                if any(a in argset for a in arg.args):
                    # Ex: Xor(x, y, Xor(x, z))
                    argset.add(arg)
                else:
                    for a in arg.args:
                        argset.add(a)
            elif arg in argset:
                argset.remove(arg)
            else:
                argset.add(arg)
        argset = argset.difference(blackset)
        if len(argset) == 0:
            return false
        elif len(argset) == 1:
            return argset.pop()
        elif True in argset:
            argset.remove(True)
            return Not(Xor(*argset))
        else:
            obj._args = tuple(ordered(argset))
            obj._argset = frozenset(argset)
            return obj

    @property
    @cacheit
    def args(self):
        return tuple(ordered(self._argset))


class Necessary(BooleanFunction):
    # XXX Need to futher narrow down the mechanism
    """ Modal logical Operator
        Value of subformula `must` evaluate to `True`:
        i.e. Necessary(False) --> entire formula evaluates to false

        Examples
        ========
        >>> from python_modal_logical.logical_connectives.custom_logical_classes import Necessary
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

        Necessary uses xreplace or subs to give symbolic variables values
        >>> Necessary(Or(x, y)).xreplace({x:True, y:False})
        True
    """
    def __new__(cls, *args, **kwargs):
        obj = super(Necessary, cls).__new__(cls, *args, **kwargs)
        return obj._args


class Possibly(BooleanFunction):
    """ Modal logical Operator
        Arguments `can` evaluate to true.
        This class returns the arguments as are.

        Examples
        ========
        >>> from

    """
    def __new__(cls, *args, **kwargs):
        obj = super(Possibly, cls).__new__(cls, *args, **kwargs)
        return obj._args



a = sympify("B & Possibly(A & C)", locals={"Possibly": Possibly} )
print(a)
