#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

def sqfrcount(N):
    """
    Counts the number of squarefree integers in the interval [1,N].
    Uses Pawlewicz's O(N**0.4 * log(log(N))**0.6) algorithm.
    Derived from the code at
    https://smsxgz.github.io/post/pe/counting_square_free_numbers/.
    """
    if N < 27: return (0,1,2,3,3,4,5,6,6,6,7,8,8,9,10,11,11,12,12,13,13,14,15,16,16,16,17,17)[N]
    Imax = int(N**0.2 * log(log(N))**0.8 * 0.45)  # TODO: Experiment with different values for the multiplier.
    D = isqrt(N // Imax)
    
    mobs = mobiussieve(D+1)
    s1 = sum(mobs[i] * (N // (i * i)) for i in range(1, D+1))
    
    for k in range(1, D+1): mobs[k] += mobs[k-1]
    # mobs now contains values of the Mertens function.
    
    Mxi_list = []
    Mxi_sum = 0
    for i in range(Imax - 1, 0, -1):
        Mxi = 1
        xi = isqrt(N // i)
        sqd = isqrt(xi)
        assert sqd < D <= xi
        for j in range(1, xi // (sqd + 1) + 1): Mxi -= (xi // j - xi // (j + 1)) * mobs[j]
        for j in range(2, sqd + 1):
            if xi // j <= D: Mxi -= mobs[xi // j]
            else:            Mxi -= Mxi_list[Imax - j * j * i - 1]
        Mxi_list.append(Mxi)
        Mxi_sum += Mxi
    return s1 + Mxi_sum - (Imax - 1) * mobs[-1]


data = ""
for n in count():
    x = sqfrcount(2 * 10**n - 1)
    y = sqfrcount(1 * 10**n - 1)
    print(n, x - y)
    data += str(x - y) + ", "
    if len(data) >= 262:
        print(data[:-2])
        exit()
