#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
from ABC import ABC, abstractmethod
from math import inf
import mreasoner_port.constants as constants

from enum import Enum
from collections import namedtuple
QuantifierArguments = namedtuple("QuantifierArguments", ["cardinality", "numprop"])


class Quantifier(Enum):
    few = lambda QuantifiedIntension(cardinality=(("?", 4), (">=", 2)), numprop=("?", 3), boundary=(("<", cardinality/2)), (">", 0)) polarity=True, footnote=True subject=False, relation=False))
    exactly = lambda QuantifiedIntension(cardinality=((? (+ N 1)) (>= N)) numprop=("=", N) boundary  ((= N)) pol  t fn   t subj nil rel nil))
    some = lambda QuantifiedIntension(cardinality=((? 4) (>= 1)) numprop   (? 2) boundary  ((<= cardinalityinality)(> 0)) pol  t fn   nil subj nil rel nil))
    all_ = lambda QuantifiedIntension(cardinality=((? 4) (>= 1)) numprop   (? 4) boundary  ((= cardinalityinality)) pol  t fn   t subj nil rel nil)
    none = lambda: QuantifiedIntension()
    no = lambda QuantifiedIntension(cardinality=((? 4) (>= 1)) numprop   (? 4) boundary  ((= cardinalityinality)) pol  nil fn   t subj nil rel nil)
    more = lambda QuantifiedIntension(cardinality=((? (+ N 2)) (>= (+ N 1))) numprop   (? (+ N 1)) boundary  ((< cardinalityinality)(> N)) pol  t fn   nil subj nil rel nil))
    less = lambda QuantifiedIntension(cardinality=((? (+ N 0)) (> N 1)) numprop   (? (- N 1)) boundary  ((< N) (> 0)) pol  t fn   nil subj nil rel nil))

class AbstractIntension(ABC):
    """
    Intensions contain five parameters. The role of each parameter is summarized here:

    i.  Cardinality: the size of the overall set, A, which is the argument of the determiner in the
                 quantifer, e.g. "Some A". It has two sorts of values, illustrated here:
                    (>= 4) means the cardinality is known to be >= 4, and other similar assertions,
                           involving >, <, =, and so (= 4) means the cardinality is known to be 4.
                    (?  4) means a cardinality of 4 has been arbitrarily assumed.
                 This system meets requirement 1. in our list above for the size of A.

    ii.  Number: the number of members of A in the quantifier that meet the relational specification.
                 In most cases, this is an arbitrarily assigned number, such as (? 3). The (? 3)
                 constraint serves as a cue for building an initial model, but that initial model rests
                 on the arbitrary assumption that M indivs should be built, which is an assumption that
                 can be violated.

                 For some quantifiers, the number is non-arbitrary, e.g., "Exactly 3 As are Bs". This value is
                 represented as (= 3), and it cannot be violated.

    iii. Boundary: the range of values that the number paramter can take on. The value can specify an upper bound,
                   a lower bound, or both. For example, for "Some A are B", the boundary is:
                   ((< cardinality) (> 0))
                   Note that the upper bound in the above boundary, (< cardinality), uses the symbol 'cardinality
                   to indicate that a corresponding model can have as many members that meet the relational
                   specification as there are members in total.

                   Let's break that down with the example above: "Some A are B" starts out with a cardinality of
                   (? 3), and so the upper bound, (< cardinality), means that the system can represent up to 2 As
                   that are Bs. Of course, the cardinality of (? 3) can be modifed to, say, (? 5), at which point
                   the system can represent up to 4 As that are Bs.

                 This system meets requirements 1. and 2. in our list above, i.e., we can tell whether a determiner
                 is numerical or not by checking whether first.parameter rtns '?' or not.

    iv.  Polarity (of the quantifier): t = affirmative, nil = negative

    v.   Universality t = The quantifier is a universal one, such as 'all' or 'none',
                 nil = the quantifier is an existential one, such as'some.
                 On Feb 22nd, SK and JL decided that the content of a footnote should always be the
                 intension of the assertion.  Hence the change in the interpretation of this parameter.
    """

    def __init__(self, cardinality, numprop, boundary, polarity, universality):
        self._cardinality = cardinality
        self._numprop = numprop
        self._boundary = boundary
        self._polarity = polarity
        self._universality = universality

    @abstractmethod
    def __repr__(self):
        """ Returns the representation of Intensions - Defined in inheriting classes"""


class AbstractMentalModel(ABC):
    """
    Abstract Base Class for all other mental models
    """

    def __init__(self, entities, footnote, capacity=inf):
        self._entitites = entities
        self._footnotes = footnote
        self._capacity = capacity

    @abstractmethod
    def __eq__(self, other):
        "Method that compares two models"

    @abstractmethod
    def find_referent_in_model(self, referent):
        """
        Returns referent in model if exists
        """


