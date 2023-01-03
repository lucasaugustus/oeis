#! /usr/bin/env python3

from labmath import *
from time import *

def A357477_0(n):   # Smallest k such that sqrt(kn) rounds to a prime
    for k in count(1):
        if isprime(round(sqrt(k*n))):
            return k

def A357477_1(n):   # A357477 without floating points
    for kn in count(n, n):
        x = isqrt(kn)
        if kn > x*x + x: x += 1
        if isprime(x): return kn // n

A357477 = A357477_1

record, index, counter = 0, 0, 0
last_time, running_avg = 0, 0
batch = 10**6
for n in count(1):
    if n % batch == 0:
        t = process_time()
        new_avg = batch / (t - last_time)
        running_avg = (running_avg + new_avg) / 2
        print('\b'*42, n//batch, int(t), int(running_avg), int(n/t), end='', flush=True)
        last_time = t
    a = A357477(n)
    if a > record:
        record, index = a, n
        counter += 1
        print('\b'*42 + "%d %d            " % (counter, index))

"""
1 1
2 19
3 67
4 154
5 218
6 251
7 601
8 651
9 652
10 7051
11 17001
12 101157
13 555039
14 971160
15 1240273
16 6191735
17 81174469
18 84349567
19 131625552
20 214344967
21 214345119
22 3974507614
23 5446707884
24 5574291825
25 41016920663
26 69752538433
Any subsequent terms are > 10^11.
"""
