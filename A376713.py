#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

def factorsieve():
    pg = primegen()
    primes = [next(pg)]
    nextprime = next(pg)
    lo, hi = 2, nextprime**2
    # We can sieve up to hi - 1.
    x = 2
    while True:
        ints = list(range(lo, hi))
        facs = [{} for _ in range(lo, hi)]
        # facs[n] will contain the factorization of n + lo.
        for p in primes:
            pp = p
            while pp < hi:
                for n in range((-lo) % pp, hi - lo, pp):
                    ints[n] //= p
                    facs[n][p] = facs[n].get(p,0) + 1
                pp *= p
        # Any entries in ints that are not 1 are prime divisors of their
        # corresponding numbers that were too large to be sieved out.
        for n in range(hi - lo):
            p = ints[n]
            if p != 1:
                facs[n][p] = 1
        
        yield from facs
        
        primes.append(nextprime)
        nextprime = next(pg)
        lo, hi = hi, nextprime**2

for n in count(1):
    for (k, kfac) in enumerate(factorsieve(), start=2):
        if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
        
        total = 0
        kk = k*k
        
        for (u,v) in product(divisors(kfac), repeat=2):
            uu, vv = u*u, v*v
            if (2*uu*vv) % (uu + vv) != 0: continue
            mm = 2 * uu * vv // (uu + vv)
            if (k*k) % mm != 0: continue
            if not (uu < mm < vv): continue
            m = isqrt(mm)
            if m*m != mm: continue
            total += 1
            if total > n: break
        
        if total == n: break
    
    print('\b'*42, n, ' ', k, sep='')

"""
Fix existing terms
Edit title to replace "triples" with "sets"
"""
