#! /usr/bin/env python3

# Numbers n such that (3*2^n-1)^2-2 is prime

from labmath import isprime, count, primegen, mpz   # Available via pip (https://pypi.org/project/labmath/)

basis = list(primegen(100000))

for n in count(0):
    print('\b'*42, n, end='', flush=True)
    x = (3 * mpz(2)**n - 1)**2 - 2
    for p in basis:
        if x % p == 0: break
    else:
        if isprime(x): print('\b'*42 + str(n) + "    ")

# 0, 1, 4, 6, 15, 21, 25, 70, 129, 399, 511, 856, 9574, 14479, 17649, 27054, 28296, 32796, 38176
# Next term >= 10**5.
