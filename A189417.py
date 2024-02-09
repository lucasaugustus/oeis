#! /usr/bin/env python3

from itertools import combinations, count
from fractions import Fraction

def iskite(x1, y1, x2, y2, x3, y3, x4, y4):
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
    convex = False
    # If we get to this line, then we have 4 distint points in general position.  For each of the line pairs (12,34), (13,24),
    # and (14,23), we find the intersection of the two lines and check whether that intersection point is in the interior of
    # both segments.  If for some pair it is, then the quadrilateral is convex.
    # If all three segment pairs fail, then the quadrilateral is concave.
    pairindex = 0
    for (ax, ay, bx, by, cx, cy, dx, dy) in ((x1, y1, x2, y2, x3, y3, x4, y4),
                                             (x1, y1, x3, y3, x2, y2, x4, y4),
                                             (x1, y1, x4, y4, x2, y2, x3, y3),):
        pairindex += 1
        # The line passing through points a and b satisfies (by - ay) * x   +   (ax - bx) * y   ==   ax by   -   ay bx.
        # The line passing through points c and d satisfies (dy - cy) * x   +   (cx - dx) * y   ==   cx dy   -   cy dx.
        p, q, r = by - ay, ax - bx, ax * by - ay * bx
        s, t, u = dy - cy, cx - dx, cx * dy - cy * dx
        D = p*t - s*q
        if D == 0: continue     # This segment pair is parallel.
        # Now we need the intersection point of px + qy = r with sx + ty = u.
        y = Fraction(u*p - s*r , p*t - s*q)
        x = Fraction(r*t - q*u , p*t - s*q)
        #assert p*x + q*y == r
        #assert s*x + t*y == u
        # Now we check whether (x,y) is in the interior of the segments ab and cd.
        if (ax <= x <= bx or bx <= x <= ax) and (ay <= y <= by or by <= y <= ay) and \
           (cx <= x <= dx or dx <= x <= cx) and (cy <= y <= dy or dy <= y <= cy): convex, pair = True, pairindex
    if not convex: return False
    # We now know that the quadrilateral is convex.
    if pair == 1: (ax, ay, cx, cy, bx, by, dx, dy) = (x1, y1, x2, y2, x3, y3, x4, y4)
    if pair == 2: (ax, ay, cx, cy, bx, by, dx, dy) = (x1, y1, x3, y3, x2, y2, x4, y4)
    if pair == 3: (ax, ay, cx, cy, bx, by, dx, dy) = (x1, y1, x4, y4, x2, y2, x3, y3)
    # The diagonals are ac and bd.  The edges are ab, bc, cd, and da.
    lab = (ax - bx)**2 + (ay - by)**2
    lbc = (bx - cx)**2 + (by - cy)**2
    lcd = (cx - dx)**2 + (cy - dy)**2
    lda = (dx - ax)**2 + (dy - ay)**2
    return (lab == lbc and lcd == lda) or (lbc == lcd and lda == lab)

def translatequad(x1, y1, x2, y2, x3, y3, x4, y4):
    # This function translates the input quad so that it has a point on the x-axis, a point on the y-axis, and no points in
    # quadrants 2, 3, and 4.  It then sorts the points so that any two translation-duplicates produce the same result,
    # regardless of what order the points are given in.
    dx = min(x1, x2, x3, x4)
    dy = min(y1, y2, y3, y4)
    return tuple(sorted(((x1 - dx, y1 - dy), (x2 - dx, y2 - dy), (x3 - dx, y3 - dy), (x4 - dx, y4 - dy))))

def doit_slowly():      # This function generates all O(n**8) sets of 4 points per iteration.
    for n in count(1):
        total = 0
        board = [(x,y) for x in range(n) for y in range(n)]
        for ((x1,y1), (x2,y2), (x3,y3), (x4,y4)) in combinations(board, 4):
            if iskite(x1, y1, x2, y2, x3, y3, x4, y4):
                total += 1
        print(n, total)

def doit_faster():
    # The kites in level n consist of those that are translation-equivalent to a kite in level n-1, plus those that do not fit
    # in level n-1.  Therefore we construct a dict {kite:(x,y)} where x and y are the x- and y-dimensions of the kite, and then
    # compute the number of translation-duplicates for each kite.
    print(1, 0)
    print(1, 1)
    kites = {((0,0), (0,1), (1,0), (1,1)):(2,2)}
    for n in count(3):
        for s in range(n):
            for t in range(n):
                board = [(x,y) for x in range(n) for y in range(n) if (s,0) != (x,y) != (t,n-1)]
                for ((x3, y3), (x4, y4)) in combinations(board, 2):
                    if iskite(s, 0, t, n-1, x3, y3, x4, y4):
                        k1 = translatequad(s, 0, t, n-1, x3, y3, x4, y4)
                        k2 = translatequad(0, s, n-1, t, y3, x3, y4, x4)
                        d = max(s, t, x3, x4) - min(s, t, x3, x4) + 1
                        kites[k1] = (d, n)
                        kites[k2] = (n, d)
        total = 0
        for (x,y) in kites.values():
            total += (n - x + 1) * (n - y + 1)
        print(n, total)

"""
doit_slowly()
"""
doit_faster()
#"""
