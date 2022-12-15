#! /usr/bin/env python3

# A358901: Number of integer partitions of n whose parts have all different numbers of prime factors

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

print("0 1")
print("1 1")

Omegas = [len(list(primefac(n))) for n in range(1000)]

for n in count(2):
    total = 0
    for party in partgen(n):
        for (k,p) in enumerate(party): party[k] = Omegas[p]
        if len(party) == len(set(party)): total += 1
    print(n, total)
