#! /usr/bin/env python3

from labmath import primegen

def abundantgen():
    """
    This is a segmented Sieve of Eratosthenes modified to yield only the abundant numbers, together
    with their numbers of distinct prime factors, prime factors with multiplicity, and divisors.
    """
    pg = primegen()
    primes = [next(pg)]
    nextprime = next(pg)
    lo, hi = 2, nextprime**2
    # We can sieve up to hi - 1.
    x = 1
    while True:
        ints = list(range(lo, hi))
        sigma0 = [1] * (hi - lo)
        sigma1 = [1] * (hi - lo)
        sigma1factors = [1] * (hi - lo)
        littleomega = bytearray(hi - lo)
        bigOmega = bytearray(hi - lo)
        exps = bytearray(hi - lo)
        # Overflowing the cells in the bytearrays will not become a concern until 2**256,
        # which is far beyond anything we could conceivably reach.
        # The number-of-divisors and sum-of-divisors functions grow too quickly for us to
        # be able to use bytearrays for them.
        
        for p in primes:
            
            for n in range((-lo) % p, hi - lo, p):
                ints[n] //= p
                exps[n] = 1
                littleomega[n] += 1
                bigOmega[n] += 1
                sigma1factors[n] = 1 + p
            
            pp = p*p
            while pp < hi:
                for n in range((-lo) % pp, hi - lo, pp):
                    ints[n] //= p
                    exps[n] += 1
                    bigOmega[n] += 1
                    sigma1factors[n] += pp
                pp *= p
            
            for n in range((-lo) % p, hi - lo, p):
                sigma0[n] *= 1 + exps[n]
                sigma1[n] *= sigma1factors[n]
            
        # Any entries in ints that are not 1 are prime divisors of their
        # corresponding numbers that were too large to be sieved out.
        for n in range(hi - lo):
            p = ints[n]
            if p != 1:
                sigma0[n] *= 2
                sigma1[n] *= 1 + p
                littleomega[n] += 1
                bigOmega[n] += 1
        
        for n in range(hi - lo):
            x += 1
            if sigma1[n] > 2*x: yield (x, littleomega[n], bigOmega[n], sigma0[n])
        
        primes.append(nextprime)
        nextprime = next(pg)
        lo, hi = hi, nextprime**2

# In what follows, w, O, and s are stand-ins for $\omega$, $\Omega$, and $\sigma_0$.
# 12 is the first abundant number.
w_current, w_record, w_runlen, w_runstart = 2, 1, 1, 12
O_current, O_record, O_runlen, O_runstart = 3, 1, 1, 12
s_current, s_record, s_runlen, s_runstart = 6, 1, 1, 12
ag = abundantgen()
next(ag)

A376818, A376819, A376820 = [12], [12], [12]  # The sequences corresponding to w, O, and s, respectively

print("Press ctrl-c at any time to stop and print a summary of the results.")

try:
    while True:
        k, w, O, s = next(ag)
        if k % 1000000 == 0: print('\b'*42, k//1000000, end='M', flush=True)
        
        if w == w_current:
            w_runlen += 1
            if w_runlen > w_record:
                assert w_runlen == w_record + 1
                w_record = w_runlen
                print('\b'*42  + "A376818[%d] = %d" % (w_record, w_runstart))
                A376818.append(w_runstart)
        else:
            w_current = w
            w_runlen = 1
            w_runstart = k
        
        
        if O == O_current:
            O_runlen += 1
            if O_runlen > O_record:
                assert O_runlen == O_record + 1
                O_record = O_runlen
                print('\b'*42  + "A376819[%d] = %d" % (O_record, O_runstart))
                A376819.append(O_runstart)
        else:
            O_current = O
            O_runlen = 1
            O_runstart = k
        
        
        if s == s_current:
            s_runlen += 1
            if s_runlen > s_record:
                assert s_runlen == s_record + 1
                s_record = s_runlen
                print('\b'*42  + "A376820[%d] = %d" % (s_record, s_runstart))
                A376820.append(s_runstart)
        else:
            s_current = s
            s_runlen = 1
            s_runstart = k
        
        if k > 10**8: break

except KeyboardInterrupt:
    print()
    print()
    print("A376818:")
    print(str(A376818)[1:-1])
    print()
    print("A376819:")
    print(str(A376819)[1:-1])
    print()
    print("A376820:")
    print(str(A376820)[1:-1])

