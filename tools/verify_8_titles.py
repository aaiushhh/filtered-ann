import os
import pypdf
import subprocess

# 1. Re-download Prokhorenkova
url = "https://arxiv.org/pdf/1907.00845.pdf"
pdf_path = "papers/prokhorenkova2020graph.pdf"
txt_path = "papers/prokhorenkova2020graph.txt"
if os.path.exists(pdf_path):
    os.remove(pdf_path)

cmd = ['curl.exe', '--ssl-no-revoke', '-L', '--max-time', '60', '-o', pdf_path, url]
subprocess.run(cmd)

reader = pypdf.PdfReader(pdf_path, strict=False)
text_pages = []
for p_idx, page in enumerate(reader.pages):
    pt = page.extract_text() or ''
    text_pages.append(f"--- PAGE {p_idx+1} ---\n{pt}")
with open(txt_path, "w", encoding="utf-8") as tf:
    tf.write("\n\n".join(text_pages))
print(f"prokhorenkova2020graph re-downloaded ({len(reader.pages)} pages).")

# 2. Check title of all 8 papers
targets = [
    "prokhorenkova2020graph",
    "diwan2024navigable",
    "indyk2023worst",
    "li2025sieve",
    "gupta2023caps",
    "xu2024multifilterann",
    "zhang2023vbase",
    "mitzenmacher2018model"
]

for t in targets:
    tp = f"papers/{t}.txt"
    with open(tp, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()[:15]
    print(f"=== {t} ===")
    for l in lines[:6]:
        if l.strip():
            print(" ", l.strip())
