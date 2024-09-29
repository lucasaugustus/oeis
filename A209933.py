#! /usr/bin/env python3

# Formatting note: this file uses lines of up to 128 characters and employs 4-space chunks for indentations.

from labmath import primegen, count, divisors       # Available via pip (https://pypi.org/project/labmath/)

def factorsieve():
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

n = 1
for (k, kfac) in enumerate(factorsieve(), start=2):
    if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
    if '0' in str(k): continue                          # This line is optional, but speeds things up.
    if any(k % int(d) != 0 for d in str(k)): continue   # This line is optional, but speeds things up.
    if all(all(d != '0' and k % int(d) == 0 for d in div) for div in map(str, divisors(kfac))):
        n += 1
        print('\b'*42, n, ' ', k, sep='')
