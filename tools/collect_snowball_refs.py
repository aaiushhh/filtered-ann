import os
import re

notes = sorted([f for f in os.listdir('notes') if f.endswith('.md')])

cited_dict = {}

for f in notes:
    k = f.replace('.md', '')
    p = os.path.join('notes', f)
    with open(p, 'r', encoding='utf-8') as fp:
        c = fp.read()

    m = re.search(r'## Useful references[^\n]*\n(.*)', c, re.DOTALL)
    if m:
        lines = [l.strip() for l in m.group(1).split('\n') if l.strip().startswith('-')]
        for l in lines:
            entry = l.lstrip('-').strip()
            cited_dict.setdefault(entry, []).append(k)

print(f"Total extracted reference entries: {len(cited_dict)}")
# Sort by number of citing notes
sorted_refs = sorted(cited_dict.items(), key=lambda x: len(x[1]), reverse=True)
for ref, citing in sorted_refs[:25]:
    print(f"[{len(citing)} notes] {ref}")
    print(f"   Cited by: {', '.join(citing[:5])}")
