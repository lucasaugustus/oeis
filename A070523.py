#! /usr/bin/env python3

from labmath import *

def isprimepower(n):
    """
    If n is of the form p**e for some prime number p and positive integer e,
    then we return (p,e).  Otherwise, we return None.
    Input: An integer.
    Output: None or a 2-tuple of integers.
    Examples:
    >>> [isprimepower(n) for n in range(6, 11)
    [None, (7, 1), (2, 3), (3, 2), None]
    """
    if n <= 1 or not isinstance(n, inttypes): return None
    x = ispower(n)
    if x is None: return (n,1) if isprime(n) else None
    assert isinstance(x, tuple)
    assert len(x) == 2
    ipp = isprimepower(x[0])
    return None if ipp is None else (ipp[0], x[1]*ipp[1])

def cyclotomiceval(n, x, nfac=None):   # Returns the value of the nth cyclotomic polynomial evaluated at x.
    if n == 1: return x - 1
    if n == 2: return x + 1
    if x == 0: return 1
    if nfac is None:
        if x in (1, -1):
            if x == -1 and n % 2 == 1: return 1
            r = isprimepower(n if x == 1 else n//2)
            return 1 if r is None else r[0]
        nfac = factorint(n)
    else:
        if x ==  1: return list(nfac)[0] if len(nfac) == 1 else 1
        if x == -1: return 2 if (len(nfac) == 1 and 2 in nfac) else (max(nfac) if len(nfac) == 2 and nfac.get(2,0) == 1 else 1)
    num, den = 1, 1
    for dfac in divisors_factored(nfac):
        d = iterprod(p**e for (p,e) in dfac.items())
        ndfac = {p:(e-dfac.get(p, 0)) for (p,e) in nfac.items() if e != dfac.get(p, 0)}
        nd = iterprod(p**e for (p,e) in ndfac.items())
        # Now d divides n and nd == n / d.
        m = mobius(ndfac)
        if   m ==  1: num *= x**d - 1
        elif m == -1: den *= x**d - 1
    return num // den

basis = list(primegen(10**6))

for n in count(1):
    print('\b'*80, "Testing", n, end='', flush=True)
    x = cyclotomiceval(n, mpz(nthprime(n)))
    if isprime(x, tb=basis): print('\b'*80, n, "       ")

# 3, 6, 7, 14, 19, 31, 34, 66, 93, 307, 402, 421, 600, 848, 1022, 1057, 1906, 3772, 4184, 4364
# All terms <= 1906 have been proven with Pari's ECPP.
# No other terms <= 20000.
