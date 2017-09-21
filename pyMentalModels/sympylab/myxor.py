#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from __future__ import print_function, division

from collections import defaultdict, Counter
from itertools import combinations, product
from sympy.core.basic import Basic
from sympy.core.cache import cacheit
from sympy.core.numbers import Number
from sympy.core.sympify import sympify
from sympy.core.singleton import Singleton, S

from sympy.logic.boolalg import *



class Xor(BooleanFunction):
    """
    Logical XOR (exclusive OR) function.


    Returns True if an odd number of the arguments are True and the rest are
    False.

    Returns False if an even number of the arguments are True and the rest are
    False.

    Examples
    ========

    >>> from sympy.logic.boolalg import Xor
    >>> from sympy import symbols
    >>> x, y = symbols('x y')
    >>> Xor(True, False)
    True
    >>> Xor(True, True)
    False
    >>> Xor(True, False, True, True, False)
    True
    >>> Xor(True, False, True, False)
    False
    >>> x ^ y
    Xor(x, y)

    Notes
    =====

    The ``^`` operator is provided as a convenience, but note that its use
    here is different from its normal use in Python, which is bitwise xor. In
    particular, ``a ^ b`` and ``Xor(a, b)`` will be different if ``a`` and
    ``b`` are integers.

    >>> Xor(x, y).subs(y, 0)
    x

    """
    def __new__(cls, *args, **kwargs):
        argset = set([])
        obj = super(Xor, cls).__new__(cls, *args, **kwargs)
        print("0: obj arguments: ", obj._args)
        counts = Counter(obj._args)
        if counts[True] > 1:
            return false
        blackset = {el for el in counts if counts[el] > 1}
        print(blackset)
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
                print("removing!")
                argset.remove(arg)
            else:
                print("adding!")
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
            print("Object._argset: ", obj._argset)
            print("Type of object is: ", type(obj))
            print("the oject is:", obj)
            return obj

    @property
    @cacheit
    def args(self):
        return tuple(ordered(self._argset))

from sympy import symbols
from sympy.abc import x, y, z, A, B, C
#a = Xor(x, y)
#print(a)
#print()
#print(a.xreplace({x: True, y:True}))
"""
print(Xor(A))
assert Xor(A, A) is false
assert Xor(True, A, A) is true
"""
b = Xor(A, A)
print(b)
print()
print(b.xreplace({A: True, B: True}))
print(Xor(True, False, False, A, B) == ~Xor(A, B))
"""
assert Xor(True) is true
assert Xor(False) is false
assert Xor(True, True ) is false
assert Xor(True, False) is true
assert Xor(False, False) is false
assert Xor(True, A) == ~A
assert Xor(False, A) == A
assert Xor(True, False, False) is true
assert Xor(True, False, A) == ~A
assert Xor(False, False, A) == A
assert isinstance(Xor(A, B), Xor)
assert Xor(A, B, Xor(C, D)) == Xor(A, B, C, D)
assert Xor(A, B, Xor(B, C)) == Xor(A, C)
assert Xor(A < 1, A >= 1, B) == Xor(0, 1, B) == Xor(1, 0, B)
e = A > 1
assert Xor(e, e.canonical) == Xor(0, 0) == Xor(1, 1)
"""




"""
class Xor(BooleanFunction):
        def __new__(cls, *args, **kwargs):
        argset = set([])
        obj = super(Xor, cls).__new__(cls, *args, **kwargs)
        print("obj arguments: ", obj._args)
        for arg in obj._args:
            if isinstance(arg, Number) or arg in (True, False):
                if arg:
                    arg = true
                else:
                    continue
            if isinstance(arg, Xor):
                print("arguments of argument Xor: ", arg.args)
                # Need to change this
                for a in arg.args:
                    print("The argset is: ",argset)
                    argset.remove(a) if a in argset else argset.add(a)
            elif arg in argset:
                argset.remove(arg)
            else:
                argset.add(arg)
        rel = [(r, r.canonical, (~r).canonical) for r in argset if r.is_Relational]
        print(rel)
        odd = False  # is number of complimentary pairs odd? start 0 -> False
        remove = []
        for i, (r, c, nc) in enumerate(rel):
            print(i, r, c, nc)
            for j in range(i + 1, len(rel)):
                rj, cj = rel[j][:2]
                print("rj and cj", rj, cj)
                if cj == nc:
                    print("here")
                    odd = ~odd
                    break
                elif cj == c:
                    break
            else:
                continue
            remove.append((r, rj))
        print("remove: ", remove,"argset" ,argset)
        if odd:
            print("here")
            argset.remove(true) if true in argset else argset.add(true)
        for a, b in remove:
            print("a, b", a,b)
            argset.remove(a)
            argset.remove(b)
        if len(argset) == 0:
            print("bla")
            return false
        elif len(argset) == 1:
            return argset.pop()
        elif True in argset:
            argset.remove(True)
            return Not(Xor(*argset))
        else:
            print("finally")
            obj._args = tuple(ordered(argset))
            obj._argset = frozenset(argset)
            print(type(obj))
            return obj

    @property
    @cacheit
    def args(self):
        return tuple(ordered(self._argset))

"""
