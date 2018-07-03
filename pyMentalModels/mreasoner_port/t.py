#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from enum import Enum
from collections import namedtuple
QuantifierArguments = namedtuple("QuantifierArguments", ["cardinality", "numprop"])


class QuantifiedIntension(object):
    def __init__(self, cardinality, numprop, boundary, polarity,
                 footnotes, subject, obj, relation):
        self._cardinality = cardinality
        self._numprop = numprop
        self._boundary = boundary
        self._polarity = polarity
        self._footnotes = footnotes
        self._subject: subject
        self._obj: obj
        self._relation = relation


class Quantifier(Enum):
    few = lambda: QuantifiedIntension(1,2,3,4,5,6,7,8)
    some = lambda: QuantifiedIntension()
    all_ = lambda: QuantifiedIntension()
    none = lambda: QuantifiedIntension()


few = Quantifier.few()
print(few._boundary)

def is_quantified(value):
    return any(quantifier() == value for quantifier in Quantifier)
    for quantifier in Quantifier:
        if quantifier() == value:
            return True
    return False

def is_few(value):
    return value == Quantifier.few()


"""
class Quantifier(Enum):
    few = QuantifierArguments(cardinality=(("?", 4), (">=", 2)), numprop=("?", 3))
    some = 2
    all_ = 3
    none = 4


class QuantifiedIntension(object):
    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def from_quantifier(cls, quantifier):
        return QuantifiedIntension(*quantifier.value)



def is_quantifier(value):
    for quantifier in Quantifier:
        if value == quantifier.value or value == quantifier:
            return True
    return False
    # ...

print(is_quantifier("aha"))
print(is_quantifier(Quantifier.few))
print(is_quantifier(((("?", 4), (">=", 2)), ("?", 3))))
"""
