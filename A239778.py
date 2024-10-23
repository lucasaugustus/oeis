#!/usr/bin/env python3

from itertools import count, product
from multiprocessing import Pool

def check_f(f):
    n = len(f)
    g = [0] * (n+1)
    total = 0
    while True:
        
        #total += all(f[f[f[i]]] == f[g[g[i]]] for i in range(n))
        
        flag = 1
        for i in range(n):
            if f[f[f[i]]] != f[g[g[i]]]:
                flag = 0
                break
        total += flag
        
        g[0] += 1
        i = 0
        while (i < n) and (g[i] == n):
            g[i] = 0
            g[i+1] += 1
            i += 1
        if g[n] == 1: break
    return total

print(0, 1)
print(1, 1)

for n in count(2):
    nn = n**n
    total = 0
    with Pool() as P:
        for (k, subtotal) in enumerate(P.imap_unordered(check_f, product(range(n), repeat=n), chunksize=100), start=1):
            print("\b"*80 + "%d / %d == %f%%" % (k, nn, 100 * k / nn), end='', flush=True)
            total += subtotal
    print('\b'*80, n, ' ', total, ' '*42, sep='')
    if n == 6: break

