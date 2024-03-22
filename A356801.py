#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

def semiprimegen_factored():
    pg = primegen()
    primes = [next(pg)]
    nextprime = next(pg)
    lo, hi = 2, nextprime**2
    # We can sieve up to hi - 1.
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
        
        for fac in facs:
            if sum(fac.values()) == 2:
                if len(fac) == 2: yield tuple(fac.keys())
                else: 
                    p = next(iter(fac))
                    yield (p, p)
        
        primes.append(nextprime)
        nextprime = next(pg)
        lo, hi = hi, nextprime**2

for n in count(1):
    for (p,q) in semiprimegen_factored():
        a, b = p*q, p+q
        if a % 100000 == 1: print('\b'*42, a//1000000, end='M', flush=True)
        if all(isprime(a + i*b) for i in range(1, n+1)) and not isprime(a + (n+1)*b):
            print('\b'*42, n, ' ', a, sep='')
            break
