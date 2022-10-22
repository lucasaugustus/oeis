#! /usr/bin/env python3

from labmath import *   # Available via pip (https://pypi.org/project/labmath/)
from decimal import *

champnum = ''.join(map(str, range(1,100000)))
champden = '1' + ('0' * len(champnum))

champnum, champden = mpz(champnum), mpz(champden)

terms = list(map(int, contfrac_rat(champnum, champden)))[:40]
convs = list(convergents(terms))

print("n A058069(n) A058068(n)")

for (n, (num, den)) in enumerate(convergents(terms)):
    print(n, num, den)
