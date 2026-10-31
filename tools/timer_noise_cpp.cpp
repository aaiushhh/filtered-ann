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
    int cpu_id = 2; // CPU 2 is a P-core (Core 1)
    if (argc > 1) cpu_id = std::atoi(argv[1]);

    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(cpu_id, &cpuset);
    if (pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset) != 0) {
        std::cerr << "Failed to set CPU affinity to CPU " << cpu_id << "\n";
        return 1;
    }

    const int repeats = 30;
    long long iterations = 1000000000LL;

    // Warm up for at least 10 seconds to ensure frequency governor reaches stable max P-state
    std::cout << "Warming up CPU " << cpu_id << " to lock frequency governor...\n";
    auto w_start = std::chrono::high_resolution_clock::now();
    while (true) {
        for (long long i = 0; i < 200000000LL; ++i) {
            asm volatile("" : "+r"(i));
        }
        auto w_now = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = w_now - w_start;
        if (elapsed.count() >= 10.0) break;
    }
    std::cout << "Warmup complete. Starting 30 measurement runs...\n";

    std::vector<double> durations(repeats);
    for (int r = 0; r < repeats; ++r) {
        auto start = std::chrono::high_resolution_clock::now();
        for (long long i = 0; i < iterations; ++i) {
            asm volatile("" : "+r"(i));
        }
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> diff = end - start;
        durations[r] = diff.count();
    }

    double sum = std::accumulate(durations.begin(), durations.end(), 0.0);
    double mean = sum / repeats;

    double sq_sum = 0.0;
    for (double d : durations) {
        sq_sum += (d - mean) * (d - mean);
    }
    double stddev = std::sqrt(sq_sum / (repeats - 1));
    double cv = (stddev / mean) * 100.0;

    std::vector<double> sorted_d = durations;
    std::sort(sorted_d.begin(), sorted_d.end());
    double median = (sorted_d[14] + sorted_d[15]) / 2.0;
    double q1 = sorted_d[7];
    double q3 = sorted_d[22];
    double iqr = q3 - q1;

    std::cout << std::fixed << std::setprecision(6);
    std::cout << "Timer Noise Test (C++, CPU " << cpu_id << ", P-core):\n";
    std::cout << "Repeats: " << repeats << "\n";
    std::cout << "Iterations per repeat: " << iterations << "\n";
    std::cout << "Mean: " << mean * 1000.0 << " ms\n";
    std::cout << "Std: " << stddev * 1000.0 << " ms\n";
    std::cout << "CV: " << cv << " %\n";
    std::cout << "Median: " << median * 1000.0 << " ms\n";
    std::cout << "IQR: " << iqr * 1000.0 << " ms\n";
    std::cout << "Status: " << (cv < 5.0 ? "PASS" : "FAIL") << "\n";

    return 0;
}
