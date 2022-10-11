#! /usr/bin/env sage

from itertools import count, permutations
from time import time
from datetime import datetime, timedelta

print("n: A350937(n) and A350938(n)")
print("0: 1 and 1")

def toeplitz(entries):  # Toeplitz matrix using the provided numbers.  First goes on the bottom left, last on the top right.
    N = len(entries)
    assert N % 2 == 1
    d = (N + 1) // 2    # We are constructing a d-by-d matrix.
    return [entries[i:i+d] for i in range(d-1, d-1-d, -1)]

inf = float('inf')

for n in count(1):
    terms = list(range(1, 2*n))
    minperm, maxperm, minmat, maxmat = +inf, -inf, 0, 0
    fac = sage.all.factorial(2*n-1)
    starttime = time()
    k = 0
    for (k,row) in enumerate(permutations(terms)):
        if k % 1000 == 0 and k > 0:
            ettc = float((time() - starttime) * (fac/k - 1.0))      # estimated time to completion
            eta = datetime.isoformat(datetime.now() + timedelta(seconds=ettc), sep=' ', timespec='seconds')
            print('\b'*160, "%d/%d = %0.5f%%; ETA %0.0f s / %s" % (k, fac, 100*k/fac, ettc, eta), end=' ', flush=True)
        M = sage.matrix.constructor.Matrix(toeplitz(row))
        perm = M.permanent()
        if perm > maxperm: maxperm, maxmat = perm, M
        if perm < minperm: minperm, minmat = perm, M
    outstr = "%d: %d and %d" % (n, minperm, maxperm)
    print(('\b'*160) + outstr + (" " * (79-len(outstr))))

"""
n: A350937(n) and A350938(n)
0: 1 and 1
1: 1 and 1                                                                     
2: 7 and 11                                                                    
3: 89 and 296                                                                  
4: 2287 and 14502                                                              
5: 89025 and 1153889                                                           
6: 5141775 and 134713213                                                       
"""
