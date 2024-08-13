#! /usr/bin/env python3

def fibogen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a+b

fibgen = fibogen()
fibo = next(fibgen)
fibcache = []

def zeckendorf_length(n):
    # returns the length of the Zeckendorf representation of n
    global fibo, fibcache
    while fibo <= n:
        fibcache.append(fibo)
        fibo = next(fibgen)
    zeck, l = 0, len(fibcache) - 1
    while n > 0:
        if fibcache[l] <= n:
            zeck += 1
            n -= fibcache[l]
            l -= 1
        l -= 1
    return zeck

def binweight(n):   # As of Python v3.10, this can be done with n.bit_count().
    c = 0
    while n:
        c += 1
        n &= n - 1
    return c

a, b, k, n = 0, 1, 1, 0
while True:
    # b is the kth Fibonacci number.
    print('\b'*42, k, end='', flush=True)
    if zeckendorf_length(2**k) == binweight(b):
        n += 1
        print('\b'*42, n, ' ', k, sep='')
    a, b, k = b, a+b, k+1

