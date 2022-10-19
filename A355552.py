#! /usr/bin/env python3

# Number of ways to select 3 or more collinear points from a 4 X n grid.

from time import process_time
from itertools import count

"""
Define V(n) to be the set of lines that are vertical.
Define H(n) to be the set of lines that are horizontal.
Define D(n) to be the set of lines that are diagonal.
Define D_4(n) to be the set of lines that are diagonal and contained in a length 4 line.
Define D_3(n) to be the set of lines that are diagonal and length 3.
a(n) = |H(n)| + |V(n)| + |D(n)|.
|H(n)| = 4*((2^n) - 1 - n*(n+1)/2).
|V(n)| = n*((2^4) - 1 - 4*(4+1)/2).
|D(n)| = |D_4(n)| + |D_3(n)|.
|D_4(n)| = floor((n-1)*(n-2)/3).
|D_3(n)| = Sum_{i=3..n} f(i).
i = 1,2,4 (mod 12) f(i) = -2*floor(n/12)
i = 3,7   (mod 12) f(i) = 28*floor(n/12) +  4.
i = 5,6,8 (mod 12) f(i) = -2*floor(n/12) +  4.
i = 9,12  (mod 12) f(i) = -2*floor(n/12) +  8.
i = 10    (mod 12) f(i) = -2*floor(n/12) -  6.
i = 11    (mod 12) f(i) = 28*floor(n/12) + 18.
"""

def H(n): return 4 * (2**n - 1 - n*(n+1)//2)
def V(n): return n * (2**4 - 1 - 4*(4+1)//2)
def D(n): return D4(n) + D3(n)
def D4(n): return ((n-1) * (n-2)) // 3
def D3(n): return sum(f(i,n) for i in range(3, n+1))
def f(i,n):
    i %= 12
    if i in (1,2,4): return -2 * (n//12)
    if i in (3,7  ): return 28 * (n//12) +  4
    if i in (5,6,8): return -2 * (n//12) +  4
    if i in (0,9  ): return -2 * (n//12) +  8
    if i in (10,  ): return -2 * (n//12) -  6
    if i in (11,  ): return 28 * (n//12) + 18

for n in range(1, 32):
    assert H(n) >= 0 and V(n) >= 0 and D3(n) >= 0 and D4(n) >= 0
    ans = H(n) + V(n) + D(n)
    diff = [1, 5, 10, 23, 54, 117, 240, 497, 1006, 2027, 4064, 8169, 16356, 32731, 65486, 131039,
            262100, 524233, 1048506, 2097103, 4194242, 8388533, 16777120, 33554365, 67108782,
            134217627, 268435332, 536870825, 1073741716, 2147483519, 4294967142, 8589934479][n] - ans
    print(n, ans)#, diff)

print()
print()
print()

def powerset(l):
    n = len(l)
    for mask in range(2**n): yield [l[i-1] for i in range(1, n+1) if mask & (1 << (i-1))]

def are_collinear(a, b, c):
    # Returns True if the points a, b, and c are collinear, and False otherwise.
    ax, ay = a
    bx, by = b
    cx, cy = c
    area = ax * by + bx * cy + cx * ay - ax * cy - bx * ay - cx * by    # Twice the area of triangle abc
    return area == 0

grid = []
for n in count(1):
    grid.extend([(0,n), (1,n), (2,n), (3,n)])
    totalcollinear = 0
    for points in powerset(grid):
        if len(points) < 3: continue    # We are only interested in sets of 3 or more.
        if all(are_collinear(points[0], points[1], points[k]) for k in range(2, len(points))): totalcollinear += 1
    print(n, totalcollinear)#, process_time())
