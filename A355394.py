#! /usr/bin/env python3

# Number of integer partitions of n such that, for all parts x, x - 1 or x + 1 is also a part.

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

print("0 1")

for n in count(1):
    total = 0
    for party in partgen(n):
        flag = True
        for x in party:
            if ((x-1) not in party) and ((x+1) not in party): flag = False
        if flag: total += 1
    print(n, total)
