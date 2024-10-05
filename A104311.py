#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

primes = list(primegen(10000))

n = 0
d, c, b = mpz(1), 1, 3
for k in count(3):
    print('\b'*42, k, end='', flush=True)
    a = (143*k**3 - 352*k**2 + 251*k - 54)*b + 4*(k-1)*(26*k**2 - 51*k + 15)*c + 16*(k-2)*(k-1)*(13*k-6)*d
    assert a % (2*k*(2*k-1)*(13*k-19)) == 0
    a //= 2*k*(2*k-1)*(13*k-19)
    if isprime(a, tb=primes):
        n += 1
        print('\b'*42, n, ' ', k, sep='')
    d, c, b = c, b, a

