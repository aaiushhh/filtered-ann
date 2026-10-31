with open("papers/filteraware2025.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'Bernstein', text)]
for m in matches:
    print("Match at:", m)
    print(text[m-20:m+300])