class QuantifiedIntension():

    """
    Quantified Intension.

    Intension for quantified assertions

    """
    # XXX Decide how to pass in the intension. As string with string processing in init method
    # or as a already parsed list.
    def __init__(self, cardinality, numprop, boundary, polarity,
                 footnotes, subject, obj, relation):
        """TODO: to be defined1.

        Parameters
        ----------
        cardinality :
        numprop : TODO
        boundary : TODO
        polarity: TODO
        footnotes: TOTO
        subject: TODO
        obj: TODO
        relation: TODO
        """
        self._cardinality = cardinality
        self._numprop = numprop
        self._boundary = boundary
        self._polarity = polarity
        self._footnotes = footnotes
        self._subject: subject
        self._obj: obj
        self._relation = relation

    def __repr__(self):
        repr_str = "{subj}{{mood}}{obj}".format(subj=self._subject, obj=self._obj)
        print(repr_str)
        # Lisp code tests for is-most is-few etc.... with helper functions. Decide wether to incorporate that as a property. Probably best to do so.
        return {self.is_some: repr_str.format(mood=),
                self.is_some_not: repr_str.format(mood=),
                self.is_all: repr_str.format(mood=),
                self.is_few: repr_str.format(mood=),
                self.is_most: repr_str.format(mood=),
                self.is_none: repr_str.format(mood=)
                }[True]

    @classmethod
    def inverse_intension(intension):
        pass

    @staticmethod
    def get_syllogistic_figure(premise_1, premise_2):
        """
        Determines figure of the two premises by establishing the respective grammatical roles of the two end terms
        Examples
        --------
        >>> get_syllogistic_figure(parse("all b are a"), parse("all b are c"))
        >>> 4
        >>> get_syllogistic_figure(parse("all b are a"), parse("all b are c"))
        >>> 4
        >>> get_syllogistic_figure(parse("all b are a"), parse("all b are c"))
        >>> 4
        >>> get_syllogistic_figure(parse("all b are a"), parse("all b are c"))
        >>> 4
        """
        subj_1 = premise_1.subj
        obj_1 = premise_1.obj
        subj_2 = premise_2.subj
        obj_2 = premise_2.obj

        # XXX end_1 = first (get-syll-end-terms premise_1 premise_2)
        # end_2 = second (get-syll-end-terms premise_1 premise_2)
        if subj_1 == end_1 and obj_2 == end_2:
            return 1
        elif obj_1 == end_1 and subj_2 == end_2:
            return 2
        elif subj_1 == end_1 and subj_2 == end_2:
            return 3
        elif obj_1 == end_1 and obj_2 == end_2:
            return 4
        else:
            raise ValueError("Not an orthodox syllogistic figure")

    @classmethod
    def init_as(cls, quantifier, **kwargs):
        # XXX Shift `?` input into constant file where i define the cardinality for `most` etc... This should not be a magic number in here
        {
            "most": clf(cardinality=(("?", 4), (">=", 2)), numprop=("?", 3), boundary=(("<", ("?", 4)), (">", (* .5 cardinality))) :pol  t :fn   t :subj nil :rel nil),

            "few":
            "exactly":
            "all":
            "some":
            "no":
            "more":


                }[quantifier.lower()]




        return cls(cardinality=(4, 2),
                   numprop=(3),
                   boundary=("cardinality")
                   polarity=
                   footnote=True,
                   )

    @classmethod
    def few(cls):
        pass

    @classmethod
    def exactly(cls):
        pass

    @classmethod
    def all(cls):
        pass

    @classmethod
    def some(cls):
        pass

    @classmethod
    def no(cls):
        pass

    @classmethod
    def more(cls):
        pass


class TemporalIntension():
    """
    TemporalIntension.

    Intension for temporal assertions
    """
    def __init__(self, subject, obj, precedence, start_time, end_time, reference_time, relation_to_utterance):
        """TODO: Docstring for __init__.

        Parameters
        ----------
        subject : TODO
        obj : TODO
        precedence : TODO
        start_time : TODO
        end_time : TODO
        reference_time : TODO
        relation_to_utterance : TODO

        Returns
        -------
        TODO

        """
        self._subj = subject
        self._obj = obj
        self._precedence = precedence
        self._start_time = start_time
        self._end_time = end_time
        self._reference_time = reference_time
        self._relation_to_utterance = relation_to_utterance

    def __repr__(self):
        """ """
        return "{subj}{relation}{obj}".format(subj=self._subj, relation=self.relation_to_utterance, obj=self._obj)

    @property
    def model_size(self):
        """
        Gets the size of a temporal model, i.e., the number of distinct events, punctate
        or durational, represented in the model.
        """


class SententialIntension():
    """
    Sentential Intension
    Intension for sentences and sentential connectives
    """

    def __init__(self, first_clause, second_clause, clause="both"):
        """
        Parameters
        ----------
        first_clause : TODO
        second_clause : TODO
        clause :
            Both
            First_only
            Second_only
            Neither
        """
        self._first_clause = first_clause
        self._second_clause = second_clause
        self._clause = clause


