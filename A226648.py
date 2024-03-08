#! /usr/bin/env python3

from labmath import *

def factorsieve():          # A segmented sieve to generate the sequence map(factorint, count(2)).
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
                    #assert ints[n] % p == 0, (p, pp, lo, hi, n, ints[n], ints, facs)
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

print(1, 1)

n = 1
t = 1
for (k,kfac) in enumerate(factorsieve(), start=2):
    if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
    t += divsigma(kfac)
    r = isqrt(1 + 8*t)
    if r*r != 1 + 8*t: continue
    r -= 1
    if r % 2 == 1: continue
    x = r // 2
    assert t == x * (x + 1) // 2
    n += 1
    print('\b'*42 + str(n) + " " + str(k))
