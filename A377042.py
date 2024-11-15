#! /usr/bin/env python3

from labmath import primegen, count, compress  # Available via pip (https://pypi.org/project/labmath/)

def squarefreegen():
    # This is the sieve of Eratosthenes modified to remove multiples of squares of primes.
    yield from (1,2,3,5,6,7,10,11,13,14,15,17,19,21,22,23,26,29,30,31,33,34,35,37,38,39,41,42,43,46,47)
    primesquares = [4, 9, 25, 49]
    pg = primegen()
    for p in primesquares: n = next(pg)
    nn = n*n
    while True:
        n = next(pg)
        ll, nn = nn, n*n
        sl = (nn - ll)
        sieve = bytearray([True]) * sl
        for pp in primesquares:
            k = (-ll) % pp
            sieve[k::pp] = bytearray([False]) * ((sl-k)//pp + 1)
        yield from compress(range(ll, ll+sl), sieve)
        primesquares.append(nn)

print(0, 0)
print(1, 0)

for n in count(2):
    
    seq = squarefreegen()
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
    
    print('\b'*42, n, ' ', x, sep='')

