#! /usr/bin/env sage

# Numbers n such that x^n + x^10 + 1 is irreducible over GF(2).

from itertools import count

P.<x> = GF(2)[]

A = [0, "\b\b\b02475", "60", "61", "63", "74","76", "77", "78", "79", "80", "81", "82", "83"]

try:
    print("Press ctrl+c at any time to halt computation and print the results.")
    results = [[] for k in range(14)]
    for n in count(1):
        for k in range(1, 14):
            print('\b'*42 + "%d %d" % (n, k), end=' ', flush=True)
            if (x^n+x^k+1).is_irreducible():
                results[k].append(n)
                print('\b'*42 + "A0574%s[%d] == %d" % (A[k], len(results[k]), n) )
except KeyboardInterrupt:
    print("\n")
    for k in range(1, 14):
        print("A0574" + A[k], results[k])
    print("\nAny subsequent terms are >= %d." % n)

"""
A002475 [2, 3, 4, 6, 7, 9, 15, 22, 28, 30, 46, 60, 63, 127, 153, 172, 303, 471, 532, 865, 900, 1366, 2380, 3310, 4495, 6321, 7447, 10198, 11425, 21846, 24369, 27286, 28713, 32767, 34353, 46383, 53484, 62481, 83406, 87382, 103468, 198958, 248833]
A057460 [1, 3, 5, 11, 21, 29, 35, 93, 123, 333, 845, 4125, 10437, 10469, 14211, 20307, 34115, 47283, 50621, 57341, 70331, 80141]
A057461 [1, 2, 4, 5, 6, 7, 10, 12, 17, 18, 20, 25, 28, 31, 41, 52, 66, 130, 151, 180, 196, 503, 650, 761, 986, 1391, 1596, 2047, 2700, 4098, 6172, 6431, 6730, 8425, 10162, 11410, 12071, 13151, 14636, 17377, 18023, 30594, 32770, 65538, 77047, 81858, 102842, 130777, 137113, 143503, 168812, 192076, 262146]
A057463 [1, 3, 7, 9, 15, 39, 57, 81, 105, 1239, 5569, 9457, 11095, 11631, 12327, 37633, 63247, 216457]
A057474 [2, 3, 6, 9, 12, 14, 17, 20, 23, 44, 47, 63, 84, 129, 236, 278, 279, 297, 300, 647, 726, 737, 2574, 2660, 4233, 4500, 8207, 11900, 16046, 21983, 23999, 24596, 24849, 84929, 130926, 156308, 160046, 185142, 270641]
A057476 [1, 3, 5, 7, 17, 31, 71, 97, 167, 175, 209, 385, 2159, 5617, 8921, 33425, 39119, 76625, 110249, 192127, 255265]
A057477 [1, 3, 4, 6, 10, 12, 15, 18, 21, 25, 31, 34, 42, 52, 55, 57, 105, 127, 172, 210, 220, 300, 393, 420, 441, 492, 772, 807, 972, 1023, 1071, 1266, 1564, 2220, 2242, 3297, 3585, 5314, 6300, 7306, 8719, 10777, 23647, 26119, 33127, 44247, 48036, 48945, 59172, 68841, 131071, 152922, 170583, 200991, 214780, 236892, 240471, 265857]
A057478 [9, 15, 39, 105, 119, 153, 177, 209, 3143, 13169, 19833, 33567, 53129, 64439, 88871, 109865, 122945, 138543]
A057479 [1, 4, 5, 8, 11, 12, 14, 18, 23, 28, 30, 36, 49, 54, 60, 68, 71, 79, 84, 103, 113, 151, 156, 191, 198, 364, 390, 470, 476, 508, 540, 620, 721, 823, 865, 1135, 1558, 1825, 1950, 4225, 4788, 8100, 12294, 12553, 14686, 18516, 19660, 24470, 30486, 32086, 43908, 54031, 58489, 65473, 73406, 75185, 76694, 82990, 84478, 91782, 98310, 129319, 171526, 185623, 196614, 245574, 271031]
A057480 [3, 7, 33, 111, 279, 511, 1047, 1239, 8119, 15727, 16153, 22617, 38407]
A057481 [2, 9, 15, 17, 18, 36, 60, 63, 84, 95, 98, 135, 156, 170, 186, 218, 540, 641, 660, 879, 1388, 1820, 1866, 1943, 2055, 2388, 3423, 3983, 6090, 6713, 9900, 14610, 18330, 18855, 22346, 26180, 32855, 36410, 43911, 44465, 82652, 88764, 131250, 154644, 231420]
A057482 [3, 5, 7, 9, 17, 49, 97, 257, 425, 895, 1385, 4807, 11303, 25175, 103943, 104975, 161993, 282455]
A057483 [28, 31, 33, 84, 87, 103, 174, 414, 574, 687, 780, 1111, 1449, 1860, 6964, 7708, 11700, 17428, 19398, 19876, 78391, 131305, 136564, 181684]

Any subsequent terms are > 300000.
"""
