import os
import re

notes = sorted([f for f in os.listdir('notes') if f.endswith('.md')])

print("bibkey | yes/no/unclear | locator")
print("---|---|---")

for f in notes:
    k = f.replace('.md', '')
    p = os.path.join('notes', f)
    with open(p, 'r', encoding='utf-8') as fp:
        content = fp.read()

    m_nov = re.search(r'Novelty check:\s*([^\n]+)', content, re.IGNORECASE)
    nov_str = m_nov.group(1).strip() if m_nov else 'none stated'

    ans = 'unclear'
    # Match starting with yes or no
    if re.search(r'^\*{0,2}yes\b', nov_str, re.IGNORECASE):
        ans = 'yes'
    elif re.search(r'^\*{0,2}no\b', nov_str, re.IGNORECASE):
        ans = 'no'

    # Extract locator from parentheses or text if present
    # Usually at the end like (p. X, §Y)
    loc_match = re.findall(r'\([^)]*p\.[^)]*\)', nov_str)
    if loc_match:
        loc = loc_match[-1]
    else:
        # search for any (p. or (§ or (Thm
        loc_match2 = re.findall(r'\([^)]*(?:p\.|§|Thm|Table)[^)]*\)', nov_str)
        if loc_match2:
            loc = loc_match2[-1]
        else:
            loc = 'in-text locator'

    print(f"`{k}` | **{ans}** | {nov_str}")
