#######################################################################
#                       Quantificational Models                       #
#######################################################################

""" There are five counterexample search strategies for quantificational models,
   as described in Khemlani & Johnson-Laird (2012). The processes of inference. They
   include:
   - moving properties from one individual to another
   - breaking properties apart from one another to create new individuals
   - adding individuals
   - breaking and adding negative individuals
   - negating individuals
"""


def move_individuals():
    pass


def break_and_add_negative():
    pass


def add_individuals():
    pass


def break_model():
    pass


def negate_individuals():
    pass


def replace_properties():
    pass


def exhaustive_search():
    pass


search_strategies = (
    move_individuals, break_and_add_negative,
    add_individuals, break_model,
    negate_individuals, replace_properties,
    exhaustive_search
)
#######################################################################
#                           Temporal Models                           #
#######################################################################
"""There are N counterexample search strategies for temporal models,
   as described in Khemlani et al. (under review). Naive temporality. They
   include:
   - shifting event earlier
   - shifting event later
"""


def shift_event(earlier_or_later="earlier"):
    """
    Parameters
    ----------
    earlier_or_later : TODO, optional

    Returns
    -------
    TODO

    """
    pass

#######################################################################
#                          Find constraints                           #
#######################################################################


def recursively_find_constraints(prop):
    """"
    Gets initial set of constraints for property, then iterates through
    all members of the set of constraints and checks to see if there are
    any additional constraints that apply. If any new constraints are found,
    then applies recursively-find-constraints one the new set of constraints.


    recursively-find-constraints '(A) '(list Aab Aac))
    => '((B) (A) (C))
    (recursively-find-constraints '(A) (list Eab Ebc))
    => '((A) (- B))"

    Parameters
    ----------
    prop:
        Property for which to find the relevant constraints

    Returns
    -------
        Valid model for `prop` given the constraints
    """
    # XXX define get_constraints
    constraints = set(get_constraints(prop))  # get constraints for property and eliminate duplicates

    (dolist (c constraints)
      (setf new-constraints
            (remove-duplicates (append new-constraints (find-constraints c fn)) :test #'equalp))
      (setf new-cont new-constraints))
    (if (every #'(lambda (x) (member x constraints)) new-constraints)
        new-constraints
      (remove-duplicates
       (append new-constraints
               (recursively-find-constraints property fn
                                             (set-difference new-constraints
                                                             constraints :test #'equal)))
       :test #'equal))))



def find_constraints(prop):
    """
    Returns constraint list for a particular property, i.e.,
    a list of all properties that *must* occur with that property.

    Parameters
    ----------
    prop : TODO

    Returns
    -------
    TODO

    Examples:
    >>> find_constraints()

    """

    # (if (null fn) nil
    #     (remove-duplicates (append (if (equal '- (first property)) nil
    #                              (find-constraint property (first fn)))
    #                            (find-constraints property (rest fn)))
    #                    :test #'equal)))

def find_constraint(intension_type="quantified"):
    """
    Quantified:
        If property != subject, then nil.
        Else, if footnote is in A-mood, return subject and object
        Else, if footnote is in E-mood, return subject and -object
        Else return nil

    Temporal:
        If property != subject, then nil.
        Else, if footnote shows while or during relation, return subject and object
        Else return nil

    Parameters
    ----------
    prop : TODO
    intension_type: str
        can be either quantified, temporal

    Returns
    -------
    TODO

    """
    pass
    # XXX Quantified
    # (cond
    #  ((is-all fn)    (list (subject fn) (object fn)))
    #  ((is-none fn)   (list (subject fn) (negate-property (object fn))))
    #  ((is-setmem fn) (list (subject fn) (object fn)))
    #  (t              nil))))
    # XXX Temporal
    #(when (or (equal (first property) (subject fn))
    #           (equal (first property) (object fn)))
    #   (cond
    #    ((is-while fn) (list (list (subject fn)) (list (object fn))))
    #;   ((is-during fn) (list (subject fn)) (list (list (object fn))))            ;;; NOT WORKING!!! ssk 27-10-2015
    #    (t           nil))))
