#! /usr/bin/env python3

from itertools import count
from gmpy2 import *             # available via pip (https://pypi.org/project/gmpy2/)

get_context().precision = 10**9   # number of bits

strcheck = False    # Set this to True to enable the string-comparison approach.

pi = const_pi()
if strcheck: pistr = str(pi)

log10 = log2(10)

a = mpfr(1)
b = rec_sqrt(2)
s = mpfr(1) / 2
oldedigs = 0

for k in count(1):
    a, b = (a + b) / 2, rootn(a*b, 2)
    aa = a * a
    s -= 2**k * (aa - b*b)
    p = 2 * aa / s
    del aa
    
    error = abs(pi - p)
    del p
    
    edigs = int(floor( - log2(error) / log10 ))
    # int(floor(...)) is required because int(mpfr(...)) rounds to the nearest integer, and floor(mpfr(...)) returns an mpfr.
    
    if strcheck:
        print(k, edigs, end=' ', flush=True)
        pstr = str(p)
        for j in range(min(len(pstr), len(pistr))):
            if pstr[j] != pistr[j]:
                break
        print(j - 2, "!" if edigs != j-2 else "")
    
    else: print(k, edigs)
    
    if edigs <= oldedigs: break
    oldedigs = edigs

print("The available precision has been exhausted.")
print("The last few terms may be wrong due to rounding errors.")
print("Run again with more precision for more terms.")

"""
There is, in my opinion, a conflict between this sequence's name and data.

Let p(n) be the result of the nth iteration of the Salamin-Brent algorithm.  Then

p(1) == 3.187672...
and
p(2) == 3.141680....

To my mind, "number of correct decimal digits" means comparing strings character-by-character and stopping at the first error.
Under this interpretation, the sequence should begin (1,3) or (2,4), depending on whether the initial 3 is included.
If we do not inlcude the initial 3, then the current data has two further errors: this interpretation requires a(12) == 5586 and
a(17) == 178829.  If we DO include the initial 3, then there are even more errors.

Clicking through links in the references shows that the data is actually floor(log(1/abs(pi - p(n)))), where the logarithm is
taken to base 10, as computed by https://sites.math.rutgers.edu/~zeilberg/tokhniot/JON.txt.

I have edited the sequence's name accordingly.
"""

"""
1 1
2 4
3 9
4 20
5 42
6 85
7 173
8 347
9 697
10 1395
11 2792
12 5587
13 11175
14 22352
15 44706
16 89414
17 178830
18 357661
19 715324
20 1430650
21 2861303
22 5722607
23 11445216
24 22890435
25 45780872
26 91561745
27 183123492
28 301029986
"""

