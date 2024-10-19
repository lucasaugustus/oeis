#! /usr/bin/env python3

from labmath import primegen, isqrt     # Available via pip (https://pypi.org/project/labmath/)

nextsq = 1
odd = 1
n = 0
for (k,p) in enumerate(primegen(), start=1):
    if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
    x = k * (p - 1)
    while x >= nextsq:
        if x == nextsq:
            n += 1
            print('\b'*42, n, ' ', k, sep='')
        odd += 2
        nextsq += odd

