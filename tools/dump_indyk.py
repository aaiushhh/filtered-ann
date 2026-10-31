with open("papers/indyk2023worst.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
print("Total pages:", len(pages))
with open("tools/indyk_summary.txt", "w", encoding="utf-8") as out:
    for i in range(1, min(7, len(pages))):
        out.write(f"\n================ PAGE {i} ================\n")
        out.write(pages[i][:1500])
