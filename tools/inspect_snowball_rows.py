import csv
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('manifest.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f'Total rows in manifest: {len(rows)}')
snowball_rows = [r for r in rows if r.get('origin') == 'snowball']
print(f'Snowball rows: {len(snowball_rows)}')

# Also check which keys exist in notes/ and refs.bib
with open('refs.bib', encoding='utf-8') as f:
    bib_text = f.read()

import os
notes = [f[:-3] for f in os.listdir('notes') if f.endswith('.md')]

print(f'\nDetailed Snowball Rows Breakdown ({len(snowball_rows)} total):')
print(f"{'bibkey':<30} | {'in_notes?':<10} | {'in_bib?':<10} | {'identifier':<30} | {'title'}")
print('-' * 120)

for r in snowball_rows:
    bk = r['bibkey']
    in_n = 'YES' if bk in notes else 'no'
    in_b = 'YES' if f'{{{bk},' in bib_text else 'no'
    ident = r.get('doi') or r.get('arxiv_id') or 'none'
    title = r.get('title', '')
    print(f"{bk:<30} | {in_n:<10} | {in_b:<10} | {ident:<30} | {title}")
