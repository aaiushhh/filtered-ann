#include <iostream>
#include <sched.h>
#include <pthread.h>
#include <cpuid.h>
#include <unistd.h>
#include <string>

int main() {
    int num_cpus = sysconf(_SC_NPROCESSORS_ONLN);
    std::cout << "Total logical CPUs: " << num_cpus << std::endl;
    for (int i = 0; i < num_cpus; ++i) {
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(i, &cpuset);
        pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);
        
        unsigned int eax = 0, ebx = 0, ecx = 0, edx = 0;
        __cpuid_count(0x1a, 0, eax, ebx, ecx, edx);
        unsigned int core_type = (eax >> 24) & 0xFF;
        std::string type_str = "Unknown";
        if (core_type == 0x20) type_str = "E-core";
        else if (core_type == 0x40) type_str = "P-core";
        std::cout << "CPU " << i << ": Core Type = 0x" << std::hex << core_type << std::dec << " (" << type_str << ")" << std::endl;
    }
    return 0;
}
