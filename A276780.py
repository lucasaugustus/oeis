#! /usr/bin/env python3

from itertools import count
from gmpy2 import *             # available via pip (https://pypi.org/project/gmpy2/)

get_context().precision = 10**9   # number of bits

strcheck = False    # Set this to True to enable the string-comparison approach.

rpi = 1 / const_pi()
if strcheck: rpistr = str(rpi)

log10 = log2(10)

y = rootn(2, 2) - 1
a = 2 - 4 * y
oldedigs = 0

for k in count(0):
    yrt = rootn(1 - y**4, 4)
    ynum = 1 - rootn(1 - y**4, 4)
    yden = 1 + rootn(1 - y**4, 4)
    y = (1 - yrt) / (1 + yrt)
    del yrt
    a *= (1+y)**4
    a -= ((y + 1) * y + 1) * y * 2**(2*k+3)
    
    error = abs(rpi - a)
    
    edigs = int(floor( - log2(error) / log10 ))
    # int(floor(...)) is required because int(mpfr(...)) rounds to the nearest integer, and floor(mpfr(...)) returns an mpfr.
    
    if strcheck:
        print(k+1, edigs, end=' ', flush=True)
        astr = str(a)
        for j in range(min(len(astr), len(rpistr))):
            if astr[j] != rpistr[j]:
                break
        print(j - 1, "!" if edigs != j-1 else "")
    
    else: print(k+1, edigs)
    
    if edigs <= oldedigs: break
    oldedigs = edigs

print("The available precision has been exhausted.")
print("The last few terms may be wrong due to rounding errors.")
print("Run again with more precision for more terms.")

"""
There is, in my opinion, a conflict between this sequence's name and data.

Let p(n) be the result of the nth iteration of the relevant algorithm.  Then

p(2) == 0.31830988618379067153776752674502872406892483...
and
1/pi == 0.31830988618379067153776752674502872406891929...

To my mind, "number of correct decimal digits" means comparing strings character-by-character and stopping at the first error.
Under this interpretation, the sequence should begin (9,40) or (10,41), depending on whether the initial 0 is included.
If we do not include the initial zero, then there are further errors at terms 5 and 8.
If we DO include the initial zero, then there are further errors at terms 3, 4, 6, and 7.

Clicking through links in the references shows that the data is actually floor(log(1/abs(pi - p(n)))), where the logarithm is
taken to base 10, as computed by https://sites.math.rutgers.edu/~zeilberg/tokhniot/JON.txt.

I have edited the sequence's name accordingly.
"""

"""
1 9
2 41
3 171
4 694
5 2790
6 11172
7 44702
8 178825
9 715319
10 2861297
11 11445210
12 45780865
13 183123485
14 301029988
15 301029988
"""

