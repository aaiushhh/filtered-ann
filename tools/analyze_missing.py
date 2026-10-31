import csv

with open('manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

orig_rows = rows[:27]
added_rows = rows[27:]

print('=== ORIGINAL SEED PAPERS (27 total) ===')
orig_ok = [r for r in orig_rows if r.get('full_text_status') == 'OK']
orig_paywalled = [r for r in orig_rows if r.get('full_text_status') == 'PAYWALLED']
orig_skipped = [r for r in orig_rows if r.get('relevance') == 'PROPOSED-DROP']

print(f'Original Seed Papers: Total=27, OK={len(orig_ok)}, PAYWALLED/MISSING={len(orig_paywalled)}, PROPOSED-DROP={len(orig_skipped)}')
print('\nMissing Original Seed Papers:')
for r in orig_paywalled:
    print(f"  - [{r['group']}] {r['bibkey']}: {r['title']} (DOI: {r.get('doi', 'none')})")

print('\n=== GATE 0.5 ADDITIONS (10 total) ===')
add_ok = [r for r in added_rows if r.get('full_text_status') == 'OK']
add_paywalled = [r for r in added_rows if r.get('full_text_status') == 'PAYWALLED']
print(f'Added Papers: Total=10, OK={len(add_ok)}, PAYWALLED/MISSING={len(add_paywalled)}')
print('\nMissing Added Papers:')
for r in add_paywalled:
    print(f"  - [{r['group']}] {r['bibkey']}: {r['title']} (DOI: {r.get('doi', 'none')})")
