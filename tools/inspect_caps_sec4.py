with open("papers/gupta2023caps.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re

for heading in ["4 Algorithm", "5 Theoretical", "6 Evaluation", "Analysis"]:
    pos = text.find(heading)
    print(f"Heading {heading}: pos={pos}")

idx = text.find("4 CAPS")
if idx == -1:
    idx = text.find("4 ")
print("Section 4 at:", idx)
if idx != -1:
    print(text[idx:idx+2000])
