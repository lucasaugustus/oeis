#! /usr/bin/env python3

# Numbers n such that (3^n + 7) / 2 is prime

from labmath import isprime, count, primegen, mpz   # Available via pip (https://pypi.org/project/labmath/)

basis = list(primegen(100000))

for n in count(1,2): # All such n must be odd.
    print('\b'*42, n, end='', flush=True)
    for p in basis:
        if p == 2: continue
        res = (pow(3, n, p) + 7) % p
        if res == 0: break
    else:
        if isprime((pow(mpz(3),n) + 7) // 2, tb=[]): print()

# 1, 3, 7, 75, 191, 395, 891, 2935, 3855, 59887
# All terms < 4000 proven with Pari's ECPP.  Next term > 17370.
# Next term >= 100251.
