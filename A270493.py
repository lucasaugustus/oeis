#! /usr/bin/env python3

from labmath import primegen

n, pg = 0, primegen()
next(pg)
for (k,p) in enumerate(pg, start=2):
    if k % 100000 == 0: print('\b'*42, k/1000000, end='M', flush=True)
    Vl, Vh, Ql, Qh = 2, 2, 1, 1
    for kj in bin(k)[2:]:
        Ql *= Qh
        if kj == '1': Qh, Vl, Vh = -Ql, (Vh * Vl - 2 * Ql) % p, (Vh * Vh + 2 * Ql) % p
        else:         Qh, Vh, Vl =  Ql, (Vh * Vl - 2 * Ql) % p, (Vl * Vl - 2 * Ql) % p
    if (Vh - Vl) % p == 0:
        n += 1
        print('\b'*42, n, ' ', k, sep='')
