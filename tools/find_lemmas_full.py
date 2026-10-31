with open("papers/rangefilters2026.txt", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("Time Complexity.Let D<")
with open("tools/sec33_lemmas_full.txt", "w", encoding="utf-8") as f:
    f.write(text[idx:idx+4000])

print("Wrote lemmas full")
