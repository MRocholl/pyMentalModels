#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
from ABC import ABC, abstractmethod
from math import inf

# ---------------------------------------------------------------------------------
# Quickstart cheatsheet
# -------------------------- -------------------------- ---------------------------
# Task                       Syntax                     Returns
# -------------------------- -------------------------- ---------------------------
#
# Start interface            (start-ui)                 NIL
#
# Parse a sentence           (parse '(sentence))        Intension
#
# Build a model              (build-model intension)    List of models
#
# Update a model             (build-model intension
#                                         list-of-mods) List of models
#
# Print model                (print-model model)        Printed model, nil
#
# Infer                      (infer '((sentence1)
#                                     (sentence2)))     Printed conclusions, nil


class AbstractIntension(ABC):
    """"""

    def __init__(self):
        """TODO: to be defined1. """
        ABC.__init__(self)


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
    def find_referent_in_model(self):
        "Returns referent in model if exists"




class QuantifiedIntension():

    """
    Quantified Intension.

    Intension for quantified assertions
    """
    def __init__(self, cardinality, numprop, boundary, polarity,
                 footnotes, subject, obj, relation):
        """TODO: to be defined1.

        Parameters
        ----------
        cardinality : TODO
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
        pass

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


class QuantifiedModel(AbstractMentalModel):

    """Quantified model in which all instances are individuals"""

    def __init__(self, individuals):
        """
        Parameters
        ----------
        individuals : TODO

        """

        self._individuals = individuals


class SententialModel(AbstractMentalModel):

    """
    Sentential model in which all instances are conjunctions of atomic
    sentences, i.e., terms that stand in place of propositions
    """

    def __init__(self, possibilities):
        """
        Parameters
        ----------
        possibilities : TODO
        """
        self._possibilities = possibilities


class TemporalModel(AbstractMentalModel):

    """
    Temporal model in which all instances are moments, i.e., episodic markers of
    past, present, future points in time along a linear timeline
    """

    def __init__(self, moments):
        """

        Parameters
        ----------
        moments : TODO

        """

        self._moments = moments
