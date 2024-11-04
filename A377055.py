#! /usr/bin/env python3

from labmath import primegen, count         # Available via pip (https://pypi.org/project/labmath/)
from heapq import *

def primepowergen1():
    # Generates the prime powers p**k with k >= 1.
    # We proceed by interleaving primegen with primepowergen2.
    # This is rather more efficient in both space and time than modifying primepowergen2 to generate this sequence directly.
    pg = primegen()
    ppg = primepowergen2()
    p, pp = next(pg), next(ppg)
    while True:
        while p < pp:
            yield p
            p = next(pg)
        while pp < p:
            yield pp
            pp = next(ppg)

def primepowergen2():
    # Generates the prime powers p**k with k >= 2.
    pg = primegen()
    powprime = [[4, next(pg)]]    # [4, 2].  This will be a list-of-lists; each sublist will be of the form [p**k, p].
    nextp = next(pg)    # == 3
    nextpow = nextp**2  # == 9
    while True:
        # This loop has two phases.
        # Phase 1: produce all prime powers below nextpow.
        # Phase 2: integrate nextp and nextpow into the lists of primes and powers.
        minpow, p = powprime[0]     # The least prime power in the list, and its prime.
        if minpow < nextpow:        # We are in phase 1.
            yield minpow
            heappushpop(powprime, [minpow*p, p])
        else:                       # We are in phase 2.
            heappush(powprime, [nextp**2, nextp])
            nextp = next(pg)
            nextpow = nextp**2

print(0, 0)
print(1, 0)

for n in count(2):
    
    seq = primepowergen1()
    diffs = [next(seq)]
    while len(diffs) <= n:
        t, diffs[0] = diffs[0], next(seq)
        for k in range(1, len(diffs)):
            t, diffs[k] = diffs[k], diffs[k-1] - t
        diffs.append(diffs[-1] - t)
    
    x = 1
    
    while diffs[-1] != 0:
        if x % 1000000 == 0: print('\b'*42, x//1000000, end='M', flush=True)
        t, diffs[0] = diffs[0], next(seq)
        for k in range(1, n+1):
            t, diffs[k] = diffs[k], diffs[k-1] - t
        x += 1
    
    print('\b'*42, n, ' ', x, ' ', len(outstr), sep='')

