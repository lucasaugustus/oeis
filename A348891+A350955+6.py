#! /usr/bin/env python3

from labmath import primegen, determinant, inf, factorial   # Available via pip (https://pypi.org/project/labmath/)
from itertools import permutations, count, islice
from time import time
from datetime import datetime, timedelta

def symmetrictoeplitz(entries):  # Symmetric Toeplitz matrix whose top row is the provided list
    N = len(entries) * 2 - 1
    newentries = list(reversed(entries))[:-1] + list(entries)
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [newentries[i:i+d] for i in range(d-1, d-1-d, -1)]

print("n: A350956(n) and A350955(n) and A348891(n)")

for n in count():
    if n == 0:
        print("0: 1 and 1 and 1")
        continue
    primes = list(islice(primegen(), n))
    maxdet = -inf
    mindet = inf
    minnonzero = inf
    maxmat, minmat = [], []
    fac = factorial(n)
    starttime = time()
    for (k,p) in enumerate(permutations(primes)):
        if k % 1000 == 0 and k > 0:
            ettc = (time() - starttime) * (fac/k - 1.0)   # estimated time to completion
            eta = datetime.isoformat(datetime.now() + timedelta(seconds=ettc), sep=' ', timespec='seconds')
            print('\b'*160, "%d/%d = %0.5f%%; ETA %0.0f s / %s" % (k, fac, 100*k/fac, ettc, eta), end=' ')
        det = determinant(symmetrictoeplitz(p))
        if det > maxdet: maxdet = det
        if det < mindet: mindet = det
        if 0 < abs(det) < minnonzero: minnonzero = abs(det)
    outstr = "%d: %d and %d and %d" % (n, maxdet, mindet, minnonzero)
    print(('\b'*160) + outstr + (" " * (79-len(outstr))))

"""
n: A350956(n) and A350955(n) and A348891(n)
0: 1 and 1 and 1
1: 2 and 2 and 2
2: 5 and -5 and 5
3: 64 and -35 and 12
4: 1107 and -435 and 11
5: 160160 and -87986 and 22
6: 5713367 and -7186995 and 84
7: 889747443 and -496722800 and 1368
8: 62837596341 and -68316404507 and 73
9: 11671262491586 and -9102428703537 and 589
10: 3090090680653053 and -3721326642272925 and 15057
11: 635672008069583520 and -488684390484513105 and 2520
12: 278356729040728193703 and -195315251884652232704 and 28209
"""
