#! /usr/bin/env python3

from labmath import isprime, count          # Available via pip (https://pypi.org/project/labmath/)

# We will count up in base 3.
# The list that holds the digits will list them in order of increasing significance:
# for example, [0,1,2] represents the number 0 * 3^0  +  1 * 3^1  +  2 * 3^2.

d = 1   # number of digits
digits = [0]
n = 0
for t in count(1):
    if t % 1000000 == 0: print('\b'*42, t//1000000, end='M', flush=True)
    digits[0] += 1
    i = 0
    while i < d-1 and digits[i] == 3:
        digits[i] = 0
        digits[i+1] += 1
        i += 1
    if i == d-1 and digits[i] == 3:
        digits[i] = 0
        digits.append(1)
        d += 1
    assert t == sum(digits[i] * 3**i for i in range(d))
    
    rotated = digits[:]
    for r in range(d):
        rotated.append(rotated.pop(0))
        x = sum(rotated[i] * 3**i for i in range(d))
        if not isprime(x): break
    else:
        n += 1
        print('\b'*42, n, ' ', t, sep='')
