#! /usr/bin/env python3

from labmath import determinant, inf, factorial       # Available via pip (https://pypi.org/project/labmath/)
from itertools import permutations, count, islice
from time import time
from datetime import datetime, timedelta

def hankel(entries):  # Hankel matrix using the provided numbers.  First goes on the top left, last on the bottom right.
    N = len(entries)
    assert N % 2 == 1
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [entries[i:i+d] for i in range(d)]

print("n: A368351(n) and A368352(n)")
print("0: 1 and 1")

for n in count(1):
    maxdet, maxperm = -inf, []
    mindet, minperm =  inf, []
    fac = factorial(2*n-1)
    starttime = time()
    for (k,p) in enumerate(permutations(range(1, 2*n))):
        if k % 1000 == 0 and k > 0:
            ettc = (time() - starttime) * (fac/k - 1.0)   # estimated time to completion
            eta = datetime.isoformat(datetime.now() + timedelta(seconds=ettc), sep=' ', timespec='seconds')
            print('\b'*160, "%d/%d = %0.5f%%; ETA %0.0f s / %s" % (k, fac, 100*k/fac, ettc, eta), end=' ')
        det = determinant(hankel(p))
        if det == maxdet: maxperm.append(p)
        if det == mindet: minperm.append(p)
        if det > maxdet: maxdet, maxperm = det, [p]
        if det < mindet: mindet, minperm = det, [p]
    outstr = "%d: %d and %d" % (n, mindet, maxdet)
    print(('\b'*160) + outstr + (" " * (79-len(outstr))))
    """
    print("max")
    for perm in maxperm:
        for row in hankel(perm):
            print(row)
        print()
    print("min")
    for perm in minperm:
        for row in hankel(perm):
            print(row)
        print()
    """

"""
n: A368351(n) and A368352(n)
0: 1 and 1
1: 1 and 1
2: -7 and 5
3: -105 and 42
4: -1810 and 2294
5: -48098 and 71753
6: -3051554 and 2737409
7: -175457984 and 114381074
"""
