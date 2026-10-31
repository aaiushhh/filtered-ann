#define _GNU_SOURCE
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <chrono>
#include <cmath>
#include <sched.h>
#include <pthread.h>
#include <unistd.h>
#include <iomanip>
#include <cstring>
#include <algorithm>
#include <cstdint>

#include "experiments/harness/filters.hpp"
#include "experiments/harness/cuckoo_filter.hpp"
#include "experiments/harness/xorfilter_singleheader.h"

using namespace filtered_ann;

// 50% of 7.6 GB RAM threshold in bytes
static constexpr size_t RAM_50PCT_LIMIT = 3977804000ULL; // ~3.79 GB

// Timer clock helper
inline double get_time_ns() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC_RAW, &ts);
    return ts.tv_sec * 1e9 + ts.tv_nsec;
}

// Canary benchmark runner: Bitmap, N=1e6, 10^7 uniform random probes
double run_canary(const BitmapFilter& canary_bm, size_t num_probes = 10000000) {
    uint64_t rng = 123456789012345ULL;
    volatile uint64_t dummy = 0;
    uint64_t sum = 0;

    double t0 = get_time_ns();
    for (size_t i = 0; i < num_probes; ++i) {
        rng ^= rng << 13;
        rng ^= rng >> 7;
        rng ^= rng << 17;
        uint32_t probe_id = rng % 1000000;
        sum += canary_bm.contains(probe_id);
    }
    double t1 = get_time_ns();
    dummy = sum;
    (void)dummy;
    return (t1 - t0) / num_probes;
}

// Fast non-member generator
inline uint32_t get_non_member(uint64_t& rng, uint32_t N) {
    rng ^= rng << 13;
    rng ^= rng >> 7;
    rng ^= rng << 17;
    // IDs in [N, 2N-1] are guaranteed non-members
    return N + (rng % N);
}

