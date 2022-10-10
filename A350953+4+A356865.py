#! /usr/bin/env python3

from labmath import determinant, inf, factorial     # Available via pip (https://pypi.org/project/labmath/)
from itertools import permutations, count, islice
from time import time
from datetime import datetime, timedelta

def symmetrictoeplitz(entries):  # Symmetric Toeplitz matrix whose top row is the provided list
    N = len(entries) * 2 - 1
    newentries = list(reversed(entries))[:-1] + list(entries)
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [newentries[i:i+d] for i in range(d-1, d-1-d, -1)]

print("n: A350954(n) and A350953(n) and A356865(n)")

for n in count():
    if n == 0:
        print("0: 1 and 1 and 1")
        continue
    maxdet = -inf
    mindet = inf
    minnonzero = inf
    fac = factorial(n)
    starttime = time()
    for (k,p) in enumerate(permutations(range(1, n+1))):
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
n: A350954(n) and A350953(n) and A356865(n)
0: 1 and 1 and 1
1: 1 and 1 and 1
2: 3 and -3 and 3
3: 15 and -12 and 8
4: 100 and -100 and 12
5: 3091 and -1749 and 3
6: 49375 and -47600 and 13
7: 1479104 and -800681 and 19
8: 43413488 and -39453535 and 5
9: 1539619328 and -1351201968 and 5
10: 64563673460 and -66984136299 and 1
11: 2877312739624 and -2938096403400 and 3
12: 252631974548628 and -235011452211680 and 1
"""
