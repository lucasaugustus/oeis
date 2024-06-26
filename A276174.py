#! /usr/bin/env python3

from labmath import primegen    # Available via pip (https://pypi.org/project/labmath/)

k = 0
for (n,p) in enumerate(primegen(), start=1):
    total = 0
    for x in range(p):
        b, c = x+1, 6 - (x*x + 4) * x
        # y^2 + by + c == 0
        D = (b*b - 4*c) % p
        # y == (-b +/- sqrt(D)) / 2 modulo p
        # If D == 0, then there is 1 solution.
        # If D >= 1 and is a QR mod p, then there are 2 solutions.
        # If D is not a QR mod p, then there are no solutions.
        # This analysis fails for p == 2, but that turns out to not matter.
        if D == 0: total += 1
        elif pow(D, (p-1)//2, p) == 1: total += 2   # Checking the Legendre symbol
    print('\b'*42, n, p, total, end='', flush=True)
    if total == p:
        k += 1
        print("\b"*42 + " "*len("%d %d %d" % (n, p, total)) + ' ' + '\b'*42 + str(k), p)

