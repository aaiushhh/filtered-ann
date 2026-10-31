#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
#include <cmath>
#include <chrono>
#include <sched.h>
#include <pthread.h>
#include <unistd.h>
#include <iomanip>

int main(int argc, char** argv) {
    int cpu_id = 0;
    if (argc > 1) cpu_id = std::atoi(argv[1]);

    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(cpu_id, &cpuset);
    if (pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset) != 0) {
        std::cerr << "Failed to set CPU affinity to CPU " << cpu_id << "\n";
        return 1;
    }

    const int repeats = 30;
    const long long loop_iters = 500000000LL;

    // 5 warmup rounds
    for (int w = 0; w < 5; ++w) {
        volatile long long dummy = 0;
        for (long long i = 0; i < loop_iters; ++i) {
            dummy += i;
        }
    }

    std::vector<double> times(repeats);
    for (int r = 0; r < repeats; ++r) {
        auto t0 = std::chrono::high_resolution_clock::now();
        volatile long long dummy = 0;
        for (long long i = 0; i < loop_iters; ++i) {
            dummy += i;
        }
        auto t1 = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> diff = t1 - t0;
        times[r] = diff.count();
    }

    double sum = std::accumulate(times.begin(), times.end(), 0.0);
    double mean = sum / repeats;
    double sq_sum = 0.0;
    for (double d : times) sq_sum += (d - mean) * (d - mean);
    double stddev = std::sqrt(sq_sum / (repeats - 1));
    double cv = (stddev / mean) * 100.0;

    std::vector<double> sorted = times;
    std::sort(sorted.begin(), sorted.end());
    double median = (sorted[14] + sorted[15]) / 2.0;
    double q1 = sorted[7];
    double q3 = sorted[22];
    double iqr = q3 - q1;

    std::cout << std::fixed << std::setprecision(4);
    std::cout << "Timer noise test (C++, CPU " << cpu_id << ", " << repeats << " repeats x " << loop_iters << " iterations):\n";
    std::cout << "  Mean:   " << mean * 1000.0 << " ms\n";
    std::cout << "  Std:    " << stddev * 1000.0 << " ms\n";
    std::cout << "  CV:     " << cv << " %\n";
    std::cout << "  Median: " << median * 1000.0 << " ms\n";
    std::cout << "  IQR:    " << iqr * 1000.0 << " ms\n";
    std::cout << "  Status: " << (cv < 5.0 ? "PASS" : "FAIL") << "\n";

    return (cv < 5.0) ? 0 : 1;
}
