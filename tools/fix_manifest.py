"""
Task 1: Fix manifest.csv
- ren2020hmann, xu2024multifilterann, zuo2023arkgraph: set IDs to UNVERIFIED
- li2025sieve, gupta2023caps: update titles to API titles
"""
import csv
import datetime

with open('manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

changes = []
for r in rows:
    bk = r['bibkey']
    
    if bk == 'ren2020hmann':
        old_arxiv = r['arxiv_id']
        r['arxiv_id'] = 'UNVERIFIED - DO NOT USE'
        changes.append(f"{bk}.arxiv_id: \"{old_arxiv}\" -> \"UNVERIFIED - DO NOT USE\"")
    
    elif bk == 'xu2024multifilterann':
        old_arxiv = r['arxiv_id']
        r['arxiv_id'] = 'UNVERIFIED - DO NOT USE'
        changes.append(f"{bk}.arxiv_id: \"{old_arxiv}\" -> \"UNVERIFIED - DO NOT USE\"")
    
    elif bk == 'zuo2023arkgraph':
        old_doi = r['doi']
        r['doi'] = 'UNVERIFIED - DO NOT USE'
        changes.append(f"{bk}.doi: \"{old_doi}\" -> \"UNVERIFIED - DO NOT USE\"")
    
    elif bk == 'li2025sieve':
        old_title = r['title']
        new_title = 'SIEVE: Effective Filtered Vector Search with Collection of Indexes'
        r['title'] = new_title
        changes.append(f"{bk}.title: \"{old_title}\" -> \"{new_title}\"")
    
    elif bk == 'gupta2023caps':
        old_title = r['title']
        new_title = 'CAPS: A Practical Partition Index for Filtered Similarity Search'
        r['title'] = new_title
        changes.append(f"{bk}.title: \"{old_title}\" -> \"{new_title}\"")

with open('manifest.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

now = datetime.datetime.now().isoformat()
with open('LOG.md', 'a', encoding='utf-8') as f:
    f.write(f'\n{now} — Task 1 (Final fix pass): manifest.csv updated ({len(changes)} changes):\n')
    for c in changes:
        f.write(f'  - {c}\n')

print(f"Done. {len(changes)} changes:")
for c in changes:
    print(f"  {c}")
