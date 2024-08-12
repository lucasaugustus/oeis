#! /usr/bin/env python3

from labmath import *
from multiprocessing import Pool

def test(p):
    p2p1 = p*p + p + 1
    p2p1_primes = set()
    for q in primefac(p2p1):
        if q in p2p1_primes: continue
        p2p1_primes.add(q)
        q2q1 = q*q + q + 1
        q2q1_primes = set()
        for r in primefac(q2q1):
            if r in q2q1_primes: continue
            q2q1_primes.add(r)
            if (r+1) % p == 0: return (p, True)
    return (p, False)

while True:
    threads = input("Enter the number of threads to use: ")
    if threads.isdecimal():
        threads = int(threads)
        if threads > 0: break
    print("You must enter a positive integer.")

with Pool(threads) as P:
    n = 0
    for (p, flag) in P.imap(test, primegen(), chunksize=100):
        print('\b'*42, p, end='', flush=True)
        if flag:
            n += 1
            print('\b'*42, n, ' ', p, sep='')

