#! /usr/bin/env python3

from labmath import *                   # Available via pip (https://pypi.org/project/labmath/)
from subprocess import getoutput

if getoutput("primecount 1e6") != "78498":
    print("For maximum efficiency, install Kim Walisch's primecount software.")
    print("You can get it at https://github.com/kimwalisch/primecount.")
    print("On Ubuntu, it can be installed with the command \"sudo apt install primecount\".")
    print("https://manpages.ubuntu.com/manpages//lunar/man1/primecount.1.html")
    print("This software is not necessary, but will speed things up.")
    print()

else:
    def primepi(n): return int(getoutput("primecount %d" % n))
    
    def nthprime(n):
        if n <= 216289611853439384: return int(getoutput("primecount -t1 -n %d" % n))
        x = prevprime(nthprimeapprox(n))
        c = primepi(x)
        # x is prime and approximates the nth prime number.
        # c is the number of primes <= x.
        # We do a single round of Newton's method before examining individual primes.
        if c == n: return x
        x = prevprime(x + int((n - c) * log(x)))
        c = primepi(x)
        while c > n:
            x = prevprime(x)
            c -= 1
        while c < n:
            x = nextprime(x)
            c += 1
        return x

if getoutput("./primesum 1e6") != "37550402023":
    print("For maximum efficiency, install Kim Walisch's primesum software.")
    print("Source code and precompiled binaries for Linux, Windows, and macOS")
    print("are available at https://github.com/kimwalisch/primesum.")
    print("This software is not necessary, but will speed things up.")
    print()

else:
    def primesum(n): return int(getoutput("./primesum %d" % n))

print(1, 7)

for n in count(2):
    lo = primepi(nextprime(10**(n-1)))
    hi = primepi(10**n) - primepi(10**(n-1))
    print(n, primesum(nthprime(hi)) - primesum(nthprime(lo-1)) - hi*(hi+1)//2 + lo*(lo-1)//2)

