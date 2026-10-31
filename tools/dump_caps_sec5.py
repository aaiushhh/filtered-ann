with open("papers/gupta2023caps.txt", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("5 CAPS")
if idx == -1:
    idx = text.find("5 ")

with open("tools/caps_sec5_clean.txt", "w", encoding="utf-8") as f_out:
    f_out.write(text[idx:idx+3000])

print("Wrote caps sec 5")
