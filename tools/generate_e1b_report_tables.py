import csv
from collections import defaultdict
import math

def compute_stats(vals):
    if not vals:
        return 0, 0, 0, 0, 0, 0
    s_vals = sorted(vals)
    n = len(s_vals)
    min_v = s_vals[0]
    max_v = s_vals[-1]
    med = s_vals[n//2] if n % 2 == 1 else 0.5 * (s_vals[n//2 - 1] + s_vals[n//2])
    q1 = s_vals[n//4]
    q3 = s_vals[3*n//4]
    iqr = q3 - q1
    mean = sum(vals) / n
    var = sum((x - mean)**2 for x in vals) / (n - 1) if n > 1 else 0
    std = math.sqrt(var)
    return med, iqr, min_v, max_v, std, q1, q3

def main():
    print("=== GENERATING E1b REPORT TABLES ===")

    # 1. Canary Pinning Table
    print("\n## 1. Pinning Comparison (10 Minutes Each)")
    for name, path in [("Setting 1 (Default Affinity)", "experiments/results/E1b/canary_default_affinity.csv"),
                       ("Setting 2 (Host P-Core Affinity 0x0FFF)", "experiments/results/E1b/canary_pcore_affinity.csv")]:
        vals = []
        with open(path, 'r') as f:
            for r in csv.DictReader(f):
                vals.append(float(r['ns_per_probe']))
        med, iqr, min_v, max_v, std, q1, q3 = compute_stats(vals)
        print(f"| {name} | {len(vals)} | {med:.4f} | {iqr:.4f} | [{q1:.4f}, {q3:.4f}] | {min_v:.4f} | {max_v:.4f} | {std:.4f} |")

    # 2. Blocked Bloom Unit Test Table
    print("\n## 2. Blocked Bloom Unit Test (filters.hpp)")
    for bpe in [6.0, 8.0, 10.0, 12.0, 16.0]:
        k = round(bpe * math.log(2))
        std_fpr = (1.0 - math.exp(-k / bpe)) ** k
        # Read from test_blocked_bloom_unit output or summary
        # Let's extract from summary_e1b at N=1e7, sigma=0.001
        pass

    # 3. Mixed Pressure Table
    print("\n## 3. Mixed-Pressure Test Summary (ns per probe + fetch)")
    print("| N | sigma | Structure | Variant | Median (ns) | IQR (ns) | Min (ns) | Max (ns) | Filter Bytes |")
    print("|---|---|---|---|---|---|---|---|---|")
    # Read mixed_pressure_summary.csv, taking the latest rerun if cell ran twice
    mixed_cells = {}
    with open('experiments/results/E1b/mixed_pressure_summary.csv', 'r') as f:
        for r in csv.DictReader(f):
            cid = int(r['cell_id'])
            mixed_cells[cid] = r
    for cid, r in sorted(mixed_cells.items(), key=lambda x: (int(x[1]['N']), float(x[1]['sigma']), x[1]['structure'])):
        print(f"| {r['N']} | {r['sigma']} | {r['structure']} | {r['variant']} | {float(r['median_ns']):.2f} | {float(r['iqr_ns']):.2f} | {float(r['min_ns']):.2f} | {float(r['max_ns']):.2f} | {int(r['memory_bytes']):,} |")

    # 4. E1b Reduced Grid Boolean Check Table
    print("\n## 4. E1b Boolean Checks")
    # parse raw_e1b
    cell_runs = defaultdict(list)
    cell_meta = {}
    with open('experiments/results/E1b/raw_e1b.csv', 'r') as f:
        for r in csv.DictReader(f):
            cid = int(r['cell_id'])
            pat = r['probe_pattern']
            cell_runs[(cid, pat)].append(float(r['ns_per_probe']))
            if cid not in cell_meta:
                cell_meta[cid] = {
                    'N': int(r['N']),
                    'sigma': float(r['sigma']),
                    'structure': r['structure'],
                    'variant': r['variant'],
                    'measured_fpr': float(r['measured_fpr']),
                    'memory_bytes': int(r['memory_bytes'])
                }

    for pat in ["uniform_random", "neighbor_list_32", "sequential_32"]:
        print(f"\n### Probe Pattern: {pat}")
        by_n_sigma = defaultdict(list)
        for (cid, p), vals in cell_runs.items():
            if p == pat:
                meta = cell_meta[cid]
                med, iqr, min_v, max_v, std, q1, q3 = compute_stats(vals)
                row_info = dict(meta)
                row_info['cell_id'] = cid
                row_info['med'] = med
                row_info['iqr'] = iqr
                row_info['q1'] = q1
                row_info['q3'] = q3
                by_n_sigma[(meta['N'], meta['sigma'])].append(row_info)

        print("| N | sigma | Best Exact | Exact Med (ns) | Exact IQR | Qualifying AMQ | AMQ Med (ns) | AMQ IQR | AMQ FPR | Speedup (%) | Non-Overlapping IQR? |")
        print("|---|---|---|---|---|---|---|---|---|---|---|")
        has_any = False
        for (N, sigma), struct_list in sorted(by_n_sigma.items()):
            exact_structs = [s for s in struct_list if s['structure'] in ['bitmap', 'hash_set']]
            if not exact_structs: continue
            best_exact = min(exact_structs, key=lambda x: x['med'])
            for s in struct_list:
                if s['structure'] not in ['bitmap', 'hash_set'] and s['measured_fpr'] <= 0.02:
                    speedup = (best_exact['med'] - s['med']) / best_exact['med']
                    is_20pct = (speedup >= 0.20)
                    non_overlap = (s['q3'] < best_exact['q1'])
                    if is_20pct and non_overlap:
                        has_any = True
                        print(f"| {N} | {sigma} | {best_exact['structure']}_{best_exact['variant']} | {best_exact['med']:.2f} | [{best_exact['q1']:.2f}, {best_exact['q3']:.2f}] | {s['structure']}_{s['variant']} | {s['med']:.2f} | [{s['q1']:.2f}, {s['q3']:.2f}] | {s['measured_fpr']:.5f} | +{speedup*100:.1f}% | TRUE |")
        if not has_any:
            print("| None | - | - | - | - | - | - | - | - | - | FALSE |")

if __name__ == '__main__':
    main()
