#! /usr/bin/env python3

# Number of reversed integer partitions of 2n whose half-alternating sum is 0.

# We define the skew-alternating sum of a sequence (A, B, C, D, E, F, G, ...) to be A - B - C + D + E - F - G + ...

# A reversed partition is one whose terms are arranged in increasing order.

from labmath import *   # Available via pip (https://pypi.org/project/labmath/)

print(0, 1)

for n in count(1):
    total = 0
    for party in partgen(2*n):  # The terms yielded by partgen are already in increasing order.
        if sum(p * [1,-1,-1,1][k%4] for (k,p) in enumerate(party)) == 0:
            total += 1
    print(n, total)

"""
0 1
1 1
2 2
3 3
4 6
5 9
6 16
7 24
8 40
9 59
10 93
11 136
12 208
13 299
14 445
15 632
16 921
17 1292
18 1848
19 2563
20 3610
21 4954
22 6881
23 9353
24 12835
25 17290
26 23469
27 31357
28 42150
29 55889
30 74463
31 98038
32 129573
33 169476
34 222339
35 289029
36 376618
37 486773
38 630313
39 810285
40 1043123
41 1334174
42 1708243
43 2174448
44 2770006
45 3510089
46 4450213
47 5615158
48 7087288
49 8906384
50 11194017
"""
