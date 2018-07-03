import re


quatificational_pattern = r"^(?P<mood>All|Some|No|Most) (?P<subject>\w+) \w+ (?P<negation>not )?(?P<object>\w+)$"
# ^(All|Some|No|Most)(\b.+\b)(are)(.+)
compiled_quantificational_pattern = re.compile(quatificational_pattern)

temporal_pattern = r"^(?P<subject>\w+) \w+ (?P<time_point>before|after|during|while) (?P<object>\w+)$"
compiled_temporal_pattern = re.compile(temporal_pattern)

assignment_pattern = r"(?P<subject>^\w+).*(?P<object>\b\w+$)"


intension_library = (
    # Set-membership intensions
    # -------------------------------------------------------------
    ("X-is-A", "X is an A"),
    ("X-isnot-A", "X is not an A"),
    ("X-is-B", "X is a B"),
    ("X-isnot-B", "X is not a B"),
    # Quantificational intensions (including "most", and "most_not"),
    # -------------------------------------------------------------
    ("Aab", "All A are B"),
    ("Aba", "All B are A"),
    ("Abc", "All B are C"),
    ("Acb", "All C are B"),
    ("Iab", "Some A are B"),
    ("Iba", "Some B are A"),
    ("Ibc", "Some B are C"),
    ("Icb", "Some C are B"),
    ("Eab", "No A are B"),
    ("Eba", "No B are A"),
    ("Ebc", "No B are C"),
    ("Ecb", "No C are B"),
    ("Oab", "Some A are not B"),
    ("Oba", "Some B are not A"),
    ("Obc", "Some B are not C"),
    ("Ocb", "Some C are not B"),
    ("Mab", "Most A are B"),
    ("Mba", "Most B are A"),
    ("Mbc", "Most B are C"),
    ("Mcb", "Most C are B"),
    ("Ma-b", "Most A are not B"),
    ("Mb-a", "Most B are not A"),
    ("Mb-c", "Most B are not C"),
    ("Mc-b", "Most C are not B"),
    ("aBb", "A happened before B"),
    ("aBc", "A happened before C"),
    ("aBd", "A happened before D"),
    ("aBe", "A happened before E"),
    ("bBa", "B happened before A"),
    ("bBc", "B happened before C"),
    ("bBd", "B happened before D"),
    ("bBe", "B happened before E"),
    ("cBa", "C happened before A"),
    ("cBb", "C happened before B"),
    ("cBd", "C happened before D"),
    ("cBe", "C happened before E"),
    ("dBa", "D happened before A"),
    ("dBb", "D happened before B"),
    ("dBc", "D happened before C"),
    ("dBe", "D happened before E"),
    ("eBa", "E happened before A"),
    ("eBb", "E happened before B"),
    ("eBc", "E happened before C"),
    ("eBd", "E happened before D"),
    # Temporal intensions
    # -------------------------------------------------------------
    ("aAb", "A happened after B"),
    ("aAc", "A happened after C"),
    ("aAd", "A happened after D"),
    ("aAe", "A happened after E"),
    ("bAa", "B happened after A"),
    ("bAc", "B happened after C"),
    ("bAd", "B happened after D"),
    ("bAe", "B happened after E"),
    ("cAa", "C happened after A"),
    ("cAb", "C happened after B"),
    ("cAd", "C happened after D"),
    ("cAe", "C happened after E"),
    ("dAa", "D happened after A"),
    ("dAb", "D happened after B"),
    ("dAc", "D happened after C"),
    ("dAe", "D happened after E"),
    ("eAa", "E happened after A"),
    ("eAb", "E happened after B"),
    ("eAc", "E happened after C"),
    ("eAd", "E happened after D"),
    ("aDb", "A happened during B"),
    ("aDc", "A happened during C"),
    ("aDd", "A happened during D"),
    ("aDe", "A happened during E"),
    ("bDa", "B happened during A"),
    ("bDc", "B happened during C"),
    ("bDd", "B happened during D"),
    ("bDe", "B happened during E"),
    ("cDa", "C happened during A"),
    ("cDb", "C happened during B"),
    ("cDd", "C happened during D"),
    ("cDe", "C happened during E"),
    ("dDa", "D happened during A"),
    ("dDb", "D happened during B"),
    ("dDc", "D happened during C"),
    ("dDe", "D happened during E"),
    ("eDa", "E happened during A"),
    ("eDb", "E happened during B"),
    ("eDc", "E happened during C"),
    ("eDd", "E happened during D"),
    ("aWb", "A happened while B"),
    ("aWc", "A happened while C"),
    ("aWd", "A happened while D"),
    ("aWe", "A happened while E"),
    ("bWa", "B happened while A"),
    ("bWc", "B happened while C"),
    ("bWd", "B happened while D"),
    ("bWe", "B happened while E"),
    ("cWa", "C happened while A"),
    ("cWb", "C happened while B"),
    ("cWd", "C happened while D"),
    ("cWe", "C happened while E"),
    ("dWa", "D happened while A"),
    ("dWb", "D happened while B"),
    ("dWc", "D happened while C"),
    ("dWe", "D happened while E"),
    ("eWa", "E happened while A"),
    ("eWb", "E happened while B"),
    ("eWc", "E happened while C"),
    ("eWd", "E happened while D"),
)


for mood, intension in intension_library:
    match_quant = re.match(compiled_quantificational_pattern, intension)
    match_temp = re.match(compiled_temporal_pattern, intension)
    if match_quant:
        print("quant")
        print(intension, match_quant.group("mood"), match_quant.group("subject"), match_quant.group("object"), True if match_quant.group("negation")else False)
    elif match_temp:
        print("temp")
        print(intension, match_temp.group("time_point"), match_temp.group("subject"), match_temp.group("object"))
    else:
        # raise ValueError("Welläh. this should never happen")
        print(intension, "specifying individual")
