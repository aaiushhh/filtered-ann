import subprocess
import pypdf
import os

url = "https://openreview.net/pdf?id=a2eBgp4sjH"
pdf_path = "papers/xu2024multifilterann.pdf"
txt_path = "papers/xu2024multifilterann.txt"

cmd = ['curl.exe', '--ssl-no-revoke', '-L', '--max-time', '60', '-o', pdf_path, url]
res = subprocess.run(cmd)

if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
    reader = pypdf.PdfReader(pdf_path, strict=False)
    print(f"Downloaded {len(reader.pages)} pages ({os.path.getsize(pdf_path)} bytes).")
    text_pages = [f"--- PAGE {i+1} ---\n{p.extract_text() or ''}" for i, p in enumerate(reader.pages)]
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(text_pages))
    print(f"Extracted text to {txt_path}, first page:\n{text_pages[0][:300]}")
else:
    print("Download failed.")
