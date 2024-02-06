#! /usr/bin/env python3

from itertools import combinations, count
from fractions import Fraction
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

def isconvex(x1, y1, x2, y2, x3, y3, x4, y4):
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
    # We now check for trapezoids.  This is because, later on, we will be dividing by a quantity that could be 0 in that case.
    slope12 = slope(x1, y1, x2, y2)
    slope13 = slope(x1, y1, x3, y3)
    slope14 = slope(x1, y1, x4, y4)
    slope23 = slope(x2, y2, x3, y3)
    slope24 = slope(x2, y2, x4, y4)
    slope34 = slope(x3, y3, x4, y4)
    # If there are < 6 distinct slopes, then we have a trapezoid, which must be convex.
    if len({slope12, slope13, slope14, slope23, slope24, slope34}) < 6: return True
    # We now know that have 4 distint points in general position, with none of the 6 segments parallel to another.
    # For each of the line pairs (12,34), (13,24), and (14,23), we find the intersection of the two lines and check whether
    # that intersection point is in the interior of both segments.  If for some pair it is, then the quadrilateral is convex.
    # If all three segment pairs fail, then the quadrilateral is concave.
    for (ax, ay, bx, by, cx, cy, dx, dy) in ((x1, y1, x2, y2, x3, y3, x4, y4),
                                             (x1, y1, x3, y3, x2, y2, x4, y4),
                                             (x1, y1, x4, y4, x2, y2, x3, y3),):
        # The line passing through points a and b satisfies (by - ay) * x   +   (ax - bx) * y   ==   ax by   -   ay bx.
        # The line passing through points c and d satisfies (dy - cy) * x   +   (cx - dx) * y   ==   cx dy   -   cy dx.
        p, q, r = by - ay, ax - bx, ax * by - ay * bx
        s, t, u = dy - cy, cx - dx, cx * dy - cy * dx
        # Now we need the intersection point of px + qy = r with sx + ty = u.
        # The denominator is guaranteed to be nonzero thanks to the prior trapezoid check.
        y = Fraction(u*p - s*r , p*t - s*q)
        x = Fraction(r*t - q*u , p*t - s*q)
        #assert p*x + q*y == r
        #assert s*x + t*y == u
        # Now we check whether (x,y) is in the interior of the segments ab and cd.
        if (ax <= x <= bx or bx <= x <= ax) and (ay <= y <= by or by <= y <= ay) and \
           (cx <= x <= dx or dx <= x <= cx) and (cy <= y <= dy or dy <= y <= cy): return True
    return False

def normalizequad(x1, y1, x2, y2, x3, y3, x4, y4):
    # We need to remove all congruence-duplicates.  We do this by computing a normalized version of each input quad, and storing
    # all the normalized quads in a set().  Every pair of congruent quads have the same normalzied version, and every pair with
    # the same normalized version are congruent.  To obtain the normalized verision, we start by computing the 8
    # rotation-reflection duplicates, then translating each of those so that it has a point on the x-axis, a point on the
    # y-axis, and no points in quadrants 2,3,4, then listing the points in whatever order Python3's built-in sorted() method
    # spits out, and finally selecting the quad that comes first in the sorted() list of all 8 resulting quads.
    # To handle rotation, we map the point (a, b) to (-b, a).
    untranslatedquads =     [(( x1,  y1), ( x2,  y2), ( x3,  y3), ( x4,  y4))]
    untranslatedquads.append(((-y1,  x1), (-y2,  x2), (-y3,  x3), (-y4,  x4)))
    untranslatedquads.append(((-x1, -y1), (-x2, -y2), (-x3, -y3), (-x4, -y4)))
    untranslatedquads.append((( y1, -x1), ( y2, -x2), ( y3, -x3), ( y4, -x4)))
    # To handle reflection, we negate the y-coordinates.
    untranslatedquads.append((( x1, -y1), ( x2, -y2), ( x3, -y3), ( x4, -y4)))
    untranslatedquads.append((( y1,  x1), ( y2,  x2), ( y3,  x3), ( y4,  x4)))
    untranslatedquads.append(((-x1,  y1), (-x2,  y2), (-x3,  y3), (-x4,  y4)))
    untranslatedquads.append(((-y1, -x1), (-y2, -x2), (-y3, -x3), (-y4, -x4)))
    # Now we translate.
    dx = [min(x for (x,y) in quad) for quad in untranslatedquads]
    dy = [min(y for (x,y) in quad) for quad in untranslatedquads]
    translatedquads = []
    for k in range(8):
        quad = untranslatedquads[k]
        translatedquads.append(tuple(sorted((
            (quad[0][0] - dx[k], quad[0][1] - dy[k]),
            (quad[1][0] - dx[k], quad[1][1] - dy[k]),
            (quad[2][0] - dx[k], quad[2][1] - dy[k]),
            (quad[3][0] - dx[k], quad[3][1] - dy[k]),
        ))))
    return sorted(translatedquads)[0]

def doit_slowly():      # This function generates all O(n**8) sets of 4 points per iteration.
    for n in count(1):
        quads = set()
        total = 0
        board = [(x,y) for x in range(n) for y in range(n)]
        for ((x1,y1), (x2,y2), (x3,y3), (x4,y4)) in combinations(board, 4):
            if isconvex(x1, y1, x2, y2, x3, y3, x4, y4):
                total += 1
                quads.add(normalizequad(x1, y1, x2, y2, x3, y3, x4, y4))
        print(n, len(quads))

def doit_faster():
    # The quads in level n consist of those in level n-1 plus those that, after normalization, have at least one point of the
    # form (x,n-1) or (n-1,y).  We therefore proceed by computing the number of quads in the 1x1 grid, then in the 2x2 grid that
    # are not in the 1x1 grid, then in the 3x3 grid that are not in the 2x2 grid, and so on.
    # For a normalized quad to be in the n x n grid but not in the n-1 x n-1 grid,
    # it must have a vertex pair of the form ((s,0) , (t,n-1)) or ((0,s) , (n-1,t)).
    # Since we are only counting congruence classes, we do not need to consider the latter case.
    # This function generates O(n**6) sets of points per iteration.
    total = 0
    for n in count(1):
        if n == 1: print(1, 0); total = 0; continue
        if n == 2: print(2, 1); total = 1; continue
        quads = set()
        for s in range(n):
            for t in range(n):
                # Some member of the quad's congruence class contains the points (s,0) and (t,n-1).
                board = [(x,y) for x in range(n) for y in range(n) if (s,0) != (x,y) != (t,n-1)]
                for ((x3, y3), (x4, y4)) in combinations(board, 2):
                    if isconvex(s, 0, t, n-1, x3, y3, x4, y4):
                        quads.add(normalizequad(s, 0, t, n-1, x3, y3, x4, y4))
        total += len(quads)
        print(n, total)

"""
doit_slowly()
"""
doit_faster()
#"""
