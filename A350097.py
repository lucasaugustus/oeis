#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

def oddsqfrsemi():
    # Generates the odd squarefree semiprimes by filtering the squares and evens out of the semiprimes.
    pg = primegen()
    semis = semiprimegen()
    p = next(pg)
    pp = p*p
    while True:
        semi = next(semis)
        if pp == semi:
            p = next(pg)
            pp = p*p
            continue
        if semi % 2 == 1: yield semi

print("n A350095(n) A350096(n) A350097(n)")

pg = primegen()
next(pg)        # 2
next(pg)        # 3
next(pg)        # 5
next(pg)        # 7
next(pg)        # 11
p = next(pg)    # 13
q = next(pg)    # 17
semis = oddsqfrsemi()
s = next(semis)
total = 1
recordtotal = 0
n = 0
while True:
    s = next(semis)
    if s < q:
        total += 1
        continue
    
    if total > recordtotal:
        n += 1
        print('\b'*42, n, ' ', p, ' ', q, ' ', total, sep='')
        recordtotal = total
    
    while not (p < s < q): p, q = q, next(pg)
    total = 1
    if q % 100000 == 1: print('\b'*42, q//1000000, end='M', flush=True)
