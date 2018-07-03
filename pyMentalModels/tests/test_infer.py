#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-


from pyMentalModels.numpy_reasoner import mental_model_builder
from pyMentalModels.infer import infer, InferenceTask

from sympy import symbols
from sympy.logic.boolalg import And, Or, Xor, Implies, Equivalent, Not
from pyMentalModels.numpy_reasoner import Insight
from pyMentalModels.modal_parser import parse_format
from pyMentalModels.constants import POS_VAL, EXPL_NEG, IMPL_NEG

import numpy.testing as npt
import numpy as np



def _eval_expr(expressions, mode):
    # Does the right thing
    result = infer([mental_model_builder(parse_format(expr), mode) for expr in expressions], InferenceTask.FOLLOWS)
    return result.model


def test_infer():
    A, B, C = symbols("A B C")


def test_premise_parirings():
    npt.assert_array_equal(_eval_expr(["A & ~A", ], Insight.INTUITIVE), np.array([[]]))
    npt.assert_array_equal(_eval_expr(["A | ~A", ], Insight.INTUITIVE), np.array([[POS_VAL, ], [EXPL_NEG, ]]))
    npt.assert_array_equal(_eval_expr(["B", "A -> B"], Insight.INTUITIVE), np.array([[POS_VAL, POS_VAL]]))
    npt.assert_array_equal(_eval_expr(["~A", "A -> B"], Insight.INTUITIVE), np.array([[]]))
    npt.assert_array_equal(_eval_expr(["~A", "A -> B"], Insight.EXPLICIT), np.array([[-4., 2.], [-4., -2.]]))
    npt.assert_array_equal(_eval_expr(["A", "A -> B", "B"], Insight.INTUITIVE), np.array([[2., 2.]]))
    npt.assert_array_equal(_eval_expr(["A", "A -> B", "B"], Insight.EXPLICIT), np.array([[2., 2.], [2., 2.], [2., 2.]]))
    npt.assert_array_equal(_eval_expr(["A", "A -> B", "A & B & C"], Insight.INTUITIVE), np.array([[2., 2., 2]]))
    npt.assert_array_equal(_eval_expr(["A", "A -> B", "A & B & C"], Insight.EXPLICIT), np.array([[2., 2., 2], [2., 2., 2], [2., 2., 2]]))
    npt.assert_array_equal(_eval_expr(["A", "A -> (B & C)", "A & B & C"], Insight.INTUITIVE), np.array([[2., 2., 2.]]))
    npt.assert_array_equal(_eval_expr(["A", "A -> (B & C)", "A & B & C"], Insight.EXPLICIT), np.array([[2., 2., 2.], [2., 2., 2.], [2., 2., 2.], [2., 2., 2.], [2., 2., 2.]]))
    npt.assert_array_equal(_eval_expr(["A", "A -> B", "B & A"], Insight.INTUITIVE), np.array([[2., 2.]]))
    npt.assert_array_equal(_eval_expr(["A", "A -> B", "B & A"], Insight.EXPLICIT), np.array([[2., 2.], [2., 2.], [2., 2.]]))
    npt.assert_array_equal(_eval_expr(["A -> B", "A & ~B"], Insight.INTUITIVE), np.array([[]]))
    npt.assert_array_equal(_eval_expr(["A -> B", "A", "~B"], Insight.INTUITIVE), np.array([[]]))
    npt.assert_array_equal(_eval_expr(["A | B", "A"], Insight.INTUITIVE), np.array([[2., -2.], [2., 2.], [2., 2.]]))
    npt.assert_array_equal(_eval_expr(["A | B", "B"], Insight.INTUITIVE), np.array([[2., 2.], [-2., 2.], [2., 2.]]))
    npt.assert_array_equal(_eval_expr(["A | B", "A & B"], Insight.INTUITIVE), np.array([[2., 2.], [2., 2.], [2., 2.]]))
    npt.assert_array_equal(_eval_expr(["A", "A | B"], Insight.INTUITIVE), np.array([[2., -2.], [2., 2.], [2., 2.]]))
    npt.assert_array_equal(_eval_expr(["A | B", "C"], Insight.INTUITIVE), np.array([[2., -2., 2.], [-2., 2., 2.], [2., 2., 2.]]))

