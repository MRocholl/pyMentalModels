#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-

from pyMentalModels.modal_parser import parse_format
from pyMentalModels.numpy_reasoner import mental_model_builder, Insight
from pyMentalModels.pretty_printing import pretty_print_atom_assign
from pyMentalModels.infer import infer, InferenceTask


import argparse
import logging


def main(args):
    expressions_to_parse = args.expression.split(", ")

    sympified_expressions = [
        parse_format(expr)
        for expr in expressions_to_parse
    ]
    print("The following expressions have been parsed:")
    for exp in sympified_expressions:
        print("\t{}".format(exp))

    models = []
    for sympified_expression in sympified_expressions:
        print("The expression to be evaluated is: {}".format(sympified_expression))
        model = mental_model_builder(sympified_expression, args.mode)
        logging.debug("{}".format(model))
        models.append(model)
        print("The mental model that has been created is:")
        for possible_world in model.model:
            print(pretty_print_atom_assign(possible_world, model.atoms_model, args.mode))

    if len(models) <= 1:
        return "Nothing to infer"
    result = infer(models, args.infer)
    if not result:
        print("The result is the empty model", result.model)
    print(result)
    for possible_world in result.model:
            print(pretty_print_atom_assign(possible_world, result.atoms_model, args.mode))


if __name__ == "__main__":

    description = """
    This is an implementation of a Mental Model theory based Reasoner.
    """

    parser = argparse.ArgumentParser(prog="pyMentalModel Reasoner", description=description)
    parser.add_argument("expression", help="Expressions to be parsed, separated by comma. i.e. 'A, A -> B'")
    parser.add_argument("-m", "--mode", choices=["intuitive", "explicit"], default="intuitive", help="Can be either intuitive or explicit")
    parser.add_argument("-v", "--verbose", choices=["INFO", "DEBUG"], default="INFO", help="Level of verbosity to set for the program")
    parser.add_argument("-i", "--infer", choices=["what_follows?", "what_follows?", "necessary?", "possible?", "probability?", "verify?"], help="""\
            Choose what to check the mental models for.
            Choices are:
                1. what_follows?,
                2. necessary?,
                3. possible?,
                4. probability?,
                5. verify?
            Otherwise just builds model of each premise
            """)

    args, unknowns = parser.parse_known_args()

    args.infer = InferenceTask(args.infer)
    args.mode = Insight(args.mode)

    log_lvl = logging.INFO if args.verbose == 'INFO' else logging.DEBUG
    logging.basicConfig(level=log_lvl)

    if unknowns:
        logging.warning('Found unknown arguments!')
        logging.warning("{}".format(unknowns))
        logging.warning('These will be ignored')
    main(args)
