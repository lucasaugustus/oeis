#! /usr/bin/env python3

from labmath import primegen, determinant, inf, factorial       # Available via pip (https://pypi.org/project/labmath/)
from itertools import permutations, count, islice
from time import time
from datetime import datetime, timedelta

def symmetrictoeplitz(entries):  # Symmetric Toeplitz matrix whose top row is the provided list
    N = len(entries) * 2 - 1
    newentries = list(reversed(entries))[:-1] + list(entries)
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [newentries[i:i+d] for i in range(d-1, d-1-d, -1)]

print("n: A358323(n) and A358324(n) and A358325(n)")
print("0: 1 and 1")
print("1: 0 and 0")

for n in count(2):
    maxdet = -inf
    mindet = inf
    minabs = inf
    fac = factorial(n)
    starttime = time()
    for (k,p) in enumerate(permutations(range(n))):
        if k % 1000 == 0 and k > 0:
            ettc = (time() - starttime) * (fac/k - 1.0)   # estimated time to completion
            eta = datetime.isoformat(datetime.now() + timedelta(seconds=ettc), sep=' ', timespec='seconds')
            print('\b'*160, "%d/%d = %0.5f%%; ETA %0.0f s / %s" % (k, fac, 100*k/fac, ettc, eta), end=' ')
        det = determinant(symmetrictoeplitz(p))
        #print(p, det)
        if det < mindet:
            mindet = det
            minmat = p
        if det > maxdet:
            maxdet = det
            maxmat = p
        if 0 < abs(det) < minabs:
            minabs = abs(det)
            minabsmat = p
    outstr = "%d: %d and %d and %d" % (n, mindet, maxdet, minabs)
    print(('\b'*160) + outstr + (" " * (79-len(outstr))))
    #for row in symmetrictoeplitz(minmat): print(row)
    #print()
    #for row in symmetrictoeplitz(maxmat): print(row)
    #print()
    #for row in symmetrictoeplitz(minabsmat): print(row)
    #print()

"""
n: A358323(n) and A358324(n) and A358325(n)
0: 1 and 1
1: 0 and 0
2: -1 and 1 and 1
3: -7 and 8 and 3
4: -60 and 63 and 12
5: -1210 and 2090 and 2
6: -34020 and 36875 and 11
7: -607332 and 1123653 and 10
8: -30448441 and 34292912 and 5
9: -1093612784 and 1246207300 and 4
10: -55400732937 and 53002204560 and 1
11: -2471079070511 and 2418538080316 and 4
12: -197500419383964 and 215120941720912 and 1
"""

