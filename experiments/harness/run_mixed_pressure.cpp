#define _GNU_SOURCE
#include <iostream>
#include <vector>
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

// Canary benchmark
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
    double q1 = (n == 5) ? vals[1] : vals[n / 4];
    double q3 = (n == 5) ? vals[3] : vals[3 * n / 4];
    iqr = q3 - q1;
}

int main(int argc, char** argv) {
    int pin_cpu = 0;
    if (argc > 1) {
        pin_cpu = std::atoi(argv[1]);
    }
    if (pin_cpu >= 0) {
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(pin_cpu, &cpuset);
        if (sched_setaffinity(0, sizeof(cpuset), &cpuset) != 0) {
            std::cerr << "[Mixed] Warning: sched_setaffinity to CPU " << pin_cpu << " failed\n";
        } else {
            std::cout << "[Mixed] Pinned process to CPU " << pin_cpu << "\n";
        }
    }

    const size_t NUM_PROBES = 10000000;
    const size_t RAM_50PCT_LIMIT = 3977804000ULL; // ~3.79 GB
    const size_t ARRAY_SIZE = 1073741824ULL;      // 1 GB array for vector fetch stand-in
    const size_t NUM_CACHE_LINES = ARRAY_SIZE / 64; // 16,777,216 lines

    std::cout << "[Mixed] Allocating and touching 1 GB array for vector fetch stand-in...\n";
    uint8_t* fetch_buf = (uint8_t*)aligned_alloc(64, ARRAY_SIZE);
    if (!fetch_buf) {
        std::cerr << "[Mixed] Error: Failed to allocate 1 GB array!\n";
        return 1;
    }
    // Touch every 4 KB page to ensure physical memory allocation
    for (size_t i = 0; i < ARRAY_SIZE; i += 4096) {
        fetch_buf[i] = static_cast<uint8_t>((i >> 12) & 0xFF);
    }
    std::cout << "[Mixed] 1 GB array mapped in RAM.\n";

    // Canary baseline setup
    BitmapFilter canary_bm(1000000);
    for (size_t i = 0; i < 1000000; i += 2) canary_bm.set(i);
    run_canary(canary_bm, 1000000);

    std::string dir = "experiments/results/E1b";
    std::ofstream f_raw(dir + "/mixed_pressure_raw.csv");
    f_raw << "run_id,cell_id,repeat,N,sigma,structure,variant,ns_per_probe_and_fetch,memory_bytes,build_time_s,canary_before_ns,canary_after_ns,canary_diff_pct,flagged,rerun\n";

    std::ofstream f_summary(dir + "/mixed_pressure_summary.csv");
    f_summary << "cell_id,N,sigma,structure,variant,median_ns,iqr_ns,min_ns,max_ns,memory_bytes,build_time_s,flagged_rerun\n";

    std::ofstream f_canary(dir + "/mixed_pressure_canary.csv");
    f_canary << "cell_id,run_type,N,sigma,structure,variant,canary_before_ns,canary_after_ns,diff_pct,flagged\n";

    std::ofstream f_skip(dir + "/mixed_pressure_skip.csv");
    f_skip << "N,sigma,structure,variant,est_memory_bytes,limit_bytes,reason\n";

    std::vector<uint32_t> N_values = {10000000, 100000000, 1000000000};
    std::vector<double> sigma_values = {0.001, 0.01};

    // 5 structures for mixed-pressure test
    std::vector<StructConfig> base_configs = {
        {"bitmap", "1-bit", 1.0, 1},
        {"hash_set", "open_addressing", 64.0, 64},
        {"xor", "8bit", 8.0, 8},
        {"cuckoo", "16bit", 16.0, 16},
        {"bloom_blocked", "b10", 10.0, 10}
    };

    std::mt19937 g(54321);
    int cell_id = 0;

    std::cout << "[Mixed] Starting Mixed-Pressure Test (probe + 1GB random cache-line read)...\n";

    for (uint32_t N : N_values) {
        for (double sigma : sigma_values) {
            uint32_t n_members = static_cast<uint32_t>(std::round(N * sigma));
            if (n_members < 1) n_members = 1;

            std::vector<StructConfig> configs = base_configs;
            std::shuffle(configs.begin(), configs.end(), g);

            for (const auto& cfg : configs) {
                cell_id++;

                size_t est_bytes = 0;
                if (cfg.name == "bitmap") {
                    est_bytes = (N + 63) / 8;
                } else if (cfg.name == "hash_set") {
                    size_t cap = 16;
                    while (cap * 0.70 < n_members) cap <<= 1;
                    est_bytes = cap * sizeof(uint32_t) + sizeof(OpenAddressingHashSet);
                } else if (cfg.name == "bloom_blocked") {
                    size_t total_bits = static_cast<size_t>(std::ceil(n_members * cfg.bpe));
                    est_bytes = ((total_bits + 511) / 512) * 64;
                } else if (cfg.name == "cuckoo") {
                    size_t num_buckets = static_cast<size_t>(std::ceil(n_members / (4.0 * 0.95)));
                    est_bytes = num_buckets * 8; // 16bit = 8 bytes per bucket
                } else if (cfg.name == "xor") {
                    size_t capacity = (size_t)(32 + 1.23 * n_members);
                    capacity = capacity / 3 * 3;
                    est_bytes = capacity * 1 + 64;
                }

                // Check total memory with 1 GB array
                size_t total_mem = est_bytes + ARRAY_SIZE;
                if (total_mem > RAM_50PCT_LIMIT) {
                    std::string reason = "Total memory with 1GB array (" + std::to_string(total_mem / 1000000) + " MB) exceeds 50% RAM limit (3790 MB)";
                    f_skip << N << "," << sigma << "," << cfg.name << "," << cfg.variant << ","
                           << total_mem << "," << RAM_50PCT_LIMIT << ",\"" << reason << "\"\n";
                    f_skip.flush();
                    std::cout << "[Mixed SKIP] Cell " << cell_id << ": " << reason << "\n";
                    continue;
                }

                for (int run_attempt = 0; run_attempt < 2; ++run_attempt) {
                    bool is_rerun = (run_attempt > 0);

                    double canary_before_ns = run_canary(canary_bm, NUM_PROBES);

                    // Build filter
                    BitmapFilter bm;
                    OpenAddressingHashSet oahs;
                    BlockedBloomFilter bbf;
                    CuckooFilter16 cf16;
                    xor8_t xf8;
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
                    double t_b0 = get_time_ns();

                    if (cfg.name == "bitmap") {
                        bm = BitmapFilter(N);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            bm.set(static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members));
                        }
                        exact_bytes = bm.size_in_bytes();
                    } else if (cfg.name == "hash_set") {
                        oahs = OpenAddressingHashSet(n_members);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            oahs.insert(static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members));
                        }
                        exact_bytes = oahs.size_in_bytes();
                    } else if (cfg.name == "bloom_blocked") {
                        bbf = BlockedBloomFilter(n_members, cfg.bpe);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            bbf.insert(static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members));
                        }
                        exact_bytes = bbf.size_in_bytes();
                    } else if (cfg.name == "cuckoo") {
                        cf16 = CuckooFilter16(n_members);
                        for (uint32_t i = 0; i < n_members; ++i) {
                            cf16.insert(static_cast<uint32_t>((static_cast<uint64_t>(i) * N) / n_members));
                        }
                        exact_bytes = cf16.size_in_bytes();
                    } else if (cfg.name == "xor") {
                        xor8_allocate(n_members, &xf8);
                        xor8_populate(xor_keys.data(), n_members, &xf8);
                        exact_bytes = xor8_size_in_bytes(&xf8);
                    }

                    double t_b1 = get_time_ns();
                    double build_time_s = (t_b1 - t_b0) / 1e9;

                    // Lambda to run probe + fetch
                    auto run_probe_and_fetch = [&](uint64_t seed_val) -> double {
                        uint64_t rng = seed_val;
                        volatile uint64_t dummy = 0;
                        double t0 = get_time_ns();

                        if (cfg.name == "bitmap") {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                bool match = bm.contains(rng % N);
                                size_t line = (rng >> 12) & 0xFFFFFFULL; // 0 to 16,777,215
                                volatile uint8_t byte = fetch_buf[line * 64];
                                dummy += (match ? byte : (byte ^ 1));
                            }
                        } else if (cfg.name == "hash_set") {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                bool match = oahs.contains(rng % N);
                                size_t line = (rng >> 12) & 0xFFFFFFULL;
                                volatile uint8_t byte = fetch_buf[line * 64];
                                dummy += (match ? byte : (byte ^ 1));
                            }
                        } else if (cfg.name == "bloom_blocked") {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                bool match = bbf.contains(rng % N);
                                size_t line = (rng >> 12) & 0xFFFFFFULL;
                                volatile uint8_t byte = fetch_buf[line * 64];
                                dummy += (match ? byte : (byte ^ 1));
                            }
                        } else if (cfg.name == "cuckoo") {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                bool match = cf16.contains(rng % N);
                                size_t line = (rng >> 12) & 0xFFFFFFULL;
                                volatile uint8_t byte = fetch_buf[line * 64];
                                dummy += (match ? byte : (byte ^ 1));
                            }
                        } else if (cfg.name == "xor") {
                            for (size_t p = 0; p < NUM_PROBES; ++p) {
                                rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
                                bool match = xor8_contain(rng % N, &xf8);
                                size_t line = (rng >> 12) & 0xFFFFFFULL;
                                volatile uint8_t byte = fetch_buf[line * 64];
                                dummy += (match ? byte : (byte ^ 1));
                            }
                        }

                        double t1 = get_time_ns();
                        return (t1 - t0) / NUM_PROBES;
                    };

                    // 1 Warm-up (discarded)
                    run_probe_and_fetch(1234567ULL + cell_id);

                    // 5 Measured repeats
                    std::vector<double> repeats;
                    for (int r = 1; r <= 5; ++r) {
                        double ns = run_probe_and_fetch(9876543210ULL + cell_id * 100 + r * 13);
                        repeats.push_back(ns);
                    }

                    if (cfg.name == "xor") {
                        xor8_free(&xf8);
                    }

                    double canary_after_ns = run_canary(canary_bm, NUM_PROBES);
                    double canary_diff_pct = std::abs(canary_after_ns - canary_before_ns) / canary_before_ns * 100.0;
                    bool flagged = (canary_diff_pct > 5.0);

                    // Log canary
                    f_canary << cell_id << "," << (is_rerun ? "RERUN" : "PRIMARY") << ","
                             << N << "," << sigma << "," << cfg.name << "," << cfg.variant << ","
                             << canary_before_ns << "," << canary_after_ns << ","
                             << canary_diff_pct << "," << (flagged ? "TRUE" : "FALSE") << "\n";
                    f_canary.flush();

                    // Log raw repeats
                    for (int r = 1; r <= 5; ++r) {
                        std::string run_id = "run_mixed_" + std::to_string(cell_id) + "_r" + std::to_string(r) + (is_rerun ? "_rerun" : "");
                        f_raw << run_id << "," << cell_id << "," << r << "," << N << "," << sigma << ","
                              << cfg.name << "," << cfg.variant << "," << repeats[r - 1] << ","
                              << exact_bytes << "," << build_time_s << ","
                              << canary_before_ns << "," << canary_after_ns << ","
                              << canary_diff_pct << "," << (flagged ? "TRUE" : "FALSE") << ","
                              << (is_rerun ? "TRUE" : "FALSE") << "\n";
                    }
                    f_raw.flush();

                    // Log summary
                    double med, iqr, min_v, max_v;
                    get_median_iqr(repeats, med, iqr, min_v, max_v);
                    f_summary << cell_id << "," << N << "," << sigma << "," << cfg.name << "," << cfg.variant << ","
                              << med << "," << iqr << "," << min_v << "," << max_v << ","
                              << exact_bytes << "," << build_time_s << "," << (flagged ? "TRUE" : "FALSE") << "\n";
                    f_summary.flush();

                    std::cout << "[Mixed CELL " << cell_id << (is_rerun ? " RERUN" : "") << "] N=" << N << ", sigma=" << sigma
                              << ", " << cfg.name << ": median=" << med << " ns/probe+fetch (IQR=" << iqr << "), "
                              << "canary_diff=" << std::fixed << std::setprecision(2) << canary_diff_pct << "%"
                              << (flagged ? " [FLAGGED]" : "") << "\n";

                    if (flagged && !is_rerun) {
                        std::cout << ">>> Flagged canary drift >5.0% (" << canary_diff_pct << "%), running rerun for mixed cell " << cell_id << "...\n";
                        continue;
                    } else {
                        break;
                    }
                }
            }
        }
    }

    free(fetch_buf);
    std::cout << "[Mixed] Mixed-pressure test complete.\n";
    return 0;
}
