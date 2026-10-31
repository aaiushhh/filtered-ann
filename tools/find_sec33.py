with open("papers/rangefilters2026.txt", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("3.3 Hash-Based Compression")
if idx == -1:
    idx = text.find("3.3")

print("Found at:", idx)
if idx != -1:
    with open("tools/sec3_3_detail.txt", "w", encoding="utf-8") as f:
        f.write(text[idx:idx+4000])
    print("Wrote detail")
