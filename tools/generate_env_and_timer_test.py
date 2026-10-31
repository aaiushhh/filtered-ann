import os
import sys
import time
import json
import platform
import subprocess
import numpy as np

# 1. Timer-noise test: empty loop benchmark x 30
# Run an empty loop 10,000,000 iterations, 30 repeats
# Optional core pinning
try:
    os.sched_setaffinity(0, {0})
    pinned = True
except (AttributeError, OSError):
    pinned = False

repeats = 30
loop_iters = 10_000_000
times = []

# Warmup
for _ in range(3):
    t0 = time.perf_counter()
    i = 0
    while i < loop_iters:
        i += 1
    _ = time.perf_counter() - t0

# Measured runs
for _ in range(repeats):
    t0 = time.perf_counter()
    i = 0
    while i < loop_iters:
        i += 1
    t1 = time.perf_counter()
    times.append(t1 - t0)

times = np.array(times)
mean_time = float(np.mean(times))
std_time = float(np.std(times, ddof=1))
cv = float(std_time / mean_time) if mean_time > 0 else 0.0
median_time = float(np.median(times))
iqr_time = float(np.percentile(times, 75) - np.percentile(times, 25))

print(f"Timer noise test ({repeats} repeats of {loop_iters} empty iterations):")
print(f"  Mean: {mean_time*1000:.4f} ms")
print(f"  Std:  {std_time*1000:.4f} ms")
print(f"  CV:   {cv*100:.4f}%")
print(f"  Median: {median_time*1000:.4f} ms, IQR: {iqr_time*1000:.4f} ms")
print(f"  Core pinned: {pinned}")

# 2. Gather environment metadata
def get_cpu_info():
    info = {}
    try:
        with open('/proc/cpuinfo') as f:
            for line in f:
                if ':' in line:
                    k, v = [x.strip() for x in line.split(':', 1)]
                    if k == 'model name' and 'model_name' not in info:
                        info['model_name'] = v
                    elif k == 'cpu cores' and 'physical_cores_per_socket' not in info:
                        info['physical_cores_per_socket'] = int(v)
    except Exception as e:
        info['error'] = str(e)
    info['total_logical_cpus'] = os.cpu_count()
    return info

def get_cache_info():
    caches = {}
    cache_dir = '/sys/devices/system/cpu/cpu0/cache'
    if os.path.exists(cache_dir):
        for idx in sorted(os.listdir(cache_dir)):
            p = os.path.join(cache_dir, idx)
            if os.path.isdir(p):
                try:
                    level = open(os.path.join(p, 'level')).read().strip()
                    c_type = open(os.path.join(p, 'type')).read().strip()
                    size = open(os.path.join(p, 'size')).read().strip()
                    caches[f'L{level}_{c_type}'] = size
                except:
                    pass
    return caches

def get_mem_info():
    try:
        with open('/proc/meminfo') as f:
            for line in f:
                if line.startswith('MemTotal:'):
                    return line.split(':', 1)[1].strip()
    except Exception as e:
        return str(e)
    return 'unknown'

def get_compiler_info():
    try:
        res = subprocess.check_output(['g++', '--version'], text=True)
        return res.splitlines()[0]
    except Exception as e:
        return str(e)

import faiss
import hnswlib
import scipy
import sklearn

# Get git commit
try:
    git_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
except Exception:
    git_hash = 'unknown'

env_data = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    "environment": "WSL2 Ubuntu 26.04 on Windows 11",
    "os": {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "distro": "Ubuntu 26.04 LTS (WSL2)"
    },
    "cpu": get_cpu_info(),
    "cache": get_cache_info(),
    "ram": get_mem_info(),
    "compiler": {
        "cxx": get_compiler_info(),
        "cxx_flags": "-O3 -march=native -std=c++17 -fopenmp"
    },
    "hardware_counters": {
        "perf": "not available (Hyper-V virtual PMU counters disabled in WSL2 kernel)",
        "pmu": "not available"
    },
    "libraries": {
        "python": sys.version,
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "scikit-learn": sklearn.__version__,
        "faiss": getattr(faiss, '__version__', '1.15.1'),
        "hnswlib": "0.8.0"
    },
    "git_commit": git_hash,
    "timer_noise_test": {
        "repeats": repeats,
        "loop_iterations": loop_iters,
        "core_pinned": pinned,
        "mean_seconds": mean_time,
        "std_seconds": std_time,
        "cv_percent": cv * 100,
        "median_seconds": median_time,
        "iqr_seconds": iqr_time,
        "raw_times_seconds": [float(x) for x in times]
    },
    "datasets": {}  # to be populated once downloads complete
}

os.makedirs('experiments/results/E0', exist_ok=True)
with open('experiments/results/E0/env.json', 'w') as f:
    json.dump(env_data, f, indent=2)

print("\nWrote environment info to experiments/results/E0/env.json")
