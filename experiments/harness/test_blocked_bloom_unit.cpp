#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <cassert>
#include "filters.hpp"

using namespace filtered_ann;

int main() {
    std::cout << "=== UNIT TEST: Blocked Bloom Filter FPR Verification ===\n";
    size_t n_members = 1000000;
    size_t n_queries = 10000000;

    bool all_passed = true;

    for (double bpe : {6.0, 8.0, 10.0, 12.0, 16.0}) {
        BlockedBloomFilter bbf(n_members, bpe);
        for (size_t i = 0; i < n_members; ++i) {
            bbf.insert(static_cast<uint32_t>(i));
        }

        size_t fp = 0;
        for (size_t i = 0; i < n_queries; ++i) {
            uint32_t query_id = static_cast<uint32_t>(n_members + 1 + i);
            if (bbf.contains(query_id)) {
                fp++;
            }
        }
        double measured_fpr = static_cast<double>(fp) / n_queries;
        size_t k = bbf.k_hashes;
        double std_fpr = std::pow(1.0 - std::exp(-static_cast<double>(k) / bpe), k);
        double ratio = measured_fpr / std_fpr;
        bool pass = (ratio <= 3.0);
        if (!pass) all_passed = false;

        std::cout << "b=" << std::setw(2) << static_cast<int>(bpe)
                  << ", k=" << std::setw(2) << k
                  << " | Standard Formula FPR: " << std::fixed << std::setprecision(6) << std_fpr
                  << " | Measured FPR: " << measured_fpr
                  << " | Ratio: " << std::setprecision(2) << ratio << "x"
                  << " | Status: " << (pass ? "PASS (<= 3x)" : "FAIL (> 3x)") << "\n";
    }

    if (all_passed) {
        std::cout << "ALL UNIT TESTS PASSED: FPR at b=10 and b=16 are strictly within 3x of standard formula.\n";
        return 0;
    } else {
        std::cerr << "UNIT TEST FAILED.\n";
        return 1;
    }
}
