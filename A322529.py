#! /usr/bin/env python3

from labmath import partgen, primefac, count

print(0, 1)

for n in count(1):
    total = 0
    for party in partgen(n):
        # Of those partitions that are counted by this sequence, only the all-ones partitions can contain ones.
        # The lists yielded by partgen have their terms in increasing order.
        # Therefore, the following line is not necessary, but speeds things up.
        if party[0] == 1 and party[-1] != 1: continue
        flag = False    # This will be set to True if a partition turns out to be bad.
        factors = set()
        factorcount = len(list(primefac(party[0])))
        for part in party:
            omega = 0
            for p in primefac(part):
                if p in factors:
                    flag = True # A factor is repeated.
                    break
                factors.add(p)
                omega += 1
                if omega > factorcount:
                    flag = True # Not all parts have the same number of factors.
                    break
            if omega != factorcount: flag = True    # Not all parts have the same number of factors.
            if flag: break
        if flag: continue
        total += 1
    print(n, total)

