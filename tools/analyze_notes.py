import os
import re
import csv

notes = sorted([f for f in os.listdir('notes') if f.endswith('.md')])
print(f"Checking {len(notes)} notes...")

table = []
flags_dict = {}
not_stated_dict = {}

for f in notes:
    k = f.replace('.md', '')
    p = os.path.join('notes', f)
    with open(p, 'r', encoding='utf-8') as fp:
        content = fp.read()

    # Check Novelty check
    m_nov = re.search(r'Novelty check:\s*([^\n]+)', content, re.IGNORECASE)
    nov_str = m_nov.group(1).strip() if m_nov else 'NOT FOUND'
    
    # extract answer & locator
    ans = 'unclear'
    if re.search(r'\byes\b', nov_str, re.IGNORECASE):
        ans = 'yes'
    elif re.search(r'\bno\b', nov_str, re.IGNORECASE):
        ans = 'no'

    table.append((k, ans, nov_str))

    # Check Flags
    m_flags = re.search(r'## Flags[^\n]*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    flags_text = m_flags.group(1).strip() if m_flags else ''
    if flags_text and flags_text.lower() not in ['none', 'none.', 'none stated', 'none stated.', 'none observed.', 'none observed']:
        flags_dict[k] = flags_text

    # Count 'not stated'
    ns_matches = re.findall(r'not stated', content, re.IGNORECASE)
    if len(ns_matches) >= 2:
        not_stated_dict[k] = (len(ns_matches), ns_matches)

print(f"Notes with Flags: {len(flags_dict)}")
for k, fl in flags_dict.items():
    print(f"  [{k}]: {fl[:100]}...")

print(f"\nNotes with >=2 not stated: {len(not_stated_dict)}")
for k, (cnt, matches) in not_stated_dict.items():
    print(f"  [{k}]: {cnt} occurrences")

yes_count = sum(1 for t in table if t[1] == 'yes')
no_count = sum(1 for t in table if t[1] == 'no')
unclear_count = sum(1 for t in table if t[1] == 'unclear')
print(f"\nNovelty check answers: yes={yes_count}, no={no_count}, unclear={unclear_count}")
