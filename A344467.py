#! /usr/bin/env python3

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

n = 0
x, y = 1, 0         # The first step is of length 1 in a cardinal direction.
nox, noy = -1, 0    # The currently-forbidden direction.
for (k,kfac) in enumerate(factorsieve(), start=2):
    if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
    for p in chain(*[[p]*e for (p,e) in sorted(kfac.items())]): # Primes are counted with multiplicity.
        
        if (x,y) != (0,0):
            mindist = inf       # This will actually hold the square of the minimum distance.
            for (a,b) in [(p,0), (0,p), (-p,0), (0,-p)]:
                # First, ensure that the step (a,b) would not backtrack.
                if a != 0: dirx, diry = a // abs(a), 0
                if b != 0: diry, dirx = b // abs(b), 0
                if dirx == nox and diry == noy: continue    # No backtracking.
                
                newx, newy = x + a, y + b
                dist = newx**2 + newy**2
                # If dist == mindist, then we could do some logic to choose a canonical direction,
                # but this does not actually matter.
                if dist <= mindist:
                    mindist = dist
                    stepx, stepy = a, b
                    minx, miny = newx, newy
                    mindirx, mindiry = dirx, diry
        
        elif x == y == 0 and (nox, noy) != (1, 0):
            stepx, stepy = p, 0
            minx, miny = p, 0
            mindirx, mindiry = 1, 0
        
        elif x == y == 0 and (nox, noy) == (1, 0):
            stepx, stepy = 0, p
            minx, miny = 0, p
            mindirx, mindiry = 0, 1
        
        else: assert False
        
        x, y = minx, miny
        nox, noy = -mindirx, -mindiry
        
        if x == y == 0:
            n += 1
            print('\b'*42, n, ' ', k, sep='')
