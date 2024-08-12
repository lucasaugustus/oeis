#! /usr/bin/env python3

from labmath import primegen        # Available via pip (https://pypi.org/project/labmath/)

def oddcomposites():
    pg = primegen()
    next(pg)
    q = next(pg)
    p = next(pg)
    while True:
        yield from range(q + (1 if q % 2 == 0 else 2), p, 2)
        p, q = next(pg), p

n, total = 0, 0
for (k,c) in enumerate(oddcomposites(), start=1):
    if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
    total += c
    base3 = []
    x = total
    while x > 0:
        x, r = divmod(x, 3)
        base3.append(r)
    l = len(base3)
    if all(base3[i] == base3[l - i - 1] for i in range(l//2)):
        n += 1
        print('\b'*42, n, k)
