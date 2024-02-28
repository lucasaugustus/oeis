#! /usr/bin/env python3

# Formatting note: this file uses lines of up to 128 characters and employs 4-space chunks for indentations.

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

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
                    assert ints[n] % p == 0, (p, pp, lo, hi, n, ints[n], ints, facs)
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

record = -inf
facs = factorsieve()
next(facs)  # discard factorint(2)
n = 0
for (k, kfac) in enumerate(facs, start=3):
    if k % 1000000 == 0: print('\b'*42, k, sep='', end='', flush=True)
    t, l = totient(kfac), carmichael(kfac)
    r = log(t) / log(l)
    if r > record:
        n += 1
        record = r
        print('\b'*42, n, ' ', k, sep='')
