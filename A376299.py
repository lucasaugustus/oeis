#! /usr/bin/env python3

from labmath import primegen        # Available via pip (https://pypi.org/project/labmath/)

def A008473():
    yield 1
    pg = primegen()
    primes = [next(pg)]
    nextprime = next(pg)
    lo, hi = 2, nextprime**2
    # We can sieve up to hi - 1.
    while True:
        ints = list(range(lo, hi))
        output = [1] * (hi - lo)
        for p in primes:
            exps = bytearray([0]) * (hi - lo)
            pp = p
            while pp < hi:
                for n in range((-lo) % pp, hi - lo, pp):
                    ints[n] //= p
                    exps[n] += 1
                pp *= p
            for n in range((-lo) % p, hi - lo, p):
                output[n] *= p + exps[n]
        # Any entries in ints that are not 1 are prime divisors of their
        # corresponding numbers that were too large to be sieved out.
        # They contribute factors of p + 1 to the output.
        for n in range(hi - lo):
            p = ints[n]
            if p != 1:
                output[n] *= p + 1
        
        yield from output
        
        primes.append(nextprime)
        nextprime = next(pg)
        lo, hi = hi, nextprime**2

n = 0
for (k,A) in enumerate(A008473(), start=1):
    if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
    if A == k:
        n += 1
        print('\b'*42, n, ' ', k, sep='')


