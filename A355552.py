#! /usr/bin/env python3

# Number of ways to select 3 or more collinear points from a 4 X n grid.

# The points of the 4xn grid shall have x-coordinates 0, 1, 2, ..., n-1 and y-coordinates 0, 1, 2, and 3.

"""
We will partition the sets of 3 or more collinear points on the 4xn grid into two classes:
the     horizontal ones, counted by the function H(n), and
the non-horizontal ones, counted by the function D(n).  "D" stands for "diagonal", but vertical sets are also included here.
The non-horizontal collinear sets D(n) are further partitioned into two classes:
the ones with 3 elements, counted by D3(n), and
the ones with 4 elements, counted by D4(n).
There are no non-horizontal ones with 5 or more points, since the grid has only 4 rows.
The non-horizontal collinear sets with 3 elements in turn have a subset whose y-coordinates are {0,1,2}.
This subset is counted by the function E(n).

The result is that
a(n) == H(n) + 3 * D4(n) + 2 * E(n), where
H(n) == 2^(n+2) - 4 - 2*n*(n+1),
D4(n) == floor((n^2 + 2) / 3), and
E(n) == floor((n^2 + 1) / 2).
"""

def H(n):   # The number of horizontal sets.
    """
    In each row, there are n points.
    There are 2**n subsets of those points.
    1 of those is empty, n have 1 element, and n * (n-1) / 2 have 2 elements.  None of those get counted.
    The rest are valid solutions, yielding 4 * (2**n - 1 - n * (n+1) / 2) horizontal sets of 3 or more points.
    
    OGF: 4 * x^3 / ( (x - 1)^3 * (2x - 1) )
    """
    return 2**(n+2) - 4 - 2*n*(n+1)

def D4(n):  # The number of 4-element non-horizontal sets.
    """
    A non-horizontal set of 4 collinear points on our grid must have one point with y == 0, one with y == 1, etc.
    Furthermore, such a set is fully determined by its points with y == 0 and y == 1.
    For any line that passes through (a,0) and (b,1) with a and b integers, the points (c,2) and (d,3) on that line will also
    have their x-coordinates be integers.  In fact, that line is x = (b-a) * y + a, so that c == 2b - a and d == 3b - 2a.
    Now if (a,0), (b,1) and (d,3) are all within the grid, then (c,2) will also be within the grid, so we need only determine
    which values of a and b yield a valid value of d.
    A value of d is valid if and only if 0 <= d < n (so that (d,3) is within the grid).
    Substituting into the inequality yields 0 <= 3b - 2a < n, so that 2a/3 <= b < n/3 + 2a/3.
    
    Let B(n,a) be the number of b-values such that the whole set of 4 points is within the grid and is not horizontal.
    
    To illustrate the next bit, I have prepared https://www.desmos.com/calculator/flrhvksmng.
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
    
    The nonzero values of B(n,a) are controlled by the remainders of n and a modulo 3:
    
    If n % 3 == 0 and a % 3 == 0, then B(n, a) == n / 3.
    If n % 3 == 0 and a % 3 == 1, then B(n, a) == n / 3.
    If n % 3 == 0 and a % 3 == 2, then B(n, a) == n / 3.
    
    If n % 3 == 1 and a % 3 == 0, then B(n, a) == (n + 2) / 3.
    If n % 3 == 1 and a % 3 == 1, then B(n, a) == (n - 1) / 3.
    If n % 3 == 1 and a % 3 == 2, then B(n, a) == (n - 1) / 3.
    
    If n % 3 == 2 and a % 3 == 0, then B(n, a) == (n + 2) / 3.
    If n % 3 == 2 and a % 3 == 1, then B(n, a) == (n + 2) / 3.
    If n % 3 == 2 and a % 3 == 2, then B(n, a) == (n - 1) / 3.
    
    Let k be a positive integer.  Then row 3*k of that table consists of 3*k copies of k, so
        D4(3*k)   == 3*k^2.
    Row 3*k+1 contains k copies of (k+1, k, k) and an additional k+1 at the end, so
        D4(3*k+1) == k * (3*k + 1) + (k + 1) == 3*k^2 + 2*k + 1.
    Row 3*k+2 contains k copies of (k+1, k+1, k) and an additional (k+1, k+1) at the end, so
        D4(3*k+2) == k * (3*k + 2) + 2 * (k+1) == 3*k^2 + 4*k + 2.
    
    Bringing those out for clarity:
        D4(3*k)   == 3*k^2,
        D4(3*k+1) == 3*k^2 + 2*k + 1, and
        D4(3*k+2) == 3*k^2 + 4*k + 2.
    
    We claim that these are all equal to D4(n) == (n^2 + 2) // 3, using Python's syntax that "//" floor division.
    When n == 3*k + 0, this becomes
        ((3*k  )^2 + 2) // 3 == (9*k^2            + 2) // 3                            == 3*k^2.
    When n == 3*k + 1, this becomes
        ((3*k+1)^2 + 2) // 3 == (9*k^2 +  6*k + 1 + 2) // 3 == (9*k^2 +  6*k + 3) // 3 == 3*k^2 + 2*k + 1.
    When n == 3*k + 2, this becomes
        ((3*k+2)^2 + 2) // 3 == (9*k^2 + 12*k + 4 + 2) // 3 == (9*k^2 + 12*k + 6) // 3 == 3*k^2 + 4*k + 2.
    
    We have therefore shown that the number of non-horizontal sets is (n^2 + 2) // 3.
    
    OGF: -x * (x + 1) * (x^2 - x + 1) / ( (x - 1)^3 * (x^2 + x + 1) )
    """
    return (n**2 + 2) // 3

