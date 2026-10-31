with open("papers/rangefilters2026.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find occurrences of alpha in text
matches = [m.start() for m in re.finditer(r'(\\alpha|false positive|false-positive|probability)', text, re.IGNORECASE)]
print(f"Found {len(matches)} matches")

idx = text.find("Sec. 3.3")
if idx == -1:
    idx = text.find("3.3")

if idx != -1:
    with open("tools/sec3_3.txt", "w", encoding="utf-8") as f:
        f.write(text[idx:idx+3500])
    print("Dumped Sec 3.3")
