#! /usr/bin/env python3

from labmath import *
from time import time
from datetime import datetime, timedelta

print("n: A215724(n)")

# Since we are concerned only with the absolute values of these determinants, we can set the bottom-left entries to +1.
# This halves the number of matrices we must examine.

def toeplitz(entries):
    # Toeplitz matrix using the provided numbers, with +1 prepended.  First goes on the bottom left, last on the top right.
    entrs = [1] + entries
    N = len(entrs)
    assert N % 2 == 1
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [entrs[i:i+d] for i in range(d-1, d-1-d, -1)]

for n in count(1):
    maxdet, maxmat = 0, []
    fac = 2**(2*n-2)
    starttime = time()
    k = 0
    for (k,negs) in enumerate(powerset(range(2*n-2))):
        row = [(-1)**(x in negs) for x in range(2*n-2)]
        if k % 1000 == 0 and k > 0:
            ettc = (time() - starttime) * (fac/k - 1.0)   # estimated time to completion
            eta = datetime.isoformat(datetime.now() + timedelta(seconds=ettc), sep=' ', timespec='seconds')
            print('\b'*160, "%d/%d = %0.5f%%; ETA %0.0f s / %s" % (k, fac, 100*k/fac, ettc, eta), end=' ', flush=True)
        M = toeplitz(row)
        det = abs(determinant(M))
        if det > maxdet: maxdet, maxmat = det, M
    #print()
    #print(maxdet)
    #for line in maxmat: print(line)
    #print()
    outstr = "%d: %d" % (n, maxdet)
    print(('\b'*160) + outstr + (" " * (79-len(outstr))))


"""
 n: A215724(n)
 0: 1
 1: 1
 2: 2
 3: 4
 4: 16
 5: 48
 6: 160
 7: 576
 8: 2560
 9: 12288
10: 73728
11: 327680
12: 2097152
13: 14929920
14: 68853760
15: 390905856
16: 2363752448

a(2) = 2:
    1  1
   -1  1

a(3) = 4:
    1  1  1
   -1  1  1
    1 -1  1

a(6) = 160
    1 -1  1  1  1  1
   -1  1 -1  1  1  1
   -1 -1  1 -1  1  1
   -1 -1 -1  1 -1  1
    1 -1 -1 -1  1 -1
    1  1 -1 -1 -1  1
"""
