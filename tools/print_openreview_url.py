with open("papers/filteraware2025.txt", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("Multifilterann:")
print(text[idx-50:idx+350])
