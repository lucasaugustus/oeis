#! /usr/bin/env python3

from labmath import primegen, count

pg = primegen()
n = 0
for k in count(1):
    print('\b'*42, k, end='', flush=True)
    for _ in range(2*k - 1): p = next(pg)
    if (p - 1) % k == 0:
        n += 1
        print('\b'*42, n, ' ', k, sep='')
