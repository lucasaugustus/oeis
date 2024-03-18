#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)
from time import sleep

def mobiussieve():          # A segmented sieve to generate the sequence map(mobius, count(1)).
    pg = primegen()
    primes = [next(pg)]
    nextprime = next(pg)
    lo, hi = 1, nextprime**2
    # We can sieve up to hi - 1.
    while True:
        ints = list(range(lo, hi))
        mobs = [1] * (hi - lo)
        for p in primes:
            for n in range((-lo) % p, hi - lo, p):
                mobs[n] *= -1
                ints[n] //= p
            pp = p*p
            while pp < hi:
                for n in range((-lo) % pp, hi - lo, pp):
                    ints[n] //= p
                    mobs[n] = 0
                pp *= p
        # Any entries in ints that are not 1 are prime divisors of their
        # corresponding numbers that were too large to be sieved out.
        for n in range(hi - lo):
            p = ints[n]
            if p != 1: mobs[n] *= -1
        
        yield from mobs
        
        primes.append(nextprime)
        nextprime = next(pg)
        lo, hi = hi, nextprime**2

data = {1:[], 2:[], 3:[], 4:[], 5:[]}
labels = {1:"A073542", 2:"A077030", 3:"A077031", 4:"A077032", 5:"A077033"}

total = 0

print("Press ctrl+c at any time to stop and summarize the results.")
sleep(3)

try:
    for (n,m) in enumerate(mobiussieve(), start=1):
        if n % 1000000 == 0: print('\b'*42, str(n//1000000) + "M", total, end='    ', flush=True)
        total += m * n
        a = abs(total)
        if a < 1 or 5 < a: continue
        data[a].append(n)
        print('\b'*42, ' '*42, sep='', end='')
        print('\b'*42, labels[a], "(", str(len(data[a])), ") = ", str(n), sep='')
        if all(len(str(x)) > 262 for x in data.values()): break
except KeyboardInterrupt: pass

print()

for x in range(1, 6):
    print()
    print(labels[x] + ":")
    print(data[x])

print()
print("Any subsequent terms are > %d." % (n-1))
