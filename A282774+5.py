#! /usr/bin/env python3

from labmath import factorint, divsigma, divisors, count    # Available via pip (https://pypi.org/project/labmath/)

A282774, A282775 = [], []

try:
    for k in count(1):
        if k % 10000 == 0: print('\b'*42, k, end='', flush=True)
        kfac = factorint(k)
        sig = divsigma(kfac)
        x = sig - sum(sig % d for d in divisors(kfac))
        if sum(kfac.values()) == 1: assert k % x == 0, (k,x)  # if isprime(k)
        elif k % x == 0 and x % k != 0: print('\b'*42 + str(k) + " A282774"        ); A282774.append(k)
        elif k % x == 0 and x % k == 0: print('\b'*42 + str(k) + " A282774 A282775"); A282774.append(k); A282775.append(k)
        elif k % x != 0 and x % k == 0: print('\b'*42 + str(k) + "         A282775");                    A282775.append(k)

except KeyboardInterrupt:
    print()
    print()
    print("A282774:", A282774)
    print()
    print("A282775:", A282775)
    print()

# A282744: 1, 8, 50, 128, 228, 9976, 32768, 41890, 47668, 53064, 501888, 564736, 1207944, 12026888,
#          14697568, 29720448, 2147483648, 2256502784, 21471264576, 35929849856
# A282745: 1, 6, 28, 120, 228, 496, 672, 8128, 30240, 32760, 125640, 501888, 523776, 1207944, 2178540,
#          23569920, 29720448, 33550336, 45532800, 142990848, 459818240, 1379454720, 1476304896, 8589869056,
#          14182439040, 31998395520, 43861478400, 51001180160
# Next terms > 6 * 10**10.
