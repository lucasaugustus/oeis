#! /usr/bin/env python3

from itertools import count
from gmpy2 import *             # available via pip (https://pypi.org/project/gmpy2/)

get_context().precision = 10**9   # number of bits

strcheck = False    # Set this to True to enable the string-comparison approach.

rpi = 1 / const_pi()
if strcheck: rpistr = str(rpi)

log10 = log2(10)

a = mpfr(1) / 3
s = (rootn(3, 2) - 1) / 2
oldedigs = 0

for k in count(0):
    r = 3 / (1 + 2 * cbrt(1 - s**3))
    s = (r - 1) / 2
    a -= 3**k
    a *= r**2
    a += 3**k
    
    error = abs(rpi - a)
    
    edigs = int(floor( - log2(error) / log10 ))
    # int(floor(...)) is required because int(mpfr(...)) rounds to the nearest integer, and floor(mpfr(...)) returns an mpfr.
    
    if strcheck:
        print(k+1, edigs, end=' ', flush=True)
        astr = str(a)
        for j in range(min(len(astr), len(rpistr))):
            if astr[j] != rpistr[j]:
                break
        print(j - 2, "!" if edigs != j-2 else "")
    
    else: print(k+1, edigs)
    
    if edigs <= oldedigs: break
    oldedigs = edigs

print("The available precision has been exhausted.")
print("The last few terms may be wrong due to rounding errors.")
print("Run again with more precision for more terms.")

"""
There is, in my opinion, a conflict between this sequence's name and data.

Let p(n) be the result of the nth iteration of the relevant algorithm.  Then

p(1) == 0.318310095755...
and
p(2) == 0.3183098861837906715377963...
and
1/pi == 0.31830988618379067153776752674502...

To my mind, "number of correct decimal digits" means comparing strings character-by-character and stopping at the first error.
Under this interpretation, the sequence should begin (4,22) or (5,23), depending on whether the initial 0 is included.
If we do not include the initial zero, then there are further errors at terms 2, 3, 5, and 9.
If we DO include the initial zero, then there are further errors at terms 2, 4, 6, 7, 8, 10, and 11.

Clicking through links in the references shows that the data is actually floor(log(1/abs(pi - p(n)))), where the logarithm is
taken to base 10, as computed by https://sites.math.rutgers.edu/~zeilberg/tokhniot/JON.txt.

I have edited the sequence's name accordingly.
"""

"""
1 6
2 22
3 71
4 218
5 659
6 1985
7 5963
8 17898
9 53704
10 161124
11 483384
12 1450164
13 4350505
14 13051531
15 39154610
16 117463847
17 301029987
18 301029987
"""

