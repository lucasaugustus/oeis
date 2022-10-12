#! /usr/bin/env sage

from itertools import count, permutations
from time import time
from datetime import datetime, timedelta

print("n: A351021(n) and A351022(n)")
print("0: 1 and 1")

primelist = []

def symmetrictoeplitz(entries):  # Symmetric Toeplitz matrix whose top row is the provided list
    N = len(entries) * 2 - 1
    newentries = list(reversed(entries))[:-1] + list(entries)
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [newentries[i:i+d] for i in range(d-1, d-1-d, -1)]

P = Primes()
inf = float('inf')

for n in count(1):
    if len(primelist) == 0: primelist.append(P.first())
    else: primelist.append(P.next(primelist[-1]))
    minperm, maxperm, minmat, maxmat = +inf, -inf, 0, 0
    fac = factorial(n)
    starttime = time()
    k = 0
    for (k,row) in enumerate(permutations(primelist)):
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
n: A351021(n) and A351022(n)
0: 1 and 1
1: 2 and 2
2: 13 and 13
3: 166 and 289
4: 4009 and 13814
5: 169469 and 1795898
6: 10949857 and 265709592
7: 1078348288 and 70163924440
8: 138679521597 and 20610999526800
9: 24402542896843 and 9097511018219760
10: 5348124003487173 and 6845834489829830144
"""
