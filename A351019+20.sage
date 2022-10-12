#! /usr/bin/env sage

from itertools import count, permutations
from time import time
from datetime import datetime, timedelta

print("n: A351019(n) and A351020(n)")
print("0: 1 and 1")

def symmetrictoeplitz(entries):  # Symmetric Toeplitz matrix whose top row is the provided list
    N = len(entries) * 2 - 1
    newentries = list(reversed(entries))[:-1] + list(entries)
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [newentries[i:i+d] for i in range(d-1, d-1-d, -1)]

inf = float('inf')

for n in count(1):
    terms = list(range(1, n+1))
    minperm, maxperm, minmat, maxmat = +inf, -inf, 0, 0
    fac = factorial(n)
    starttime = time()
    k = 0
    for (k,row) in enumerate(permutations(terms)):
        if k % 1000 == 0 and k > 0:
            ettc = float((time() - starttime) * (fac/k - 1.0))   # estimated time to completion
            eta = datetime.isoformat(datetime.now() + timedelta(seconds=ettc), sep=' ', timespec='seconds')
            print('\b'*160, "%d/%d = %0.5f%%; ETA %0.0f s / %s" % (k, fac, 100*k/fac, ettc, eta), end=' ', flush=True)
        M = Matrix(symmetrictoeplitz(row))
        perm = M.permanent()
        if perm > maxperm: maxperm, maxmat = perm, M
        if perm < minperm: minperm, minmat = perm, M
    outstr = "%d: %d and %d" % (n, minperm, maxperm)
    print(('\b'*160) + outstr + (" " * (79-len(outstr))))

"""
n: A351019(n) and A351020(n)
0: 1 and 1
1: 1 and 1
2: 5 and 5
3: 36 and 64
4: 480 and 1650
5: 9991 and 66731
6: 296913 and 3968777
7: 12099604 and 323676148
8: 637590728 and 34890266414
9: 43090005714 and 4780256317586
10: 3550491371994 and 814873637329516
11: 359557627057876 and 168491370685328792
"""
