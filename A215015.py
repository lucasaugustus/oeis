#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

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
        yield from compress(range(ll,ll+sl), sieve)
        primesquares.append(nn)

def sphenics():
    quasisphenics = almostprimegen(3)   # The numbers with exactly 3 prime factors, counted with multipicity.
    squarefrees = squarefreegen()
    s, q = next(squarefrees), next(quasisphenics)
    while True:
        if s < q:
            s = next(squarefrees)
            continue
        if q < s:
            q = next(quasisphenics)
            continue
        assert q == s
        yield q
        q = next(quasisphenics)
        s = next(squarefrees)
    # We need to yield every term that is yielded by both of those two generators.
    raise NotImplementedError       # TODO

sphgen = sphenics()
y = next(sphgen)
x = next(sphgen)
twins = 0
p10 = 100
n = 2

print(1, 0)

while True:
    if x == y + 1: twins += 1
    x, y = next(sphgen), x
    if x > p10 > y:
        print(n, twins)
        n += 1
        p10 *= 10
