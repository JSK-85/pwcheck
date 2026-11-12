"""Classify passwords as 'weak' or 'strong' based on length, character sets,
and common-word substrings.
"""

from .automaton import AhoCorasick

_DIGITS = frozenset("0123456789")
_UPPER = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
_LOWER = frozenset("abcdefghijklmnopqrstuvwxyz")


def _only(pwd, charset):
    return all(c in charset for c in pwd)


def get_password_strength(passwords, common_words):
    """Return 'weak' or 'strong' for each password using an Aho-Corasick automaton."""
    ac = AhoCorasick(common_words)
    results = []
    for pwd in passwords:
        weak = (
            len(pwd) < 6
            or _only(pwd, _DIGITS)
            or _only(pwd, _UPPER)
            or _only(pwd, _LOWER)
            or ac.contains_any(pwd)
        )
        results.append("weak" if weak else "strong")
    return results


def get_password_strength_naive(passwords, common_words):
    """Reference implementation using a nested loop for substring matching."""
    results = []
    for pwd in passwords:
        weak = (
            len(pwd) < 6
            or _only(pwd, _DIGITS)
            or _only(pwd, _UPPER)
            or _only(pwd, _LOWER)
            or any(w and w in pwd for w in common_words)
        )
        results.append("weak" if weak else "strong")
    return results

