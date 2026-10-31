#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int xor_cmpfunc(const void * a, const void * b) {
  return (int)( *(const uint64_t*)a - *(const uint64_t*)b );
}

int main() {
    uint64_t a = 0x100000000ULL;
    uint64_t b = 0ULL;
    printf("diff cast to int: %d\n", xor_cmpfunc(&a, &b));
    return 0;
}
