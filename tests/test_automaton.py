import random
from pwcheck import AhoCorasick


def brute_force(patterns, text):
    return any(p in text for p in patterns if p)


def test_classic_overlapping_patterns():
    ac = AhoCorasick(["he", "she", "his", "hers"])
    assert ac.contains_any("ushers")
    assert ac.first_match("ushers") == (2, 4)
    assert not ac.contains_any("xyz")


def test_pattern_is_suffix_of_another():
    ac = AhoCorasick(["abcd", "bc"])
    assert ac.first_match("xabcdx") == (2, 4)


def test_empty_and_no_patterns():
    assert not AhoCorasick([]).contains_any("anything")
    assert not AhoCorasick([""]).contains_any("anything")


def test_matches_brute_force_randomized():
    rnd = random.Random(7)
    for _ in range(500):
        pats = ["".join(rnd.choices("abc", k=rnd.randint(1, 4)))
                for _ in range(rnd.randint(1, 6))]
        text = "".join(rnd.choices("abc", k=rnd.randint(0, 30)))
        assert AhoCorasick(pats).contains_any(text) == brute_force(pats, text), (pats, text)

