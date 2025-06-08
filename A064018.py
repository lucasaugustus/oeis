#! /usr/bin/env python3

from time import time
from math import log, isqrt, inf
from itertools import takewhile, compress, count




def primegen(limit=inf):
    """
    Generates primes strictly less than limit almost-lazily by a segmented
    sieve of Eratosthenes.  Memory usage depends on the sequence of prime
    gaps; on Cramer's conjecture, it is O(sqrt(p) * log(p)^2), where p is
    the most-recently-yielded prime.
    
    Input: limit -- a number (default = inf)
    
    Output: sequence of integers
    
    Examples:
    
    >>> list(islice(primegen(), 19))
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]
    
    >>> list(primegen(71))
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]
    """
    # We do not sieve 2, so we ought to be able to get sigificant savings by halving the length of the sieve.
    # But the tiny extra computation involved in that seems to exceed the savings.
    yield from takewhile(lambda x: x < limit, (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47))
    pl, pg = [3,5,7], primegen()
    for p in pl: next(pg)
    while True:
        lo = pl[-1]**2
        if lo >= limit: break
        pl.append(next(pg))
        hi = min(pl[-1]**2, limit)
        sieve = bytearray([True]) * (hi - lo)
        for p in pl: sieve[(-lo)%p::p] = bytearray([False]) * ((hi-1)//p - (lo-1)//p)
        yield from compress(range(lo,hi,2), sieve[::2])




def introot(n, r=2):    # TODO Newton iteration?
    """
    Returns the rth root of n, rounded to the nearest integer in the
    direction of zero.  Returns None if r is even and n is negative.
    
    Input:
        n -- an integer
        r -- a natural number or None
    
    Output: An integer
    
    Examples:
    
    >>> [introot(-729, 3), introot(-728, 3)]
    [-9, -8]
    
    >>> [introot(1023, 2), introot(1024, 2)]
    [31, 32]
    """
    if n < 0: return None if r%2 == 0 else -introot(-n, r)
    if n < 2: return n
    if r == 1: return n
    if r == 2: return isqrt(n)
    if r % 2 == 0: return introot(isqrt(n), r//2)
    lower = upper = 1 << (n.bit_length() // r)
    while lower ** r >  n: lower >>= 2
    while upper ** r <= n: upper <<= 2
    while lower != upper - 1:
        mid = (lower + upper) // 2
        m = mid**r
        if   m == n: return  mid
        elif m <  n: lower = mid
        elif m >  n: upper = mid
    return lower




def mobiussieve(limit=inf):
    """
    Uses a segmented sieve to compute the Mobius function for all positive
    integers strictly less than the input.
    
    The time- and space-complexities to iterate over the first n terms
    are within logarithmic factors of O(n) and O(sqrt(n)), respectively.
    
    Input: limit -- an integer.  Default == inf.
    
    Output: Sequence of integers
    
    Example:
    
    >>> list(mobiussieve(21))
    [1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0, -1, 1, 1, 0, -1, 0, -1, 0]
    """
    if limit <= 1: return
    yield 1
    pg = primegen()
    primes = [next(pg)]
    nextp = next(pg)
    lo, hi = 2, min(nextp**2, limit)
    # We can sieve up to hi - 1.
    while lo < limit:
        mobs = [1] * (hi - lo)
        for p in primes:
            for n in range((-lo) %   p  , hi - lo,  p ): mobs[n] *= -p
            for n in range((-lo) % (p*p), hi - lo, p*p): mobs[n]  =  0
        for n in range(hi - lo):
            m = mobs[n]
            if m == 0: continue
            if -lo-n < m < lo+n:
                if m > 0: mobs[n] = -1
                if m < 0: mobs[n] =  1
            else:
                if m > 0: mobs[n] =  1
                if m < 0: mobs[n] = -1
        
        yield from mobs
        
        primes.append(nextp)
        nextp = next(pg)
        lo, hi = hi, min(nextp**2, limit)




def totientsum(n):
    if n <= 10: return 0 if n < 0 else (0,1,2,4,6,10,12,18,22,28,32)[n]
    
    a = introot(int((n / log(log(n)))**2), 3)
    b = n // a
    nr = isqrt(n)
    if verbose:
        print("ln(ln(n)):", log(log(n)))
        print("sqrt(n)/b:", nr//b)
        print("  sqrt(a):", isqrt(a))
        print("        b:", b)
        print("  sqrt(n):", nr)
        print("        a:", a)
        starttime = time()
        p2batchnum = 0
    Mover = [0] * (b + 1)  # Mover[n//x] will store Mertens(x) for large x.
    Mblock = []
    
    mert = 0
    X, Y, Z = 0, 0, 0
    
    s = nr - (nr == n//nr)
    chi = n // s
    
    d = b
    xp = isqrt(n//d)
    
    for (x, mu) in enumerate(mobiussieve(a+1), start=1):
        #if x == 100: exit()
        v = int(str(n // x))    # The int(str( ... )) pushes us back down into the 64-bit data types, when applicable.
        mert += mu
        X += mu * (v * (v+1) // 2)
        
        if x <= nr:
            Mblock.append(mert)
            
            if x > 1 and mu != 0:
                if verbose and (x<10*b or x%b<2): print("\b"*80, " Phase 1:", x, "%f%%" % (100*x/nr), end='    ', flush=True)
                if mu > 0:
                    for y in range(1, min(b, v//x) + 1):
                        Mover[y] -= v // y
                else:
                    for y in range(1, min(b, v//x) + 1):
                        Mover[y] += v // y
            
            while x == xp:
                Mover[d] += 1 - (n//d) + x * mert
                d = (d - 1) if d > 1 else n
                xp = isqrt(n//d)
            
            if x % b == 0 or x == nr:
                if verbose: print("\b"*80, " P1 Batch", x//b, "%f%%" % (100*x/nr), end='    ', flush=True)
                A = 1 + (b * (x//b) if x % b != 0 else (x - b))
                for t in range(1, b+1):
                    #if verbose and x < 20*b: print("\b"*80, "         ", x//b, t, "%f%%" % (100*x/a), end='    ', flush=True)
                    nt = n // t
                    lmin = 1 + n // (t * (x+1))
                    lmax = min(isqrt(n//t), nt // A)
                    for l in range(lmin, lmax + 1):
                        k = nt // l
                        assert A <= k <= x
                        Mover[t] -= Mblock[k - A]
                Mblock.clear()
                if verbose and x == nr:
                    phase1time = time()
                    print("\b"*80 + ("Phase 1 took %f seconds.    " % (phase1time - starttime)))
        
        elif x == chi:
            if verbose and len(Mblock) % 100 == 0: print("\b"*80, " Phase 2:", x, "%f%%" % (100*x/a), end='    ', flush=True)
            if v != b:
                if len(Mblock) == 0: A = v
                Mblock.append(mert)
                B = v
            s -= 1
            chi = n // s
        
        if (x == a and len(Mblock) > 0) or (x > nr and len(Mblock) == b):
            if verbose:
                p2batchnum += 1
                print("\b"*80, " P2 Batch", p2batchnum, "%f%%" % (100*x/a), end='    ', flush=True)
            BnBn = B * n // (B + n)
            for y in range(1, b+1):
                ny = n // y
                tmin = max(2, BnBn // y)
                tmax = min(isqrt(ny), (A + 1) // y)
                for t in range(tmin, tmax+1):
                    nty = ny // t
                    if nr < nty:
                        if B <= n // nty <= A:
                            Mover[y] -= Mblock[A - t*y]
                    else: break
            Mblock.clear()
        
    Z = mert * (b * (b+1) // 2)
    
    if verbose:
        phase2time = time()
        print("\b"*80 + ("Phase 2 took %f seconds.    " % (phase2time - phase1time)))
    
    for y in range(b, 0, -1):
        v = n // y
        vr = isqrt(v)
        Mv = 0
        for t in count(2):
            if n >= (b+1) * (v//t): break
            Mv -= Mover[n//(v//t)]
        # Mv is now Mertens(v).
        Mover[y] += Mv
        Y += y * Mover[y]
    
    if verbose:
        phase3time = time()
        print("\b"*80 + ("Phase 3 took %f seconds." % (phase3time - phase2time)))
    
    return X + Y - Z




verbose = False
for n in count():
    print(n, end=' ', flush=True)
    print(totientsum(10**n))




