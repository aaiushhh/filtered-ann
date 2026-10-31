#include <iostream>
#include <vector>
#include <cmath>
#include <cstdint>
#include <iomanip>

inline uint64_t hash64(uint64_t k) {
    k ^= k >> 33;
    k *= 0xff51afd7ed558ccdULL;
    k ^= k >> 33;
    k *= 0xc4ceb9fe1a85ec53ULL;
    k ^= k >> 33;
    return k;
}

struct Block512 {
    uint64_t words[8];
    Block512() { for (int i = 0; i < 8; ++i) words[i] = 0; }
};

class BlockedBloomFilterFixed {
public:
    size_t num_blocks;
    size_t k_hashes;
    std::vector<Block512> blocks;

    BlockedBloomFilterFixed(size_t n_elements = 0, double bits_per_entry = 8.0) {
        init(n_elements, bits_per_entry);
    }

    void init(size_t n_elements, double bits_per_entry) {
        size_t total_bits = static_cast<size_t>(std::ceil(n_elements * bits_per_entry));
        num_blocks = (total_bits + 511) / 512;
        if (num_blocks == 0) num_blocks = 1;
        blocks.assign(num_blocks, Block512());
        k_hashes = static_cast<size_t>(std::round(bits_per_entry * 0.69314718056));
        if (k_hashes < 1) k_hashes = 1;
        if (k_hashes > 16) k_hashes = 16;
    }

    void insert(uint32_t val) {
        uint64_t h1 = hash64(val ^ 0x517cc1b727220a95ULL);
        uint64_t h2 = hash64(val ^ 0x9e3779b97f4a7c15ULL);
        uint64_t h3 = hash64(val ^ 0xbf58476d1ce4e5b9ULL) | 1ULL;
        size_t block_idx = h1 % num_blocks;
        Block512& blk = blocks[block_idx];
        for (size_t i = 0; i < k_hashes; ++i) {
            uint64_t bit_in_block = (h2 + i * h3) & 511;
            blk.words[bit_in_block / 64] |= (1ULL << (bit_in_block % 64));
        }
    }

    bool contains(uint32_t val) const {
        uint64_t h1 = hash64(val ^ 0x517cc1b727220a95ULL);
        uint64_t h2 = hash64(val ^ 0x9e3779b97f4a7c15ULL);
        uint64_t h3 = hash64(val ^ 0xbf58476d1ce4e5b9ULL) | 1ULL;
        size_t block_idx = h1 % num_blocks;
        const Block512& blk = blocks[block_idx];
        for (size_t i = 0; i < k_hashes; ++i) {
            uint64_t bit_in_block = (h2 + i * h3) & 511;
            if (!(blk.words[bit_in_block / 64] & (1ULL << (bit_in_block % 64)))) {
                return false;
            }
        }
        return true;
    }
};

int main() {
    std::cout << "Testing BlockedBloomFilterFixed...\n";
    size_t n_members = 1000000;
    size_t n_queries = 10000000;

    for (double bpe : {6.0, 8.0, 10.0, 12.0, 16.0}) {
        BlockedBloomFilterFixed bbf(n_members, bpe);
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

        std::cout << "b=" << bpe << ", k=" << k
                  << " | Standard FPR: " << std::fixed << std::setprecision(6) << std_fpr
                  << " | Measured FPR: " << measured_fpr
                  << " | Ratio: " << std::setprecision(2) << ratio << "x"
                  << " | Within 3x: " << (ratio <= 3.0 ? "PASS" : "FAIL") << "\n";
    }
    return 0;
}
