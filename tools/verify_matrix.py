import csv

with open('matrix.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Matrix rows: {len(rows)}")
print(f"Columns ({len(reader.fieldnames)}): {reader.fieldnames}")

nov_counts = {}
sel_counts = {}
for r in rows:
    nov = r['novelty_check']
    sel = r['selectivity_cost_model'].split()[0]
    nov_counts[nov] = nov_counts.get(nov, 0) + 1
    sel_counts[sel] = sel_counts.get(sel, 0) + 1

print('novelty_check counts in matrix.csv:', nov_counts)
print('selectivity_cost_model counts in matrix.csv:', sel_counts)

print('\nPapers with selectivity_cost_model = yes:')
for r in rows:
    if r['selectivity_cost_model'].startswith('yes'):
        print(f"  {r['bibkey']}: {r['selectivity_cost_model']}")
