#define _GNU_SOURCE
#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <sstream>
#include <fstream>
#include <chrono>
#include <random>
#include <algorithm>
#include <cmath>
#include <cstring>
#include <iomanip>
#include <sched.h>
#include <unistd.h>

#include "filters.hpp"
#include "cuckoo_filter.hpp"
#include "xorfilter_singleheader.h"

using namespace filtered_ann;

inline double get_time_ns() {
    auto now = std::chrono::high_resolution_clock::now();
    return static_cast<double>(std::chrono::duration_cast<std::chrono::nanoseconds>(now.time_since_epoch()).count());
}

// Canary benchmark: bitmap, N=1e6, 10^7 uniform probes
inline double run_canary(const BitmapFilter& bm, size_t num_probes) {
    uint64_t rng = 123456789ULL;
    volatile uint64_t sum = 0;
    double t0 = get_time_ns();
    for (size_t i = 0; i < num_probes; ++i) {
        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
        sum += bm.contains(static_cast<uint32_t>(rng % 1000000));
    }
    double t1 = get_time_ns();
    return (t1 - t0) / num_probes;
}

struct StructConfig {
    std::string name;
    std::string variant;
    double bpe;
    int bits;
};

// Calculate median and IQR from vector of doubles
inline void get_median_iqr(std::vector<double> vals, double& median, double& iqr, double& min_v, double& max_v) {
    if (vals.empty()) {
        median = iqr = min_v = max_v = 0.0;
        return;
    }
    std::sort(vals.begin(), vals.end());
    size_t n = vals.size();
    min_v = vals.front();
    max_v = vals.back();
    if (n % 2 == 1) {
        median = vals[n / 2];
    } else {
        median = 0.5 * (vals[n / 2 - 1] + vals[n / 2]);
    }
    // Q1 and Q3
    double q1, q3;
    if (n == 5) {
        q1 = vals[1];
        q3 = vals[3];
    } else {
        size_t mid = n / 2;
        if (mid % 2 == 1) {
            q1 = vals[mid / 2];
            q3 = vals[n - 1 - (mid / 2)];
        } else {
            q1 = 0.5 * (vals[mid / 2 - 1] + vals[mid / 2]);
            q3 = 0.5 * (vals[n - mid + (mid / 2) - 1] + vals[n - mid + (mid / 2)]);
        }
    }
    iqr = q3 - q1;
}

