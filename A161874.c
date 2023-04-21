#include <stdio.h>
#include <inttypes.h>
#include <time.h>

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

int main(void) {
    uint64_t b, x, bb, b2;
    int log;
    time_t start = time(NULL);
    const char backspaces[] = "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b";
    const char spaces[] = "                    ";
    for (b = ((uint64_t) 2); b < (((uint64_t) 1) << ((uint64_t) 30)); b += ((uint64_t) 1)) {
        if ((b & (b-1)) == 0) { /* If b is a power of 2, then we print some timing data. */
            log = ((int) 0);
            b2 = bb = b;
            while (bb > ((uint64_t) 1)) {
                log += ((int) 1);
                bb /= ((uint64_t) 2);
            } 
            printf("%s2^%d: %d sec%s\n", backspaces, log, (int) (time(NULL) - start), spaces);
        }
        if (b % ((uint64_t) 1) == ((uint64_t) 0)) {
            printf("%s%" PRIu64 " %7f", backspaces, b, ((float) b) / ((float) b2));
            fflush(stdout);
        }
        x = munhappy(b);
        if (x != ((uint64_t) 2)) printf("%s%" PRIu64 " %" PRIu64 "%s\n", backspaces, b, x, spaces);
    }
    printf("\n");
    return 0;
}

/*
This program prints two types of output line.

The first resembles "2^16: 22 sec".
This indicates that it has examined all bases up to 2^16, and that it took 22 seconds to do so.

The second resembles "130 20".
This indicates that 130 is a base whose least unhappy number is > 2, and that the least unhappy number in that base is 20.

2^16:     22 sec
2^17:     85 sec (x3.86)
2^18:    327 sec (x3.84)
2^19:   1259 sec (x3.85)
2^20:   4862 sec (x3.86)
2^21:  19281 sec (x3.96)
2^22:  75322 sec (x3.91)
2^23: 294220 sec (x3.90)

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
*/
