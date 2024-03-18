#! /usr/bin/env python3

from labmath import *       # Available via pip (https://pypi.org/project/labmath/)

array = []
n = 0
data = ""
for (k,p) in enumerate(primegen(), start=1):
    print('\b'*42, k, end='', flush=True)
    array.append(mpz(p))
    for x in range(k-2, -1, -1): array[x] += array[x+1]
    if isprime(array[0]):
        n += 1
        print('\b'*42, n, ' ', k, sep='')
        data += ", " + str(k)
        if len(data) > 262:
            print(data)
            exit()
