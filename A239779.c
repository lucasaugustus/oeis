#include <stdio.h>
#include <inttypes.h>

uint64_t A239778(uint_fast8_t n) {
    /* This algorithm brute-forces its way through all possible f,g pairs, resuling in O(n^(2n+1)) time complexity. */
    uint_fast8_t nn=n+n,  f[nn+1], *g=f+n, score, i;
    uint64_t total=0, cycles=0, totalcycles=1;
    for (i=0; i<n+n; i++) {totalcycles *= n;}
    /* We can imagine f and g as the base-n representations of integers in the interval [0, n^n),
    with leading zeros included.  We need to iterate over all such numbers.
    Furthermore, we can consider the concatenation of the two lists to be a single 2n-digit number.
    We will therfore iterate over the integers in [0, n^(2n)), store the digits in a single array,
    and use pointer tricks to split into f and g.  This allows us to use a single, flat main loop
    rather than nesting a loop for g within a loop for f. */
    for (i=0; i<nn+1; i++) {f[i] = 0;}
    /* f will be the first n slots; g will be the next n slots,
    and the extra slot will be used to detect completion. */
    while (1) {
        
        /* First, check whether f and g have the desired property. */
        score = 1;
        for (i=0; i<n; i++) {
            if (f[f[f[i]]] != f[g[g[i]]]) {
                score = 0;
                break;
            }
        }
        total += (uint64_t) score;
        
        /* Now we increment the array. */
        f[0] += 1;
        i = 0;
        while ((i < nn) && (f[i] == n)) {
            f[i] = 0;
            f[i+1] += 1;
            i += 1;
        }
        if (f[nn] == 1) {
            /* If we get to this point, then we have run through all possible pairs of f and g. */
            break;
        }
        
        cycles += 1;
        if ((cycles % 1000000000) == 0) {
            for (i=0; i<80; i++) {printf("\b");}
            printf("%" PRIu64 "B / %" PRIu64 "B == %f%%", cycles/1000000000, totalcycles/1000000000,
                                                 100. * ((double) cycles) / ((double) totalcycles));
            fflush(stdout);
        }
    }
    return total;
}

int main() {
    uint64_t a;
    uint_fast8_t i, n;
    printf("0 1\n1 1\n");
    for (n=2; n<=8; n++) {
        a = A239778(n);
        for (i=0; i<42; i++) {printf("\b");}
        printf("%" PRIuFAST8 " %" PRIu64, n, a);
        for (i=0; i<42; i++) {printf(" ");}
        printf("\n");
    }
    printf("\n");
    return 0;
}
