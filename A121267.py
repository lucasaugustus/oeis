#! /usr/bin/env python3

from labmath import isprime     # Available via pip (https://pypi.org/project/labmath/)
import gmpy2
mpz = gmpy2.mpz

digits = 1000000
history = set()
n = 0
x = mpz(0)
dc = 0
for d in str(gmpy2.const_pi(int(digits * gmpy2.log2(10)))):
    if d == '.': continue
    print("\b"*42, dc, end='', flush=True)
    x *= 10
    x += mpz(d)
    dc += 1
    if not isprime(x): continue
    if x in history: continue
    n += 1
    print("\b"*42, n, ' ', dc, sep='')
    history.add(x)
    x = 0
    dc = 0

