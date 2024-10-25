#! /usr/bin/env python3

from labmath import primegen, compress, count       # Available via pip (https://pypi.org/project/labmath/)

def nonsquarefreegen():
    yield from (4,8,9,12,16,18,20,24,25,27,28,32,36,40,44,45,48)
    primesquares = [4, 9, 25, 49]
    pg = primegen()
    for p in primesquares: n = next(pg)
    nn = n*n
    while True:
        n = next(pg)
        ll, nn = nn, n*n
        sl = (nn - ll)
        sieve = bytearray([False]) * sl
        for pp in primesquares:
            k = (-ll) % pp
            sieve[k::pp] = bytearray([True]) * ((sl-k)//pp + 1)
        yield from compress(range(ll,ll+sl), sieve)
        primesquares.append(nn)

print(0, 0)
print(1, 0)

outstr = "0, 0"

try:
    for n in count(2):
        
        seq = nonsquarefreegen()
        diffs = [next(seq)]
        while len(diffs) <= n:
            t, diffs[0] = diffs[0], next(seq)
            for k in range(1, len(diffs)):
                t, diffs[k] = diffs[k], diffs[k-1] - t
            diffs.append(diffs[-1] - t)
        
        x = 1
        
        while diffs[-1] != 0:
            if x % 1000000 == 0: print('\b'*42, x//1000000, end='M', flush=True)
            t, diffs[0] = diffs[0], next(seq)
            for k in range(1, n+1):
                t, diffs[k] = diffs[k], diffs[k-1] - t
            x += 1
        
        outstr += ", " + str(x)
        print('\b'*42, n, ' ', x, ' ', len(outstr), sep='')
        if len(outstr) > 260: break

except KeyboardInterrupt:
    print()
    print(outstr)