int main(int argc, char** argv) {
    // Pin to CPU 0 (P-core)
    int target_cpu = 0;
    if (argc > 1) target_cpu = std::atoi(argv[1]);

    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(target_cpu, &cpuset);
    if (pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset) != 0) {
        std::cerr << "Failed to set CPU affinity to CPU " << target_cpu << "\n";
        return 1;
    }
    std::cout << "[E1] Successfully pinned to CPU " << target_cpu << " (P-core)\n";

    // Initialize Canary Bitmap (N=1e6, 50% bits set)
    std::cout << "[E1] Initializing Canary Bitmap (N=1e6)...\n";
    BitmapFilter canary_bm(1000000);
    for (uint32_t i = 0; i < 1000000; i += 2) {
        canary_bm.set(i);
    }

    // Warmup canary
    std::cout << "[E1] Warming up canary...\n";
    for (int w = 0; w < 3; ++w) {
        run_canary(canary_bm, 10000000);
    }

    // Check already completed cells for resume capability
    std::unordered_set<int> completed_cells;
    bool has_existing = false;
    {
        std::ifstream fin("/mnt/c/NIRMA/SEM-1/DSA/filtered-ann/experiments/results/E1/microbenchmarks_e1.csv");
        std::string line;
        if (std::getline(fin, line)) {
            has_existing = true;
            while (std::getline(fin, line)) {
                if (line.empty()) continue;
                size_t comma = line.find(',');
                if (comma != std::string::npos) {
                    try {
                        completed_cells.insert(std::stoi(line.substr(0, comma)));
                    } catch (...) {}
                }
            }
        }
    }
    std::cout << "[E1] Found " << completed_cells.size() << " already completed cells in microbenchmarks_e1.csv\n";

    // Output files (append if resuming, overwrite if fresh)
    auto open_mode = has_existing ? (std::ios::out | std::ios::app) : std::ios::out;
    std::ofstream f_micro("/mnt/c/NIRMA/SEM-1/DSA/filtered-ann/experiments/results/E1/microbenchmarks_e1.csv", open_mode);
    if (!has_existing) {
        f_micro << "cell_id,N,sigma,structure,variant,probe_pattern,ns_per_probe,measured_fpr,theoretical_fpr,memory_bytes,build_time_s,canary_before_ns,canary_after_ns,canary_diff_pct,flagged\n";
    }

    std::ofstream f_canary("/mnt/c/NIRMA/SEM-1/DSA/filtered-ann/experiments/results/E1/canary_log.csv", open_mode);
    if (!has_existing) {
        f_canary << "cell_id,structure,N,sigma,canary_before_ns,canary_after_ns,diff_pct,flagged\n";
    }

    std::ofstream f_skip("/mnt/c/NIRMA/SEM-1/DSA/filtered-ann/experiments/results/E1/skip_list.csv", open_mode);
    if (!has_existing) {
        f_skip << "N,sigma,structure,variant,est_memory_bytes,limit_bytes,reason\n";
    }

    std::ofstream f_raw("/mnt/c/NIRMA/SEM-1/DSA/filtered-ann/experiments/results/E1/raw.csv", open_mode);
    if (!has_existing) {
        f_raw << "run_id,exp_id,dataset,N,d,predicate_type,correlation,sigma_target,sigma_actual,strategy,structure,bits_per_entry,M,efC,efS,k,repeat,recall_at_10,valid_fraction_at_10,qps,lat_p50_us,lat_p95_us,lat_p99_us,dist_comps_mean,nodes_visited_mean,filter_probes_mean,filter_fp_mean,filter_bytes,setup_s,seed,timestamp,notes\n";
    }

    std::vector<uint32_t> N_values = {1000000, 10000000, 100000000, 1000000000};
    std::vector<double> sigma_values = {0.001, 0.01, 0.1, 0.5};

    struct StructConfig {
        std::string name;
        std::string variant;
        double bpe;
        int bits;
    };

    std::vector<StructConfig> configs = {
        {"attribute_array", "uint32", 32.0, 32},
        {"bitmap", "1-bit", 1.0, 1},
        {"hash_set", "open_addressing", 0.0, 32},
        {"bloom_standard", "b6", 6.0, 6},
        {"bloom_standard", "b8", 8.0, 8},
        {"bloom_standard", "b10", 10.0, 10},
        {"bloom_standard", "b12", 12.0, 12},
        {"bloom_standard", "b16", 16.0, 16},
        {"bloom_blocked", "b6", 6.0, 6},
        {"bloom_blocked", "b8", 8.0, 8},
        {"bloom_blocked", "b10", 10.0, 10},
        {"bloom_blocked", "b12", 12.0, 12},
        {"bloom_blocked", "b16", 16.0, 16},
        {"cuckoo", "8bit", 8.4, 8},
        {"cuckoo", "12bit", 12.6, 12},
        {"cuckoo", "16bit", 16.8, 16},
        {"xor", "8bit", 9.84, 8},
        {"xor", "16bit", 19.68, 16}
    };

    int total_cells_planned = 0;
    int total_cells_run = 0;
    int total_cells_skipped = 0;
    int total_flagged = 0;

    const size_t NUM_PROBES = 10000000;

    std::cout << "[E1] Starting Grid Execution...\n";

    int cell_id = 0;

    for (uint32_t N : N_values) {
        for (double sigma : sigma_values) {
            uint32_t n_members = static_cast<uint32_t>(std::round(N * sigma));
            if (n_members < 1) n_members = 1;

            for (const auto& cfg : configs) {
                total_cells_planned++;
                cell_id++;

                if (completed_cells.count(cell_id)) {
                    total_cells_run++;
                    continue;
                }

                // Memory estimation check
                size_t est_bytes = 0;
                size_t est_build_peak = 0;
                bool skip = false;
                std::string skip_reason = "";

                if (cfg.name == "attribute_array") {
                    est_bytes = static_cast<size_t>(N) * sizeof(uint32_t);
                    est_build_peak = est_bytes;
                } else if (cfg.name == "bitmap") {
                    est_bytes = (static_cast<size_t>(N) + 63) / 64 * 8;
                    est_build_peak = est_bytes;
                } else if (cfg.name == "hash_set") {
                    size_t cap = 16;
                    while (cap * 0.70 < n_members) cap <<= 1;
                    est_bytes = cap * sizeof(uint32_t);
                    est_build_peak = est_bytes;
                } else if (cfg.name == "bloom_standard") {
                    est_bytes = static_cast<size_t>(std::ceil(n_members * cfg.bpe / 64.0)) * 8;
                    est_build_peak = est_bytes;
                } else if (cfg.name == "bloom_blocked") {
                    size_t bits = static_cast<size_t>(std::ceil(n_members * cfg.bpe));
                    size_t blocks = (bits + 511) / 512;
                    est_bytes = blocks * 64;
                    est_build_peak = est_bytes;
                } else if (cfg.name == "cuckoo") {
                    size_t num_buckets = static_cast<size_t>(std::ceil(n_members / (4.0 * 0.95)));
                    size_t b_size = (cfg.bits == 8) ? 4 : ((cfg.bits == 12) ? 6 : 8);
                    est_bytes = num_buckets * b_size;
                    est_build_peak = est_bytes;
                } else if (cfg.name == "xor") {
                    size_t capacity = (size_t)(32 + 1.23 * n_members);
                    capacity = capacity / 3 * 3;
                    est_bytes = capacity * (cfg.bits / 8) + 64;
                    // Xor populate peak memory: sets (16 bytes/elem) + Q (16 bytes/elem) + keys (8 bytes/elem)
                    est_build_peak = est_bytes + capacity * 32 + static_cast<size_t>(n_members) * 8;
                }

                if (est_bytes > RAM_50PCT_LIMIT) {
                    skip = true;
                    skip_reason = "Structure memory (" + std::to_string(est_bytes / 1000000) + " MB) exceeds 50% RAM limit (3790 MB)";
                } else if (est_build_peak > RAM_50PCT_LIMIT) {
                    skip = true;
                    skip_reason = "Build peak memory (" + std::to_string(est_build_peak / 1000000) + " MB) exceeds 50% RAM limit (3790 MB)";
                }

                if (skip) {
                    total_cells_skipped++;
                    f_skip << N << "," << sigma << "," << cfg.name << "," << cfg.variant << ","
                           << est_bytes << "," << RAM_50PCT_LIMIT << ",\"" << skip_reason << "\"\n";
                    f_skip.flush();
                    std::cout << "[E1 SKIP] N=" << N << ", sigma=" << sigma << ", " << cfg.name << " (" << cfg.variant << "): " << skip_reason << "\n";
                    continue;
                }

                // Run Canary BEFORE
                double canary_before_ns = run_canary(canary_bm, NUM_PROBES);

                // Build Member Keys
                // Use deterministic stride generator to avoid large key vector in memory when possible
                // For Xor filter, keys must be provided as array
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
                double build_time_s = 0.0;
                double theoretical_fpr = 0.0;

                // Instantiate & Build Structure
                double t_b0 = get_time_ns();

                std::vector<uint32_t> attr_arr;
                BitmapFilter bm;
                OpenAddressingHashSet oahs;
                BloomFilter bf;
                BlockedBloomFilter bbf;
                CuckooFilter8 cf8;
                CuckooFilter12 cf12;
                CuckooFilter16 cf16;
                xor8_t xf8;
                xor16_t xf16;

                if (cfg.name == "attribute_array") {
                    attr_arr.assign(N, 0);
                    for (uint32_t i = 0; i < n_members; ++i) {
                        uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                        attr_arr[id] = 1;
                    }
                    exact_bytes = attr_arr.size() * sizeof(uint32_t);
                    theoretical_fpr = 0.0;
                } else if (cfg.name == "bitmap") {
                    bm = BitmapFilter(N);
                    for (uint32_t i = 0; i < n_members; ++i) {
                        uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                        bm.set(id);
                    }
                    exact_bytes = bm.size_in_bytes();
                    theoretical_fpr = 0.0;
                } else if (cfg.name == "hash_set") {
                    oahs = OpenAddressingHashSet(n_members);
                    for (uint32_t i = 0; i < n_members; ++i) {
                        uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                        oahs.insert(id);
                    }
                    exact_bytes = oahs.size_in_bytes();
                    theoretical_fpr = 0.0;
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
                    // Standard Bloom formula for comparison (EXPERIMENTS.md rule 3)
                    theoretical_fpr = std::pow(1.0 - std::exp(-static_cast<double>(k) / cfg.bpe), k);
                } else if (cfg.name == "cuckoo") {
                    if (cfg.bits == 8) {
                        cf8 = CuckooFilter8(n_members);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                            cf8.insert(id);
                        }
                        exact_bytes = cf8.size_in_bytes();
                        theoretical_fpr = 8.0 * std::pow(2.0, -8.0); // ~0.03125
                    } else if (cfg.bits == 12) {
                        cf12 = CuckooFilter12(n_members);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                            cf12.insert(id);
                        }
                        exact_bytes = cf12.size_in_bytes();
                        theoretical_fpr = 8.0 * std::pow(2.0, -12.0); // ~0.00195
                    } else {
                        cf16 = CuckooFilter16(n_members);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            uint32_t id = static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members);
                            cf16.insert(id);
                        }
                        exact_bytes = cf16.size_in_bytes();
                        theoretical_fpr = 8.0 * std::pow(2.0, -16.0); // ~0.000122
                    }
                } else if (cfg.name == "xor") {
                    if (cfg.bits == 8) {
                        xor8_allocate(n_members, &xf8);
                        xor8_populate(xor_keys.data(), n_members, &xf8);
                        exact_bytes = xor8_size_in_bytes(&xf8);
                        theoretical_fpr = std::pow(2.0, -8.0); // ~0.003906
                    } else {
                        xor16_allocate(n_members, &xf16);
                        xor16_populate(xor_keys.data(), n_members, &xf16);
                        exact_bytes = xor16_size_in_bytes(&xf16);
                        theoretical_fpr = std::pow(2.0, -16.0); // ~0.000015
                    }
                }

                double t_b1 = get_time_ns();
                build_time_s = (t_b1 - t_b0) / 1e9;

                // Measure Probe Pattern 1: Uniform Random IDs
                double ns_uniform = 0.0;
                {
                    uint64_t rng = 9876543210987ULL + cell_id;
                    volatile uint64_t dummy = 0;
                    uint64_t sum = 0;
                    double t0 = get_time_ns();

                    if (cfg.name == "attribute_array") {
                        for (size_t p = 0; p < NUM_PROBES; ++p) {
                            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                            sum += (attr_arr[rng % N] == 1);
                        }
                    } else if (cfg.name == "bitmap") {
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
                        if (cfg.bits == 8) {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                sum += cf8.contains(rng % N);
                            }
                        } else if (cfg.bits == 12) {
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

                    double t1 = get_time_ns();
                    dummy = sum;
                    (void)dummy;
                    ns_uniform = (t1 - t0) / NUM_PROBES;
                }

                // Measure Probe Pattern 2: Batches of 32 IDs
                double ns_batch32 = 0.0;
                {
                    uint64_t rng = 11223344556677ULL + cell_id;
                    volatile uint64_t dummy = 0;
                    uint64_t sum = 0;
                    size_t num_batches = NUM_PROBES / 32;
                    uint32_t max_base = (N > 32) ? (N - 32) : 1;
                    double t0 = get_time_ns();

                    if (cfg.name == "attribute_array") {
                        for (size_t b = 0; b < num_batches; ++b) {
                            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                            uint32_t base = rng % max_base;
                            for (uint32_t o = 0; o < 32; ++o) sum += (attr_arr[base + o] == 1);
                        }
                    } else if (cfg.name == "bitmap") {
                        for (size_t b = 0; b < num_batches; ++b) {
                            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                            uint32_t base = rng % max_base;
                            for (uint32_t o = 0; o < 32; ++o) sum += bm.contains(base + o);
                        }
                    } else if (cfg.name == "hash_set") {
                        for (size_t b = 0; b < num_batches; ++b) {
                            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                            uint32_t base = rng % max_base;
                            for (uint32_t o = 0; o < 32; ++o) sum += oahs.contains(base + o);
                        }
                    } else if (cfg.name == "bloom_standard") {
                        for (size_t b = 0; b < num_batches; ++b) {
                            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                            uint32_t base = rng % max_base;
                            for (uint32_t o = 0; o < 32; ++o) sum += bf.contains(base + o);
                        }
                    } else if (cfg.name == "bloom_blocked") {
                        for (size_t b = 0; b < num_batches; ++b) {
                            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                            uint32_t base = rng % max_base;
                            for (uint32_t o = 0; o < 32; ++o) sum += bbf.contains(base + o);
                        }
                    } else if (cfg.name == "cuckoo") {
                        if (cfg.bits == 8) {
                            for (size_t b = 0; b < num_batches; ++b) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                uint32_t base = rng % max_base;
                                for (uint32_t o = 0; o < 32; ++o) sum += cf8.contains(base + o);
                            }
                        } else if (cfg.bits == 12) {
                            for (size_t b = 0; b < num_batches; ++b) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                uint32_t base = rng % max_base;
                                for (uint32_t o = 0; o < 32; ++o) sum += cf12.contains(base + o);
                            }
                        } else {
                            for (size_t b = 0; b < num_batches; ++b) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                uint32_t base = rng % max_base;
                                for (uint32_t o = 0; o < 32; ++o) sum += cf16.contains(base + o);
                            }
                        }
                    } else if (cfg.name == "xor") {
                        if (cfg.bits == 8) {
                            for (size_t b = 0; b < num_batches; ++b) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                uint32_t base = rng % max_base;
                                for (uint32_t o = 0; o < 32; ++o) sum += xor8_contain(base + o, &xf8);
                            }
                        } else {
                            for (size_t b = 0; b < num_batches; ++b) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                uint32_t base = rng % max_base;
                                for (uint32_t o = 0; o < 32; ++o) sum += xor16_contain(base + o, &xf16);
                            }
                        }
                    }

                    double t1 = get_time_ns();
                    dummy = sum;
                    (void)dummy;
                    ns_batch32 = (t1 - t0) / (num_batches * 32);
                }

                // Measure False Positive Rate (10^7 non-member probes)
                double measured_fpr = 0.0;
                if (cfg.name == "attribute_array" || cfg.name == "bitmap" || cfg.name == "hash_set") {
                    measured_fpr = 0.0; // Exact structures have zero false positives
                } else {
                    uint64_t rng = 55667788990011ULL + cell_id;
                    size_t fp_count = 0;

                    if (cfg.name == "bloom_standard") {
                        for (size_t p = 0; p < NUM_PROBES; ++p) {
                            uint32_t non_member = get_non_member(rng, N);
                            fp_count += bf.contains(non_member);
                        }
                    } else if (cfg.name == "bloom_blocked") {
                        for (size_t p = 0; p < NUM_PROBES; ++p) {
                            uint32_t non_member = get_non_member(rng, N);
                            fp_count += bbf.contains(non_member);
                        }
                    } else if (cfg.name == "cuckoo") {
                        if (cfg.bits == 8) {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                uint32_t non_member = get_non_member(rng, N);
                                fp_count += cf8.contains(non_member);
                            }
                        } else if (cfg.bits == 12) {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                uint32_t non_member = get_non_member(rng, N);
                                fp_count += cf12.contains(non_member);
                            }
                        } else {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                uint32_t non_member = get_non_member(rng, N);
                                fp_count += cf16.contains(non_member);
                            }
                        }
                    } else if (cfg.name == "xor") {
                        if (cfg.bits == 8) {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                uint32_t non_member = get_non_member(rng, N);
                                fp_count += xor8_contain(non_member, &xf8);
                            }
                        } else {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                uint32_t non_member = get_non_member(rng, N);
                                fp_count += xor16_contain(non_member, &xf16);
                            }
                        }
                    }
                    measured_fpr = static_cast<double>(fp_count) / NUM_PROBES;
                }

                // Cleanup Xor filter memory
                if (cfg.name == "xor") {
                    if (cfg.bits == 8) xor8_free(&xf8);
                    else xor16_free(&xf16);
                }

                // Run Canary AFTER
                double canary_after_ns = run_canary(canary_bm, NUM_PROBES);
                double canary_diff_pct = std::abs(canary_after_ns - canary_before_ns) / canary_before_ns * 100.0;
                bool flagged = (canary_diff_pct > 5.0);
                if (flagged) total_flagged++;

                total_cells_run++;

                // Log canary
                f_canary << cell_id << "," << cfg.name << "_" << cfg.variant << "," << N << "," << sigma << ","
                         << canary_before_ns << "," << canary_after_ns << "," << canary_diff_pct << "," << (flagged ? "TRUE" : "FALSE") << "\n";

                // Log microbenchmark rows (2 rows per cell: uniform_random and batch_32)
                f_micro << cell_id << "," << N << "," << sigma << "," << cfg.name << "," << cfg.variant << ","
                        << "uniform_random," << ns_uniform << "," << measured_fpr << "," << theoretical_fpr << ","
                        << exact_bytes << "," << build_time_s << "," << canary_before_ns << "," << canary_after_ns << ","
                        << canary_diff_pct << "," << (flagged ? "TRUE" : "FALSE") << "\n";

                f_micro << cell_id << "," << N << "," << sigma << "," << cfg.name << "," << cfg.variant << ","
                        << "batch_32," << ns_batch32 << "," << measured_fpr << "," << theoretical_fpr << ","
                        << exact_bytes << "," << build_time_s << "," << canary_before_ns << "," << canary_after_ns << ","
                        << canary_diff_pct << "," << (flagged ? "TRUE" : "FALSE") << "\n";

                // Log raw.csv standard schema rows
                std::string timestamp = "2026-10-31T18:40:00Z";
                // Uniform row
                f_raw << "run_E1_" << cell_id << "_u,E1,none," << N << ",0,P3,independent," << sigma << "," << sigma << ",none,"
                      << cfg.name << "_" << cfg.variant << "," << cfg.bpe << ",0,0,0,0,1,0,0,"
                      << (1e9 / ns_uniform) << "," << (ns_uniform / 1e3) << ",0,0,0,0," << NUM_PROBES << "," << (measured_fpr * NUM_PROBES) << ","
                      << exact_bytes << "," << build_time_s << ",42," << timestamp << ",\"uniform_random; FPR_theory=" << theoretical_fpr << "; canary_diff=" << canary_diff_pct << "%\"\n";

                // Batch row
                f_raw << "run_E1_" << cell_id << "_b,E1,none," << N << ",0,P3,independent," << sigma << "," << sigma << ",none,"
                      << cfg.name << "_" << cfg.variant << "," << cfg.bpe << ",0,0,0,0,1,0,0,"
                      << (1e9 / ns_batch32) << "," << (ns_batch32 / 1e3) << ",0,0,0,0," << NUM_PROBES << "," << (measured_fpr * NUM_PROBES) << ","
                      << exact_bytes << "," << build_time_s << ",42," << timestamp << ",\"batch_32; FPR_theory=" << theoretical_fpr << "; canary_diff=" << canary_diff_pct << "%\"\n";

                f_micro.flush();
                f_canary.flush();
                f_raw.flush();

                std::cout << "[E1 CELL " << cell_id << "] N=" << N << ", sigma=" << sigma << ", " << cfg.name << " (" << cfg.variant
                          << "): " << exact_bytes << " bytes, ns/probe(uniform)=" << std::fixed << std::setprecision(2) << ns_uniform
                          << ", ns/probe(b32)=" << ns_batch32 << ", FPR=" << std::setprecision(5) << measured_fpr
                          << " (theory=" << theoretical_fpr << "), canary_diff=" << std::setprecision(2) << canary_diff_pct
                          << "%" << (flagged ? " [FLAGGED]" : "") << "\n";
            }
        }
    }

    f_micro.close();
    f_canary.close();
    f_skip.close();
    f_raw.close();

    std::cout << "\n======================================================\n";
    std::cout << "[E1 COMPLETED] Planned: " << total_cells_planned
              << ", Run: " << total_cells_run
              << ", Skipped: " << total_cells_skipped
              << ", Flagged: " << total_flagged << "\n";
    std::cout << "======================================================\n";

    return 0;
}
