with open("papers/mitzenmacher2018model.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
with open("tools/mitzen_sec4.txt", "w", encoding="utf-8") as out:
    for i in [6, 7, 8]:
        if i < len(pages):
            out.write(f"\n================ PAGE {i} ================\n")
            out.write(pages[i][:2500])
