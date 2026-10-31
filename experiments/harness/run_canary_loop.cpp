#include <iostream>
#include <vector>
#include <chrono>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <string>
#include <sched.h>
#include <unistd.h>

inline double get_time_ns() {
    auto now = std::chrono::high_resolution_clock::now();
    return static_cast<double>(std::chrono::duration_cast<std::chrono::nanoseconds>(now.time_since_epoch()).count());
}

struct Bitmap {
    std::vector<uint64_t> words;
    Bitmap(size_t n = 1000000) {
        words.resize((n + 63) / 64, 0);
        // set some bits
        for (size_t i = 0; i < n; i += 2) {
            words[i / 64] |= (1ULL << (i % 64));
        }
    }
    inline bool contains(uint32_t id) const {
        return (words[id / 64] >> (id % 64)) & 1ULL;
    }
};

int main(int argc, char** argv) {
    int duration_sec = 600; // 10 minutes default
    if (argc > 1) {
        duration_sec = std::atoi(argv[1]);
    }
    std::string out_file = "canary_run.csv";
    if (argc > 2) {
        out_file = argv[2];
    }
    int pin_cpu = -1; // -1 means default/no pin
    if (argc > 3) {
        pin_cpu = std::atoi(argv[3]);
    }

    if (pin_cpu >= 0) {
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(pin_cpu, &cpuset);
        if (sched_setaffinity(0, sizeof(cpuset), &cpuset) != 0) {
            std::cerr << "Warning: sched_setaffinity failed\n";
        }
    }

    std::ofstream fout(out_file);
    fout << "iter,elapsed_sec,ns_per_probe\n";

    Bitmap bm(1000000);
    const size_t NUM_PROBES = 10000000;

    auto start_time = std::chrono::steady_clock::now();
    int iter = 0;

    std::cout << "Starting canary loop for " << duration_sec << " seconds, output to " << out_file
              << ", pinned_cpu=" << pin_cpu << "...\n";

    while (true) {
        auto now = std::chrono::steady_clock::now();
        double elapsed_sec = std::chrono::duration_cast<std::chrono::seconds>(now - start_time).count();
        if (elapsed_sec >= duration_sec) {
            break;
        }

        uint64_t rng = 123456789ULL + iter * 10007ULL;
        volatile uint64_t sum = 0;
        double t0 = get_time_ns();
        for (size_t p = 0; p < NUM_PROBES; ++p) {
            rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
            sum += bm.contains(static_cast<uint32_t>(rng % 1000000));
        }
        double t1 = get_time_ns();
        double ns_per_probe = (t1 - t0) / NUM_PROBES;
        iter++;

        fout << iter << "," << elapsed_sec << "," << std::fixed << std::setprecision(5) << ns_per_probe << "\n";
        fout.flush();

        if (iter % 20 == 0) {
            std::cout << "[Iter " << iter << " at " << elapsed_sec << "s] ns/probe: " << ns_per_probe << "\n";
        }
    }

    std::cout << "Completed " << iter << " canary iterations in " << duration_sec << " seconds.\n";
    return 0;
}
