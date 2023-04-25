#include <stdio.h>
#include <inttypes.h>
#include <time.h>
#include <stdlib.h>

uint64_t munhappy(uint64_t b) { // uses Brent's cycle finder
    uint64_t n, f, g, p, l, x, y, z = ((uint64_t) 3) * (b - ((uint64_t) 1)) * (b - ((uint64_t) 1));
    if (b == ((uint64_t) 1)) return ((uint64_t) 2);
    for (n = ((uint64_t) 2); n <= z; n++) {
        p = l = ((uint64_t) 1);
        f = n;
        x = f % b; f /= b;
        y = f % b; f /= b;
        g = f*f + y*y + x*x;
        f = n;
        while (f != g) {
            if (p == l) {
                f = g;
                p *= ((uint64_t) 2);
                l = ((uint64_t) 0);
            }
            x = g % b; g /= b;
            y = g % b; g /= b;
            g = g*g + y*y + x*x;
            if (g == ((uint64_t) 1)) goto next;
            l += ((uint64_t) 1);
        }
        return n;
        next: ;
    }
    return ((uint64_t) 0);
}

int main(int argc, char *argv[]) {
    uint64_t b, x, bb, start, step;
    int log;
    
    if (argc == 1) {
        step  = (uint64_t) 1;
        start = (uint64_t) 2;
    } else if (argc == 3) {
        step  = (uint64_t) atoi(argv[1]);
        start = (uint64_t) atoi(argv[2]);
    } else {
        printf("Either zero or two arguments are required.\n");
        exit(1);
    }
    printf("Start: %" PRIu64 "\n", start);
    printf("Step:  %" PRIu64 "\n", step );
    
    time_t starttime = time(NULL);
    const char backspaces[] = "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b";
    const char spaces[] = "                    ";
    for (b = start; b < (((uint64_t) 1) << ((uint64_t) 30)); b += step) {
        if ((b & (b-1)) == 0) { // if b is a power of 2, then we print some timing info.
            log = __builtin_ctz(b); // number of trailing zeros in b
            bb = b;
            printf("%s2^%d: %d sec%s\n", backspaces, log, (int) (time(NULL) - starttime), spaces);
        }
        if (step == 1) printf("%s%" PRIu64 " %7f", backspaces, (uint64_t) b, ((float) b) / ((float) bb) - 1.0);
        else           printf("%s%" PRIu64       , backspaces, (uint64_t) b                                  );
        fflush(stdout);
        x = munhappy(b);
        if (x != ((uint64_t) 2)) printf("%s%" PRIu64 " %" PRIu64 "%s\n", backspaces, (uint64_t) b, (uint64_t) x, spaces);
    }
    printf("\n");
    return 0;
}

/*
Usage: ./munhappy [a b]
Behavior: finds the least unhappy number in base b, then a + b, then 2a + b, etc.
If no arguments are given, then we take a == 1 and b == 2, so that all bases are examined in increasing order.

This program prints two types of output line.
The first resembles "2^16: 22 sec".
This indicates that it has examined all bases up to 2^16, and that it took 22 seconds to do so.
If the arguments result in not checking base 2^k for some k, then the corresponding output line is skipped.

On my computer, which has an AMD 7950X, running with no arguments resulted in the following timing data:
2^17:     25 sec
2^18:     93 sec (x3.72)
2^19:    343 sec (x3.69)
2^20:   1305 sec (x3.80)

The second type of output line resembles "130 20".
This indicates that 130 is a base whose least unhappy number is > 2, and that the least unhappy number in that base is 20.

16 3
18 7
20 3
30 5
130 20
256 3
1042 12
4710 3
7202 3
10082 14
47274 3
65536 3
65600 3
351634 3
426530 3
431730 3
764930 23
5921514 3
26639560 23
32435910 3
88605010 261
97025190 6
99562110 12
*/
