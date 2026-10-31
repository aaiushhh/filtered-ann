#pragma once

#include <vector>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include "filters.hpp"

namespace filtered_ann {

template <typename FingerprintType>
class CuckooFilter {
public:
    static constexpr size_t BUCKET_SIZE = 4;
    static constexpr size_t MAX_KICKS = 500;

    struct Bucket {
        FingerprintType slots[BUCKET_SIZE];
        Bucket() {
            std::memset(slots, 0, sizeof(slots));
        }
    };

    size_t num_buckets;
    size_t num_items;
    std::vector<Bucket> table;

    CuckooFilter(size_t max_items = 1000) {
        init(max_items);
    }

    void init(size_t max_items) {
        // Load factor around 0.95, 4 slots per bucket
        num_buckets = static_cast<size_t>(std::ceil(max_items / (BUCKET_SIZE * 0.95)));
        if (num_buckets == 0) num_buckets = 1;
        table.assign(num_buckets, Bucket());
        num_items = 0;
    }

    FingerprintType get_fingerprint(uint64_t hash_val) const {
        FingerprintType fp = static_cast<FingerprintType>(hash_val);
        if (fp == 0) fp = 1; // 0 indicates empty
        return fp;
    }

    size_t alt_index(size_t i, FingerprintType fp) const {
        uint64_t fp_hash = hash64(fp);
        return (i ^ fp_hash) % num_buckets;
    }

    bool insert(uint32_t val) {
        uint64_t h1 = hash64(val ^ 0xa5a5a5a5ULL);
        FingerprintType fp = get_fingerprint(hash64(val ^ 0x5a5a5a5aULL));
        size_t i1 = h1 % num_buckets;
        size_t i2 = alt_index(i1, fp);

        // Try bucket 1
        for (size_t s = 0; s < BUCKET_SIZE; ++s) {
            if (table[i1].slots[s] == 0) {
                table[i1].slots[s] = fp;
                num_items++;
                return true;
            }
        }
        // Try bucket 2
        for (size_t s = 0; s < BUCKET_SIZE; ++s) {
            if (table[i2].slots[s] == 0) {
                table[i2].slots[s] = fp;
                num_items++;
                return true;
            }
        }

        // Must kick a victim
        size_t cur_i = (rand() % 2 == 0) ? i1 : i2;
        FingerprintType cur_fp = fp;

        for (size_t kick = 0; kick < MAX_KICKS; ++kick) {
            size_t slot = rand() % BUCKET_SIZE;
            std::swap(cur_fp, table[cur_i].slots[slot]);
            cur_i = alt_index(cur_i, cur_fp);

            for (size_t s = 0; s < BUCKET_SIZE; ++s) {
                if (table[cur_i].slots[s] == 0) {
                    table[cur_i].slots[s] = cur_fp;
                    num_items++;
                    return true;
                }
            }
        }

        // Table full (unlikely if capacity is correctly sized)
        return false;
    }

    bool contains(uint32_t val) const {
        uint64_t h1 = hash64(val ^ 0xa5a5a5a5ULL);
        FingerprintType fp = get_fingerprint(hash64(val ^ 0x5a5a5a5aULL));
        size_t i1 = h1 % num_buckets;
        size_t i2 = alt_index(i1, fp);

        for (size_t s = 0; s < BUCKET_SIZE; ++s) {
            if (table[i1].slots[s] == fp) return true;
        }
        for (size_t s = 0; s < BUCKET_SIZE; ++s) {
            if (table[i2].slots[s] == fp) return true;
        }
        return false;
    }

    size_t size_in_bytes() const {
        return table.size() * sizeof(Bucket);
    }
};

using CuckooFilter8 = CuckooFilter<uint8_t>;
using CuckooFilter16 = CuckooFilter<uint16_t>;

} // namespace filtered_ann
