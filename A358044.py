#! /usr/bin/env python3

from labmath import *
from time import *

def is_square(n):
    """
    Checks whether n is square.
    If n is square, then we return its square root.
    Otherwise, we return False.
    For the sake of speed, we include a bunch of modular prefilters.
    """
    if n % 64 not in {0, 1, 4, 9, 16, 17, 25, 33, 36, 41, 49, 57}:                return False
    if n % 63 not in {0, 1, 4, 7, 9, 16, 18, 22, 25, 28, 36, 37, 43, 46, 49, 58}: return False
    if n % 25 not in {0, 1, 4, 6, 9, 11, 14, 16, 19, 21, 24}:                     return False
    if n % 31 not in {0, 1, 2, 4, 5, 7, 8, 9, 10, 14, 16, 18, 19, 20, 25, 28}:    return False
    if n % 23 not in {0, 1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18}:                    return False
    if n % 19 not in {0, 1, 4, 5, 6, 7, 9, 11, 16, 17}:                           return False
    if n % 17 not in {0, 1, 2, 4, 8, 9, 13, 15, 16}:                              return False
    if n % 11 not in {0, 1, 3, 4, 5, 9}:                                          return False
    r = isqrt(n)
    if r*r == n: return r
    return False

def is_triangular(n):
    """
    Checks whether n is triangular.
    A positive integer n is triangular iff there exists an integer x such that (x^2 + x) / 2 == n.
    Solving for x yields x == (-1 + sqrt(1 + 8 * n)) / 2.
    """
    if n == 1: return True
    x = is_square(1 + 8 * n)
    if not x: return False
    return (x - 1) % 2 == 0

print(1, 1)
run = 1
record = 1
tdcount = 1
for n in count(2):
    if n % 1000 == 0: print('\b'*42, n, end='', flush=True)
    n_tdcount = sum(is_triangular(d) for d in divisors(n))
    if n_tdcount == tdcount:
        run += 1
        if run > record:
            record = run
            print(('\b'*42 + "%d %d" + " "*24) % (record, n - run + 1))
    else:
        run = 1
        tdcount = n_tdcount

"""
1 1
2 1
3 55
4 5402
5 2515069
Any subsequent terms are > 10^10.
"""
