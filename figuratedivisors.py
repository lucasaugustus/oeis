#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

print("Press ctrl+c at any time to halt and print a collated version of the results.")

# This file computes sequences from the OEIS that list the smallest numbers with exactly n divisors of various figurate types.
# Specifically:
A358539 = {}    # a(n) is the smallest number with exactly n divisors that are n-gonal numbers.
A358540 = {}    # a(n) is the smallest number with exactly n divisors that are n-gonal pyramidal numbers.
A358541 = {}    # a(n) is the smallest number with exactly n divisors that are centered n-gonal numbers.
A358542 = {}    # a(n) is the smallest number with exactly n divisors that are tetrahedral numbers.
A358543 = {}    # a(n) is the smallest number with exactly n divisors that are square pyramidal numbers.
A358544 = {}    # a(n) is the smallest number with exactly n divisors that are centered triangular numbers.
A358545 = {}    # a(n) is the smallest number with exactly n divisors that are centered square numbers.

def is_square(n):
    """
    Checks whether n is square.
    If n is square, we return its square root.
    Otherwise, we return False.
    For the sake of speed, we include a bunch of modular prefilters --- otherwise, this would be a major bottleneck.
    """
    if n % 64 not in {0, 1, 4, 9, 16, 17, 25, 33, 36, 41, 49, 57}:                return False
    if n % 63 not in {0, 1, 4, 7, 9, 16, 18, 22, 25, 28, 36, 37, 43, 46, 49, 58}: return False
    if n % 25 not in {0, 1, 4, 6, 9, 11, 14, 16, 19, 21, 24}:                     return False
    if n % 31 not in {0, 1, 2, 4, 5, 7, 8, 9, 10, 14, 16, 18, 19, 20, 25, 28}:    return False
    if n % 23 not in {0, 1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18}:                    return False
    if n % 19 not in {0, 1, 4, 5, 6, 7, 9, 11, 16, 17}:                           return False
    if n % 17 not in {0, 1, 2, 4, 8, 9, 13, 15, 16}:                              return False
    if n % 11 not in {0, 1, 3, 4, 5, 9}:                                          return False
    r = isqrt(n)
    if r*r == n: return r
    return False

