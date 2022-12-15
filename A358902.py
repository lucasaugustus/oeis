#! /usr/bin/env python3

# A358902: Number of integer compositions of n whose parts have weakly decreasing numbers of distinct prime factors

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

print("0 1")
print("1 1")

omegas = [len(set(primefac(n))) for n in range(1000)]
factorials = [1]
for n in range(1, 1000): factorials.append(n * factorials[-1])

for n in count(2):
    total = 0
    for party in partgen(n):
        # A composition is a permutation of a partition.
        data = {}
        # The keys of the dictionary "data" shall be set(omegas[p] for p in party).
        # The values shall be dictionaries.
        # For each k, the keys of data[k] shall be the parts p of the partition such that Omegas[p] == k.
        # The value data[k][p] shall be the number of times that p appears in the partition.
        for p in party:
            k = omegas[p]
            if k not in data: data[k] = {}
            if p not in data[k]: data[k][p] = 0
            data[k][p] += 1
        # The compositions that get counted by A358902 are those that start with some permutation of those parts with the
        # maximal number of prime factors, followed by some permutation of those parts with the second-maximal number of prime
        # factors, etc.
        subtotal = 1
        for k in sorted(data, reverse=True):
            subdata = data[k]
            # How many strings are there that have (value1) copies of (key1), (value2) copies of (key2), etc?
            # Multinomial coefficients to the rescue!
            num = factorials[sum(subdata.values())]
            denom = iterprod(factorials[x] for x in subdata.values())
            assert num % denom == 0, (n, num, denom, party, k, data)
            subtotal *= num // denom
        total += subtotal
    print(n, total)
