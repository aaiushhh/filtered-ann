import subprocess
import pypdf
import os

pdf_path = "papers/prokhorenkova2020graph.pdf"
txt_path = "papers/prokhorenkova2020graph.txt"
url = "https://arxiv.org/pdf/1907.00845.pdf"

# Resume download
cmd = ['curl.exe', '--ssl-no-revoke', '-L', '-C', '-', '--max-time', '180', '-o', pdf_path, url]
subprocess.run(cmd)

size = os.path.getsize(pdf_path)
print(f"prokhorenkova2020graph size: {size}")

reader = pypdf.PdfReader(pdf_path, strict=False)
print(f"prokhorenkova2020graph pages: {len(reader.pages)}")

text_pages = []
for p_idx, page in enumerate(reader.pages):
    pt = page.extract_text() or ''
    text_pages.append(f"--- PAGE {p_idx+1} ---\n{pt}")

with open(txt_path, "w", encoding="utf-8") as tf:
    tf.write("\n\n".join(text_pages))

print(f"prokhorenkova2020graph extracted {len(text_pages)} pages.")
