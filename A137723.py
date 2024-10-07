#! /usr/bin/env python3

from labmath import nextprime, count, primegen     # Available via pip (https://pypi.org/project/labmath/)

def factorsieve():  # generates the sequence (set(primefac(n)) for n in count(2)).
    pg = primegen()
    primes = [next(pg)]
    nextprime = next(pg)
    lo, hi = 2, nextprime**2
    # We can sieve up to hi - 1.
    while True:
        ints = list(range(lo, hi))
        facs = [set() for _ in range(lo, hi)]
        # facs[n] will contain the factorization of n + lo.
        for p in primes:
            for n in range((-lo) % p, hi - lo, p):
                ints[n] //= p
                facs[n].add(p)
            pp = p*p
            while pp < hi:
                for n in range((-lo) % pp, hi - lo, pp):
                    ints[n] //= p
                pp *= p
        # Any entries in ints that are not 1 are prime divisors of their
        # corresponding numbers that were too large to be sieved out.
        for n in range(hi - lo):
            p = ints[n]
            if p != 1:
                facs[n].add(p)
        
        yield from facs
        
        primes.append(nextprime)
        nextprime = next(pg)
        lo, hi = hi, nextprime**2

for n in count(1):
    
    hasgap = bytearray([False]) * (n + 2)
    fs = factorsieve()
    for x in range(n+2):
        ps = next(fs)
        pl = sorted(ps)
        pl.pop()
        hasgap[x] = (any(nextprime(p) not in ps for p in pl))
    
    # hasgap is now initialized to tell us whether 2, 3, 4, ..., n+3 have gaps.
    
    for k in count(3):
        if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
        
        # hasgap[0] is True iff k - 1 has a gap.
        # hasgap[1] is True iff k     has a gap.
        # hasgap[2] is True iff k + 1 has a gap.
        # etc.
        
        if (not hasgap[0]) and all(hasgap[x] for x in range(1, n+1)) and (not hasgap[n+1]): break
        
        hasgap.pop(0)
        ps = next(fs)
        pl = sorted(ps)
        pl.pop()
        hasgap.append(any(nextprime(p) not in ps for p in pl))
    
    print('\b'*42, n, ' ', k, sep='')

