#! /usr/bin/env python3

from labmath import primegen        # Available via pip (https://pypi.org/project/labmath/)
from heapq import *

def primepowergen():
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

pg = primegen()
ppg = primepowergen()

next(pg); next(pg)    # 2, 3
p = next(pg)    # 5
q = next(pg)    # 7
k = 3

# The interval [p,q] will have a pair of consecutive primes as its endpoints.

x = next(ppg)   # 4

n = 0

while True:
    p, q = q, next(pg)  # Move the interval up one notch.
    k += 1
    if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
    while True:
        if x > p: break
        x = next(ppg)
    # x is now the least prime power > p.
    if x > q: continue
    # At this point, we have p,q,x,k such that p < x < q, p is the kth prime,
    # q is the (k+1)th prime, and x is the least prime power > p.
    ppcount = 1
    x = next(ppg)
    while x < q:
        ppcount += 1
        x = next(ppg)
    # Now x is the least prime power above the interval,
    # and ppcount is the number of prime powers in the interval.
    if ppcount == 2:
        n += 1
        print('\b'*42, n, ' ', k, sep='')

