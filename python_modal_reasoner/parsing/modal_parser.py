#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-


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


def sympify_formatter(args, rules):
    """ Formatting function to make the parsed list sympify-readable
        For sympify refer to:  http://docs.sympy.org/latest/modules/core.html
    """
    if len(args) == 1 or isinstance(args, str):
        return "{}".format(args)
    if len(args) == 2:
        op, arg = args
        return "{}({})".format(rules[op], sympify_formatter(arg, rules))
    if len(args) >= 3:
        op = rules[args[1]]
        arguments = (sympify_formatter(expr, rules) for expr in args[::2])
        # Sympify takes general form of Operator(#args > 2)
        return "{operator}({f_args})".format(operator=op,
                                             f_args=", ".join(arguments))


