#! /usr/bin/env python3

from labmath import primegen, inf, count

def bigomegasieve(limit=inf):
    """
    A segmented sieve to generate the numbers of prime factors of the positive integers, in order, with multiplicity.
    """
    if limit < 1: return
    yield 0
    pg = primegen()
    primes = [next(pg)]
    nextprime = next(pg)
    lo, hi = 2, nextprime**2
    # We can sieve up to hi - 1.
    x = 2
    while True:
        ints = list(range(lo, hi))
        facs = [0] * (hi - lo)
        for p in primes:
            pp = p
            while pp < hi:
                for n in range((-lo) % pp, hi - lo, pp):
                    ints[n] //= p
                    facs[n] += 1
                pp *= p
        # Any entries in ints that are not 1 are prime divisors of their
        # corresponding numbers that were too large to be sieved out.
        for n in range(hi - lo):
            p = ints[n]
            if p != 1:
                facs[n] += 1
        
        for (x,fac) in enumerate(facs, start=x):
            if x >= limit: return
            yield fac
        x += 1
        
        primes.append(nextprime)
        nextprime = next(pg)
        lo, hi = hi, nextprime**2

# The nth tetrahedral number is n * (n+1) * (n+2) / 6.

print(0, 1)
print(1, -1)

for n in count(2):
    Omegas = bigomegasieve()
    a, b, c = next(Omegas), next(Omegas), next(Omegas)
    for k in count(1):
        if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
        if a + b + c - 2 == n: break
        a, b, c = b, c, next(Omegas)
    print('\b'*42, n, ' ', k, sep='')

