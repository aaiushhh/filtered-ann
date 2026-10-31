with open("papers/li2025sieve.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
with open("tools/sieve_cost_model.txt", "w", encoding="utf-8") as out:
    for i in [4, 5, 6, 7]:
        if i < len(pages):
            out.write(f"\n================ PAGE {i} ================\n")
            out.write(pages[i][:2500])
