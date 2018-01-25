#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-


""" Default operator name mapping """

explicit_op = {
    '[]': "Necessary",
    '<>': "Possibly",
    '~': "Not",
    '|': "Or",
    '&': "And",
    '->': "Implies",
    '<->': "Equivalent",
    '^': "Xor",
}


""" Operators to be used when building fast model """

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