# #| Illustrative calls using test-task for different tasks
#
# (test-task nil            *single-premises*)
# (test-task 'necessary?    *illusions-2*)
# (test-task 'what-follows? *premises-for-what-follows*)
# (test-task 'what-follows? *premises-for-modulation*)
# (test-task 'necessary?    *premises-it-follows*)
# (test-task 'necessary?    *it-follows-modulation*)
# (test-task 'necessary?    *defeasance-examples*)
# (test-task 'necessary?    *infer-cases*)
# (test-task 'possible?     *hinterecker*)
# (test-task 'verify?       *premises-to-verify*)
# (test-task 'probability?  *premises-to-verify*)
# (test-task nil            *sklarek-1*)            |#
#
# (defvar *single-premises* '(
#      ((if a then b))
#      ((iff a then b))
#      ((a ore b))
#      ((a or b))
#      ((a and not a))
#      ((a or not a))
#      ((iff j ore not q then j))
#      ((n or b ore comma b or c))
#      ((r and s ore r))
#      ((a ore b ore c)) ))
#
# (defvar *premises-it-follows* '(
#      ((If A then B)(A)(B))
#      ((If A then B)(Not A)(Not B))
#      ((If A then B)(B)(A))
#      ((If A then B)(Not B)(Not A))
#      ((Iff A then B)(A)(B))
#      ((Iff A then B)(Not A)(Not B))
#      ((Iff A then B)(B)(A))
#      ((Iff A then B)(Not B)(Not A))
#      ((A or B)(A)(Not B))
#      ((A or B)(B)(Not A))
#      ((A or B)(Not A)(B))
#      ((A or B)(Not B)(A))
#      ((A ore B)(A)(Not B))
#      ((A ore B)(B)(Not A))
#      ((A ore B)(Not A)(B))
#      ((A ore B)(Not B)(A))
#      ((A or B)(A ore B))
#      ((A ore B)(A or B))))
#
# (setf *test-intuition* '(
#  ((if a then b)(if b then c))
#  ((a ore b)(b ore c))
#  ((a ore b)(not a ore b))
#  ((if a then b)(if not a then b))
#  ((if a then b)(if a then not b))
#
#  ((a and b)(c ore d))
#  ((a and b)(a ore b))
#  ((if a then b)(a ore b))
#  ((if a then b)(a ore c))
#  ((if a then b)(not a ore c))
#  ((if a then b)(not a ore b))
#  ((a ore b ore c)(a))
#  ((a ore b ore c)(not a and not c))
# ; illusions
#  ((if a then b ore if not a then b))
#  ((a ore b ore c))
#  ((a ore b ore comma c ore b))
#  ((a ore b ore b))
#  ((a ore b ore c)(a))
#  ((if k then a ore if not k then a)(k))
#  ((if k then a ore if q then a)(k))
#  ((a or b ore comma not a or b)(b))
#  ((a ore b and comma not a ore b)(b))
#  ((r and s ore r)(not s))
#  ((iff j ore not q then j)(q)) ))
#
# (setf *test-m-d* '(
#     ((a or b)(b or a))
#     ((a and b and c)(a and b))
#     ((a or b)(a ore b))
#     ((a or b)(a and b))
#     ((a ore b)(a))
#     ((a ore b)(a or b))
#     ((a and b)(a or b))
#     ((a)(a ore b))
#     ((a ore b)(a ore c))
#     ((a ore b)(not a ore b))
#     ((a)(b))))
#
# (setf *hinterecker* '(
#                       ((A or B)(A and B))
#                       ((A ore B)(A and B))
#                       ((A or B)(A ore B))
#                       ((A ore B)(A or B))))
#
# (defvar *sklarek-1* '(
#                     ((A ore B)(not A ore B))
#                     ((A ore B)(A ore not B))
#                     ((A ore B)(not A ore not B))
#                     ((A ore not B)(not A ore B))
#
#                     ((A or B)(A or not B))
#                     ((A or B)(not A or B))
#                     ((A or B)(not A or not B))
#                     ((A or not B)(not A or B))
#                     ((A and B)(A or B))
#                     ((not A and not B)(not A or not B)) ))
#
# #|
# A ore B, ¬A ore B         1
# A ore B, A ore ¬B         2
# A ore B, ¬A ore ¬B        3
# A ore ¬B, ¬A ore B        4
# (A and B) ore B           5
# (A and ¬B) ore ¬B         6
# (A and B) ore (¬A and ¬B) 7
# (A and B) ore (¬A and B)  8
# (A ore ¬B), ¬B            9
# (¬A ore ¬B), ¬B          10
# (A ore ¬B), B            11
# (¬A ore ¬B), B           12
# |#
#
# (defvar *sklarek-1.2* '(
#                     ((A ore B)(C ore B))
#                     ((A ore B)(A ore C))
#                     ((A ore B)(not A ore not B))
#                     ((A ore not B)(not A ore B))
#
#                     ((A or B)(A or not B))
#                     ((A or B)(not A or B))
#                     ((A or B)(not A or not B))
#                     ((A or not B)(not A or B))
#                     ((A and B)(A or B))
#                     ((not A and not B)(not A or not B)) ))
#
# ; illusions and controls
# (setf *illusions-1* '(
#       ((if a then b ore comma if not a then b)(a))
#       ((a and not b ore comma not a and b)(a))
#       ((if a then b ore a)(a))
#       ((if a then b ore not a)(a))
#
#       ((a or b ore comma c or b)(not a and not b))
#       ((a ore b ore comma c ore b)(a and c))
#       ((a ore b ore comma c ore b)(not a and not c))
# ))
#
# (defvar *illusions-2* '(
#      ((if k then a ore if not k then a)(k)(a))
#      ((if k then a ore if q then a)(k)(a))
#      ((a or b ore comma not a or b)(b))
#      ((a or b ore comma c or b)(not a and not c)(b))
#      ((a ore b and comma not a ore b)(b))
#      ((a or b and comma not a or b)(b))
#      ((r and s ore r)(not s))
#      ((iff j ore not q then j)(q)) ))
#
# (defvar *infer-cases* '(
#                          ((If A then B)(A)(not B))
#                          ((A)(If A then comma B and C)(A and B and C))
#                          ((A)(if A or B then C)(C))
#                          ((A or B)(A and B))
#                          ((A)(A or B))
#                          ((A ore B)(C and D))))
#
# ; Longer list of illustrative inferences:
# (defvar *illustrations* '(
#                         ((A and not A))
#                         ((A or not A))
#                         ((B)(If A then B))
#                         ((Not A)(If A then B))
#                         ((A)(If A then B)(B))
#                         ((A)(If A then B)(A and B and C))
#                         ((A)(If A then comma B and C)(A and B and C))
#                         ((A)(If A then B)(B and A))
#                         ((If A then B)(A and not B))
#                         ((If A then B)(A)(not B))
#                         ((A or B)(A))
#                         ((A or B)(B))
#                         ((A or B)(A and B))
#                         ((A)(A or B))
#                         ((A or B)(C))
#                         ((A)(A ore B)(not B))
#                         ((not A)(A ore B)(B))
#                         ((not A)(A or B)(B))
#                         ((A or B)(Not B)(A))
#                         ((A or B)(Not A)(Not A and B and C))
#                         ((A or B)(Not B)(A and not B))
#                         ((A or B)(Not A)(Not B))
#                         ((A ore B)(A or B))
#                         ((A or B)(A ore B))
#                         ))
#
# (defvar *illusions* '(
#      ((if there is a king then there is an ace ore if not there is a king then there is an ace)(there is an ace))
#      ((you have the bread ore comma you have the soup ore you have the salad)(you have the bread)
#       (you have the soup ore you have the salad))
#      ((albert is here or betty is here ore comma charlie is here or betty is here)
#       (not albert is here and not charlie is here)(betty is here))
#      ((king or ace ore comma queen or ace)(ace))
#      ((iff jack ore not queen then jack))
#      ((there is a nail or there is a bolt ore comma there is a bolt and there is a wrench)
#       (there is a nail and there is a bolt and there is a wrench))
#      ((red and square ore red))))
#
# (defvar *premises-for-modulation* '(
#    ((if raining then hot)(not raining))
#    ((if not raining then not Louvre in Paris)(raining))
#    ((if raining then pouring)(not raining))
#    ((not raining or not pouring)(not raining))
#    ((if god exists then atheism is wrong)(not god exists))
#    ((god exists or atheism is right)(atheism is right))
#    ((iff god exists then atheism is right)(god exists))))
#
#
# (defvar *it-follows-modulation* '(
#     ((if louvre in paris then he is married)(he is married))
#     ((if louvre in paris then not he is married)(he is married))
#     ((if not louvre in paris then he is married)(not he is married))
#     ((if not louvre in paris then not he is married)(not he is married))
#     ((if she is married then not louvre in paris)(not she is married))
#     ))
#
# (setf *defeasance-examples* '(
#    ((if a poisonous snake bites her then she dies)(a poisonous snake bites her)(not she dies))
#    ((if pull trigger then gun fires)(pull trigger)(not gun fires))))
#
# ;----------------------------------------------------
# ; Part 9.3: List of inferences used for modeling data
# ;----------------------------------------------------
# #|
# I.Necessary?
#  To model Hinterecker et al Expt 1: inferences from disjunctions to disjunction
# A or B but not both.
# Therefore, A or B or both.	Valid	 Reject	 3
# A or B or both.
# Therefore, A or B but not both.	Invalid	 Reject	24
#
# With *gamma* of .01, weak validity is almost certain to occur, and so:
# (inference '((a or b)(a ore b)) 'necessary?) => YES
# (inference '((a ore b)(a or b)) 'necessary?) => NO
# With *gamma* of .99 weak validity is almost certain NOT to occur, and so:
# (inference '((a or b)(a ore b)) 'necessary?) => NO
# (inference '((a ore b)(a or b)) 'necessary?) => NO
#
# II. POSSIBLE?
# 1. Hinterecker et al Expt 3:
#   A or B or both
#   (inference '((a or b)(a)) 'possible?) sys1: yes sys2: yes
#   Therefore, possibly A	 	        91% respond yes
#   (inference '((a or b)(b)) 'possible?) sys1: yes sys2: yes
#   Therefore, possibly B	 	        94% respond yes
#   (inference '((a or b)(a and b)) 'possible?) sys1: yes sys2: yes
#   Therefore, possibly A and B	        88% respond yes
#   (inference '((a or b)(not a and not b)) 'possible?) sys1: no sys2: no
#   Therefore, possibly not A and not B	18% respond yes
# 5. Goodwin & Johnson-Laird (2016):
#   If A then B
#   (inference '((if a then b)(a and b)) 'possible?)         sys1: yes  sys2: yes  ok
#   Therefore, possibly A and B.
#   (inference '((if a then b)(a and not b)) 'possible?)     sys1: no   sys2: no   ok
#   Therefore, possibly A and not B.
#   (inference '((if a then b)(not a and b)) 'possible?)     sys1: no  sys2: yes   ok
#   Therefore, possible not-A and B.
#   (inference '((if a then b)(not a and not b)) 'possible?) sys1: yes  sys2: yes  ok
#   Therefore, possibly not-A and not-B.
# 6. Hinterecker et al Expt 1:
#   A or B,
#   (inference '((if a then b)(not a and not b)) 'possible?)  sys1: yes  sys2: yes ok
#   Therefore, possibly A and B.
#   A ore B,
#   (inference '((a ore b)(a and b)) 'possible?) sys1: no   sys2: no               ok
#   Therefore, possibly A and B.
#   A or B.
#   (inference '((a or b)(a ore b)) 'possible?)  sys1: no  sys2: yes               ok
#   Therefore, possibly A ore B.
# |#
#
# (defparameter *schroyens-&-schaeken-2003-exp1*
#   '((((if a then b) (a))                                     necessary? YES  100)
#     (((if a then b) (b))                                     necessary  NO   -1)
#     (((if a then b) (not a))                                 necessary? NO   -1)
#     (((if a then b) (not b))                                 necessary? YES  -1)))
#
# (defparameter *hinterecker-et-al-2016-exp1*
#   '((((A or B) (A and B))                                    possible?  YES  82)
#     (((A ore B) (A and B))                                   possible?  NO   10)
#     (((A ore B) (A or B))                                    necessary? NO   3)
#     (((A or B) (A ore B))                                    necessary? YES  24)))
#
# (defparameter *hinterecker-et-al-2016-exp3*
#   '((((A or B)(A))                                           possible?  YES  91)
#     (((A or B)(B))                                           possible?  YES  94)
#     (((A or B)(A and B))                                     possible?  YES  88)
#     (((A or B)(Not A and not B))                             possible?  YES  18)))
#
# (defparameter *khemlani-&-jl-2009-exp2*
#   '((((a and b ore comma b ore c) (not a and b and not c))   possible?  YES  90)
#     (((a and b ore comma b ore c) (a and b and not c))       possible?  NO   40)
#     (((a and b ore comma b or c) (not a and b and not c))    possible?  YES  100)
#     (((a and b ore comma b or c) (a and b and not c))        possible?  NO   20)
#     (((a and b or comma b ore c) (not a and b and c))        possible?  NO   80)
#     (((a and b or comma b ore c) (a and not b and c))        possible?  YES  20)
#     (((a and b or comma b or c) (not a and not b and not c)) possible?  NO   100)
#     (((a and b or comma b or c) (a and not b and c))         possible?  YES  30)))
#
# ;---------------------------------------------------------------------------------------------------------------------------
# ; End of file
# ;---------------------------------------------------------------------------------------------------------------------------
#
#
#
#
#
