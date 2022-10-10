#! /usr/bin/env python3

# Odd numbers N for which numerator(sigma(N^2)/N^2) is prime, but sigma(N^2) is composite.

from labmath import divsigma, count, isprime, gcd, factorint    # Available via pip (https://pypi.org/project/labmath/)

for n in count(1,2):
    if n % 10**6 == 1: print('\b'*42, n // 10**6, end=' M', flush=True)
    den = n*n
    nfac = factorint(n)
    nnfac = {p:2*e for (p,e) in nfac.items()}
    num = divsigma(nnfac)
    g = gcd(num, den)
    if g == 1: continue
    numg = num // g
    if isprime(numg): print('\b'*42 + str(n) + "    ")

# 39, 507, 2379, 6591, 13167, 29511, 148955, 1672209, 8852259, 212370543, 1929229929.
# Next term > 10^10.
