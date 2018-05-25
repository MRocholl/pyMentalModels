#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-





""" Operators to be used when building fast model """

# XXX `Or` might be mapped to Xor in case of an intuitive model
# XXX

intuit_op = {
    '[]': "Necessary",
    '<>': "Possibly",
    '~': "Not",
    '|': "Or",
    '&': "And",
    '->': "And",
    '<->': "And",
    '^': "Xor",
}
