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

print("n A349995(n) A350098(n) A350099(n)")

data = ""

semis = oddsqfrsemi()
x = next(semis)
maxgap = 0
n = 0
while True:
    x, y = next(semis), x
    if x % 1000000 == 1:
        t = len(str(x))
        print('\b' * t, ' ' * t, '\b' * t, x//1000000, 'M', sep='', end='', flush=True)
    if x - y > maxgap:
        maxgap = x - y
        n += 1
        t = len(str(x))
        print('\b' * t, ' ' * t, '\b' * t, n, ' ', x - y, ' ', y, ' ', x, sep='')
        data += str(x - y) + ", "
        if len(data) >= 262:
            print(data[:-2])
            break
#                                                                       TODO n -= 1 in data
"""
n A349995(n) A350098(n) A350099(n)
1 6 15 21
2 12 21 33
3 16 95 111
4 20 267 287
5 22 2369 2391
6 24 6559 6583
7 26 8817 8843
8 28 13705 13733
9 32 15261 15293
10 36 21583 21619
11 38 35981 36019
12 40 66921 66961
13 44 113009 113053
14 50 340891 340941
15 52 783757 783809
16 60 872219 872279
17 64 3058853 3058917
18 70 3586843 3586913
19 74 5835191 5835265
20 84 12345473 12345557
21 90 108994623 108994713
22 92 248706917 248707009
23 100 268749691 268749791
24 102 679956119 679956221
25 116 709239621 709239737
26 118 3648864859 3648864977
27 120 3790337723 3790337843
28 132 4171420481 4171420613
29 136 33955869693 33955869829
30 138 34279038379 34279038517
31 140 34840796369 34840796509
32 142 47462006869 47462007011
33 146 49167925231 49167925377
34 152 92536603493 92536603645
35 154 129337756741 129337756895
36 156 157470083579 157470083735
37 164 272335233683 272335233847
38 170 300557118821 300557118991
39 184 317837251043 317837251227
40 186 3803186246263 3803186246449
41 210 5357701754449 5357701754659
"""
