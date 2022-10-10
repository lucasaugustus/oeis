#! /usr/bin/env python3

# m such that numerator(Sum_{k=1..m} m^(k-1)/k!) is prime.

from labmath import isprime, count, primegen    # Available via pip (https://pypi.org/project/labmath/)
from gmpy2 import fac, mpq

basis = list(primegen(10**5))

for m in count(1):
    print('\b'*42, m, end=' ', flush=True)
    sn = sum(mpq(m**(k-1), fac(k)) for k in range(1, m+1)).numerator
    print(sn.bit_length(), end='    ', flush=True)
    if isprime(sn, tb=basis): print()

# 2, 17, 102, 112, 316, 447, 535, 820, 1396, 1475, 1650, 5575, 6486, 6832
# Next term >= 10**4
