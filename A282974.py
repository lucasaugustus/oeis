#! /usr/bin/env python3

from labmath import isprime, count, primegen    # Available via pip (https://pypi.org/project/labmath/)
from gmpy2 import *

basis = list(primegen(10**5))

get_context().precision = int(log2(10) * 10**5) + 1000
pi = const_pi()

for k in count():
    print('\b'*42, k, end=' ', flush=True)
    n = mpz(rint(pi * mpz(10)**k))
    if isprime(n, tb=basis): print()

# 1, 2, 6, 12, 1902, 3971, 5827, 16208, 47577
# Next term >= 65536.
