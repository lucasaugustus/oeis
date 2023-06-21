#! /usr/bin/env python3

# This file searches for integers n such that n == nthrpime(P(n)) + totient(P(n)),
# where P(n) is the product of the decimal digits of n.  It proceeds by checking
# increasingly large values of P.

# I strongly recommend installing Kim Walisch's primecount software.  We
# need to calculate the nth prime for some largeish values of n, and the
# nthprime function from labmath is much slower and far more memory-hungry.
# https://github.com/kimwalisch/primecount
# On Ubuntu, it can be installed with the command "sudo apt install primecount".
# https://manpages.ubuntu.com/manpages//lunar/man1/primecount.1.html

from subprocess import getoutput
if getoutput("primecount 1e6") == "78498":
    def nthprime(n):
        return int(getoutput("primecount -n %d" % n))
else: from labmath import nthprime      # Available via pip (https://pypi.org/project/labmath/)

from labmath import hamming, iterprod, log

# All values of P(n) factor fully over {2,3,5,7}.

def totient(x):
    tot = x
    for p in (2,3,5,7):
        if x % p == 0:
            tot //= p
            tot *= p - 1
    return tot

for (k,P) in enumerate(hamming(2,3,5,7)):
    if P < 10**17: continue
    if P > 9**45: break
    print('\b'*80, P, k, round(log(P,10),3), end='   ', flush=True)
    n = nthprime(P) + totient(P)
    if P == iterprod(map(int, str(n))):
        print('\b'*80, n, "        ")
