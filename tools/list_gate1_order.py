import csv

with open('manifest.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

group_order = {'D': 1, 'C': 2, 'A': 3, 'B': 4, 'E': 5}
eligible = [r for r in rows if r.get('full_text_status') == 'OK' and r.get('relevance') != 'PROPOSED-DROP']
eligible.sort(key=lambda x: (group_order.get(x['group'], 99), x['bibkey']))

print(f"Total eligible papers for Gate 1: {len(eligible)}")
for idx, e in enumerate(eligible, 1):
    print(f"{idx}. [{e['group']}] {e['bibkey']} - {e['title'][:70]} (version: {e['text_version']})")
