#! /usr/bin/env python3

# Let r_1 = 1. Let r_{m+1} = r_1 + 1/(r_2 + 1/(r_3 +...(r_{m-1} + 1/r_m)...)), a continued fraction of rational terms.
# A138742: Then row n of this irregular array contains the simple continued fraction terms of r_n.
# A138743: Then a(n) is the number of (positive integer) terms in the simple continued fraction of r_n.
# A138744: Then a(n) is the sum of the (positive integer) terms in the simple continued fraction of r_n.

from labmath import Fraction as Frac, contfrac_rat, convergents, count  # Available via pip (https://pypi.org/project/labmath/)
try: from gmpy2 import mpq as Frac
except ModuleNotFoundError: pass

r = [Frac(1,1)]

A138742, A138743, A138744 = [1], [1], [1]

print()
print("Press ctrl+c at any time to print the results thus far.")
print("Only the first 103 terms of A138742 will be printed.")
print("This corresponds to the first 9 iterations.")
print()

try:
    for n in count(2):
        r_new = Frac(*list(convergents(r))[-1])
        r.append(r_new)
        r_new_scf = list(contfrac_rat(r_new.numerator, r_new.denominator))
        A138742.extend(r_new_scf)
        A138743.append(len(r_new_scf))
        A138744.append(sum(r_new_scf))
        print(("\b"*80) + "Computed %d iterations.  A138742 contains %d terms." % (n, len(A138742)), end='', flush=True)
except KeyboardInterrupt:
    print("\n\nA138742:", list(map(int, A138742))[:104])
    print("\nA138743:", list(map(int, A138743)))
    print("\nA138744:", list(map(int, A138744)))


# A138742: [1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 4, 23, 1, 1, 2, 2, 9, 1, 90, 1, 14, 5, 2, 1, 1, 2, 2, 7, 1, 2, 4, 5, 1, 2, 4, 1, 8, 32, 2, 1, 8, 3, 1, 2, 1, 8, 5, 2, 3, 1, 1, 2, 2, 8, 11, 4, 3, 3, 2, 3, 4, 3, 8, 1, 6, 22, 4, 2, 1, 1, 1, 1, 1, 5, 1, 1, 2, 2, 1, 11, 1, 4, 3, 3, 97, 3, 1, 1, 4, 1, 1, 3, 87, 5, 2, 7, 3]
# A138743: [1, 1, 1, 3, 6, 6, 11, 26, 48, 82, 201, 379, 836, 1554, 3197, 6420, 12639, 25298, 50675, 101675, 203379, 405946, 811519, 1622692, 3249540, 6494117, 12998399, 25991681]
# A138744: [1, 1, 2, 4, 8, 33, 128, 109, 344, 3760, 1829, 18367, 11168, 35246, 41103, 79356, 151643, 344725, 1249071, 1678788, 5385320, 19780986, 17348076, 30966961, 85647848, 160394455, 451333739, 623813606]

