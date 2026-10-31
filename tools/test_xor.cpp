#include <iostream>
#include <vector>
#include "experiments/harness/xorfilter_singleheader.h"

int main() {
    xor8_t filter8;
    std::vector<uint64_t> keys = {10, 20, 30, 40, 50, 100, 200, 300};
    if (!xor8_allocate(keys.size(), &filter8)) {
        std::cerr << "xor8_allocate failed\n";
        return 1;
    }
    if (!xor8_populate(keys.data(), keys.size(), &filter8)) {
        std::cerr << "xor8_populate failed\n";
        return 1;
    }
    std::cout << "xor8 contains 20: " << xor8_contain(20, &filter8) << "\n";
    std::cout << "xor8 contains 25: " << xor8_contain(25, &filter8) << "\n";
    std::cout << "xor8 size: " << xor8_size_in_bytes(&filter8) << " bytes\n";
    xor8_free(&filter8);

    xor16_t filter16;
    if (!xor16_allocate(keys.size(), &filter16)) {
        std::cerr << "xor16_allocate failed\n";
        return 1;
    }
    if (!xor16_populate(keys.data(), keys.size(), &filter16)) {
        std::cerr << "xor16_populate failed\n";
        return 1;
    }
    std::cout << "xor16 contains 20: " << xor16_contain(20, &filter16) << "\n";
    std::cout << "xor16 contains 25: " << xor16_contain(25, &filter16) << "\n";
    std::cout << "xor16 size: " << xor16_size_in_bytes(&filter16) << " bytes\n";
    xor16_free(&filter16);

    std::cout << "Xor filter test passed!\n";
    return 0;
}
