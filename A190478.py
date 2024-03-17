#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

"""
print(1, 2)
oldA = 2
for n in count(2):
    pg = primegen()
    while next(pg) < oldA: pass
    primes = [next(pg) for _ in range(n)]
    x = 2 * primes[n-1] + 3
    flags = []
    pg2 = primegen()
    p2 = next(pg2)
    while p2 <= x: p2 = next(pg2)
    flags = [isprime(2*p + 3) for p in primes]
    hits = sum(flags)
    
    
    # We now have:
    # primes is a list of n consecutive primes, in increasing order, starting with nextprime(oldA)
    # p == primes[-1]
    # next(pg) will be the smallest prime greater than p
    # x == 2 * p + 3
    # p2 == nextprime(x)
    # next(pg2) will be nextprime(p2)
    # flags[k] is True iff 2 * primes[k] + 3 is prime
    # hits is the number of Trues in flags
    
    while hits != n:
        p = primes.pop(0)
        if flags.pop(0): hits -= 1
        p = next(pg)
        primes.append(p)
        x = 2 * p + 3
        while True:
            if p2 < x:
                p2 = next(pg2)
            elif p2 == x:
                flags.append(True)
                hits += 1
                p2 = next(pg2)
                break
            else:   # p2 > x
                flags.append(False)
                break
        
        # Except for ", starting with nextprime(oldA)", the whole comment block above is true here as well.
        
        if p % 1000000 == 1:
            print('\b'*42, p, end='', flush=True)
            #if p > 10**9: exit()
    
    oldA = primes[0]
    print('\b'*42, n, ' ', oldA, sep='')


"""


print(1, 2)
oldA = 2
pg = primegen()
next(pg)
primes = [next(pg) for _ in range(2)]
for n in count(2):
    flags = [isprime(2*p + 3) for p in primes]
    while not all(flags):
        del primes[0]
        del flags[0]
        p = next(pg)
        primes.append(p)
        flags.append(isprime(2*p + 3))
        if p % 1000000 == 1:
            print('\b'*42, p, end='', flush=True)
            #if p > 10**9: exit()
    oldA = primes[0]
    print('\b'*42, n, ' ', oldA, sep='')
    primes.append(next(pg))
#"""
