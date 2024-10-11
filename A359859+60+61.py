#! /usr/bin/env python3

from itertools import product, count
from math import gcd, isqrt

outstrV = ""
outstrE = ""
outstrF = ""

print("n A359859(n) A359860(n) A359861(n)")

def normalize(a, b, c, s):
    """
    The input tuple (a,b,c,s) consists of integers with s == +/- 1, and represents the quadratic number (a + s * sqrt(b)) / c.
    We compute a tuple (x,y,z,w,t) of integers with t == +/- 1 such that x/y + t * sqrt(z/w) equals the input surd, and every
    two equal input surds have the same result.
    First, we ensure that the denominator is positive:
    """
    if c < 0: a, c, s = -a, -c, -s
    """
    Distributing the denominator yields a/c + s * sqrt(b/c^2).
    """
    g = gcd(a, c)
    x = a // g
    y = c // g
    g = gcd(b, c*c)
    z = b // g
    w = (c*c) // g
    """
    The surd is now x/y + s * sqrt(z/w).  There are still a few things to clean up.
    """
    r = isqrt(z)
    v = isqrt(w)
    if r**2 == z and v**2 == w:
        """
        The surd is in fact x/y + s * r/v.
        """
        num = x*v + s*r*y
        den = y*v
        g = gcd(num, den)
        return (num//g, den//g, 0, 1, 1)
    if z == 0: s = 1
    return (x,y,z,w,s)

for N in count(1):
    
    """
    First, we assemble the list of points that we generate the circles from.
    """
    grid = [(x,0) for x in range(N)] + [(x,1) for x in range(N)]
    """
    The meaning assigned to n in the above line is now carried by the number of terms in the list of points.
    We can, and will, reassign it without worry.
    """
    
    circles = set()
    circles_with_ints = {}  # This dictionary will keep track of which intersection points each circle has.
    for ((a,b), (c,d)) in product(grid, repeat=2):
        if (a,b) == (c,d): continue
        """
        (x - a)^2 + (y - b)^2 == (c - a)^2 + (d - b)^2
        x^2 + y^2 - 2ax - 2by + a^2 + b^2 == a^2 + b^2 + c^2 + d^2 - 2ac - 2bd
        x^2 + y^2 - 2ax - 2by == c^2 + d^2 - 2ac - 2bd
        """
        circles.add((-2*a, -2*b, c*c + d*d - 2*a*c - 2*b*d))
        circles_with_ints[(-2*a, -2*b, c*c + d*d - 2*a*c - 2*b*d)] = set()
    
    """
    The meanings assigned to a,b,c,d in the above loop are now carried by the elements of the list of circles.
    We can, and will, reassign them without worry.
    """
    
    intersections = set()
    for ((a,b,c), (d,e,f)) in product(circles, repeat=2):
        if (a,b,c) == (d,e,f): continue
        """
        We are intersecting the circles x^2 + y^2 + ax + by == c and x^2 + y^2 + dx + ey == f.
        x^2 + y^2 + ax + by == c
        x^2 + y^2 + dx + ey == f
        (a-d)x + (b-e)y == (c-f)
        """
        g = a - d
        h = b - e
        i = c - f
        """
        gx + hy == i
        """
        if h != 0:
            """
            gx + hy == i
            y == (i - gx) / h
            x^2     + (i - gx)^2 / h^2      + ax     + b (i - gx) / h == c
            h^2 x^2 + (i - gx)^2            + ah^2 x + bhi - bgh x    == ch^2
            h^2 x^2 + i^2 - 2ig x + g^2 x^2 + ah^2 x + bhi - bgh x    == ch^2
            (g^2 + h^2) x^2 + i^2 - 2ig x   + ah^2 x + bhi - bgh x    == ch^2
            (g^2 + h^2) x^2       - 2ig x   + ah^2 x + bhi - bgh x    == ch^2       - i^2
            (g^2 + h^2) x^2       - 2ig x   + ah^2 x       - bgh x    == ch^2 - bhi - i^2
            (g^2 + h^2) x^2    + (- 2ig     + ah^2         - bgh) x   == ch^2 - bhi - i^2
            (g^2 + h^2) x^2    - (  2ig     - ah^2         + bgh) x   + (i^2 + bhi - ch^2) == 0
            """
            j = g*g + h*h
            k = 2*i*g + b*g*h - a*h*h
            l = i*i + b*h*i - c*h*h
            """
            jx^2 - kx + l == 0
            x == (k +/- sqrt(k^2 - 4jl)) / (2j)
            """
            m = k*k - 4*j*l
            if m < 0: continue  # The circles enclose disjoint regions.
            n = 2*j
            """
            x == (k +/- sqrt(m)) / n
            Recall that
            y == (i - gx) / h
            y == (i - gk/n -/+ g sqrt(m) / n) / h
            y == (in - gk -/+ g sqrt(m)) / nh
            Let s == 1 if g is negative; otherwise, let s == -1.  Then
            y == (in - gk +/- s * sqrt(mg^2)) / nh
            """
            o = i*n - g*k
            p = g*g*m
            q = n*h
            s = 1 if g < 1 else -1
            """
            We have two intersection points: one coming from the + root of the x-equation, and one coming from the - root.
            These are given by
            x == (k + s * sqrt(m)) / n    and    y == (o - s * sqrt(p)) / q,
            where for the + root we have s == 1, and for the minus root we have s == -1.
            We can thus represent each point as the pair of 4-tuples (k, m, n, s) and (o, p, q, -s).
            We need to normalize these representations; the function normalize() returns a 5-tuple (x,y,z,w,t)
            that represents the expression x/y + t * (z/w).
            """
            xp = normalize(k, m, n,  1)
            yp = normalize(o, p, q,  s)
            xm = normalize(k, m, n, -1)
            ym = normalize(o, p, q, -s)
            """
            We now have normalized representations of the x- and y-coordinates of the intersection points:
            they are (xp, yp) for the plus root and (xm, ym) for the minus.
            """
        else:
            if g == 0: continue     # The circles are concentric.
            """
            gx + hy = i
            Since h == 0, we have
            x == i / g
            i^2 / g^2 +     y^2 + ai/g +    b y == c
            i^2       + g^2 y^2 + aig  + bg^2 y == cg^2
            g^2 y^2 + bg^2 y + (i^2 + aig - cg^2) == 0
            """
            j = g*g
            k = -b*g*g
            l = i*i + a*i*g - c*g*g
            """
            jy^2 - ky + l == 0
            y == (k +/- sqrt(k^2 - 4*j*l)) / (2*j)
            """
            m = k*k - 4*j*l
            if m < 0: continue  # The circles enclose disjoint regions.
            n = 2*j
            """
            y == (k +/- sqrt(m)) / n
            x == (i +/- sqrt(0)) / g
            """
            xp = normalize(i, 0, g,  1)
            xm = xp
            yp = normalize(k, m, n,  1)
            ym = normalize(k, m, n, -1)
        
        intersections.add((xp,yp))
        intersections.add((xm,ym))
        circles_with_ints[(a,b,c)].add((xp,yp))
        circles_with_ints[(d,e,f)].add((xp,yp))
        circles_with_ints[(a,b,c)].add((xm,ym))
        circles_with_ints[(d,e,f)].add((xm,ym))
    
    """
    The number of intersection points (A359859) is just len(intersections).
    The number of edges that a circle contributes is the number of intersection points that it has.
    The number of regions is then computed via Euler's formula.
    """
    V = len(intersections)
    E = sum(map(len, circles_with_ints.values()))
    F = 1 + E - V
    
    print(N, V, F, E)
    outstrV += str(V) + ", "
    outstrE += str(E) + ", "
    outstrF += str(F) + ", "

