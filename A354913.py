#! /usr/bin/env python3

from labmath import primegen        # Available via pip (https://pypi.org/project/labmath/)
from math import comb, isqrt

print("n A354913(n) A376552(n)")
print(0, 1)
print(1, -2)

"""
This program computes sequences A354913 and A376552.  For n >= 1, A354913(n) isthe degree-0 term of the Swinnerton-Dyer polynomial
for the sets {2, 3, 5, 7, ...,, nthprime(n)}.  For n >= 2, these numbers are all squares; we report their square roots as well.
We proceed by computing the whole Swinnerton-Dyer polynomial.  TODO: Find a better way.
We start by observing that the SDP for {2} is x^2 - 2:
"""

a = {0:-2, 2:1}
n = 2

"""
n stores the degree of the polynomial stored in a.
"""

for q in primegen():
    if q == 2: continue
    
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
        print('\b'*42, l, " / ", 2*n, end='', sep='', flush=True)
    a = newa
    n *= 2
    ar = isqrt(a[0])
    assert ar**2 == a[0]
    print('\b'*42, n.bit_length(), ' ', a[0], ' ', isqrt(a[0]), sep='')
