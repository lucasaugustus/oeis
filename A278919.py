#! /usr/bin/env python3

from labmath import primegen

def totientsieve():
    yield 1
    pg = primegen()
    primes = [next(pg)]
    nextprime = next(pg)
    lo, hi = 2, nextprime**2
    # We can sieve up to hi - 1.
    while True:
        ints = list(range(lo, hi))
        tots = list(range(lo, hi))
        for p in primes:
            for n in range((-lo) % p, hi - lo, p):
                tots[n] //= p
                tots[n] *= p - 1
            pp = p
            while pp < hi:
                for n in range((-lo) % pp, hi - lo, pp):
                    ints[n] //= p
                pp *= p
        # Any entries in ints that are not 1 are prime divisors of their
        # corresponding numbers that were too large to be sieved out.
        for n in range(hi - lo):
            p = ints[n]
            if p != 1:
                tots[n] //= p
                tots[n] *= p - 1
        
        yield from tots
        
        primes.append(nextprime)
        nextprime = next(pg)
        lo, hi = hi, nextprime**2

def sigmasieve():
    yield 1
    pg = primegen()
    primes = [next(pg)]
    nextprime = next(pg)
    lo, hi = 2, nextprime**2
    # We can sieve up to hi - 1.
    while True:
        ints = list(range(lo, hi))
        sigs = [1] * (hi - lo)
        for p in primes:
            for n in range((-lo) % p, hi - lo, p):
                e = 0
                while ints[n] % p == 0:
                    ints[n] //= p
                    e += 1
                sigs[n] *= (p**(e+1) - 1) // (p - 1)
        # Any entries in ints that are not 1 are prime divisors of their
        # corresponding numbers that were too large to be sieved out.
        for n in range(hi - lo):
            p = ints[n]
            if p != 1:
                sigs[n] *= p + 1
        
        yield from sigs
        
        primes.append(nextprime)
        nextprime = next(pg)
        lo, hi = hi, nextprime**2

totients = totientsieve()
sigmas = sigmasieve()

km2tot = next(totients)
km1sig = next(sigmas)
km1sig = next(sigmas)
k      = 3
n      = 0
while True:
    if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
    if (km1sig + 1) % km2tot == 0:
        n += 1
        print('\b'*42, n, ' ', k, sep='')
    km2tot, km1sig, k = next(totients), next(sigmas), k + 1
