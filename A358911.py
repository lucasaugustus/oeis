#! /usr/bin/env python3

# A358911: Number of integer compositions of n whose parts all have the same number of prime factors, counted with multiplicity

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

print("0 1")
print("1 1")

Omegas = [len(list(primefac(n))) for n in range(1000)]
factorials = [1]
for n in range(1, 1000): factorials.append(n * factorials[-1])

for n in count(2):
    total = 0
    for party in partgen(n):
        if len(set(Omegas[p] for p in party)) != 1: continue
        # A composition is a permutation of a partition.
        data = {}
        # The keys of the dictionary "data" shall be set(party).
        # The values shall be the multiplicities of the keys in the partition.
        for p in party: data[p] = data.get(p, 0) + 1
        # How many strings are there that have (value1) copies of (key1), (value2) copies of (key2), etc?
        # Multinomial coefficients to the rescue!
        num = factorials[sum(data.values())]
        denom = iterprod(factorials[x] for x in data.values())
        assert num % denom == 0, (n, num, denom, party, data)
        total += num // denom
    print(n, total)
