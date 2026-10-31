with open("papers/zhang2023vbase.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
with open("tools/vbase_cost.txt", "w", encoding="utf-8") as out:
    for i in [8, 9, 10, 11]:
        if i < len(pages):
            out.write(f"\n================ PAGE {i} ================\n")
            out.write(pages[i][:2500])
