with open("papers/rangefilters2026.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find Lemma 1 and Lemma 2
for lemma in ["Lemma 1", "Lemma 2", "Lemma"]:
    matches = [m.start() for m in re.finditer(re.escape(lemma), text)]
    print(f"Found {len(matches)} matches for '{lemma}'")

idx1 = text.find("Lemma 1")
if idx1 != -1:
    print("--- LEMMA 1 CONTEXT ---")
    print(text[idx1-200:idx1+1000])

idx2 = text.find("Lemma 2")
if idx2 != -1:
    print("--- LEMMA 2 CONTEXT ---")
    print(text[idx2-200:idx2+1000])
