#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-


expressions = [
    "(<> Hund | <> Katze) -> ([] Tier & [] Lebewesen)",
    "Bread ^ Butter ^ Salad",
]  # To be exported to own submodule at later point /tests

parsed_expressions = [
    [[['<>', 'Hund'], '|', ['<>', 'Katze']], '->', [['[]', 'Tier'], '&', ['[]', 'Lebewesen']]],
    ['Bread', '^', 'Butter', '^', 'Salad'],
    # other parsed expressions to be added here
]
