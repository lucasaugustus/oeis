#! /usr/bin/env python3

# Number of reversed integer partitions of 2n whose half-alternating sum is 0.

# We define the half-alternating sum of a sequence (A, B, C, D, E, F, G, ...) to be A + B - C - D + E + F - G - ...

# A reversed partition is one whose terms are arranged in increasing order.

from labmath import *

print(0, 1)

for n in count(1):
    total = 0
    for party in partgen(2*n):  # The terms yielded by partgen are already in increasing order.
        if sum(p * [1,1,-1,-1][k%4] for (k,p) in enumerate(party)) == 0:
            total += 1
    print(n, total)

"""
0 1
1 0
2 2
3 1
4 6
5 4
6 15
7 13
8 37
9 37
10 86
11 94
12 194
13 223
14 416
15 497
16 867
17 1056
18 1746
19 2159
20 3424
21 4272
22 6546
23 8215
24 12248
25 15418
26 22449
27 28311
28 40415
29 50985
30 71543
31 90222
32 124730
33 157132
34 214392
35 269696
36 363733
37 456739
38 609611
39 763969
40 1010203
41 1263248
42 1656335
43 2066552
44 2688866
45 3346981
46 4324362
47 5370038
48 6893593
49 8540114
50 10897991
"""
