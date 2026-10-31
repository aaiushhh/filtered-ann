#include <iostream>
#include <vector>
#include <cmath>
#include <cstdint>
#include <iomanip>

inline uint64_t splitmix64(uint64_t x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

struct Block512 {
    uint64_t words[8];
    Block512() { for (int i = 0; i < 8; ++i) words[i] = 0; }
};

int main() {
    size_t n_members = 1000000;
    size_t n_queries = 10000000;
    double bpe = 16.0;

    for (int k_test : {7, 8, 9, 10, 11}) {
        size_t total_bits = static_cast<size_t>(std::ceil(n_members * bpe));
        size_t num_blocks = (total_bits + 511) / 512;
        std::vector<Block512> blocks(num_blocks);

        for (size_t i = 0; i < n_members; ++i) {
            uint64_t h = splitmix64(i);
            size_t block_idx = h % num_blocks;
            uint64_t h2 = splitmix64(h);
            uint64_t h3 = splitmix64(h2) | 1ULL;
            Block512& blk = blocks[block_idx];
            for (int k = 0; k < k_test; ++k) {
                uint64_t bit = (h2 + k * h3) & 511;
                blk.words[bit / 64] |= (1ULL << (bit % 64));
            }
        }

        size_t fp = 0;
        for (size_t i = 0; i < n_queries; ++i) {
            uint64_t q = n_members + 1 + i;
            uint64_t h = splitmix64(q);
            size_t block_idx = h % num_blocks;
            uint64_t h2 = splitmix64(h);
            uint64_t h3 = splitmix64(h2) | 1ULL;
            const Block512& blk = blocks[block_idx];
            bool match = true;
            for (int k = 0; k < k_test; ++k) {
                uint64_t bit = (h2 + k * h3) & 511;
                if (!(blk.words[bit / 64] & (1ULL << (bit % 64)))) {
                    match = false;
                    break;
                }
            }
            if (match) fp++;
        }

        double measured_fpr = static_cast<double>(fp) / n_queries;
        double std_fpr = std::pow(1.0 - std::exp(-static_cast<double>(k_test) / bpe), k_test);
        std::cout << "k=" << k_test << " | Std FPR: " << std_fpr
                  << " | Measured: " << measured_fpr
                  << " | Ratio: " << (measured_fpr / std_fpr) << "x\n";
    }
    return 0;
}
