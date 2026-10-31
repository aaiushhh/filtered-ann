#pragma once

#include <vector>
#include <cstdint>
#include <cstring>
#include <cmath>
#include <memory>
#include <unordered_set>
#include <algorithm>

namespace filtered_ann {

// MurmurHash3 64-bit mixer
inline uint64_t hash64(uint64_t k) {
    k ^= k >> 33;
    k *= 0xff51afd7ed558ccdULL;
    k ^= k >> 33;
    k *= 0xc4ceb9fe1a85ec53ULL;
    k ^= k >> 33;
    return k;
}

// Kirsch-Mitzenmacher double hashing
inline void get_two_hashes(uint64_t val, uint64_t& h1, uint64_t& h2) {
    h1 = hash64(val ^ 0x517cc1b727220a95ULL);
    h2 = hash64(val ^ 0x9e3779b97f4a7c15ULL);
    if (h2 == 0) h2 = 1;
}

inline uint64_t splitmix64(uint64_t x) {
    x += 0x9e3779b97f4a7c15ULL;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    return x ^ (x >> 31);
}

// ============================================================================
// 1. Exact Filters
// ============================================================================

// N-bit Bitmap: 1 bit per vector ID
class BitmapFilter {
public:
    size_t num_bits;
    std::vector<uint64_t> words;

    BitmapFilter(size_t n = 0) : num_bits(n) {
        words.resize((n + 63) / 64, 0);
    }

    void set(uint32_t id) {
        if (id < num_bits) {
            words[id / 64] |= (1ULL << (id % 64));
        }
    }

    bool contains(uint32_t id) const {
        if (id >= num_bits) return false;
        return (words[id / 64] & (1ULL << (id % 64))) != 0;
    }

    size_t size_in_bytes() const {
        return words.size() * sizeof(uint64_t);
    }
};

// Exact Hash Set
class HashSetFilter {
public:
    std::unordered_set<uint32_t> ids;

    HashSetFilter() = default;

    void insert(uint32_t id) {
        ids.insert(id);
    }

    bool contains(uint32_t id) const {
        return ids.find(id) != ids.end();
    }

    size_t size_in_bytes() const {
        return ids.bucket_count() * sizeof(void*) + ids.size() * sizeof(uint32_t);
    }
};

// Open-addressing Hash Set with linear probing
class OpenAddressingHashSet {
public:
    static constexpr uint32_t EMPTY_KEY = 0xFFFFFFFF;
    size_t capacity;
    size_t mask;
    size_t count;
    std::vector<uint32_t> table;

    OpenAddressingHashSet(size_t max_items = 0) {
        init(max_items);
    }

    void init(size_t max_items) {
        count = 0;
        if (max_items == 0) {
            capacity = 16;
        } else {
            // Target load factor <= 0.70
            size_t cap = 16;
            while (cap * 0.70 < max_items) {
                cap <<= 1;
            }
            capacity = cap;
        }
        mask = capacity - 1;
        table.assign(capacity, EMPTY_KEY);
    }

    void insert(uint32_t val) {
        size_t idx = hash64(val) & mask;
        while (table[idx] != EMPTY_KEY) {
            if (table[idx] == val) return;
            idx = (idx + 1) & mask;
        }
        table[idx] = val;
        count++;
    }

    bool contains(uint32_t val) const {
        size_t idx = hash64(val) & mask;
        while (table[idx] != EMPTY_KEY) {
            if (table[idx] == val) return true;
            idx = (idx + 1) & mask;
        }
        return false;
    }

    size_t size_in_bytes() const {
        return table.size() * sizeof(uint32_t) + sizeof(OpenAddressingHashSet);
    }
};

// ============================================================================
// 2. Standard Bloom Filter
// ============================================================================

class BloomFilter {
public:
    size_t num_bits;
    size_t k_hashes;
    std::vector<uint64_t> words;

    BloomFilter(size_t n_elements = 0, double bits_per_entry = 8.0) {
        init(n_elements, bits_per_entry);
    }

    void init(size_t n_elements, double bits_per_entry) {
        num_bits = static_cast<size_t>(std::ceil(n_elements * bits_per_entry));
        if (num_bits < 64) num_bits = 64;
        words.assign((num_bits + 63) / 64, 0);
        // Optimal k = (m/n) * ln(2) = bits_per_entry * 0.693147
        k_hashes = static_cast<size_t>(std::round(bits_per_entry * 0.69314718056));
        if (k_hashes < 1) k_hashes = 1;
        if (k_hashes > 30) k_hashes = 30;
    }

    void insert(uint32_t val) {
        uint64_t h1, h2;
        get_two_hashes(val, h1, h2);
        for (size_t i = 0; i < k_hashes; ++i) {
            uint64_t bit_idx = (h1 + i * h2) % num_bits;
            words[bit_idx / 64] |= (1ULL << (bit_idx % 64));
        }
    }

    bool contains(uint32_t val) const {
        uint64_t h1, h2;
        get_two_hashes(val, h1, h2);
        for (size_t i = 0; i < k_hashes; ++i) {
            uint64_t bit_idx = (h1 + i * h2) % num_bits;
            if (!(words[bit_idx / 64] & (1ULL << (bit_idx % 64)))) {
                return false;
            }
        }
        return true;
    }

    size_t size_in_bytes() const {
        return words.size() * sizeof(uint64_t);
    }
};

// ============================================================================
// 3. Blocked Bloom Filter (512-bit / 64-byte Cache-Line Blocked)
// ============================================================================

struct alignas(64) Block512 {
    uint64_t words[8];
    Block512() {
        std::memset(words, 0, sizeof(words));
    }
};

class BlockedBloomFilter {
public:
    size_t num_blocks;
    size_t k_hashes;
    std::vector<Block512> blocks;

    BlockedBloomFilter(size_t n_elements = 0, double bits_per_entry = 8.0) {
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
        uint64_t h = splitmix64(static_cast<uint64_t>(val));
        size_t block_idx = h % num_blocks;
        Block512& blk = blocks[block_idx];
        uint64_t s = h;
        for (size_t i = 0; i < k_hashes; ++i) {
            s = splitmix64(s);
            uint64_t bit_in_block = s & 511ULL;
            blk.words[bit_in_block / 64] |= (1ULL << (bit_in_block % 64));
        }
    }

    bool contains(uint32_t val) const {
        uint64_t h = splitmix64(static_cast<uint64_t>(val));
        size_t block_idx = h % num_blocks;
        const Block512& blk = blocks[block_idx];
        uint64_t s = h;
        for (size_t i = 0; i < k_hashes; ++i) {
            s = splitmix64(s);
            uint64_t bit_in_block = s & 511ULL;
            if (!(blk.words[bit_in_block / 64] & (1ULL << (bit_in_block % 64)))) {
                return false;
            }
        }
        return true;
    }

    size_t size_in_bytes() const {
        return blocks.size() * sizeof(Block512);
    }
};

} // namespace filtered_ann
