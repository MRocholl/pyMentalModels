#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

"""
    Implementation of Custom logical connectives:
    (1) Xor: Takes multiple arguments instead of 2
    (2) Necessary
    The problem is that the truth value of A does not determine the truth value for []A. For example, when A is ‘Dogs are dogs’, []A is true, but when A is ‘Dogs are pets’, []A is false

    (3) Possible

    Rules for the modal logical system:
    ==================================

    (~) v(~A, w)=T iff v(A, w)=F.

    (->) v(A -> B, w)=T iff v(A, w)=F or v(B, w)=T. !!!!! Implication is AND in implicit mode

    (5) v([]A, w)=T iff for every world w′ in W, v(A, w′)=T.



    """
# XXX Will probalby need to subclass all operators to ensure modal logical behavior

#  Imports {{{ #
from sympy.logic.boolalg import Xor


from collections import Counter
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


class ModalAnd(LatticeOp, BooleanFunction):
    # XXX TODO  Change docstring to reflect modal logical behavior. Also got rid of all the relational stuff
    """
    Logical AND function.

    It evaluates its arguments in order, giving False immediately
    if any of them are False, and True if they are all True.

    Examples
    ========

    >>> from sympy.logic.boolalg import sympify
    >>> from pyMentalModels.logical_connectives import ModalAnd
    >>> sympfify("x & y", {"ModalAnd": ModalAnd})
    ModalAnd(x, y)

    >>> ModalAnd(x, y).subs(x, 1)
    y

    """
    zero = false
    identity = true

    nargs = None

    @classmethod
    def _new_args_filter(cls, args):
        newargs = []
        rel = []
        for x in reversed(list(args)):
            if isinstance(x, Number) or x in (0, 1):
                newargs.append(True if x else False)
                continue
            if isinstance(x, Possibly):
                for el in x._args:
                    newargs.append(el)
                    continue
            else:
                newargs.append(x)
        return LatticeOp._new_args_filter(newargs, And)

    #def as_set(self):
    #    """
    #    Rewrite logic operators and relationals in terms of real sets.

    #    Examples
    #    ========

    #    >>> from sympy import And, Symbol
    #    >>> x = Symbol('x', real=True)
    #    >>> And(x<2, x>-2).as_set()
    #    Interval.open(-2, 2)
    #    """
    #    from sympy.sets.sets import Intersection
    #    if len(self.free_symbols) == 1:
    #        return Intersection(*[arg.as_set() for arg in self.args])
    #    else:
    #        raise NotImplementedError("Sorry, And.as_set has not yet been"
    #                                  " implemented for multivariate"
    #                                  " expressions")



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
        obj = super(MulXor, cls).__new__(cls, *args, **kwargs)
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
        >>> from pyMentalModels.logical_connectives.custom_logical_classes import Necessary
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
        necessaries.append(obj._args[0])
        arg = obj._args[0]
        return obj._args[0]


class Possibly(BooleanFunction):
    """ Modal logical Operator
        Arguments `can` evaluate to true.
        This class returns the arguments as are.

        Examples
        ========
        >>> from pyMentalModels.logical_connectives.custom_logical_classes import Possibly

    """
    def __new__(cls, *args, **kwargs):
        obj = super(Possibly, cls).__new__(cls, *args, **kwargs)
        return obj

"""
Furthermore, [](A&B) entails []A&[]B and vice versa; while []A|[]B entails [](A|B), but not vice versa. This reflects the patterns exhibited by the universal quantifier: ∀x(A&B) entails ∀xA&∀xB and vice versa, while ∀xA ∨ ∀xB entails ∀x(A ∨ B) but not vice versa
"""


