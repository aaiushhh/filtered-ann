with open("papers/survey2025filtered.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

import re

matches = re.findall(r'.{0,100}multifilter.{0,100}', text, re.IGNORECASE)
print(f"Matches for multifilter in survey: {len(matches)}")
for m in matches[:10]:
    print(" ", m.strip())

matches2 = re.findall(r'.{0,100}multi-filter.{0,100}', text, re.IGNORECASE)
print(f"Matches for multi-filter in survey: {len(matches2)}")
for m in matches2[:10]:
    print(" ", m.strip())
