#! /usr/bin/env python3

# Numbers n such that 3^n + n^2 is prime

from labmath import isprime, count, primegen, mpz   # Available via pip (https://pypi.org/project/labmath/)

basis = list(primegen(100000))

for n in count(2,2): # All such n must be even.
    print('\b'*42, n, end='', flush=True)
    for p in basis:
        if p == 2: continue
        res = (pow(3, n, p) + n*n) % p
        if res == 0: break
    else:
        if isprime(mpz(3)**n + n*n, tb=[]): print()

# 2, 4, 10, 22, 40, 304, 1582, 3602, 46162
# All terms <= 3602 proven with Pari's ECPP.
# Next term >= 103670.
