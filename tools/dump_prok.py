with open("papers/prokhorenkova2020graph.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
with open("tools/prok_summary.txt", "w", encoding="utf-8") as out:
    for i in range(1, min(10, len(pages))):
        out.write(f"\n================ PAGE {i} ================\n")
        out.write(pages[i][:1500])
