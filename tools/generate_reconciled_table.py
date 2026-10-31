import os
import re

notes_keys = sorted([f.replace('.md', '') for f in os.listdir('notes') if f.endswith('.md')])

reconciled_table = []

for k in notes_keys:
    note_path = os.path.join('notes', f"{k}.md")
    with open(note_path, 'r', encoding='utf-8') as fp:
        c = fp.read()

    m = re.search(r'Novelty check:[ \t]*([^\n]+(?:\n[^\n#]+)?)', c, re.IGNORECASE)
    raw = ' '.join(m.group(0).split()) if m else 'NOT FOUND'
    after = re.sub(r'^(?:Novelty check:\s*)+', '', raw, flags=re.IGNORECASE).strip()

    ans = 'unclear'
    if after.lower().startswith('yes'):
        ans = 'yes'
    elif after.lower().startswith('no'):
        ans = 'no'

    # Extract locator from parentheses
    locators = re.findall(r'\([^)]*(?:p\.|§|Thm|Table|Figure)[^)]*\)', after)
    loc = locators[-1] if locators else 'in-text locator'

    reconciled_table.append((k, ans, loc, after))

# Print markdown table
print("| bibkey | Novelty Answer | Locator | Details |")
print("|---|:---:|---|---|")
for k, ans, loc, aft in reconciled_table:
    # clean aft for markdown table
    clean_detail = aft.replace('|', '\\|')
    print(f"| `{k}` | **{ans}** | {loc} | {clean_detail} |")
