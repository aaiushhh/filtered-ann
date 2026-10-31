import csv
import math
from collections import defaultdict

def analyze_e1():
    # 1. Read microbenchmarks_e1.csv
    micro_rows = []
    with open("experiments/results/E1/microbenchmarks_e1.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            micro_rows.append({
                'cell_id': int(r['cell_id']),
                'N': int(r['N']),
                'sigma': float(r['sigma']),
                'structure': r['structure'],
                'variant': r['variant'],
                'probe_pattern': r['probe_pattern'],
                'ns_per_probe': float(r['ns_per_probe']),
                'measured_fpr': float(r['measured_fpr']),
                'theoretical_fpr': float(r['theoretical_fpr']),
                'memory_bytes': int(r['memory_bytes']),
                'build_time_s': float(r['build_time_s']),
                'canary_before_ns': float(r['canary_before_ns']),
                'canary_after_ns': float(r['canary_after_ns']),
                'canary_diff_pct': float(r['canary_diff_pct']),
                'flagged': r['flagged'] == 'TRUE'
            })

    # 2. Read canary_log.csv
    canary_rows = []
    with open("experiments/results/E1/canary_log.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            canary_rows.append({
                'cell_id': int(r['cell_id']),
                'structure': r['structure'],
                'N': int(r['N']),
                'sigma': float(r['sigma']),
                'canary_before_ns': float(r['canary_before_ns']),
                'canary_after_ns': float(r['canary_after_ns']),
                'diff_pct': float(r['diff_pct']),
                'flagged': r['flagged'] == 'TRUE'
            })

    # 3. Read skip_list.csv
    skip_rows = []
    with open("experiments/results/E1/skip_list.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            skip_rows.append(r)

    print("=== GATE E1 RAW COUNTS ===")
    print(f"Total microbenchmark rows: {len(micro_rows)}")
    unique_cells = len(set(r['cell_id'] for r in micro_rows))
    print(f"Total unique cells executed: {unique_cells}")
    print(f"Total skipped cells: {len(skip_rows)}")
    print(f"Total planned cells: {unique_cells + len(skip_rows)}")

    # Canary analysis
    canary_diffs = [r['diff_pct'] for r in canary_rows]
    flagged_canary = [r for r in canary_rows if r['flagged']]
    mean_diff = sum(canary_diffs) / len(canary_diffs) if canary_diffs else 0
    sorted_diffs = sorted(canary_diffs)
    med_diff = sorted_diffs[len(sorted_diffs)//2] if sorted_diffs else 0
    max_diff = max(canary_diffs) if canary_diffs else 0

    print("\n=== CANARY BENCHMARK LOG SUMMARY ===")
    print(f"Total canary tests: {len(canary_rows)}")
    print(f"Canary drift mean: {mean_diff:.2f}%")
    print(f"Canary drift median: {med_diff:.2f}%")
    print(f"Canary drift max: {max_diff:.2f}%")
    print(f"Flagged cells (>5% drift): {len(flagged_canary)} / {len(canary_rows)} ({len(flagged_canary)/len(canary_rows)*100:.2f}%)")

    # Skip list
    print("\n=== SKIP LIST (Memory > 50% RAM ~3.79 GB) ===")
    print(f"{'N':<12} | {'sigma':<8} | {'structure':<16} | {'variant':<8} | {'memory_MB':<10} | {'reason'}")
    print("-" * 80)
    for r in skip_rows:
        mb = int(r['est_memory_bytes']) / 1e6
        print(f"{int(r['N']):<12} | {float(r['sigma']):<8} | {r['structure']:<16} | {r['variant']:<8} | {mb:<10.1f} | {r['reason']}")

    # Cache step up check (Requirement 5)
    print("\n=== CACHE STEP-UP BOOLEAN CHECK (Requirement 5) ===")
    print("Evaluating bitmap and attribute_array under uniform random probes:")
    print("Cache thresholds: L2 = 1.25 MB (1,250,000 bytes), L3 = 24.0 MB (24,000,000 bytes)")

    # Group by structure and N
    u_rows = [r for r in micro_rows if r['probe_pattern'] == 'uniform_random']

    # Bitmap
    bm_by_N = defaultdict(list)
    for r in u_rows:
        if r['structure'] == 'bitmap':
            bm_by_N[r['N']].append(r)

    print("\nBitmap:")
    bm_summary = []
    for N in sorted(bm_by_N.keys()):
        rows = bm_by_N[N]
        avg_ns = sum(x['ns_per_probe'] for x in rows) / len(rows)
        bytes_val = rows[0]['memory_bytes']
        mb = bytes_val / 1e6
        tier = "L2 (<1.25 MB)" if bytes_val < 1250000 else ("L3 (1.25-24 MB)" if bytes_val <= 24000000 else "RAM (>24 MB)")
        bm_summary.append((N, bytes_val, mb, avg_ns, tier))
        print(f"  N={N:<10} | Bytes: {bytes_val:<10} ({mb:6.2f} MB) | Tier: {tier:<16} | ns/probe: {avg_ns:.2f}")

    # Attribute array
    aa_by_N = defaultdict(list)
    for r in u_rows:
        if r['structure'] == 'attribute_array':
            aa_by_N[r['N']].append(r)

    print("\nAttribute Array:")
    aa_summary = []
    for N in sorted(aa_by_N.keys()):
        rows = aa_by_N[N]
        avg_ns = sum(x['ns_per_probe'] for x in rows) / len(rows)
        bytes_val = rows[0]['memory_bytes']
        mb = bytes_val / 1e6
        tier = "L2 (<1.25 MB)" if bytes_val < 1250000 else ("L3 (1.25-24 MB)" if bytes_val <= 24000000 else "RAM (>24 MB)")
        aa_summary.append((N, bytes_val, mb, avg_ns, tier))
        print(f"  N={N:<10} | Bytes: {bytes_val:<10} ({mb:6.2f} MB) | Tier: {tier:<16} | ns/probe: {avg_ns:.2f}")

    # Step up evaluation
    print("\nStep-up Boolean Evaluation:")
    # For bitmap:
    # Size 1 (125 KB, L2) -> Size 2 (1.25 MB, L2/L3 boundary) -> Size 3 (12.5 MB, L3) -> Size 4 (125 MB, RAM)
    bm_step_L2_to_L3 = bm_summary[2][3] > bm_summary[0][3]  # 12.5 MB vs 125 KB
    bm_step_L3_to_RAM = bm_summary[3][3] > bm_summary[2][3] # 125 MB vs 12.5 MB
    print(f"  Bitmap steps up near 1.25 MB (L2 -> L3): {bm_step_L2_to_L3} (from {bm_summary[0][3]:.2f} ns at 125 KB to {bm_summary[2][3]:.2f} ns at 12.5 MB)")
    print(f"  Bitmap steps up near 24 MB (L3 -> RAM):   {bm_step_L3_to_RAM} (from {bm_summary[2][3]:.2f} ns at 12.5 MB to {bm_summary[3][3]:.2f} ns at 125 MB)")

    # For attribute array:
    # Size 1 (4.0 MB, L3) -> Size 2 (40 MB, RAM) -> Size 3 (400 MB, RAM) -> Size 4 (skipped)
    aa_step_L3_to_RAM = aa_summary[1][3] > aa_summary[0][3]
    print(f"  Attribute array steps up near 24 MB (L3 -> RAM): {aa_step_L3_to_RAM} (from {aa_summary[0][3]:.2f} ns at 4 MB to {aa_summary[1][3]:.2f} ns at 40 MB)")

    # 4. AMQ vs Best Exact Check (EXPERIMENTS.md §5 E1)
    # "does any AMQ structure have ns/probe at least 20% lower than the best exact structure at measured FPR <= 2%? In which (N, sigma) cells?"
    print("\n=== EXPERIMENTS.md §5 (E1) CHECK: AMQ vs Best Exact (ns/probe <= 0.80 * Best Exact at FPR <= 2%) ===")
    exact_names = {'attribute_array', 'bitmap', 'hash_set'}

    for pattern in ['uniform_random', 'batch_32']:
        print(f"\n--- Probe Pattern: {pattern} ---")
        p_rows = [r for r in micro_rows if r['probe_pattern'] == pattern]

        # Group by (N, sigma)
        grouped = defaultdict(list)
        for r in p_rows:
            grouped[(r['N'], r['sigma'])].append(r)

        qualifying_cells = []
        for (c_N, c_sigma), rows in sorted(grouped.items()):
            exacts = [r for r in rows if r['structure'] in exact_names]
            if not exacts:
                continue
            best_exact = min(exacts, key=lambda x: x['ns_per_probe'])
            threshold = 0.80 * best_exact['ns_per_probe']

            # Find AMQs with measured_fpr <= 0.02 and ns_per_probe <= threshold
            better_amqs = [r for r in rows if r['structure'] not in exact_names and r['measured_fpr'] <= 0.02 and r['ns_per_probe'] <= threshold]
            if better_amqs:
                for b in better_amqs:
                    qualifying_cells.append({
                        'N': c_N,
                        'sigma': c_sigma,
                        'best_exact_name': f"{best_exact['structure']}_{best_exact['variant']}",
                        'best_exact_ns': best_exact['ns_per_probe'],
                        'amq_name': f"{b['structure']}_{b['variant']}",
                        'amq_ns': b['ns_per_probe'],
                        'amq_fpr': b['measured_fpr'],
                        'speedup_pct': (1.0 - b['ns_per_probe'] / best_exact['ns_per_probe']) * 100
                    })

        print(f"Total qualifying (N, sigma, structure) configurations: {len(qualifying_cells)}")
        if qualifying_cells:
            print(f"{'N':<12} | {'sigma':<8} | {'best_exact':<22} | {'exact_ns':<10} | {'amq':<22} | {'amq_ns':<10} | {'FPR':<10} | {'gain_%'}")
            print("-" * 110)
            for q in qualifying_cells:
                print(f"{q['N']:<12} | {q['sigma']:<8} | {q['best_exact_name']:<22} | {q['best_exact_ns']:<10.2f} | {q['amq_name']:<22} | {q['amq_ns']:<10.2f} | {q['amq_fpr']:<10.5f} | {q['speedup_pct']:.1f}%")
        else:
            print("None.")

if __name__ == '__main__':
    analyze_e1()
