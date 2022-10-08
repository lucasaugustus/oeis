#! /usr/bin/env python3

# A243843: a(n) is the smallest semiprime that belongs to a cycle of length n under repeated iteration
# of the map (k -> concatenation of prime divisors of k) until a non-semiprime is reached.

# TODO: clarify that this sequence uses the squarefree semiprimes.
# TODO: use a word other than "cycle", which suggests periodic behavior.

from labmath import * # available via pip (https://pypi.org/project/labmath/)

results = {}
minunknown = 1

for x in semiprimegen():
    if isqrt(x)**2 == x: continue
    if x % 1000 == 1: print('\b'*42, minunknown, x, len(results), end="...", flush=True)
    y = x
    iters = 0
    while True:
        p = next(primefac(x))
        q = x // p
        if q == 1 or p == q or not isprime(q): break
        x = int(str(min(p,q)) + str(max(p,q)))
        iters += 1
    if iters in results: continue
    results[iters] = y
    if iters != minunknown: continue
    while minunknown in results:
        print('\b'*42, minunknown, results[minunknown], len(results), end="   \n")
        minunknown += 1

"""
1 6
2 38
3 34
4 15
5 265
6 161
7 1126
8 4891
9 1253
10 250231
11 100462
12 49869178
13 234139657
14 68279314
*15 2318271253
*16 636542506
*17 
"""
