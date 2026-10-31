with open("papers/rangefilters2026.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'3\.3\s+[^\n]+', text)]
for m in matches:
    print("Match at", m, ":", text[m:m+100])

if matches:
    pos = matches[-1]
    with open("tools/sec33_heading.txt", "w", encoding="utf-8") as f:
        f.write(text[pos:pos+4000])
