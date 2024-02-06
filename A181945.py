#! /usr/bin/env python3

from itertools import combinations, count
from math import gcd

def slope(a, b, c, d):
    # The slope of the line passing through (a,b) and (c,d) is (d - b) / (c - a).
    # Since the coordinates are all integers, this is rational or infinite.
    # We return a tuple (p, q) such that the slope is p/q, in lowest terms,
    # or (0,1) if the slope is infinite, or (1,0) if the slope is 0.
    # The degenerate case of a == c and b ==d will not happen.
    if a == c: return (0, 1)
    if b == d: return (1, 0)
    p, q = d - b, c - a
    if q < 0: p, q = -p, -q
    g = gcd(p, q)
    return (p//g, q//g)

def istrap(x1, y1, x2, y2, x3, y3, x4, y4):
    # We do not need to worry about two points being the same.
    # The variable x12 represents the x-component of the vector from point 1 to point 2, etc.
    x12, y12 = x1 - x2, y1 - y2
    x13, y13 = x1 - x3, y1 - y3
    x14, y14 = x1 - x4, y1 - y4
    x23, y23 = x2 - x3, y2 - y3
    x24, y24 = x2 - x4, y2 - y4
    x34, y34 = x3 - x4, y3 - y4
    # First, we check for any collinearities.
    # Distinct points P,Q,R are collinear if and only if the cross-product (P-Q) x (P-R) vanishes.
    # In our case, the z-components of the input vectors are all 0, so we only need to check the z-components of the crosses.
    if x12 * y13 == y12 * x13: return False     # 123: (x12, y12, 0) x (x13, y13, 0)
    if x23 * y24 == y23 * x24: return False     # 234: (x23, y23, 0) x (x24, y24, 0)
    if x34 * y13 == y34 * x13: return False     # 341: (x34, y34, 0) x (x13, y13, 0)
    if x14 * y24 == y14 * x24: return False     # 412: (x14, y14, 0) x (x24, y24, 0)
    # If we get to this line, then we have four distinct points in general position.
    # We now check for parallels.
    slope12 = slope(x1, y1, x2, y2)
    slope13 = slope(x1, y1, x3, y3)
    slope14 = slope(x1, y1, x4, y4)
    slope23 = slope(x2, y2, x3, y3)
    slope24 = slope(x2, y2, x4, y4)
    slope34 = slope(x3, y3, x4, y4)
    if len({slope12, slope13, slope14, slope23, slope24, slope34}) == 6: return False
    # Reaching this line means that we have 4 distint points in general position, with at least 1 pair of parallel segments.
    # This is enough to guarantee that we have a non-degenerate trapezoid.
    return True

def normalizetrap(x1, y1, x2, y2, x3, y3, x4, y4):
    # We need to remove all congruence-duplicates.  We do this by computing a normalized version of each input trapezoid, and
    # storing all the normalized trapezoids in a set().  Every pair of congruent trapezoids have the same normalzied version,
    # and every pair with the same normalized version are congruent.  To obtain the normalized verision, we start by computing
    # the 8 rotation-reflection duplicates, then translating each of those so that it has a point on the x-axis, a point on the
    # y-axis, and no points in quadrants 2,3,4, then listing the points in whatever order Python3's built-in sorted() method
    # spits out, and finally selecting the trapezoid that comes first in the sorted() list of all 8 resulting trapezoids.
    # To handle rotation, we map the point (a, b) to (-b, a).
    untranslatedtraps =     [(( x1,  y1), ( x2,  y2), ( x3,  y3), ( x4,  y4))]
    untranslatedtraps.append(((-y1,  x1), (-y2,  x2), (-y3,  x3), (-y4,  x4)))
    untranslatedtraps.append(((-x1, -y1), (-x2, -y2), (-x3, -y3), (-x4, -y4)))
    untranslatedtraps.append((( y1, -x1), ( y2, -x2), ( y3, -x3), ( y4, -x4)))
    # To handle reflection, we negate the y-coordinates.
    untranslatedtraps.append((( x1, -y1), ( x2, -y2), ( x3, -y3), ( x4, -y4)))
    untranslatedtraps.append((( y1,  x1), ( y2,  x2), ( y3,  x3), ( y4,  x4)))
    untranslatedtraps.append(((-x1,  y1), (-x2,  y2), (-x3,  y3), (-x4,  y4)))
    untranslatedtraps.append(((-y1, -x1), (-y2, -x2), (-y3, -x3), (-y4, -x4)))
    # Now we translate.
    dx = [min(x for (x,y) in trap) for trap in untranslatedtraps]
    dy = [min(y for (x,y) in trap) for trap in untranslatedtraps]
    translatedtraps = []
    for k in range(8):
        trap = untranslatedtraps[k]
        translatedtraps.append(tuple(sorted((
            (trap[0][0] - dx[k], trap[0][1] - dy[k]),
            (trap[1][0] - dx[k], trap[1][1] - dy[k]),
            (trap[2][0] - dx[k], trap[2][1] - dy[k]),
            (trap[3][0] - dx[k], trap[3][1] - dy[k]),
        ))))
    return sorted(translatedtraps)[0]

def doit_slowly():      # This function generates all O(n**8) sets of 4 points per iteration.
    for n in count(1):
        traps = set()
        total = 0
        board = [(x,y) for x in range(n) for y in range(n)]
        for ((x1,y1), (x2,y2), (x3,y3), (x4,y4)) in combinations(board, 4):
            if istrap(x1, y1, x2, y2, x3, y3, x4, y4):
                total += 1
                traps.add(normalizetrap(x1, y1, x2, y2, x3, y3, x4, y4))
        print(n, len(traps))

def doit_faster():
    # The trapezoids in level n consist of those in level n-1 plus those that, after normalization, have at least one point of
    # the form (x,n-1) or (n-1,y).  We therefore proceed by computing the number of trapezoids in the 1x1 grid, then in the 2x2
    # grid that are not in the 1x1 grid, then in the 3x3 grid that are not in the 2x2 grid, and so on.
    # For a normalized trapezoid to be in the n x n grid but not in the n-1 x n-1 grid,
    # it must have a vertex pair of the form ((s,0) , (t,n-1)) or ((0,s) , (n-1,t)).
    # Since we are only counting congruence classes, we do not need to consider the latter case.
    # This function generates O(n**6) sets of points per iteration.
    total = 0
    for n in count(1):
        if n == 1: print(1, 0); total = 0; continue
        if n == 2: print(2, 1); total = 1; continue
        traps = set()
        for s in range(n):
            for t in range(n):
                # Some member of the trapezoid's congruence class contains the points (s,0) and (t,n-1).
                board = [(x,y) for x in range(n) for y in range(n) if (s,0) != (x,y) != (t,n-1)]
                for ((x3, y3), (x4, y4)) in combinations(board, 2):
                    if istrap(s, 0, t, n-1, x3, y3, x4, y4):
                        traps.add(normalizetrap(s, 0, t, n-1, x3, y3, x4, y4))
        total += len(traps)
        print(n, total)

"""
doit_slowly()
"""
doit_faster()
#"""
