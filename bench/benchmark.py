import os
import random
import statistics
import string
import sys
import time

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)

from original_solution import getPasswordStrength
from pwcheck import get_password_strength


def timed(fn, *args):
    t0 = time.perf_counter()
    result = fn(*args)
    return result, time.perf_counter() - t0


def bench_one(passwords, words, runs=3):
    original_times = []
    automaton_times = []
    for _ in range(runs):
        _, t = timed(getPasswordStrength, passwords, words)
        original_times.append(t)
        _, t = timed(get_password_strength, passwords, words)
        automaton_times.append(t)
    return statistics.median(original_times), statistics.median(automaton_times)


def main():
    rnd = random.Random(42)

    def random_word():
        return "".join(rnd.choices(string.ascii_lowercase, k=rnd.randint(5, 10)))

    def random_password():
        return "".join(rnd.choices(string.ascii_letters + string.digits, k=16))

    sizes = [
        (1_000, 1_000),
        (1_000, 10_000),
        (10_000, 10_000),
        (10_000, 50_000),
    ]

    print(f"Python {sys.version}")
    print(f"{'P':>10} | {'W':>10} | {'original (s)':>12} | {'automaton (s)':>13} | speedup")
    print("-" * 68)

    for P, W in sizes:
        passwords = [random_password() for _ in range(P)]
        words = [random_word() for _ in range(W)]
        t_orig, t_auto = bench_one(passwords, words, runs=3)
        speedup = t_orig / t_auto if t_auto > 0 else float("inf")
        print(f"{P:>10,} | {W:>10,} | {t_orig:>12.3f} | {t_auto:>13.3f} | {speedup:>6.1f}x")


if __name__ == "__main__":
    main()

