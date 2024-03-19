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
print(2, 1)

facs = factorsieve()
sigmas = [divsigma(next(facs), 0),
          divsigma(next(facs), 0),
          divsigma(next(facs), 0)]
m = 2
for n in count(3):
    while True:
        if m % 1000000 == 0: print('\b'*42, m//1000000, end='M', flush=True)
        if all(sigmas[x-1] == sigmas[0] * x for x in range(2, n+1)): break
        sigmas.pop(0)
        sigmas.append(divsigma(next(facs), 0))
        m += 1
    print('\b'*42, n, ' ', m, sep='')
    sigmas.append(divsigma(next(facs), 0))
