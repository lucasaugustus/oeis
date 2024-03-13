#! /usr/bin/env python3

from itertools import count
from math import prod

def istetra(a,b,c,d,e,f):
    # Determines whether there exists a tetrahedron whose side lengths are the given numbers in a particular order.
    # We employ https://ems.press/content/serial-article-files/45383; to match this code's notation to that of the article,
    # use (a, b, c, d, e, f) == (x, y, z, xbar, ybar, zbar).
    
    aa, bb, cc, dd, ee, ff = a*a, b*b, c*c, d*d, e*e, f*f
    
    D  = 2 * aa * dd * (-aa + bb + cc - dd + ee + ff)
    D += 2 * bb * ee * ( aa - bb + cc + dd - ee + ff)
    D += 2 * cc * ff * ( aa + bb - cc + dd + ee - ff)
    D += (aa - dd) * (bb - ee) * (cc - ff)
    D -= (aa + dd) * (bb + ee) * (cc + ff)
    
    D1 = - (d + e + f) * (d + e - f) * (e + f - d) * (f + d - e)
    
    return D > 0 > D1

print(0, 0)

for n in count(1):
    tuples = set()
    for a in range(1, n+1):
        for b in range(1, n+1):
            for c in range(1, n+1):
                for d in range(1, n+1):
                    for e in range(1, n+1):
                        for f in range(1, n+1):
                            if istetra(a,b,c,d,e,f):
                                tuples.add(tuple(sorted((a,b,c,d,e,f))))
    total = 0
    for t in tuples:
        multiplicities = {}
        for x in t: multiplicities[x] = multiplicities.get(x,0) + 1
        total += 720 // prod((1, 1, 2, 6, 24, 120, 720)[x] for x in multiplicities.values())
    print(n, total)
