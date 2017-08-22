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

from __future__ import print_function, division

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


class MyXor(BooleanFunction):

    """
        Intuitive Xor that behaves slightly differently to the normal xor
        Normal Xor is a binary operator.
        i.e. Xor(a, b, c) ~  Xor(Xor(a, b), c)
        In natural language Xor may take more than two arguments resulting in different behavior

        Examples
        ========
        >>> from alternative_operators import MyXor
        >>> from sympy import symbols
        >>> x, y, z = symbols('x y z')
        >>> MyXor(True, False)
        True
        >>> MyXor(True, True)
        False

        Multiple arguments are not evaluated in a dyadic manner but as one
        >>> MyXor(True, True, False)
        False
        >>> MyXor(True, False, False, False)
        True

        MyXor uses xreplace or subs to give symbolic variables values
        >>> MyXor(Or(x, y), And(x,y)).xreplace({x:True, y:False})
        True

    """

    def __new__(cls, *args, **kwargs):
        argset = set([])
        obj = super(MyXor, cls).__new__(cls, *args, **kwargs)
        from collections import Counter
        if Counter(obj._args)[True] > 1:
            return false
        for arg in obj._args:
            if isinstance(arg, Number) or arg in (True, False):
                if arg:
                    arg = true
                else:
                    continue
            if isinstance(arg, Xor):
                for a in arg.args:
                    argset.remove(a) if a in argset else argset.add(a)
            elif arg in argset:
                argset.remove(arg)
            else:
                argset.add(arg)
        rel = [(r, r.canonical, (~r).canonical) for r in argset if r.is_Relational]
        odd = False  # is number of complimentary pairs odd? start 0 -> False
        remove = []
        for i, (r, c, nc) in enumerate(rel):
            for j in range(i + 1, len(rel)):
                rj, cj = rel[j][:2]
                if cj == nc:
                    odd = ~odd
                    break
                elif cj == c:
                    break
            else:
                continue
            remove.append((r, rj))
        if odd:
            argset.remove(true) if true in argset else argset.add(true)
        for a, b in remove:
            argset.remove(a)
            argset.remove(b)
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


class Necessary:
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
        >>> MyXor(Or(x, y)).xreplace({x:True, y:False})
        True
    """
    def __new__(cls, *args, **kwargs):
        pass


class Possibly:
    """ Modal logical Operator
        Arguments `can` evaluate to true.
        This class returns the arguments as are.

        Examples
        ========
        >>> from



    """
        def __new__():
            argset = set([])
            obj = super(Possibly, cls).__new__(cls, *args, **kwargs)
            return obj._args

