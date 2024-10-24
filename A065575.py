#! /usr/bin/env python3

from labmath import mpz, isprime, primegen
from gmpy2 import const_pi


primes = list(primegen(10000))
pi = str(const_pi(1000000)).replace('.','')
n = 0
x = mpz(0)
k = 0
for D in pi:
    print('\b'*42, k, end='')
    d = int(D)
    if d >= 7: continue
    k += 1
    x = 7*x + d
    if isprime(x, tb=primes):
        n += 1
        print('\b'*42, n, ' ', k, sep='')
