#! /usr/bin/env python3

from labmath import primegen        # Available via pip (https://pypi.org/project/labmath/)

print("n A092663(n) A092664(n) A092665(n)")

pg = primegen()
lastp = next(pg)
runlength1, runcount1 = 0, 0
runlength3, runcount3 = 0, 0
target10 = 10
n = 1
for p in pg:
    if p % 1000000 == 1: print('\b'*42, p//1000000, end='M', flush=True)
    if p > target10 > lastp:
        print('\b'*42, n, ' ', runcount1, ' ', runcount3, ' ', abs(runcount1 - runcount3), sep='')
        n += 1
        target10 *= 10
    if p % 4 == 1:
        if runlength3 == 10: runcount3 += 1
        runlength3 = 0
        runlength1 += 1
    else:
        if runlength1 == 10: runcount1 += 1
        runlength1 = 0
        runlength3 += 1

