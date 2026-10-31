import os
import re

notes = sorted([f for f in os.listdir('notes') if f.endswith('.md')])

results = []

for f in notes:
    k = f.replace('.md', '')
    p = os.path.join('notes', f)
    with open(p, 'r', encoding='utf-8') as fp:
        content = fp.read()

    # Search for Novelty check
    m = re.search(r'Novelty check:[ \t]*([^\n]+(?:\n[^\n#]+)?)', content, re.IGNORECASE)
    raw = m.group(1).strip() if m else 'NOT FOUND'

    # Clean up raw
    clean_raw = ' '.join(raw.split())

    # Determine yes / no / unclear
    # Look for leading answer:
    ans = 'unclear'
    if re.search(r'\byes\b', clean_raw[:30], re.IGNORECASE):
        ans = 'yes'
    elif re.search(r'\bno\b', clean_raw[:30], re.IGNORECASE):
        ans = 'no'
    elif 'unclear' in clean_raw[:30].lower():
        ans = 'unclear'

    # Extract locator
    loc_match = re.findall(r'\([^)]*(?:p\.|§|Thm|Table|Figure)[^)]*\)', clean_raw)
    loc = loc_match[-1] if loc_match else 'in-text locator'

    results.append((k, ans, loc, clean_raw))

print(f"{'bibkey':<30} | {'Answer':<8} | {'Locator'}")
print("-" * 75)
for k, ans, loc, raw in results:
    print(f"{k:<30} | {ans:<8} | {loc}")
