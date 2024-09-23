#! /usr/bin/env python3

from labmath import primegen, count         # Available via pip (https://pypi.org/project/labmath/)

for n in count(1):
    pg = primegen()
    primes = [next(pg) for _ in range(2*n + 1)]
    while True:
        if all(primes[k] % 6 == 5 for k in range(n         )) and \
               primes[n] % 6 == 1                             and \
           all(primes[k] % 6 == 5 for k in range(n+1, 2*n+1)): break
        p = primes.pop(0)
        if p % 1000000 == 1: print('\b'*42, p//1000000, end='M', flush=True)
        primes.append(next(pg))
    print('\b'*42, n, ' ', primes[n], sep='')
