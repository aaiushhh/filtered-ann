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
        uint64_t kick_rng = val ^ 0x9e3779b97f4a7c15ULL;
        size_t cur_i = (kick_rng & 1) ? i1 : i2;
        FingerprintType cur_fp = fp;

        for (size_t kick = 0; kick < MAX_KICKS; ++kick) {
            kick_rng ^= kick_rng << 13;
            kick_rng ^= kick_rng >> 7;
            kick_rng ^= kick_rng << 17;
            size_t slot = kick_rng % BUCKET_SIZE;
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

struct Bucket12 {
    uint8_t raw[6];
    Bucket12() {
        std::memset(raw, 0, 6);
    }
    uint16_t get_slot(size_t s) const {
        if (s == 0) return raw[0] | ((raw[1] & 0x0F) << 8);
        if (s == 1) return (raw[1] >> 4) | (raw[2] << 4);
        if (s == 2) return raw[3] | ((raw[4] & 0x0F) << 8);
        return (raw[4] >> 4) | (raw[5] << 4);
    }
    void set_slot(size_t s, uint16_t fp) {
        fp &= 0x0FFF;
        if (s == 0) {
            raw[0] = fp & 0xFF;
            raw[1] = (raw[1] & 0xF0) | ((fp >> 8) & 0x0F);
        } else if (s == 1) {
            raw[1] = (raw[1] & 0x0F) | ((fp & 0x0F) << 4);
            raw[2] = (fp >> 4) & 0xFF;
        } else if (s == 2) {
            raw[3] = fp & 0xFF;
            raw[4] = (raw[4] & 0xF0) | ((fp >> 8) & 0x0F);
        } else {
            raw[4] = (raw[4] & 0x0F) | ((fp & 0x0F) << 4);
            raw[5] = (fp >> 4) & 0xFF;
        }
    }
};

class CuckooFilter12 {
public:
    static constexpr size_t BUCKET_SIZE = 4;
    static constexpr size_t MAX_KICKS = 500;

    size_t num_buckets;
    size_t num_items;
    std::vector<Bucket12> table;

    CuckooFilter12(size_t max_items = 1000) {
        init(max_items);
    }

    void init(size_t max_items) {
        num_buckets = static_cast<size_t>(std::ceil(max_items / (BUCKET_SIZE * 0.95)));
        if (num_buckets == 0) num_buckets = 1;
        table.assign(num_buckets, Bucket12());
        num_items = 0;
    }

    uint16_t get_fingerprint(uint64_t hash_val) const {
        uint16_t fp = static_cast<uint16_t>(hash_val & 0x0FFF);
        if (fp == 0) fp = 1;
        return fp;
    }

    size_t alt_index(size_t i, uint16_t fp) const {
        uint64_t fp_hash = hash64(fp);
        return (i ^ fp_hash) % num_buckets;
    }

    bool insert(uint32_t val) {
        uint64_t h1 = hash64(val ^ 0xa5a5a5a5ULL);
        uint16_t fp = get_fingerprint(hash64(val ^ 0x5a5a5a5aULL));
        size_t i1 = h1 % num_buckets;
        size_t i2 = alt_index(i1, fp);

        for (size_t s = 0; s < BUCKET_SIZE; ++s) {
            if (table[i1].get_slot(s) == 0) {
                table[i1].set_slot(s, fp);
                num_items++;
                return true;
            }
        }
        for (size_t s = 0; s < BUCKET_SIZE; ++s) {
            if (table[i2].get_slot(s) == 0) {
                table[i2].set_slot(s, fp);
                num_items++;
                return true;
            }
        }

        uint64_t kick_rng = val ^ 0x9e3779b97f4a7c15ULL;
        size_t cur_i = (kick_rng & 1) ? i1 : i2;
        uint16_t cur_fp = fp;

        for (size_t kick = 0; kick < MAX_KICKS; ++kick) {
            kick_rng ^= kick_rng << 13;
            kick_rng ^= kick_rng >> 7;
            kick_rng ^= kick_rng << 17;
            size_t slot = kick_rng % BUCKET_SIZE;
            uint16_t kicked = table[cur_i].get_slot(slot);
            table[cur_i].set_slot(slot, cur_fp);
            cur_fp = kicked;
            cur_i = alt_index(cur_i, cur_fp);

            for (size_t s = 0; s < BUCKET_SIZE; ++s) {
                if (table[cur_i].get_slot(s) == 0) {
                    table[cur_i].set_slot(s, cur_fp);
                    num_items++;
                    return true;
                }
            }
        }
        return false;
    }

    bool contains(uint32_t val) const {
        uint64_t h1 = hash64(val ^ 0xa5a5a5a5ULL);
        uint16_t fp = get_fingerprint(hash64(val ^ 0x5a5a5a5aULL));
        size_t i1 = h1 % num_buckets;
        size_t i2 = alt_index(i1, fp);

        for (size_t s = 0; s < BUCKET_SIZE; ++s) {
            if (table[i1].get_slot(s) == fp) return true;
        }
        for (size_t s = 0; s < BUCKET_SIZE; ++s) {
            if (table[i2].get_slot(s) == fp) return true;
        }
        return false;
    }

    size_t size_in_bytes() const {
        return table.size() * sizeof(Bucket12);
    }
};

} // namespace filtered_ann
