#include <stdio.h>

const unsigned MAX_INT = 32768;

unsigned calculate_f_4_1(unsigned n) {
    unsigned cache[MAX_INT];
    
    cache[0] = ((n + 1) * (n + 1) + n) % MAX_INT;

    for(unsigned i = 1; i < MAX_INT; i++) {
        cache[i] = ((2 + cache[i - 1]) * (n + 1) - 1) % MAX_INT;
    }

    return cache[cache[n]];
}

int main() {
    for(unsigned n = 0; n < MAX_INT; n++) {
        if (calculate_f_4_1(n) == 6) {
            printf("The result: %d\n", n);
            return 0;
        }
    }

    printf("The result not found");
    return -1;
}
