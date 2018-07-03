#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
from ABC import ABC, abstractmethod
from math import inf
import mreasoner_port.constants as constants

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


class QuantifiedModel(AbstractMentalModel):

    """Quantified model in which all instances are individuals"""

    def __init__(self, individuals):
        """
        Parameters
        ----------
        individuals : TODO

        """

        self._individuals = individuals

    def generate_all_combinations(self, terms, quantified_intension):
        """
        (defmethod generate-all-combinations ((terms list) (intension q-intension))
              (when (is-setmem intension :n 1) (setf terms (remove-if #'(lambda (x) (equal x (subject intension))) terms)))
              (if (null terms) (list nil)
                  (append (mapcar #'(lambda (x) (cons (first terms) x)) (generate-all-combinations (rest terms) intension))
                          (mapcar #'(lambda (x) (cons (negate (first terms)) x)) (generate-all-combinations (rest terms) intension)))))
        """
        from itertools import product
        return [combination for comination in product(terms) if ...]

    def start_model_stochastically(self, quantified_intension, attempts=constants.build_attempts):
        """
        TODO: Docstring for start_model_stochastically.

            (defmethod start-model-stochastically ((intension q-intension) &key (attempt *build-attempts*))
              (let* ((capacity              (generate-size))
                     (subject               (subject intension))
                     (object                (object intension))
                     (full-individuals      (generate-all-combinations (list subject object) intension))
                     (canonical-individuals (cond
                                             ((is-all      intension)      `((,subject ,object)))
                                             ((is-some     intension)      `((,subject ,object) (,subject)))
                                             ((is-none     intension)      `((,subject ,(negate object)) (,(negate subject) ,object)))
                                             ((is-some-not intension)      `((,subject ,(negate object)) (,subject ,object) (,object)))
                                             ((is-most     intension)      (if (affirmative-intension intension)
                                                                               `((,subject ,object) (,subject))
                                                                             `((,subject ,(negate object)) (,subject ,object))))
                                             ((is-setmem    intension :n 1) (if (affirmative-intension intension)
                                                                                `((,subject ,object) (,object))
                                                                              `((,subject ,(negate object)) (,object))))))
                     sample-individuals individuals model)
                (loop repeat capacity do
                      (setf sample-individuals (if (build-canonical?) canonical-individuals full-individuals))
                      (push (nth (random (length sample-individuals)) sample-individuals) individuals))
                (setf model (make-instance 'q-model :indivs individuals :fn (list intension) :capacity capacity))
                (cond
                 ((and (verify intension (list model))
                       (find-referent-in-model subject model)
                       (find-referent-in-model object model))  model)
                 ((> attempt 0)                                (start-model-stochastically intension :attempt (1- attempt)))
                 (t                                            (error "Could not construct model.")))))

        Parameters
        ----------
        quantified_intension : TODO
        attempts : TODO, optional

        Returns
        -------
        TODO

        """
        capacity = generate_size()
        subject = quantified_intension.subject
        obj = quantified_intension.obj
        full_individuals = generate_all_combinations( [self.subj, self.obj], quantified_intension )
        canonial_individuals =

    """

            (defmethod add-object ((intension intension) models)
              "Add-object calls start-mod to add an object to each model in modelset.
               It assumes that each model in model set contains the subject of the intension"
              (let* (outmodels)
                (dolist (mod models outmodels)
                  (setf outmodels (append outmodels (list (funcall #'start-mod intension (copy-class-instance mod))))))
                (trc "System 1" (format nil "Added object of ~A to model" (abbreviate intension)) :m outmodels)
                outmodels))

            #|

            Function calls
            start-mod                 -- starts a model or adds obj to it
               make-individuals         -- to start a model by listing a set of individuals of given cardinality
               negate-property          -- negates a property (in API)
               combine-footnotes        -- combines a fn in existing model with one for current intension
                  find-footnote         -- rtns footnote from a model (in API)
               add-new-property         -- adds a new-property to n individuals in model that contain old-property
                                           and drops footnote from model (because combine-footnotes will update it)
                  add-property          -- adds property, which is a list to allow for negatives, to an individual
                  member-property       -- rtns property iff it is in indiv

             Modified Feb 22 so that footnote is set to intension of premise, parameter is intension instead
             of predicate
             |#

            (defmethod start-mod ((intension q-intension) &optional mod)
            "if no model, makes cardinal number of arg
             if negative polarity, such as 'no', negates predicate argument, '(B) => (- B)
             if negative polarity, such as 'some not', negates predicate too
             if null footnote, i.e., 'some, adds outliers
             if numprop less that 1 (it's a proportion) so multiplies it by cardinality to yield a number that is a
                      proportion of cardinality
             adds property in predicate to individuals in model having art in them"
              (let* ((card (cardinality-value intension)) (numprop (numprop-value intension))
                     (subj (subject intension)) (obj (object intension)) (model mod))
                (when (null mod) (setf model (make-individuals card subj))) ; inserts card initial individuals

                (cond

                 ; For set-membership assertions
                 ((is-setmem intension :n 1)
                  (cond
                   ((negative-intension intension)
                    (setf (individuals model) (add-new-property subj (negate-property obj) (individuals model) 1))
                    (when (null mod) (setf (individuals model) (append (individuals model) (individuals (make-individuals 3 obj))))))
                   ((affirmative-intension intension)
                    (setf (individuals model) (add-new-property subj obj (individuals model) 1))
                    (when (null mod) (setf (individuals model) (append (individuals model) (individuals (make-individuals 2 obj))))))))

                 ; For assertions with determiner: "most"
                 ((or (is-most intension))
                  (cond
                   ((negative-intension intension)
                    (setf (individuals model) (add-new-property subj (negate-property obj) (individuals model) (- (get-referent-cardinality subj model) 1)))
                    (setf (individuals model) (add-new-property subj obj (individuals model) (- card numprop))))
                   ((afirmative-intension intension)
                    (setf (individuals model) (add-new-property subj obj (individuals model) (- (get-referent-cardinality subj model) 1))))))

                 ; For assertions with determiner: "none"
                 ((is-none intension)
                  (setf (individuals model) (append (individuals model) (individuals (make-individuals 1 obj))))
                  (setf (individuals model) (add-new-property subj (negate-property obj) (individuals model) (get-referent-cardinality subj model))))

                 ; For assertions with quantifier: "some_not"
                 ((is-some-not intension)
                  (setf (individuals model) (append (individuals model) (individuals (make-individuals 1 obj))))
                  (setf (individuals model) (add-new-property subj (negate-property obj) (individuals model) numprop)))

                 ; For assertions with determiner: "some"
                 ((is-some intension)
                  (setf (individuals model) (add-new-property subj obj (individuals model) numprop)))

                 ; For assertions with determiner: "all"
                 ((is-all intension)
                  (cond
                   ((affirmative-intension intension)
                    (setf (individuals model) (add-new-property subj obj (individuals model) (get-referent-cardinality subj model))))
                   ((negative-intension intension)
                    (setf (individuals model) (add-new-property subj (negate-property obj) (individuals model) (get-referent-cardinality subj model)))))))

                (add-footnote model intension)
                model))

            (defun add-new-property (old-property new-property indivs numprop)
              " ok adds a new-property to n individuals in model that contain old-property
               (add-new-property '(A) '(B) '( ((A))((A))((A)) ) 1) =>
                 (((A) (B)) ((A)) ((A)))
               (add-new-property '(A) '(B) '( ((A))((A))((A)) ) 3)
                 (((A) (B)) ((A) (B)) ((A) (B)))
               But drops footnote, because start-mod updates it"
              (cond
            ;   ((and (null indivs) (> numprop 0))
            ;    (append indivs (list (list new-property)) (add-new-property old-property new-property indivs (decf numprop))))
               ((null indivs) nil)
               ((and (not (member-property new-property (first indivs)))
                     (member-property old-property (first indivs))
                     (not (member-property (negate-property new-property) (first indivs)))
                     (> numprop 0))
                (cons (add-property new-property (first indivs) old-property)
                      (add-new-property old-property new-property (rest indivs) (decf numprop))))
               (t
                (cons (first indivs) (add-new-property old-property new-property (rest indivs) numprop)))))

            (defun add-property (property indiv &optional old-property)
              "ok adds property, which is a list to allow for negatives, to an individual, e.g.
               (add-property '(baker) '((artist)(chemist))) => ((ARTIST) (CHEMIST) (BAKER))"
              (if old-property
                  (let* ((pos-in-indiv     (position old-property indiv :test 'equal))
                         (pos-in-rev-indiv (position old-property (reverse indiv) :test 'equal)))
                    (if (>= pos-in-indiv pos-in-rev-indiv)
                        (append indiv (list property))
                      (append (list property) indiv)))
                (reverse (cons property (reverse indiv)))))

            (defun member-property (property indiv)
              "ok [from file highlevel.lisp] checks whether individual in model has property
               rtns property iff it is in indiv
                (member-property '(- b) '((a)(- b)(c))) => (- B)"
              (cond((null indiv) nil)
                   ((equal property (car indiv)) property)
                   (t (member-property property (cdr indiv)))))
    """


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
