#! /usr/bin/env python3

import primesieve # available via pip (https://pypi.org/project/primesieve/)

def primegen(increment=10**10):
    lo, hi = 0, increment
    while True:
        yield from primesieve.primes(lo, hi-1)
        lo, hi = hi, hi + increment

k, ps = 0, 0
for p in primegen():
    k += 1
    ps += p
    rem = ps % p
    if k % 1000000 == 0: print('\b'*42, k, end='', flush=True)
    if rem == k: print('\b'*42, k)

"""
2
7
12
83408
5290146169416
No further terms < 10^13.
"""

