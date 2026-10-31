import csv
import math
from collections import defaultdict

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

def analyze_canary_pinning(file_default, file_pcore):
    print("=== SECTION E: CANARY PINNING COMPARISON (10 MINUTES EACH) ===")
    
    vals_default = []
    try:
        with open(file_default, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                vals_default.append(float(r['ns_per_probe']))
    except Exception as e:
        print(f"Error reading {file_default}: {e}")

    vals_pcore = []
    try:
        with open(file_pcore, 'r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                vals_pcore.append(float(r['ns_per_probe']))
    except Exception as e:
        print(f"Error reading {file_pcore}: {e}")

    med_d, iqr_d, min_d, max_d, std_d, q1_d, q3_d = compute_stats(vals_default)
    med_p, iqr_p, min_p, max_p, std_p, q1_p, q3_p = compute_stats(vals_pcore)

    print(f"Setting 1: Default Affinity")
    print(f"  Samples: {len(vals_default)}")
    print(f"  Median:  {med_d:.4f} ns/probe")
    print(f"  IQR:     {iqr_d:.4f} ns/probe (Q1={q1_d:.4f}, Q3={q3_d:.4f})")
    print(f"  Max:     {max_d:.4f} ns/probe (Min={min_d:.4f})")
    print(f"  StdDev:  {std_d:.4f} ns/probe")

    print(f"\nSetting 2: P-Core Restricted Affinity")
    print(f"  Samples: {len(vals_pcore)}")
    print(f"  Median:  {med_p:.4f} ns/probe")
    print(f"  IQR:     {iqr_p:.4f} ns/probe (Q1={q1_p:.4f}, Q3={q3_p:.4f})")
    print(f"  Max:     {max_p:.4f} ns/probe (Min={min_p:.4f})")
    print(f"  StdDev:  {std_p:.4f} ns/probe")

    lower_var = "Setting 2 (P-Core Restricted)" if std_p < std_d else "Setting 1 (Default Affinity)"
    print(f"\nSelected Lower-Variance Setting: {lower_var}")

def analyze_e1b_results():
    print("\n=== SECTION G: E1b BOOLEAN CHECK (AMQ vs Best Exact) ===")
    # Criteria: ns/probe at least 20% lower than best exact at measured FPR <= 2%, non-overlapping IQR over 5 repeats
    # For patterns: uniform_random and neighbor_list_32
    
    # Read raw_e1b to get Q1 and Q3 per cell and pattern
    cell_runs = defaultdict(list) # (cell_id, pattern) -> [ns_per_probe]
    cell_meta = {} # cell_id -> dict
    with open('experiments/results/E1b/raw_e1b.csv', 'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
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
        print(f"\n--- Probe Pattern: {pat} ---")
        # Group by (N, sigma)
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

        qualifying = []
        for (N, sigma), struct_list in sorted(by_n_sigma.items()):
            # Find exact structures
            exact_structs = [s for s in struct_list if s['structure'] in ['bitmap', 'hash_set']]
            if not exact_structs:
                continue
            best_exact = min(exact_structs, key=lambda x: x['med'])

            # Compare AMQ structures with FPR <= 0.02
            for s in struct_list:
                if s['structure'] not in ['bitmap', 'hash_set'] and s['measured_fpr'] <= 0.02:
                    speedup = (best_exact['med'] - s['med']) / best_exact['med']
                    is_20pct = (speedup >= 0.20)
                    # Non-overlapping IQR: s['q3'] < best_exact['q1']
                    non_overlap = (s['q3'] < best_exact['q1'])
                    if is_20pct and non_overlap:
                        qualifying.append({
                            'N': N,
                            'sigma': sigma,
                            'exact_name': f"{best_exact['structure']}_{best_exact['variant']}",
                            'exact_med': best_exact['med'],
                            'exact_q1': best_exact['q1'],
                            'exact_q3': best_exact['q3'],
                            'amq_name': f"{s['structure']}_{s['variant']}",
                            'amq_med': s['med'],
                            'amq_q1': s['q1'],
                            'amq_q3': s['q3'],
                            'fpr': s['measured_fpr'],
                            'speedup': speedup * 100.0
                        })

        print(f"Total qualifying (N, sigma, structure) configurations: {len(qualifying)}")
        if qualifying:
            print("N          | sigma   | best_exact       | exact_med | exact_IQR_range | amq_structure    | amq_med   | amq_IQR_range   | FPR        | speedup")
            print("------------------------------------------------------------------------------------------------------------------------------------------------")
            for q in qualifying:
                print(f"{q['N']:<10} | {q['sigma']:<7} | {q['exact_name']:<16} | {q['exact_med']:<9.2f} | [{q['exact_q1']:.2f}, {q['exact_q3']:.2f}]    | {q['amq_name']:<16} | {q['amq_med']:<9.2f} | [{q['amq_q1']:.2f}, {q['amq_q3']:.2f}]    | {q['fpr']:<10.5f} | +{q['speedup']:.1f}%")
        else:
            print("None.")

if __name__ == '__main__':
    analyze_canary_pinning('experiments/results/E1b/canary_default_affinity.csv', 'experiments/results/E1b/canary_pcore_affinity.csv')
    try:
        analyze_e1b_results()
    except Exception as e:
        print(f"Note: E1b summary analysis pending run completion ({e})")
