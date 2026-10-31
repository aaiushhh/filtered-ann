import csv
import math

with open('experiments/results/E1/microbenchmarks_e1.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows: {len(rows)}")

# 1. Blocked Bloom FPR vs Standard Bloom Formula
print("\n=== BLOCKED BLOOM FPR VS STANDARD BLOOM FORMULA ===")
bb_rows = [r for r in rows if r['structure'] == 'bloom_blocked' and r['probe_pattern'] == 'uniform_random']
by_variant = {}
for r in bb_rows:
    v = r['variant']
    if v not in by_variant:
        by_variant[v] = []
    by_variant[v].append(float(r['measured_fpr']))

print("variant | bits_per_entry | k | standard_formula | measured_fpr_mean | measured_fpr_min | measured_fpr_max")
for v in ['b6', 'b8', 'b10', 'b12', 'b16']:
    b = int(v[1:])
    k = math.floor(b * math.log(2))
    std_fpr = (1.0 - math.exp(-k / b)) ** k
    vals = by_variant.get(v, [])
    mean_val = sum(vals)/len(vals) if vals else 0
    min_val = min(vals) if vals else 0
    max_val = max(vals) if vals else 0
    print(f"{v} | {b} | {k} | {std_fpr:.6f} | {mean_val:.6f} | {min_val:.6f} | {max_val:.6f}")

# Standard Bloom FPR vs Formula for comparison
print("\n=== STANDARD BLOOM FPR VS STANDARD FORMULA ===")
std_bloom_rows = [r for r in rows if r['structure'] == 'bloom_standard' and r['probe_pattern'] == 'uniform_random']
by_v_std = {}
for r in std_bloom_rows:
    v = r['variant']
    if v not in by_v_std:
        by_v_std[v] = []
    by_v_std[v].append(float(r['measured_fpr']))

for v in ['b6', 'b8', 'b10', 'b12', 'b16']:
    b = int(v[1:])
    k = math.floor(b * math.log(2))
    std_fpr = (1.0 - math.exp(-k / b)) ** k
    vals = by_v_std.get(v, [])
    mean_val = sum(vals)/len(vals) if vals else 0
    min_val = min(vals) if vals else 0
    max_val = max(vals) if vals else 0
    print(f"{v} | {b} | {k} | {std_fpr:.6f} | {mean_val:.6f} | {min_val:.6f} | {max_val:.6f}")

# Cuckoo Filter FPR
print("\n=== CUCKOO FILTER FPR ===")
cuckoo_rows = [r for r in rows if r['structure'] == 'cuckoo' and r['probe_pattern'] == 'uniform_random']
by_cuckoo = {}
for r in cuckoo_rows:
    v = r['variant']
    if v not in by_cuckoo:
        by_cuckoo[v] = []
    by_cuckoo[v].append(float(r['measured_fpr']))

for v in ['8bit', '12bit', '16bit']:
    vals = by_cuckoo.get(v, [])
    mean_val = sum(vals)/len(vals) if vals else 0
    min_val = min(vals) if vals else 0
    max_val = max(vals) if vals else 0
    print(f"{v} | mean={mean_val:.6f} | min={min_val:.6f} | max={max_val:.6f}")

# Xor Filter FPR
print("\n=== XOR FILTER FPR ===")
xor_rows = [r for r in rows if r['structure'] == 'xor' and r['probe_pattern'] == 'uniform_random']
by_xor = {}
for r in xor_rows:
    v = r['variant']
    if v not in by_xor:
        by_xor[v] = []
    by_xor[v].append(float(r['measured_fpr']))

for v in ['8bit', '16bit']:
    vals = by_xor.get(v, [])
    mean_val = sum(vals)/len(vals) if vals else 0
    min_val = min(vals) if vals else 0
    max_val = max(vals) if vals else 0
    print(f"{v} | mean={mean_val:.6f} | min={min_val:.6f} | max={max_val:.6f}")

print("\n=== CANARY DRIFT BY N ===")
by_n_drift = {}
with open('experiments/results/E1/canary_log.csv', 'r') as f:
    c_reader = csv.DictReader(f)
    for r in c_reader:
        n = r['N']
        if n not in by_n_drift:
            by_n_drift[n] = []
        by_n_drift[n].append(float(r['diff_pct']))

for n in ['1000000', '10000000', '100000000', '1000000000']:
    d = by_n_drift.get(n, [])
    if d:
        mean_d = sum(d)/len(d)
        flagged = sum(1 for x in d if x > 5.0)
        print(f"N={n} | count={len(d)} | mean_drift={mean_d:.2f}% | max_drift={max(d):.2f}% | flagged={flagged}/{len(d)} ({flagged/len(d)*100:.1f}%)")

print("\n=== LATENCY COMPARISON: UNIFORM RANDOM VS BATCH 32 (AT N=1e7, sigma=0.01) ===")
for r in rows:
    if r['N'] == '10000000' and r['sigma'] == '0.01':
        print(f"{r['structure']} ({r['variant']}) | pattern={r['probe_pattern']} | ns={float(r['ns_per_probe']):.2f} | bytes={int(r['memory_bytes']):,}")
