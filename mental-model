#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from pyMentalModels.modal_parser import parse_format
from pyMentalModels.operators import intuit_op, explicit_op
from pyMentalModels.numpy_reasoner import mental_model_builder
from pyMentalModels.pretty_printing import pretty_print_atom_assign
from pyMentalModels.infer import infer


import argparse
import logging


def main(args):
    mode = intuit_op if args.mode == "intuitive" else explicit_op

    expressions_to_parse = args.expression.split(", ")

    sympified_expressions = [
        parse_format(expr, mode=mode)
        for expr in expressions_to_parse
    ]
    print(sympified_expressions)

    models = []
    for sympified_expression in sympified_expressions:
        print("The expression to be evaluated is: {}".format(sympified_expression))
        model = mental_model_builder(sympified_expression)
        print(model)
        models.append(model)
        print("The mental model that has been created is:")
        for possible_world in model.model:
            print(pretty_print_atom_assign(model.atoms_model, possible_world, args.mode))

    if len(models) <= 1:
        return "Nothing to infer"
    result = infer(models)
    if not result:
        print("The result is the empty model", result.model)
    for possible_world in result.model:
            print(pretty_print_atom_assign(result.atoms_model, possible_world, args.mode))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="pyMentalModel Reasoner")
    parser.add_argument("expression", help="Expressions to be parsed, separated by comma. i.e. 'A, A -> B'")
    parser.add_argument("-m", "--mode", choices=["intuitive", "explicit"], default="intuitive", help="Can be either intuitive or explicit")
    parser.add_argument("-v", "--verbose", choices=["INFO", "DEBUG"], default="INFO", help="Level of verbosity to set for the program")

    args, unknowns = parser.parse_known_args()

    log_lvl = logging.INFO if args.verbose == 'INFO' else logging.DEBUG
    logging.basicConfig(level=log_lvl)

    if unknowns:
        logging.warning('Found unknown arguments!')
        logging.warning("{}".format(unknowns))
        logging.warning('These will be ignored')
    main(args)
