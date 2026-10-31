with open("papers/survey2025filtered.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

idx = text.rfind("REFERENCES")
if idx == -1:
    idx = text.rfind("References")

print(f"References index: {idx}")
if idx != -1:
    print(text[idx:idx+1500])
