import csv

with open('experiments/results/E1/microbenchmarks_e1.csv', 'r') as f:
    rows = list(csv.DictReader(f))

# Let's inspect the 5 qualifying AMQ configurations in detail
print("=== DETAILED QUALIFYING AMQ TABLE ===")
for r in rows:
    # check conditions
    if r['probe_pattern'] == 'uniform_random' and r['N'] in ['100000000', '1000000000'] and r['sigma'] == '0.001':
        if r['structure'] in ['bitmap', 'xor', 'cuckoo']:
            print(f"N={r['N']} sigma={r['sigma']} struct={r['structure']} var={r['variant']} ns={r['ns_per_probe']} fpr={r['measured_fpr']} bytes={r['memory_bytes']}")
