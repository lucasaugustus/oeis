#! /usr/bin/env python3

from labmath import nthprimeapprox, log, prevprime, nextprime   # Available via pip (https://pypi.org/project/labmath/)
from subprocess import getoutput
from itertools import count
from time import time

if getoutput("primecount 1e6") != "78498":
    print("This program requires Kim Walisch's primecount software.")
    print("You can get it at https://github.com/kimwalisch/primecount.")
    print("On Ubuntu, it can be installed with the command \"sudo apt install primecount\".")
    print("https://manpages.ubuntu.com/manpages//lunar/man1/primecount.1.html")
    exit()

def primecount(n): return int(getoutput("primecount %d" % n))

def nthprime(n):
    if n <= 216289611853439384: return int(getoutput("primecount -n %d" % n))
    x = prevprime(nthprimeapprox(n))
    c = primecount(x)
    # x is prime and approximates the nth prime number.
    # c is the number of primes <= x.
    # We do a single round of Newton's method before examining individual primes.
    if c == n: return x
    x = prevprime(x + int((n - c) * log(x)))
    c = primecount(x)
    while c > n:
        x = prevprime(x)
        c -= 1
    while c < n:
        x = nextprime(x)
        c += 1
    return x

a, n = 1, 1
z = time()
while True:
    print(n, a, time() - z)
    a = 2 * nthprime(a)
    n += 1

, 1611548301646589127698, 166820830882144877428234
