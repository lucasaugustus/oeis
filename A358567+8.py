#! /usr/bin/env python3

from labmath import *                       # Available via pip (https://pypi.org/project/labmath/)
from itertools import permutations, count
from time import time
from datetime import datetime, timedelta

def toeplitz(entries):  # Toeplitz matrix using the provided numbers.  First goes on the bottom left, last on the top right.
    N = len(entries)
    assert N % 2 == 1
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [entries[i:i+d] for i in range(d-1, d-1-d, -1)]

print("n: A358567(n) and A358568(n)")

print("0: 1 and 1")
print("1: 0 and 0")
for n in count(2):
    maxdet = -inf
    mindet = inf
    fac = factorial(2*n-1)
    starttime = time()
    for (k,p) in enumerate(permutations(range(2*n-1))):
        # Because the determinant is invariant under transposition, we can skip any matrices in which 0 is not in the top row.
        if any(p[x] == 0 for x in range(n-1)): continue
        if k % 1000 == 0 and k > 0:
            ettc = (time() - starttime) * (fac/k - 1.0)   # estimated time to completion
            eta = datetime.isoformat(datetime.now() + timedelta(seconds=ettc), sep=' ', timespec='seconds')
            print('\b'*160, "%d/%d = %0.5f%%; ETA %0.0f s / %s" % (k, fac, 100*k/fac, ettc, eta), end=' ')
        det = determinant(toeplitz(p))
        #print(p, det)
        if det > maxdet: maxdet = det
        if det < mindet: mindet = det
    outstr = "%d: %d and %d" % (n, mindet, maxdet)
    print(('\b'*160) + outstr + (" " * (79-len(outstr))))

"""
n: A358567(n) and A358568(n)
0: 1 and 1
1: 0 and 0
2: -2 and 4
3: -31 and 74
4: -1297 and 1781
5: -39837 and 58180
6: -2256911 and 2579770
7: -99518694 and 152337045
"""
