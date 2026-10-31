import csv

with open('manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows in manifest: {len(rows)}")
for r in rows:
    print(f"{r['bibkey']}: group={r['group']}, status={r.get('status', '')}, full_text={r.get('full_text_status', '')}")
