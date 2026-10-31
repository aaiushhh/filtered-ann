with open("papers/rangefilters2026.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re

out = []

for m in re.finditer(r'(Lemma\s+[12][^\.\n]*[\.\n].*?)(?=(Lemma\s+\d|Theorem|\n\n\n|Proof|\Z))', text, re.DOTALL):
    start = max(0, m.start() - 300)
    end = min(len(text), m.end() + 500)
    out.append("================ MATCH ================\n" + text[start:end])

with open("tools/lemma_extract.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(out))

print("Dumped to tools/lemma_extract.txt")
