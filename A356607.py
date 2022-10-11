#! /usr/bin/env python3

# Number of integer partitions of n into distinct parts with at least one neighborless part.

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

print("0 0")

for n in range(1, 101):
    total = 0
    for party in partgen(n):
        partyset = set(party)
        if len(party) != len(partyset): continue
        if any(((x-1) not in partyset) and ((x+1) not in partyset) for x in partyset): total += 1
    print(n, total)
