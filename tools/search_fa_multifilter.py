with open("papers/filteraware2025.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

matches = re.findall(r'.{0,100}multifilter.{0,100}', text, re.IGNORECASE)
print(f"Matches for multifilter: {len(matches)}")
for m in matches[:5]:
    print(" ", m.strip())

matches2 = re.findall(r'.{0,100}multi-filter.{0,100}', text, re.IGNORECASE)
print(f"Matches for multi-filter: {len(matches2)}")
for m in matches2[:5]:
    print(" ", m.strip())