def D3(n):  # The number of 3-element non-horizontal sets.
    """
    Any 3-element non-horizontal collinear set in the grid that skips the line y == 2 can be converted into a 4-element version
    of the same by inserting the relevant point on the line y == 2.  Conversely, any such 4-element set can be converted into a
    3-element non-horizontal collinear set that skips y == 2 by deleting the relevant point.
    Similar logic applies to 3-element sets that skip y == 1.
    Thus D3(n) == 2 * D4(n) + 2 * E(n), where E(n) is the number of 3-element sets whose y-coordinates are {0,1,2}.
    """
    return 2 * D4(n) + 2 * E(n)

def E(n):   # The number of 3-element non-horizontal sets whose y-coordinates are {0,1,2}.
    """
    Let B(n,a) be the number of b-values such that the set of points (a,0), (b,1), (c,2) is collinear and within the grid.
    Using similar logic to that in the prior comment, we obtain the following data:
    
    The entries of this table are B(n,a).  Empty cells are zeros.
    n\a 0  1  2  3  4  5  6  7  8  9 10
    1   1  .  .  .  .  .  .  .  .  .  .
    2   1  1  .  .  .  .  .  .  .  .  .
    3   2  1  2  .  .  .  .  .  .  .  .         
    4   2  2  2  2  .  .  .  .  .  .  .
    5   3  2  3  2  3  .  .  .  .  .  .
    6   3  3  3  3  3  3  .  .  .  .  .
    7   4  3  4  3  4  3  4  .  .  .  .
    8   4  4  4  4  4  4  4  4  .  .  .
    9   5  4  5  4  5  4  5  4  5  .  .
    10  5  5  5  5  5  5  5  5  5  5  .
    11  6  5  6  5  6  5  6  5  6  5  6
    
    (See also https://www.desmos.com/calculator/xnz2zle9t8.)
    
    The nonzero values of B(n,a) are controlled by the remainders of n and a modulo 2:
    
    If n % 2 == 0 and a % 2 == 0, then B(n, a) == n / 2.
    If n % 2 == 0 and a % 2 == 1, then B(n, a) == n / 2.
    
    If n % 2 == 1 and a % 2 == 0, then B(n, a) == (n + 1) / 2.
    If n % 2 == 1 and a % 2 == 1, then B(n, a) == (n - 1) / 2.
    
    Let k be a positive integer.  Then row 2*k of that table consists of 2*k copies of k, so
        E(2*k)   == 2*k^2.
    Row 2*k+1 contains k copies of (k+1, k) and an additional k+1 at the end, so
        E(2*k+1) == k * (2*k + 1) + (k + 1) == 2*k^2 + 2*k + 1.
    
    Bringing those out for clarity:
        E(2*k)   == 2*k^2,          and
        E(2*k+1) == 2*k^2 + 2*k + 1.
    
    We claim that these both equal E(n) == (n^2 + 1) // 2.
    When n == 2*k + 0, this becomes
        ((2*k  )^2 + 1) // 2 == (4*k^2           + 1) // 2                           == 2*k^2.
    When n == 2*k + 1, this becomes
        ((2*k+1)^2 + 1) // 2 == (4*k^2 + 4*k + 1 + 1) // 2 == (4*k^2 + 4*k + 2) // 2 == 2*k^2 + 2*k + 1.
    
    We have therefore shown that the number of 3-element non-horizontal sets whose y-coordinates are {0,1,2} is (n^2 + 1) // 2.
    
    OGF: -x * (x^2 + 1) / ( (x - 1)^3 * (x + 1) )
    """
    return (n**2 + 1) // 2

from itertools import count

for n in count(1):
    h = H(n)                            # Number of horizontal sets
    d3 = D3(n)                          # Number of 3-element non-horizontal sets
    d4 = D4(n)                          # Number of 4-element non-horizontal sets
    ans = h + d3 + d4
    print(n, ans)

# OGF for a(n): -x * (6x^4 + 3x^3 - 2x^2 + 5) / ( (x - 1)^2 * (2x^2 + x - 1) * (x^2 + x + 1) )
