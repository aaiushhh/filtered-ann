import csv

def clean_csv(path, key_fields):
    rows = []
    header = None
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for line_num, r in enumerate(reader):
            if line_num == 0:
                header = r
                continue
            if not r or len(r) != len(header):
                print(f"Skipping malformed row at line {line_num} in {path}: {r}")
                continue
            rows.append(r)
    
    # Deduplicate by key_fields, keeping latest
    seen = {}
    for r in rows:
        key = tuple(r[k] for k in key_fields)
        seen[key] = r
    
    cleaned_rows = list(seen.values())
    print(f"{path}: original rows {len(rows)}, deduplicated {len(cleaned_rows)}")
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in cleaned_rows:
            writer.writerow(r)

if __name__ == '__main__':
    # Clean canary_log: key = (cell_id,)
    clean_csv("experiments/results/E1/canary_log.csv", [0])
    # Clean microbenchmarks_e1: key = (cell_id, probe_pattern)
    clean_csv("experiments/results/E1/microbenchmarks_e1.csv", [0, 5])
    # Clean raw.csv: key = (run_id,)
    clean_csv("experiments/results/E1/raw.csv", [0])
