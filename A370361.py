#! /usr/bin/env python3

from labmath import *

trial_limit = 10**7

for n in count(2):
    p2 = 2**(n-1)
    gpf_so_far = inf
    recordholder = inf
    output = ''
    for x in range(p2-1):   # We do not want the repdigits.
        if x % 1000 == 0:
            c = len(output)
            output = str(x) + ' ' + str(gpf_so_far) + ' ' + str(recordholder)
            print('\b'*c + ' '*c + '\b'*c + output, end='', flush=True)
        strx = bin(p2 + x)[2:]
        for a in "0123456789":
            for b in "0123456789":
                if b == a: continue # We want 2 distinct digits.
                stry = strx.replace('0', '_').replace('1', a).replace('_', b)
                if stry[0] == '0' or stry[-1] == '0': continue   # We want a length-n number that is not a multiple of 10.
                y = int(stry)
                
                if gpf_so_far > trial_limit: gpfy = max(primefac(y, methods=(pollardrho_brent, ecm, siqs)))
                else:
                    z = y
                    gpfy = 0
                    for p in primes:
                        while z % p == 0:
                            z //= p
                            gpfy = p
                    if z != 1: continue
                
                if gpfy <= gpf_so_far:
                    if (gpfy == gpf_so_far and y < recordholder) or gpfy < gpf_so_far: recordholder = y
                    gpf_so_far = gpfy
                    
                    c = len(output)
                    output = str(x) + ' ' + str(gpf_so_far) + ' ' + str(recordholder)
                    print('\b'*c + ' '*c + '\b'*c + output, end='', flush=True)
                    
                    if gpfy < trial_limit: primes = list(primegen(gpfy + 1))
    
    c = len(output)
    print('\b'*c + ' '*c + '\b'*c, end='')
    print('\b'*80, n, ' ', gpf_so_far, ' ', recordholder, sep='')

