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
    pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);

    const int repeats = 30;
    long long iterations = 1000000000LL; // ~250ms

    // Multiple warmups to ensure CPU frequency scaling has locked to max P-state
    for (int w = 0; w < 5; ++w) {
        for (long long i = 0; i < iterations; ++i) {
            asm volatile("" : "+r"(i));
        }
    }

    std::vector<double> durations(repeats);
    for (int r = 0; r < repeats; ++r) {
        auto start = std::chrono::high_resolution_clock::now();
        for (long long i = 0; i < iterations; ++i) {
            asm volatile("" : "+r"(i));
        }
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> diff = end - start;
        durations[r] = diff.count();
        std::cout << "r=" << r << ": " << durations[r]*1000.0 << " ms\n";
    }

    double sum = std::accumulate(durations.begin(), durations.end(), 0.0);
    double mean = sum / repeats;
    double sq_sum = 0.0;
    for (double d : durations) sq_sum += (d - mean) * (d - mean);
    double stddev = std::sqrt(sq_sum / (repeats - 1));
    double cv = (stddev / mean) * 100.0;

    std::cout << "Mean: " << mean * 1000.0 << " ms, Std: " << stddev * 1000.0 << " ms, CV: " << cv << " %\n";
    return 0;
}
