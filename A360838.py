#! /usr/bin/env python3

from labmath import primegen, semiprimegen      # Available via pip (https://pypi.org/project/labmath/)

def evensemis():
    for p in primegen():
        yield 2 * p

def oddsemis():
    for s in semiprimegen():
        if s % 2 == 1: yield s

n = 0
esgen, osgen = evensemis(), oddsemis()
es, os = next(esgen), next(osgen)
esum, osum = 0, 0
ecount, ocount = 0, 0
while True:
    if (ecount + ocount) % 1000000 == 0: print('\b'*80, esum, ecount, ocount, end='', flush=True)
    if esum == osum:
        n += 1
        print('\b'*80, n, ' ', esum, ' ', ecount, ' ', ocount, sep='')
        esum += es
        osum += os
        es, os = next(esgen), next(osgen)
        ecount += 1
        ocount += 1
    elif esum < osum:
        esum += es
        es = next(esgen)
        ecount += 1
    else:   # osum < esum
        osum += os
        os = next(osgen)
        ocount += 1
