#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from sympy import sympify
from typing import List, Dict

from pyMentalModels.custom_logical_classes import Necessary, Possibly


def parse_expr(expression):
    """
    Parses expression and returns a list

    """
    import pyparsing as pp

    # The following block consists of the grammar specification

    atom = pp.Word(pp.alphas)
    ops = pp.infixNotation(
        atom,
        [  # Operator precedence is given by the following order: 1. [] 2. <> 3....
            ("[]", 1, pp.opAssoc.RIGHT,),    # necessary
            ("<>", 1, pp.opAssoc.RIGHT,),    # possibly
            ('~', 1, pp.opAssoc.RIGHT),    # negation
            ('|', 2, pp.opAssoc.LEFT,),    # or
            ("&", 2, pp.opAssoc.LEFT,),    # and
            ("->", 2, pp.opAssoc.LEFT,),   # imply
            ("<->", 2, pp.opAssoc.LEFT,),  # biconditional
            ("^", 2, pp.opAssoc.LEFT,),    # xor
        ]
    )
    # Expressins are declared to be of the following form
    expr = ops + pp.ZeroOrMore(ops)
    return expr.parseString(expression)[0]


def sympify_formatter(args: List, rules: Dict[str, str]):
    """
    Formatting function to make the parsed list sympify-readable
    For sympify refer to:  http://docs.sympy.org/latest/modules/core.html

    Parameters:
    args: List[str]
        List of Lists with logical expressions

    rules: Dict[str, str]
        Dict that maps each logical operator to its sympify readable counterpart

    Returns
    -------
        Sympify ready formatted str of the original expression
    """
    if len(args) == 1 or isinstance(args, str):
        return "{}".format(args)
    elif len(args) == 2:
        op, arg = args
        return "{}({})".format(rules[op], sympify_formatter(arg, rules))
    elif len(args) >= 3:
        op = rules[args[1]]
        arguments = (sympify_formatter(expr, rules) for expr in args[::2])
        # Sympify takes general form of Operator(#args > 2)
        return "{operator}({f_args})".format(operator=op,
                                             f_args=", ".join(arguments))
    else:
        raise ValueError("Args cannot be empty list")


def parse_format(expression: str, mode):
    """
    Short function to both parse and format an expression and return a sympy object
    """
    parsed_expression = parse_expr(expression)
    return sympify(sympify_formatter(parsed_expression, mode), locals={"Necessary": Necessary, "Possibly": Possibly})
