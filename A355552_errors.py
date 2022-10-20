#! /usr/bin/env python3

# Number of ways to select 3 or more collinear points from a 4 X n grid.

A355552 = [1, 5, 10, 23, 54, 117, 240, 497, 1006, 2027, 4064, 8169, 16356, 32731, 65486, 131039,
           262100, 524233, 1048506, 2097103, 4194242, 8388533, 16777120, 33554365, 67108782,
           134217627, 268435332, 536870825, 1073741716, 2147483519, 4294967142, 8589934479]

# The points of the 4xn grid shall have x-coordinates 0, 1, 2, ..., n-1 and y-coordinates 0, 1, 2, and 3.

from time import process_time
from itertools import count, combinations

# The following is copied directly from the FORMULA section:
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

# First we implement the given formula.
# I agree with the formulas for H, V, and D4.

def H(n):   # The number of horizontal sets.
    # In each row, there are n points.
    # There are 2**n subsets of those points.
    # 1 of those is empty, n have 1 element, and n * (n-1) / 2 have 2 elements.  None of those get counted.
    # The rest are valid solutions.
    return 4 * (2**n - 1 - n*(n+1)//2)  # This matches the given formula for H(n).

def V(n):   # The number of vertical sets.
    # In each column, there are 4 points, and there are 5 3-or-more-element subsets thereof.
    return n * 5                        # This matches the given formula for V(n).

def D4(n):  # The number of 4-element diagonal sets.
    """
    A diagonal set of 4 collinear points on our grid must have one point with y == 0, one with y == 1, etc.
    Furthermore, such a set is fully determined by its points with y == 0 and y == 1.
    For any line that passes through (a,0) and (b,1) with a and b integers, the points (c,2) and (d,3) on that line will also
    have their x-coordinates be integers.  In fact, that line is x = (b-a) * y + a, so that c == 2b - a and d == 3b - 2a.
    Now if (a,0), (b,1) and (d,3) are all within the grid, then (c,2) will also be within the grid, so we need only determine
    which values of a and b yield a valid value of d.
    A value of d is valid if and only if d != a (so that the line is not vertical) and 0 <= d < n (so that (d,3) is within the
    grid).  Substituting into the inequality yields 0 <= 3b - 2a < n, so that 2a/3 <= b < n/3 + 2a/3.
    
    Let B(n,a) be the number of b-values such that the whole set of 4 points is within the grid and is not horizontal.
    Note that this includes the vertical sets.
    
    To illustrate the next bit, I have prepared https://www.desmos.com/calculator/tca6jzrelv.
    To use it to obtain B(n,a), set the n-slider and a-slider to the desired values and count the number of times that the green
    lines cross the thick black line (including the line's endpoints).
    
    The entries of this table are B(n,a).  Empty cells are zeros.
    n\a 0  1  2  3  4  5  6  7  8  9 10
    1   1  .  .  .  .  .  .  .  .  .  .
    2   1  1  .  .  .  .  .  .  .  .  .
    3   1  1  1  .  .  .  .  .  .  .  .
    4   2  1  1  2  .  .  .  .  .  .  .
    5   2  2  1  2  2  .  .  .  .  .  .
    6   2  2  2  2  2  2  .  .  .  .  .
    7   3  2  2  3  2  2  3  .  .  .  .
    8   3  3  2  3  3  2  3  3  .  .  .
    9   3  3  3  3  3  3  3  3  3  .  .
    10  4  3  3  4  3  3  4  3  3  4  .
    11  4  4  3  4  4  3  4  4  3  4  4
    
    The sum of row n is D4(n) + n: D4(n) for the diagonal lines, plus n for the verticals.
    
    Let k be a positive integer.  Then row 3*k of that table consists of 3*k copies of k, so
        D4(3*k)   + n == 3*k^2.
    To obtain row 3*k+1, we increment the nonzero entries with a % 3 == 0 and append k+1, so
        D4(3*k+1) + n == 3*k^2 + k + (k+1) == 3*k^2 + 2*k + 1.
    To obtain row 3*k+2, we increment the nonzero entries with a % 3 == 1 and append another k+1, so
        D4(3*k+2) + n == 3*k^2 + 2*k + 1 + k + (k+1) == 3*k^2 + 4*k + 2.
    Bringing those +n terms to the RHS yields
        D4(3*k)   == 3*k^2 - 3*k,
        D4(3*k+1) == 3*k^2 + 2*k + 1 - (3*k+1), and
        D4(3*k+2) == 3*k^2 + 4*k + 2 - (3*k+2),
    so
        D4(3*k)   == 3*k^2 - 3*k,
        D4(3*k+1) == 3*k^2 -   k, and
        D4(3*k+2) == 3*k^2 +   k.
    
    Now consider the proposed formula D4(n) == (n^2 - 3*n + 2) // 3.
    When n == 3*k + 0, this becomes
        ((3*k  )^2 - 3*(3*k  ) + 2) // 3 == (9*k^2            - 9*k     + 2) // 3                       == 3*k^2 - 3*k.
    When n == 3*k + 1, this becomes
        ((3*k+1)^2 - 3*(3*k+1) + 2) // 3 == (9*k^2 +  6*k + 1 - 9*k - 3 + 2) // 3 == (9*k^2 - 3*k) // 3 == 3*k^2 -   k.
    When n == 3*k + 2, this becomes
        ((3*k+2)^2 - 3*(3*k+2) + 2) // 3 == (9*k^2 + 12*k + 4 - 9*k - 6 + 2) // 3 == (9*k^2 + 3*k) // 3 == 3*k^2 +   k.
    
    Thus the proposed formula for D4 is proved.
    """
    return (n**2 - 3*n + 2) // 3

def D3g(n): # The given formula for the number of 3-element diagonal sets.  The "g" in the function name stands for "given".
    return sum(f(i,n) for i in range(3, n+1))    # Something here appears to be wrong.

def f(i,n): # The function f from the FORMULA section.
    if i % 12 in [1,2,4]: return -2 * (n//12)
    if i % 12 in [3,7  ]: return 28 * (n//12) +  4
    if i % 12 in [5,6,8]: return -2 * (n//12) +  4
    if i % 12 in [0,9  ]: return -2 * (n//12) +  8
    if i % 12 in [10   ]: return -2 * (n//12) -  6
    if i % 12 in [11   ]: return 28 * (n//12) + 18

print("Now we show that the given formula does not match the data.")

for n in range(1, 32):
    h, v, d3g, d4 = H(n), V(n), D3g(n), D4(n)
    ans = h + v + d3g + d4
    diff = A355552[n] - ans
    print(n, h, v, d3g, d4, ans, diff)

print("If the formula matched the data, then that last column would be all zeros.")

print()
print()
print()

# Now begins my own work, showing that the data is also wrong.

def powerset(l):    # The input must be indexable.
    n = len(l)
    for mask in range(2**n): yield [l[i-1] for i in range(1, n+1) if mask & (1 << (i-1))]

def are_collinear(a, b, c):
    # Input: Three 2-tuples.
    # Output: Returns True if the points a, b, and c are collinear, and False otherwise.
    # Example: are_collinear((0,0), (1,1), (2,0)) returns False.
    # Example: are_collinear((0,0), (1,1), (2,2)) returns True.
    ax, ay = a
    bx, by = b
    cx, cy = c
    area = ax * by + bx * cy + cx * ay - ax * cy - bx * ay - cx * by    # Twice the area of triangle abc
    return area == 0

def D3m(n):     # The number of 3-element diagonal sets.  The "m" stands "mine".
    # A 3-element diagonal set must have all of its x-coordinates distinct,
    # and its set of y-coordinates must be {0,1,2}, {0,1,3}, {0,2,3}, or {1,2,3}.
    # There is a bijection between the {0,1,2} sets and the {1,2,3} sets by replacing the y-coordinate y with 3-y,
    # and that same operation is a bijection between the {0,1,3} sets and the {0,2,3} sets.
    # Therefore we need only count the {0,1,2} sets and the {0,1,3} sets and then double the result.
    d3 = 0
    for a in range(n):
        for b in range(n):
            if b == a: continue # We want diagonals only; b == a implies a vertical.
            # For (a,0), (b,1), and (c,2) to be collinear, we need c == 2*b - a.
            c = 2*b - a
            if 0 <= c < n: d3 += 1
            # For (a,0), (b,1), and (d,3) to be collinear, we need d == 3*b - 2*a
            d = 3*b - 2*a
            if 0 <= d < n: d3 += 1
    return d3 * 2

for n in range(1,32):
    h, v, d3, d4 = H(n), V(n), D3m(n), D4(n)
    h = H(n)                            # Number of horizontal sets
    v = V(n)                            # Number of vertical sets
    d3 = D3m(n)                         # Number of 3-element diagonal sets
    d4 = D4(n)                          # Number of 4-element diagonal sets
    ans = h + v + d3 + d4
    diff = A355552[n] - ans
    print(n, h, v, d3, d4, ans, diff)

"""
# The following is the brutest of brute force methods.  It examines every element of the powerset of the points in the grid.
grid = []
for n in count(1):
    grid.extend([(n-1,0), (n-1,1), (n-1,2), (n-1,3)])
    totalcollinear = 0
    H, V, D3, D4 = 0, 0, 0, 0
    for points in powerset(grid):
        if len(points) < 3: continue    # We are only interested in sets of 3 or more.
        if all(are_collinear(points[0], points[1], points[k]) for k in range(2, len(points))):
            totalcollinear += 1
            exes = set()
            whys = set()
            for (x,y) in points:
                exes.add(x)
                whys.add(y)
            if   len(exes) == 1: V += 1     # All x-coords equal ==> vertical
            elif len(whys) == 1: H += 1     # All y-coords equal ==> horizontal
            else:                           # Diagonal
                assert len(points) < 5      # Cannot have a diagonal line with 5 or more points on a 4xn grid
                if len(points) == 3: D3 += 1
                if len(points) == 4: D4 += 1
        assert totalcollinear == V + H + D3 + D4
    print(n, H, V, D3, D4, totalcollinear)
"""
