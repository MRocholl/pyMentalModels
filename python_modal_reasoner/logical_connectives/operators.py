#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-


""" Default operator name mapping """

op_names = {'[]': "Necessary",
            '<>': "Possibly",
            '~': "Not",
            '|': "Or",
            '&': "And",
            '->': "Implies",
            '<->': "Equivalent",
            '^': "Xor",
            }


""" Operators to be used when building fast model """

intuit_op = {'[]': "Necessary",
             '<>': "Possibly",
             '~': "Not",
             '|': "Xor",
             '&': "And",
             '->': "And",
             '<->': "And",
             '^': "Xor",
             }
