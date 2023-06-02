#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

Z = 10**100 + mpz(267)

primes = list(primegen(100000))
Zpn = [0] * (primes[-1] + 1)

for n in count(1):
    Zn = Z**n
    for p in primes: Zpn[p] = pow(pow(10, 100, p) + 267, n, p)
    for k in count(2, 2):
        print('\b'*42, n, k, end='', flush=True)
        #Zp = pow(10, 100, p) + 267
        #Zpn = pow(Zp, n, p)
        #if any((k * pow(pow(10, 100, p) + 267, n, p) + 1) % p == 0 for p in primegen(100)): continue
        if any((k * Zpn[p] + 1) % p == 0 for p in primes): continue
        if isprime(k * Zn + 1, tb=[]): break
        #if isprime(k * Zn + 1): break
    assert isprime_nm1(k * Zn + 1, {Z:n})
    print()