int main(int argc, char** argv) {
    int pin_cpu = 0; // default P-core 0
    if (argc > 1) {
        pin_cpu = std::atoi(argv[1]);
    }
    if (pin_cpu >= 0) {
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(pin_cpu, &cpuset);
        if (sched_setaffinity(0, sizeof(cpuset), &cpuset) != 0) {
            std::cerr << "[E1b] Warning: sched_setaffinity to CPU " << pin_cpu << " failed\n";
        } else {
            std::cout << "[E1b] Pinned process to CPU " << pin_cpu << "\n";
        }
    }

    const size_t NUM_PROBES = 10000000;
    const size_t RAM_50PCT_LIMIT = 3977804000ULL; // ~3.79 GB

    // Canary baseline setup
    BitmapFilter canary_bm(1000000);
    for (size_t i = 0; i < 1000000; i += 2) canary_bm.set(i);

    // Warm up canary
    run_canary(canary_bm, 1000000);

    // Output files
    std::string dir = "experiments/results/E1b";
    std::ofstream f_raw(dir + "/raw_e1b.csv");
    f_raw << "run_id,cell_id,repeat,N,sigma,structure,variant,probe_pattern,ns_per_probe,measured_fpr,theoretical_fpr,memory_bytes,build_time_s,canary_before_ns,canary_after_ns,canary_diff_pct,flagged,rerun\n";

    std::ofstream f_summary(dir + "/summary_e1b.csv");
    f_summary << "cell_id,N,sigma,structure,variant,probe_pattern,median_ns,iqr_ns,min_ns,max_ns,measured_fpr,theoretical_fpr,memory_bytes,build_time_s,flagged_rerun\n";

    std::ofstream f_canary(dir + "/canary_log_e1b.csv");
    f_canary << "cell_id,run_type,N,sigma,structure,variant,canary_before_ns,canary_after_ns,diff_pct,flagged\n";

    std::ofstream f_skip(dir + "/skip_list_e1b.csv");
    f_skip << "N,sigma,structure,variant,est_memory_bytes,limit_bytes,reason\n";

    std::vector<uint32_t> N_values = {10000000, 100000000, 1000000000};
    std::vector<double> sigma_values = {0.001, 0.01};

    std::vector<StructConfig> base_configs = {
        {"bitmap", "1-bit", 1.0, 1},
        {"hash_set", "open_addressing", 64.0, 64},
        {"bloom_standard", "b10", 10.0, 10},
        {"bloom_blocked", "b10", 10.0, 10},
        {"cuckoo", "12bit", 12.0, 12},
        {"cuckoo", "16bit", 16.0, 16},
        {"xor", "8bit", 8.0, 8},
        {"xor", "16bit", 16.0, 16}
    };

    std::cout << "[E1b] Starting Reduced Grid Benchmarks (N in {1e7, 1e8, 1e9}, sigma in {0.001, 0.01}, 8 structures)...\n";

    std::mt19937 g(12345);
    int cell_id = 0;

    for (uint32_t N : N_values) {
        for (double sigma : sigma_values) {
            uint32_t n_members = static_cast<uint32_t>(std::round(N * sigma));
            if (n_members < 1) n_members = 1;

            // Randomized order across structures
            std::vector<StructConfig> configs = base_configs;
            std::shuffle(configs.begin(), configs.end(), g);

            for (const auto& cfg : configs) {
                cell_id++;

                // Skip check
                size_t est_bytes = 0;
                size_t est_build_peak = 0;
                if (cfg.name == "bitmap") {
                    est_bytes = (N + 63) / 8;
                    est_build_peak = est_bytes;
                } else if (cfg.name == "hash_set") {
                    size_t cap = 16;
                    while (cap * 0.70 < n_members) cap <<= 1;
                    est_bytes = cap * sizeof(uint32_t) + sizeof(OpenAddressingHashSet);
                    est_build_peak = est_bytes;
                } else if (cfg.name == "bloom_standard") {
                    est_bytes = (static_cast<size_t>(std::ceil(n_members * cfg.bpe)) + 63) / 8;
                    est_build_peak = est_bytes;
                } else if (cfg.name == "bloom_blocked") {
                    size_t total_bits = static_cast<size_t>(std::ceil(n_members * cfg.bpe));
                    size_t blocks = (total_bits + 511) / 512;
                    est_bytes = blocks * 64;
                    est_build_peak = est_bytes;
                } else if (cfg.name == "cuckoo") {
                    size_t num_buckets = static_cast<size_t>(std::ceil(n_members / (4.0 * 0.95)));
                    size_t b_size = (cfg.bits == 12) ? 6 : 8;
                    est_bytes = num_buckets * b_size;
                    est_build_peak = est_bytes;
                } else if (cfg.name == "xor") {
                    size_t capacity = (size_t)(32 + 1.23 * n_members);
                    capacity = capacity / 3 * 3;
                    est_bytes = capacity * (cfg.bits / 8) + 64;
                    est_build_peak = est_bytes + capacity * 32 + static_cast<size_t>(n_members) * 8;
                }

                if (est_bytes > RAM_50PCT_LIMIT || est_build_peak > RAM_50PCT_LIMIT) {
                    std::string reason = (est_bytes > RAM_50PCT_LIMIT) ? 
                        "Structure memory (" + std::to_string(est_bytes / 1000000) + " MB) exceeds 50% RAM limit (3790 MB)" :
                        "Build peak memory (" + std::to_string(est_build_peak / 1000000) + " MB) exceeds 50% RAM limit (3790 MB)";
                    f_skip << N << "," << sigma << "," << cfg.name << "," << cfg.variant << ","
                           << est_bytes << "," << RAM_50PCT_LIMIT << ",\"" << reason << "\"\n";
                    f_skip.flush();
                    std::cout << "[E1b SKIP] Cell " << cell_id << " N=" << N << ", sigma=" << sigma << ", " << cfg.name << " (" << cfg.variant << "): " << reason << "\n";
                    continue;
                }

                // Execute cell with optional rerun if canary drifts >5%
                bool do_rerun = false;
                for (int run_attempt = 0; run_attempt < 2; ++run_attempt) {
                    bool is_rerun = (run_attempt > 0);

                    // Canary BEFORE
                    double canary_before_ns = run_canary(canary_bm, NUM_PROBES);

                    // Build Structure
                    BitmapFilter bm;
                    OpenAddressingHashSet oahs;
                    BloomFilter bf;
                    BlockedBloomFilter bbf;
                    CuckooFilter12 cf12;
                    CuckooFilter16 cf16;
                    xor8_t xf8;
                    xor16_t xf16;
                    std::vector<uint64_t> xor_keys;

                    if (cfg.name == "xor") {
                        xor_keys.resize(n_members);
                        uint64_t k_rng = 42 + cell_id;
                        for (uint32_t i = 0; i < n_members; ++i) {
                            k_rng ^= k_rng << 13; k_rng ^= k_rng >> 7; k_rng ^= k_rng << 17;
                            xor_keys[i] = (static_cast<uint64_t>(i) * (N / n_members)) + (k_rng % (N / n_members));
                        }
                    }

                    size_t exact_bytes = 0;
                    double theoretical_fpr = 0.0;
                    double t_b0 = get_time_ns();

                    if (cfg.name == "bitmap") {
                        bm = BitmapFilter(N);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                            bm.set(id);
                        }
                        exact_bytes = bm.size_in_bytes();
                    } else if (cfg.name == "hash_set") {
                        oahs = OpenAddressingHashSet(n_members);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                            oahs.insert(id);
                        }
                        exact_bytes = oahs.size_in_bytes();
                    } else if (cfg.name == "bloom_standard") {
                        bf = BloomFilter(n_members, cfg.bpe);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                            bf.insert(id);
                        }
                        exact_bytes = bf.size_in_bytes();
                        size_t k = bf.k_hashes;
                        theoretical_fpr = std::pow(1.0 - std::exp(-static_cast<double>(k) / cfg.bpe), k);
                    } else if (cfg.name == "bloom_blocked") {
                        bbf = BlockedBloomFilter(n_members, cfg.bpe);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                            bbf.insert(id);
                        }
                        exact_bytes = bbf.size_in_bytes();
                        size_t k = bbf.k_hashes;
                        theoretical_fpr = std::pow(1.0 - std::exp(-static_cast<double>(k) / cfg.bpe), k);
                    } else if (cfg.name == "cuckoo") {
                        if (cfg.bits == 12) {
                            cf12 = CuckooFilter12(n_members);
                            for (uint32_t i = 0; i < n_members; ++i) {
                                uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                                cf12.insert(id);
                            }
                            exact_bytes = cf12.size_in_bytes();
                            theoretical_fpr = 8.0 * std::pow(2.0, -12.0);
                        } else {
                            cf16 = CuckooFilter16(n_members);
                            for (uint32_t i = 0; i < n_members; ++i) {
                                uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                                cf16.insert(id);
                            }
                            exact_bytes = cf16.size_in_bytes();
                            theoretical_fpr = 8.0 * std::pow(2.0, -16.0);
                        }
                    } else if (cfg.name == "xor") {
                        if (cfg.bits == 8) {
                            xor8_allocate(n_members, &xf8);
                            xor8_populate(xor_keys.data(), n_members, &xf8);
                            exact_bytes = xor8_size_in_bytes(&xf8);
                            theoretical_fpr = std::pow(2.0, -8.0);
                        } else {
                            xor16_allocate(n_members, &xf16);
                            xor16_populate(xor_keys.data(), n_members, &xf16);
                            exact_bytes = xor16_size_in_bytes(&xf16);
                            theoretical_fpr = std::pow(2.0, -16.0);
                        }
                    }

                    double t_b1 = get_time_ns();
                    double build_time_s = (t_b1 - t_b0) / 1e9;

                    // Lambda to execute probe pattern
                    auto run_probe = [&](const std::string& pattern, uint64_t seed_val) -> double {
                        uint64_t rng = seed_val;
                        volatile uint64_t sum = 0;
                        double t0 = get_time_ns();

                        if (pattern == "uniform_random") {
                            if (cfg.name == "bitmap") {
                                for (size_t p = 0; p < NUM_PROBES; ++p) {
                                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                    sum += bm.contains(rng % N);
                                }
                            } else if (cfg.name == "hash_set") {
                                for (size_t p = 0; p < NUM_PROBES; ++p) {
                                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                    sum += oahs.contains(rng % N);
                                }
                            } else if (cfg.name == "bloom_standard") {
                                for (size_t p = 0; p < NUM_PROBES; ++p) {
                                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                    sum += bf.contains(rng % N);
                                }
                            } else if (cfg.name == "bloom_blocked") {
                                for (size_t p = 0; p < NUM_PROBES; ++p) {
                                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                    sum += bbf.contains(rng % N);
                                }
                            } else if (cfg.name == "cuckoo") {
                                if (cfg.bits == 12) {
                                    for (size_t p = 0; p < NUM_PROBES; ++p) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        sum += cf12.contains(rng % N);
                                    }
                                } else {
                                    for (size_t p = 0; p < NUM_PROBES; ++p) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        sum += cf16.contains(rng % N);
                                    }
                                }
                            } else if (cfg.name == "xor") {
                                if (cfg.bits == 8) {
                                    for (size_t p = 0; p < NUM_PROBES; ++p) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        sum += xor8_contain(rng % N, &xf8);
                                    }
                                } else {
                                    for (size_t p = 0; p < NUM_PROBES; ++p) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        sum += xor16_contain(rng % N, &xf16);
                                    }
                                }
                            }
                        } else if (pattern == "neighbor_list_32") {
                            size_t batches = NUM_PROBES / 32;
                            uint32_t ids[32];
                            if (cfg.name == "bitmap") {
                                for (size_t b = 0; b < batches; ++b) {
                                    for (int j = 0; j < 32; ++j) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        ids[j] = rng % N;
                                    }
                                    for (int j = 0; j < 32; ++j) sum += bm.contains(ids[j]);
                                }
                            } else if (cfg.name == "hash_set") {
                                for (size_t b = 0; b < batches; ++b) {
                                    for (int j = 0; j < 32; ++j) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        ids[j] = rng % N;
                                    }
                                    for (int j = 0; j < 32; ++j) sum += oahs.contains(ids[j]);
                                }
                            } else if (cfg.name == "bloom_standard") {
                                for (size_t b = 0; b < batches; ++b) {
                                    for (int j = 0; j < 32; ++j) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        ids[j] = rng % N;
                                    }
                                    for (int j = 0; j < 32; ++j) sum += bf.contains(ids[j]);
                                }
                            } else if (cfg.name == "bloom_blocked") {
                                for (size_t b = 0; b < batches; ++b) {
                                    for (int j = 0; j < 32; ++j) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        ids[j] = rng % N;
                                    }
                                    for (int j = 0; j < 32; ++j) sum += bbf.contains(ids[j]);
                                }
                            } else if (cfg.name == "cuckoo") {
                                if (cfg.bits == 12) {
                                    for (size_t b = 0; b < batches; ++b) {
                                        for (int j = 0; j < 32; ++j) {
                                            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                            ids[j] = rng % N;
                                        }
                                        for (int j = 0; j < 32; ++j) sum += cf12.contains(ids[j]);
                                    }
                                } else {
                                    for (size_t b = 0; b < batches; ++b) {
                                        for (int j = 0; j < 32; ++j) {
                                            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                            ids[j] = rng % N;
                                        }
                                        for (int j = 0; j < 32; ++j) sum += cf16.contains(ids[j]);
                                    }
                                }
                            } else if (cfg.name == "xor") {
                                if (cfg.bits == 8) {
                                    for (size_t b = 0; b < batches; ++b) {
                                        for (int j = 0; j < 32; ++j) {
                                            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                            ids[j] = rng % N;
                                        }
                                        for (int j = 0; j < 32; ++j) sum += xor8_contain(ids[j], &xf8);
                                    }
                                } else {
                                    for (size_t b = 0; b < batches; ++b) {
                                        for (int j = 0; j < 32; ++j) {
                                            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                            ids[j] = rng % N;
                                        }
                                        for (int j = 0; j < 32; ++j) sum += xor16_contain(ids[j], &xf16);
                                    }
                                }
                            }
                        } else if (pattern == "sequential_32") {
                            size_t batches = NUM_PROBES / 32;
                            uint32_t limit = (N >= 32) ? (N - 32) : 1;
                            if (cfg.name == "bitmap") {
                                for (size_t b = 0; b < batches; ++b) {
                                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                    uint32_t base_id = rng % limit;
                                    for (int j = 0; j < 32; ++j) sum += bm.contains(base_id + j);
                                }
                            } else if (cfg.name == "hash_set") {
                                for (size_t b = 0; b < batches; ++b) {
                                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                    uint32_t base_id = rng % limit;
                                    for (int j = 0; j < 32; ++j) sum += oahs.contains(base_id + j);
                                }
                            } else if (cfg.name == "bloom_standard") {
                                for (size_t b = 0; b < batches; ++b) {
                                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                    uint32_t base_id = rng % limit;
                                    for (int j = 0; j < 32; ++j) sum += bf.contains(base_id + j);
                                }
                            } else if (cfg.name == "bloom_blocked") {
                                for (size_t b = 0; b < batches; ++b) {
                                    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                    uint32_t base_id = rng % limit;
                                    for (int j = 0; j < 32; ++j) sum += bbf.contains(base_id + j);
                                }
                            } else if (cfg.name == "cuckoo") {
                                if (cfg.bits == 12) {
                                    for (size_t b = 0; b < batches; ++b) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        uint32_t base_id = rng % limit;
                                        for (int j = 0; j < 32; ++j) sum += cf12.contains(base_id + j);
                                    }
                                } else {
                                    for (size_t b = 0; b < batches; ++b) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        uint32_t base_id = rng % limit;
                                        for (int j = 0; j < 32; ++j) sum += cf16.contains(base_id + j);
                                    }
                                }
                            } else if (cfg.name == "xor") {
                                if (cfg.bits == 8) {
                                    for (size_t b = 0; b < batches; ++b) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        uint32_t base_id = rng % limit;
                                        for (int j = 0; j < 32; ++j) sum += xor8_contain(base_id + j, &xf8);
                                    }
                                } else {
                                    for (size_t b = 0; b < batches; ++b) {
                                        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                        uint32_t base_id = rng % limit;
                                        for (int j = 0; j < 32; ++j) sum += xor16_contain(base_id + j, &xf16);
                                    }
                                }
                            }
                        }
                        double t1 = get_time_ns();
                        return (t1 - t0) / NUM_PROBES;
                    };

                    // Measure empirical FPR
                    double measured_fpr = 0.0;
                    if (cfg.name == "bitmap" || cfg.name == "hash_set") {
                        measured_fpr = 0.0;
                    } else {
                        size_t fp_count = 0;
                        uint32_t base_nm = N + 1000;
                        if (cfg.name == "bloom_standard") {
                            for (size_t i = 0; i < NUM_PROBES; ++i) fp_count += bf.contains(base_nm + i);
                        } else if (cfg.name == "bloom_blocked") {
                            for (size_t i = 0; i < NUM_PROBES; ++i) fp_count += bbf.contains(base_nm + i);
                        } else if (cfg.name == "cuckoo") {
                            if (cfg.bits == 12) {
                                for (size_t i = 0; i < NUM_PROBES; ++i) fp_count += cf12.contains(base_nm + i);
                            } else {
                                for (size_t i = 0; i < NUM_PROBES; ++i) fp_count += cf16.contains(base_nm + i);
                            }
                        } else if (cfg.name == "xor") {
                            if (cfg.bits == 8) {
                                for (size_t i = 0; i < NUM_PROBES; ++i) fp_count += xor8_contain(base_nm + i, &xf8);
                            } else {
                                for (size_t i = 0; i < NUM_PROBES; ++i) fp_count += xor16_contain(base_nm + i, &xf16);
                            }
                        }
                        measured_fpr = static_cast<double>(fp_count) / NUM_PROBES;
                    }

                    // 1 Warmup + 5 Measured Repeats for each pattern
                    std::vector<std::string> patterns = {"uniform_random", "neighbor_list_32", "sequential_32"};
                    std::map<std::string, std::vector<double>> pattern_runs;

                    for (const auto& pat : patterns) {
                        // 1 Warmup (discarded)
                        run_probe(pat, 1111111ULL + cell_id);

                        // 5 Measured repeats
                        for (int r = 1; r <= 5; ++r) {
                            double ns = run_probe(pat, 9876543210ULL + cell_id * 100 + r * 7);
                            pattern_runs[pat].push_back(ns);
                        }
                    }

                    // Cleanup Xor filter memory
                    if (cfg.name == "xor") {
                        if (cfg.bits == 8) xor8_free(&xf8);
                        else xor16_free(&xf16);
                    }

                    // Canary AFTER
                    double canary_after_ns = run_canary(canary_bm, NUM_PROBES);
                    double canary_diff_pct = std::abs(canary_after_ns - canary_before_ns) / canary_before_ns * 100.0;
                    bool flagged = (canary_diff_pct > 5.0);

                    // Log Canary
                    f_canary << cell_id << "," << (is_rerun ? "RERUN" : "PRIMARY") << ","
                             << N << "," << sigma << "," << cfg.name << "," << cfg.variant << ","
                             << canary_before_ns << "," << canary_after_ns << ","
                             << canary_diff_pct << "," << (flagged ? "TRUE" : "FALSE") << "\n";
                    f_canary.flush();

                    // Log Raw Rows (5 repeats x 3 patterns = 15 rows)
                    for (const auto& pat : patterns) {
                        for (int r = 1; r <= 5; ++r) {
                            std::string run_id = "run_E1b_" + std::to_string(cell_id) + "_" + pat + "_r" + std::to_string(r) + (is_rerun ? "_rerun" : "");
                            f_raw << run_id << "," << cell_id << "," << r << "," << N << "," << sigma << ","
                                  << cfg.name << "," << cfg.variant << "," << pat << ","
                                  << pattern_runs[pat][r - 1] << "," << measured_fpr << "," << theoretical_fpr << ","
                                  << exact_bytes << "," << build_time_s << ","
                                  << canary_before_ns << "," << canary_after_ns << ","
                                  << canary_diff_pct << "," << (flagged ? "TRUE" : "FALSE") << ","
                                  << (is_rerun ? "TRUE" : "FALSE") << "\n";
                        }
                    }
                    f_raw.flush();

                    // Summary statistics (median and IQR)
                    for (const auto& pat : patterns) {
                        double med, iqr, min_v, max_v;
                        get_median_iqr(pattern_runs[pat], med, iqr, min_v, max_v);
                        f_summary << cell_id << "," << N << "," << sigma << "," << cfg.name << "," << cfg.variant << ","
                                  << pat << "," << med << "," << iqr << "," << min_v << "," << max_v << ","
                                  << measured_fpr << "," << theoretical_fpr << "," << exact_bytes << ","
                                  << build_time_s << "," << (flagged ? "TRUE" : "FALSE") << "\n";
                    }
                    f_summary.flush();

                    std::cout << "[E1b CELL " << cell_id << (is_rerun ? " RERUN" : "") << "] N=" << N << ", sigma=" << sigma
                              << ", " << cfg.name << " (" << cfg.variant << "): "
                              << "uniform=" << pattern_runs["uniform_random"][2] << " ns, "
                              << "neighbor=" << pattern_runs["neighbor_list_32"][2] << " ns, "
                              << "seq=" << pattern_runs["sequential_32"][2] << " ns, "
                              << "FPR=" << measured_fpr << ", canary_diff=" << std::fixed << std::setprecision(2) << canary_diff_pct << "%"
                              << (flagged ? " [FLAGGED]" : "") << "\n";

                    // Check if rerun required
                    if (flagged && !is_rerun) {
                        std::cout << ">>> Flagged canary drift >5.0% (" << canary_diff_pct << "%), running rerun for cell " << cell_id << "...\n";
                        continue; // runs run_attempt = 1
                    } else {
                        break; // proceed to next cell
                    }
                }
            }
        }
    }

    std::cout << "[E1b] Reduced grid benchmarks complete.\n";
    return 0;
}