def is_ngonal_pyramidal(k, n):
    """
    Checks whether k is an n-gonal pyramidal number.
    An integer k is n-gonal-pyramidal iff there exists a positive integer x such that x * (x+1) * (n*x - 2*x - n + 5) / 6 == k.
    This can be rearranged as (n-2)x^3 + 3x^2 + (5-n)x - 6k == 0.
    By Descartes's rule of signs, there will be exactly one positive root for the values of n and k that we consider.
    We have n >= 3.  Then 9 <= 3n, so 13 - 7n <= 4 - 4n,
    so                 3         +      (n^2 - 7n + 10) <=  4 - 4n + n^2,
    so                 3         +    (n - 5) * (n - 2) <=     (n - 2)^2,
    so                 3         +    (n - 5) * (n - 2) <  3 * (n - 2)^2,
    so                 1/(n-2)^2 + (1/3) * (n-5)/(n-2)  <  1,
    so            sqrt(1/(n-2)^2 + (1/3) * (n-5)/(n-2)) <  1,
    so -1/(n-2) + sqrt(1/(n-2)^2 + (1/3) * (n-5)/(n-2)) <  1.
    The lesser side of this inequality is the greater root of 3 * (n-2) * x^2 + 6*x - (n-5),
    which is the derivative of the cubic being considered.
    Therefore the greater critical point of the cubic is < 1, so the cubic is both increasing and concave-up for all x >= 1.
    Now we need a (preferably slight) overestimate of that positive root that we are looking for.
    """
    if k == 1: return True
    a, c, d = n-2, 5-n, 6*k
    lo, hi = 1, 1 + max(3, d//a + 1)   # From Cauchy's bound
    # Since the cubic is increasing and concave-up on the intervals we will be considering, the secant line from lo to hi will
    # intersect the x-axis below the root, and the tangent line at hi will intersect the x-axis above the root.
    loy = ((a*lo + 3) * lo + c) * lo - d
    hiy = ((a*hi + 3) * hi + c) * hi - d
    if loy == 0: return True
    if hiy == 0: return True
    while hi != lo + 1:
        #assert loy < 0 < hiy
        mid = (lo + hi) // 2
        midy = ((a*mid + 3) * mid + c) * mid - d
        if  midy == 0: return True
        if  midy <  0: lo, loy = mid, midy
        elif 0 < midy: hi, hiy = mid, midy
    return False

def is_centered_ngonal(k, n):
    """
    Checks whether k is a centered n-gonal number.
    An integer k is centered n-gonal iff there exists a positive integer x such that n * x * (x+1) / 2 + 1 == k.
    Solving for x yields x == ( sqrt( (8k - 8) / n + 1 ) - 1 ) / 2.
    """
    z = 8*k - 8
    if z % n != 0: return False
    z //= n
    z += 1
    x = is_square(z)
    if not x: return False
    x -= 1
    if x % 2 == 1: return False
    x //= 2
    assert ((n * x * (x+1)) // 2) + 1 == k
    return True

def is_tetrahedral(n):
    """
    Checks whether n is a tetrahedral number.
    A positive integer n is tetrahedral iff there exists a positive integer x such that x * (x + 1) * (x + 2) / 6 == n.
    This can be rearranged as x^3 + 3x^2 + 2x - 6n == 0.
    By Descartes's rule of signs, there will be exactly one positive root for the values of n that we consider.
    Lemma: that root is always between cbrt(6n) and cbrt(6n) - 1.
    Proof:
    1.  Evaluating the polynomial at cbrt(6n) yields a positive quantity.
    2.  Evaluating the polynomial at cbrt(6n) - 1 yields -cbrt(6n), which is negative.
    It therefore suffices to check whether floor(cbrt(6n)) is a root of the polynomial.
    """
    x = introot(6*n, 3)
    return ((x + 3) * x + 2) * x == 6*n

def is_square_pyramidal(n):
    """
    Checks whether n is a square pyramidal number.
    A positive integer n is square-pyramidal iff there exists a positive integer x such that x * (x + 1) * (2x + 1) / 6 == n.
    This can be rearranged as 2x^3 + 3x^2 + x - 6n == 0.
    By Descartes's rule of signs, there will be exactly one positive root for the values of n that we consider.
    Lemma: that root is always between cbrt(3n) and cbrt(3n) - 1.
    Proof:
    1.  Evaluating the polynomial at cbrt(3n) yields a positive quantity.
    2.  Evaluating the polynomial at cbrt(3n) - 1 yields -3 * cbrt(3n)^2, which is negative.
    It therefore suffices to check whether floor(cbrt(3n)) is a root of the polynomial.
    """
    x = introot(3*n, 3)
    return ((2*x + 3) * x + 1) * x == 6*n

def is_centered_triangular(n):
    """
    Checks whether n is a centered triangular number.
    The centered triangulars are given by (3n^2 + 3n + 2) / 2.
    Therefore n is centered-triangular iff there exists an integer x such that 2n == 3x^2 + 3x + 2.
    Solving for x yields x == (sqrt((8n - 5) / 3) - 1) / 2.
    """
    if n % 3 != 1: return False
    z = (8*n - 5) // 3
    zr = is_square(z)
    if not zr: return False
    if zr % 2 != 1: return False
    x = (zr - 1) // 2
    t = (x + 1) * x * 3 + 2
    assert t % 2 == 0
    assert t // 2 == n
    return True

def is_centered_square(n):
    """
    Checks whether n is a centered square number.
    The centered squares are given by n^2 + (n-1)^2.
    Therefore n is centered-square iff there exists an integer x such that n == 2x^2 - 2x + 1.
    Solving for x yields x == (sqrt(2n-1) + 1) / 2.
    """
    z = 2*n - 1
    zr = is_square(z)
    if not zr: return False
    x = zr + 1
    assert x % 2 == 0
    x //= 2
    assert x**2 + (x-1)**2 == n
    return True

def is_ngonal(k, n):
    """
    Checks whether k is an n-gonal number.
    A positive integer k is n-gonal iff there exists an integer x such that ((n-2) * x^2 - (n-4) * x) / 2 == k.
    Solving for x yields x == ((n-4) + sqrt((n-4)^2 + 8 * (n-2) * k)) / (2*n-4).
    """
    if   k == 1: return True
    z = (n-4)**2 + 8 * (n-2) * k
    x = is_square(z)
    if not x: return False
    return (x + n - 4) % (2*n-4) == 0

# TODO: The main bottleneck is is_ngonal_pyramidal.

def minfacsieve(end):
    """
    Minimum factor sieve.  Returns a list sieve of length (end+1) such that sieve[n] contains the smallest prime factor of n.
    """
    sieve = list(range(end+1))
    primes = list(primegen(isqrt(end)+1))
    for p in reversed(primes): sieve[p::p] = [p] * (end//p)
    return sieve

def factorint_mfs(n, mfs):
    """
    Given n and a minimum factor sieve mfs, return factorint(n).
    """
    fac = {}
    while n > 1:
        p = mfs[n]
        fac[p] = fac.get(p,0) + 1
        n //= p
    return fac

try:
    mfs_limit = 6 * 10**8
    mfs = minfacsieve(mfs_limit)
    
    data1 = [#(A358539, "A358539", is_ngonal),
             #(A358540, "A358540", is_ngonal_pyramidal),
             #(A358541, "A358541", is_centered_ngonal),
             ]
    data2 = [#(A358542, "A358542", is_tetrahedral),
             (A358543, "A358543", is_square_pyramidal),
             #(A358544, "A358544", is_centered_triangular),
             #(A358545, "A358545", is_centered_square),
             ]

    for x in count(1):
        if x % 1000 == 0: print('\b'*42, x, end='', flush=True)
        if x < mfs_limit: divs = list(divisors(factorint_mfs(x, mfs)))
        else:             divs = list(divisors(x))
        
        for n in range(3, len(divs)+1):
            for (dictionary, string, test) in data1:
                if n not in dictionary and len([d for d in divs if test(d, n)]) == n:
                    dictionary[n] = x
                    print('\b'*42, "%s(%2d) == %d" % (string, n, x))
        
        for (dictionary, string, test) in data2:
            z = len([d for d in divs if test(d)])
            if z > 0 and z not in dictionary: dictionary[z] = x; print('\b'*42, "%s(%2d) == %d" % (string, z, x))

except KeyboardInterrupt:
    print()
    print()
    for (dictionary, string, _) in data1:
        print("%s:" % string, dictionary)
        for k in range(3, max(dictionary)+1): print("%s(%2d) == %s" % (string, k, dictionary.get(k, "unknown")))
        print()
    for (dictionary, string, _) in data2:
        print("%s:" % string, dictionary)
        for k in range(1, max(dictionary)+1): print("%s(%2d) == %s" % (string, k, dictionary.get(k, "unknown")))
        print()
    print("Any missing or subsequent terms, if they exist, are >= %d." % x)
