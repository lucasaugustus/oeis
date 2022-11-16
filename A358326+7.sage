#! /usr/bin/env sage

from itertools import count, permutations
from time import time
from datetime import datetime, timedelta

print("n: A358326(n) and A358327(n)")
print("0: 1 and 1")

primelist = []

def symmetrictoeplitz(entries):  # Symmetric Toeplitz matrix whose top row is the provided list
    N = len(entries) * 2 - 1
    newentries = list(reversed(entries))[:-1] + list(entries)
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [newentries[i:i+d] for i in range(d-1, d-1-d, -1)]

inf = float('inf')

for n in count(1):
    minperm, maxperm, minmat, maxmat = +inf, -inf, 0, 0
    fac = factorial(n)
    starttime = time()
    k = 0
    for (k,row) in enumerate(permutations(range(n))):
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
n: A358326(n) and A358327(n)
0: 1 and 1
1: 0 and 0
2: 1 and 1
3: 4 and 12
4: 34 and 304
5: 744 and 12696
6: 17585 and 778785
7: 688202 and 64118596
8: 33248174 and 7014698888
9: 2144597292 and 965862895732
10: 169696358796 and 166105870928994
11: 16521881847592 and 34460169208369298
"""

