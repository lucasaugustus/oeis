#! /usr/bin/env python3

from labmath import primegen, count, chain  # Available via pip (https://pypi.org/project/labmath/)

print(0, 0)
print(1, 0)

for n in count(2):
    
    seq = chain([1], primegen())
    diffs = [next(seq)]
    while len(diffs) <= n:
        t, diffs[0] = diffs[0], next(seq)
        for k in range(1, len(diffs)):
            t, diffs[k] = diffs[k], diffs[k-1] - t
        diffs.append(diffs[-1] - t)
    
    x = 1
    
    while diffs[-1] != 0:
        if x % 1000000 == 0: print('\b'*42, x//1000000, end='M', flush=True)
        t, diffs[0] = diffs[0], next(seq)
        for k in range(1, n+1):
            t, diffs[k] = diffs[k], diffs[k-1] - t
        x += 1
    
    print('\b'*42, n, ' ', x, ' ', len(outstr), sep='')

