#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/).
from subprocess import getoutput

if getoutput("primecount 1e6") != "78498":
    print("For maximum efficiency, install Kim Walisch's primecount software.")
    print("You can get it at https://github.com/kimwalisch/primecount.")
    print("On Ubuntu, it can be installed with the command \"sudo apt install primecount\".")
    print("https://manpages.ubuntu.com/manpages//lunar/man1/primecount.1.html")
    print("This software is not necessary, but will speed things up.")
    print()
    
    primepi0 = primepi

else:
    def primepi0(n, ps, picache):
        if n not in picache:
            if n < 10**9.5: picache[n] = primepi(n, ps, picache)
            else: picache[n] = int(getoutput("primecount %d" % n))
        return picache[n]


"""
We are looking for integers that have exactly 8 divisors.
These numbers have the shape p**7, p**3 * q, and p*q*r, where p, q, and r are distinct primes.
"""

a = {1:0}
print(1, 0)

for e in count(2):
    M = 10**e
    total = 0
    
    rt3 = introot(M,3)+1
    
    ps, picache = list(primegen(isqrt(M)+1)), {0:0, 1:0}
    
    l = 1
    for (n,p) in enumerate(ps):
        for l in range(l+1, p): picache[l] = n
        picache[p] = n+1
    
    # p**7
    total = primepi0(introot(M,7), ps, picache)
    
    # p**3 * q
    total += sum(primepi0(M//p**3, ps, picache) for p in takewhile(lambda x: x < rt3, ps)) - primepi0(introot(M,4), ps, picache)
    
    # p*q*r
    for p in takewhile(lambda x: x < rt3, ps):
        rt = isqrt(M//p)+1
        for q in takewhile(lambda x: x < rt, ps):
            if q <= p: continue
            total += primepi0(M//(p*q), ps, picache) - primepi0(q, ps, picache)
    
    # total is now the count of all 8-divisor numbers up to M.
    
    a[e] = total - sum(a[f] for f in range(1, e))
    print(e, a[e])

"""
1 0
2 10
3 170
4 1934
5 20067
6 202246
7 2003991
8 19674052
9 192215670
10 1873532828
11 18242642732
12 177582019015
13 1728951136938
14 16840198807124
15 164117159854744
"""
