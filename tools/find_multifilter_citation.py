with open("papers/filteraware2025.txt", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("MultiFilterANN paper")
if idx != -1:
    print(text[idx-100:idx+400])

# Also check bibliography in filteraware2025
ref_idx = text.find("Bern")
if ref_idx != -1:
    print("Found Bern at:", text[ref_idx-50:ref_idx+300])
