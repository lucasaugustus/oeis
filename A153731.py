#! /usr/bin/env python3

from labmath import primegen        # Available via pip (https://pypi.org/project/labmath/)
from math import comb

"""
This program computes the coefficients of the Swinnerton-Dyer polynomials for the sets {2}, {2,3}, {2,3,5}, {2,3,5,7}, ....
We start by observing that the SDP for {2} is x^2 - 2:
"""

a = {0:-2, 2:1}
n = 2

"""
n stores the degree of the polynomial stored in a.
"""

#print(2)
print(-2, 1)

for q in primegen(20):
    if q == 2: continue
    #print(q)
    
    """
    We have the coefficients of the SDP for {2, 3, 5, 7, ..., prevprime(q)} stored in the dictionary a.
    All odd-index coefficients are 0, so we do not store them; instead, we will access the dictionary by a.get(z, 0).
    We proceed to compute the coefficients of the SDP for {2,3,5,7,...,q} in order of increasing degree.
    The coefficients will be stored in the dictionary newa.
    """
    
    newa = {}
    
    for l in range(0, 2*n+1, 2):
        # We skip all odd l because those turn out to be 0.
        total = 0
        for k in range(l, 2*n+1):
            g = 0
            for j in range(k+1):
                multiplier = a.get(j,0) * a.get(k-j,0)
                if multiplier == 0: continue
                subtotal = sum(comb(j, l-m) * comb(k-j, m) * int((-1)**(k-j-m)) for m in range(l+1))
                # We do not need the int() there for theory reasons;
                # we use it because (-1)**(negative) always returns a float, even when the exponent is an integer.
                g += subtotal * multiplier
            if k % 2 == 1: assert g == 0
            else:
                assert (k - l) % 2 == 0
                # Because of the if-statement, we have even k; because of that and the fact that l loops over even numbers,
                # the floor division in this exponent is in fact a true division.
                total += q**((k-l)//2) * g
        if total != 0:
            newa[l] = total
            print(newa[l], end=' ', flush=True)
    print()
    a = newa
    n *= 2
    assert n == max(a.keys())

