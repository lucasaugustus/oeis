#! /usr/bin/env python3

from labmath import primegen, determinant, inf, factorial       # Available via pip (https://pypi.org/project/labmath/)
from itertools import permutations, count, islice
from time import time
from datetime import datetime, timedelta

def toeplitz(entries):  # Toeplitz matrix using the provided numbers.  First goes on the bottom left, last on the top right.
    N = len(entries)
    assert N % 2 == 1
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [entries[i:i+d] for i in range(d-1, d-1-d, -1)]

print("n: A350933(n) and A350932(n)")

for n in count():
    if n == 0:
        print("0: 1 and 1")
        continue
    primes = list(islice(primegen(), 2*n-1))
    maxdet = -inf
    mindet = inf
    fac = factorial(2*n-1)
    starttime = time()
    for (k,p) in enumerate(permutations(primes)):
        if k % 1000 == 0 and k > 0:
            ettc = (time() - starttime) * (fac/k - 1.0)   # estimated time to completion
            eta = datetime.isoformat(datetime.now() + timedelta(seconds=ettc), sep=' ', timespec='seconds')
            print('\b'*160, "%d/%d = %0.5f%%; ETA %0.0f s / %s" % (k, fac, 100*k/fac, ettc, eta), end=' ')
        det = determinant(toeplitz(p))
        #print(p, det)
        if det > maxdet: maxdet = det
        if det < mindet: mindet = det
    outstr = "%d: %d and %d" % (n, maxdet, mindet)
    print(('\b'*160) + outstr + (" " * (79-len(outstr))))

"""
n: A350933(n) and A350932(n)
0: 1 and 1
1: 2 and 2
2: 19 and -11
3: 1115 and -286
4: 86087 and -57935
5: 9603283 and -5696488
6: 2307021183 and -1764195984
7: 683793949387 and -521528189252
"""
