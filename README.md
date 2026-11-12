# pwcheck

Classify passwords as `"weak"` or `"strong"`. A password is weak if it is shorter than 6 characters, consists only of digits (0-9), consists only of uppercase (A-Z) or only lowercase (a-z) letters, or contains a word from a common-words list as a substring. This is a follow-up to a HackerRank interview question.

## Run tests

```
pip install pytest
python -m pytest -v
```

## Run the benchmark

```
python bench/benchmark.py
```

## Approach

The interview version uses a nested loop: for each password, check `word in pwd` for every common word. This is O(P * W * L) where P = passwords, W = common words, L = password length.

The fixed version builds an Aho-Corasick automaton from the common-words list in O(sum of word lengths), then scans each password in O(password length), independent of W. Total: O(sum of word lengths + total password characters). The automaton is a trie with failure links — on a mismatch, instead of restarting, it follows a precomputed link to the longest suffix that is also a prefix of some pattern, so no character is scanned twice.

Space complexity is O(sum of word lengths) for the trie nodes. In pure Python, each node stores a dictionary of transitions, so memory overhead per state is noticeable at hundreds of thousands of words, but lightweight for typical dictionary sizes.

The tradeoff: the automaton has a one-time build cost (trie construction + BFS for failure links). For small word lists (under ~100 words), the naive `in` loop can be faster because Python's `in` operator runs a C-optimized substring search and avoids trie build overhead.

## Bugs found in my original solution

In my interview code (`original_solution.py`), using `isupper()`, `islower()`, and `isdigit()` caused two bugs:

1. **`isupper()` / `islower()` ignore non-letter characters.** `"ABC123".isupper()` returns `True` because digits are skipped — but `"ABC123"` is not "only uppercase letters". Same for `"abc123".islower()`. The fix checks membership in an explicit `frozenset("A-Z")` / `frozenset("a-z")`.

2. **`isdigit()` accepts Unicode characters outside 0-9.** `"²".isdigit()` returns `True` (Unicode superscript two), so `"²²²²²²"` is wrongly flagged as weak. The fix checks against `frozenset("0123456789")`.

Both are covered by `test_original_differs_on_mixed_alphanumeric` and `test_original_differs_on_unicode_digits` in `tests/test_strength.py`.

## Benchmark

Median of 3 runs. Each run includes automaton build time. Random 16-char passwords, random 5-10 char lowercase common words.

```
Python 3.13.2 — Apple M2, 16 GB RAM
```

| Passwords (P) | Common words (W) | Original (s) | Automaton (s) | Speedup |
|---:|---:|---:|---:|---:|
| 1,000 | 1,000 | 0.023 | 0.005 | 4.7x |
| 1,000 | 10,000 | 0.233 | 0.032 | 7.3x |
| 10,000 | 10,000 | 2.336 | 0.052 | 44.8x |
| 10,000 | 50,000 | 11.783 | 0.269 | 43.8x |

The speedup grows with the word list because the original's cost scales with W while the automaton's per-password cost is independent of W. For small word lists (say, under 100 words), the naive loop is likely faster — Python's built-in `in` runs optimized C code, and the trie build overhead isn't worth it.

Raw benchmark output:

```
$ python bench/benchmark.py
Python 3.13.2 (v3.13.2:4f8bb3947cf, Feb  4 2025, 11:51:10) [Clang 15.0.0 (clang-1500.3.9.4)]
         P |          W | original (s) | automaton (s) | speedup
--------------------------------------------------------------------
     1,000 |      1,000 |        0.023 |         0.005 |    4.7x
     1,000 |     10,000 |        0.233 |         0.032 |    7.3x
    10,000 |     10,000 |        2.336 |         0.052 |   44.8x
    10,000 |     50,000 |       11.783 |         0.269 |   43.8x
```

## Limitations

- Matching is case-sensitive, as in the original problem. Case-insensitive matching would be a `.lower()` on both inputs.
- The pure-Python trie uses a dict per node, so memory use is non-trivial for very large dictionaries (100k+ words).
- No leetspeak substitution (`p@ssw0rd`) or keyboard-walk detection.
- Empty strings in `common_words` are silently ignored (otherwise `"" in pwd` is always `True`).

---

Built with AI assistance for refactoring and benchmarking; I reviewed and can explain every line.
