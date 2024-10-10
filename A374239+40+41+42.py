#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)
from time import time
from multiprocessing import Pool
from itertools import permutations
from datetime import datetime, timedelta

print("n: A374239(n) A374240(n) A374241(n) A374242(n)")
print("0: 1 1 1 -")

def symmetrictoeplitz1_det(entries):
    # Symmetric Toeplitz matrix whose top row is [1] + entries.
    entrs = entries[::-1] + (1,) + entries
    N = len(entrs)
    assert N % 2 == 1
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return determinant([entrs[i:i+d] for i in range(d-1, d-1-d, -1)])

for n in count(1):
    maxdet, mindet, maxabsdet, minabsdet = -inf, inf, -inf, inf
    fac = factorial(n-1)
    starttime = time()
    with Pool(16) as P:
        for (k,det) in enumerate(P.imap_unordered(symmetrictoeplitz1_det, permutations(range(1,n)), chunksize=1000), start=1):
            if k % 1000 == 0:
                ettc = (time() - starttime) * (fac/k - 1.0)   # estimated time to completion
                eta = datetime.isoformat(datetime.now() + timedelta(seconds=ettc), sep=' ', timespec='seconds')
                print('\b'*160, "%d/%d = %0.5f%%; ETA %0.0f s / %s" % (k, fac, 100*k/fac, ettc, eta), end=' ', flush=True)
            if det > maxdet: maxdet = det
            if det < mindet: mindet = det
            if abs(det) > maxabsdet: maxabsdet = abs(det)
            if abs(det) < minabsdet and det != 0: minabsdet = abs(det)
    if n < 3: outstr = "%d: %d %d %d -"  % (n, mindet, maxdet, maxabsdet)
    else:     outstr = "%d: %d %d %d %d" % (n, mindet, maxdet, maxabsdet, minabsdet)
    print(('\b'*160) + outstr + (" " * (79-len(outstr))))


