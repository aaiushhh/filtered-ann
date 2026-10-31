with open("papers/rangefilters2026.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re

out = []
for line_idx, line in enumerate(text.split("\n"), 1):
    if any(k in line.lower() for k in ["alpha", "false positive", "probability", "lemma 1", "lemma 2", "bloom filter"]):
        out.append(f"L{line_idx}: {line}")

with open("tools/alpha_lines.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Dumped to tools/alpha_lines.txt")
