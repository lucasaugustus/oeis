#! /usr/bin/env python3

from labmath import primegen, isprime

n = 0
for i in primegen():
    if i % 1000000 == 1: print('\b'*42, i//1000000, end='M', flush=True)
    delta = 0
    bit = 1
    while bit <= i:
        if isprime(i^bit): delta += 1
        else:              delta -= 1
        bit *= 2
    if delta > 0:
        n += 1
        print('\b'*42, n, ' ', i, sep='')
