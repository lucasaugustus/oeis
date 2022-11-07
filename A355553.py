#! /usr/bin/env python3

# Number of ways to select 3 or more collinear points from an n X n grid.

# The points of the shall have x-coordinates 0, 1, 2, ..., n-1 and y-coordinates from the same set.

from itertools import combinations, count
from math import gcd

def A355553(n):
    """
    A collinear set of 3 or more points in the grid corresponds to precisely one line that contains at least two grid points,
    and each line with at least two grid points has a chance of containing some number of collinear sets.
    
    Our algorithm is therefore:
    1.  For every pair of points in the grid, determine a "normalized" equation for the line that passes through those points.
    2.  Discard all duplicate lines.  This is why the normalization of the equations is needed.
    3.  For each equation that remains, determine the number of grid points it contains.  Call that n.
    4.  That line then contributes 2**n - 1 - n - nC2 collinear sets.
    
    For A355553(n), the grid contains n**2 points, so stage 1 considers O(n**4) pairs.  For n == 32, this is just over 1,000,000
    points, but many of those pairs will generate identical lines, so we should not run into memory issues before then.
    
    Now for the normalized form of the line equations:
    We need to be able to handle lines with any rational or infinite slope, so we shall use the "rx + sy + t = 0" form.
    If the line passes through (ax, ay) and (bx, by), then r == ay - by and s == bx - ax and t == ax*by - ay*bx.
    Since ax, ay, bx, and by are all integers, r, s, and t will all be integers as well.
    The normalized form shall have t >= 0.  If t == 0, then it shall have s >= 0.  If also s == 0, then it shall have r >= 0.
    The normalized form shall have r, s, and t be setwise coprime.
    The line r*x + s*y + t == 0 shall be stored in memory as the 3-tuple (r, s, t).
    
    Once the set of lines has been constructed, we will want to compute which grid points each line contains.  The neat thing is
    that we can compute this as we compute the set of lines: once we have determined that the points (ax,ay) and (bx,by) are on
    the line (r,s,t), we automatically know that the line (r,s,t) contains those points.  So we shall construct a dictionary
    whose keys are the lines (r,s,t) and whose values are sets, and every time we determine that two points generate the line
    (r,s,t), we shall add those two points to the corresponding set.  Once we have iterated through all pairs of points to
    generate the lines, we will then already have the points that are on those lines.
    """
    grid = [(x,y) for x in range(n) for y in range(n)]
    lines = {}
    for ((ax,ay), (bx,by)) in combinations(grid, 2):
        r = ay - by
        s = bx - ax
        t = ax * by - ay * bx
        if t < 0: r, s, t = -r, -s, -t
        if t == 0 and s < 0: r, s = -r, -s
        if t == 0 and s == 0: r = -r
        g = gcd(gcd(r, s), t)
        assert g > 0, (ax, ay, bx, by)
        r, s, t = r//g, s//g, t//g
        # r*x + s*y + t == 0 should now be the normalized form of the line through (ax,ay) and (bx,by).
        assert r * ax + s * ay + t == 0, (r,s,t,ax,ay,bx,by)
        assert r * bx + s * by + t == 0, (r,s,t,ax,ay,bx,by)
        if (r,s,t) not in lines: lines[(r,s,t)] = set()
        lines[(r,s,t)].add((ax,ay))
        lines[(r,s,t)].add((bx,by))
    total = 0
    for (r,s,t) in lines:
        n = len(lines[(r,s,t)])
        total += 2**n - 1 - n - ((n * (n-1)) // 2)
    return total

for n in count(1): print(n, A355553(n))
