with open("papers/gupta2023caps.txt", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("5 CAPS")
if idx == -1:
    idx = text.find("5 ")
print("Section 5 at:", idx)
if idx != -1:
    print(text[idx:idx+2500])
