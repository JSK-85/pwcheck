import random
import string

from original_solution import getPasswordStrength as original_strength
from pwcheck import get_password_strength, get_password_strength_naive


def test_spec_examples():
    cw = ["password", "admin"]
    pws = ["Ab1", "123456", "ABCDEF", "abcdef", "myPassword1", "Xk9Qm2Lp"]
    assert get_password_strength(pws, cw) == ["weak", "weak", "weak", "weak", "strong", "strong"]


def test_common_word_substring():
    assert get_password_strength(["xxadminxxAB1"], ["admin"]) == ["weak"]
    assert get_password_strength(["xxAdminxxAB1"], ["admin"]) == ["strong"]


def test_mixed_letters_and_digits_are_strong():
    assert get_password_strength(["ABC123", "abc123"], []) == ["strong", "strong"]


def test_unicode_digit_not_treated_as_0_9():
    assert get_password_strength(["²²²²²²"], []) == ["strong"]


def test_empty_inputs():
    assert get_password_strength([], ["a"]) == []
    assert get_password_strength(["Abcd12"], []) == ["strong"]
    assert get_password_strength([""], ["a"]) == ["weak"]


def test_matches_naive_randomized():
    rnd = random.Random(3)
    alpha = string.ascii_letters + string.digits
    for _ in range(300):
        cw = ["".join(rnd.choices(alpha, k=rnd.randint(1, 4)))
              for _ in range(rnd.randint(0, 6))]
        pw = ["".join(rnd.choices(alpha, k=rnd.randint(0, 12)))
              for _ in range(20)]
        assert get_password_strength(pw, cw) == get_password_strength_naive(pw, cw)


def test_original_agrees_on_unambiguous_inputs():
    cw = ["password", "admin"]
    pws = ["Ab1", "123456", "ABCDEF", "abcdef", "myPassword1", "Xk9Qm2Lp"]
    assert original_strength(pws, cw) == get_password_strength(pws, cw)


def test_original_differs_on_mixed_alphanumeric():
    # isupper() and islower() ignore digits, so "ABC123".isupper() is True
    assert original_strength(["ABC123"], []) == ["weak"]
    assert get_password_strength(["ABC123"], []) == ["strong"]

    assert original_strength(["abc123"], []) == ["weak"]
    assert get_password_strength(["abc123"], []) == ["strong"]


def test_original_differs_on_unicode_digits():
    # "²".isdigit() is True, but superscript 2 is not an ASCII digit in 0-9
    assert original_strength(["²²²²²²"], []) == ["weak"]
    assert get_password_strength(["²²²²²²"], []) == ["strong"]

