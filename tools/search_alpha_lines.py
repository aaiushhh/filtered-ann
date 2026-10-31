with open("papers/rangefilters2026.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re

for line in text.split("\n"):
    if any(k in line.lower() for k in ["alpha", "false positive", "probability", "lemma 1", "lemma 2"]):
        print(line[:120])
