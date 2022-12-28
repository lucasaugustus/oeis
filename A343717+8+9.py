#! /usr/bin/env python3

# Python program for A343717, A343718, and A343719.
# Derived from code by Michael S. Branicky, May 18 2021, at https://oeis.org/A343717/a343717.py.txt.

from labmath import *   # Available via pip (https://pypi.org/project/labmath/)

from sys import exit
from os.path import exists
from time import time
starttime = time()

if not exists("b343717.txt"):
    print("This program will write a file b343717.txt in this directory.")
    start = 0
else:
    print("A file b343717.txt was found in this directory.")
    A343718, A343719 = [1], [0]
    with open("b343717.txt", "r") as bfile:
        start = -1
        for (n,line) in enumerate(bfile):
            line = line.split()
            start += 1
            try:
                assert len(line) == 2
                a = int(line[0])
                assert a == n
                b = int(line[1])
                if b > A343718[-1]:
                    A343718.append(b)
                    A343719.append(n)
            except:
                print("A problem with the b-file was found at line %d." % n)
                print("Quitting.")
                exit()
    start += 1
    print("The last line in the b-file was for n == %d." % (start - 1))
    print("Computation will start at n == %d." % start)

print("The results for A343717 will be appended to b343717.txt.")
print("The results for A343718 and A343719 will be printed to the screen.")

# A343717		a(n) is the smallest number that yields a prime when appended to n!.
# A343718		Record values in A343717.
# A343719		Indices at which record values occur in A343717.

primes = list(primegen(10**4))  # The set of primes for use in trial division.
del primes[0]                   # We will set up our loops so that we do not need to try 2.

def A343717(n, primes):
    # We handle the concatenation of numbers by passing to strings and then back to numbers.
    # It would probably be more efficient to stay in the numerical types and multiply by the appropriate power of 10
    # and add k, but we spend almost all of our time in isprime(), so ... meh.
    fac = str(factorial(n))
    if isprime(mpz(fac+'1')): return 1
    # Let 1 < k <= n.  Then concat(fac, k) is a multiple of k.  Therefore, we cannot have 1 < a(n) <= n.
    # We have concat(fac, k) == fac * 10^t + k, where t is a positive integer.
    # Every prime <= n divides fac, so for concat(fac, k) to be prime, we need k to not be divisible by any prime <= n.
    # Therefore any composite k must be > n^2.
    for k in count(n + 1 + (n%2), 2):
        if k <= n**2 and not isprime(k): continue
        print('\b'*42, n, k, int(time()-starttime), end=' ', flush=True)
        if isprime(mpz(fac + str(k)), tb=primes): return k

with open('b343717.txt', "a") as f:
    for n in count(start):
        an = A343717(n, primes)
        if an > A343718[-1]:
            A343718.append(an)
            A343719.append(n)
            print('\b'*42, end='')
            print("A343718(%d) == %d " % (len(A343718), an))
            print("A343719(%d) == %d " % (len(A343719), n))
        f.write("%d %d\n" % (n, an))
        f.flush()
        print('\b'*42, n, an, int(time()-starttime), end=' ', flush=True)
        if an > 1 and not isprime(an): print(sorted(primefac(an)))
        if n == 2**ilog(n, 2): print('\b'*42 + "Reached n == %d in %.0f seconds." % (n, time() - starttime))
