#! /usr/bin/env python3

from labmath import determinant, inf, factorial     # Available via pip (https://pypi.org/project/labmath/)
from itertools import permutations, count, islice
from time import time
from datetime import datetime, timedelta

def toeplitz(entries):  # Toeplitz matrix using the provided numbers.  First goes on the bottom left, last on the top right.
    N = len(entries)
    assert N % 2 == 1
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [entries[i:i+d] for i in range(d-1, d-1-d, -1)]

print("n: A350931(n) and A350930(n)")

for n in count():
    if n == 0:
        print("0: 1 and 1")
        continue
    primes = list(range(1, 2*n))
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
n: A350931(n) and A350930(n)
0: 1 and 1
1: 1 and 1                                                                     
2: 7 and -5                                                                    
3: 105 and -42                                                                 
4: 2294 and -1810                                                              
5: 71753 and -48098                                                            
6: 3051554 and -2737409
7: 175457984 and -114381074
"""
