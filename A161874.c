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
    uint64_t b, x, bb, start, stop, step;
    int log;
    
    if (argc == 1) {
        start =  (uint64_t) 2;
        stop  = ((uint64_t) 1) << 32;
        step  =  (uint64_t) 1;
    } else if (argc == 4) {
        start = (uint64_t) atoi(argv[1]);
        stop  = (uint64_t) atoi(argv[2]);
        step  = (uint64_t) atoi(argv[3]);
    } else {
        printf("This is a program for computing A161874 and A362026.\n");
        printf("Either zero or three arguments are required.\n");
        printf("If three arguments are provided as ./munhappy x y z,\n");
        printf("then we examine all bases in [x, y) that are congruent to x modulo z.\n");
        printf("If no arguments are provided, then we take (x,y,z) == (2, 4294967296, 1).\n");
        printf("\n");
        printf("This program prints two types of output line.\n");
        printf("The first resembles \"2^17: 25 sec\".\n");
        printf("This would be printed after examining base 2^17,\n");
        printf("and indicates that 25 seconds elapsed since starting the program.\n");
        printf("If the arguments result in not checking base 2^k for some k,\n");
        printf("then the corresponding output line is skipped.\n");
        printf("On my computer, running with no arguments produced the following timing data:\n");
        printf("2^17:   22 sec\n");
        printf("2^18:   87 sec (x3.95)\n");
        printf("2^19:  341 sec (x3.92)\n");
        printf("2^20: 1332 sec (x3.91)\n");
        printf("\n");
        printf("The second type of output line resembles \"130 20\".\n");
        printf("This indicates that 130 is a base whose least unhappy number is > 2 (A161874),\n");
        printf("and that the least unhappy number in that base is 20 (A362026).\n");
        exit(1);
    }
    printf("Start: %" PRIu64 "\n", start);
    printf("Stop:  %" PRIu64 "\n", stop );
    printf("Step:  %" PRIu64 "\n", step );
    
    time_t starttime = time(NULL);
    const char backspaces[] = "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b";
    const char spaces[] = "                    ";
    for (b = start; b < stop; b += step) {
        if ((b & (b-1)) == 0) { // if b is a power of 2, then we print some timing info.
            log = __builtin_ctz(b); // number of trailing zeros in b
            bb = b;
            printf("%s2^%d: %d sec%s\n", backspaces, log, (int) (time(NULL) - starttime), spaces);
        }
        if (step == 1) printf("%s%" PRIu64 " %7f", backspaces, (uint64_t) b, ((float) b) / ((float) bb) - 1.0);
        else           printf("%s%" PRIu64       , backspaces, (uint64_t) b                                  );
        //fflush(stdout);
        x = munhappy(b);
        if (x != ((uint64_t) 2)) printf("%s%" PRIu64 " %" PRIu64 "%s\n", backspaces, (uint64_t) b, (uint64_t) x, spaces);
    }
    printf("\n");
    return 0;
}

/*
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
