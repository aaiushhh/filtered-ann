with open("papers/filteraware2025.txt", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("Bernstein, P. A.")
print(text[idx:idx+400])
