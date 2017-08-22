#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
# vim:foldmethod=marker


from sympy.logic.boolalg import And, Or, Xor, Implies, sympify
from parsing.modal_parser import parse_expr, sympify_formatter
from reasoner.reasoner import populate_np_array
from data.expressions import expressions, parsed_expressions
from logical_connectives.operators import op_names

DEBUG = True

cat_dog_expr, triv_ragni_ex = parsed_expressions


#  Sympify formatter (transforms list to string that is sympify-readable) {{{ #



sympify_ready_triv_expr = sympify_formatter(triv_ragni_ex, op_names)
sympify_ready_cat_dog_expr = sympify_formatter(cat_dog_expr, op_names)
sympified_expr_triv = sympify(sympify_ready_triv_expr)
sympified_expr_pars = sympify(sympify_ready_cat_dog_expr)
#  }}} Sympify formatter (transforms list to string that is sympify-readable) #


if DEBUG:
    print("sympify_ready_triv_expr\t", sympify_ready_triv_expr)
    print("sympify_ready_cat_dog_expr\t", sympify_ready_cat_dog_expr)
    print()
    print("The outer-most junctor is of type: ", type(sympified_expr_triv))
    print("The atoms are: ", sympified_expr_triv.atoms())
    print("The outer-most junctor is of type: ", type(sympified_expr_pars))
    print("The atoms are: ", sympified_expr_pars.atoms())

    """
    print(combs)
    for combination in combs:
        for term, value in truth_table(sympified_expr, combination):
            print(term, value)
    """

possible, necessary, possible_worlds = populate_np_array(sympified_expr_triv)

if DEBUG:
    print()
    print("The modal possible valuations of the atoms are: ", possible)
    print("The modal necessary valuations of the atoms are: ", necessary)
    print("The possible worlds are: \n", possible_worlds)

