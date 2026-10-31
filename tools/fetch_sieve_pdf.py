import subprocess
import pypdf
import os

url = "https://www.vldb.org/pvldb/vol18/p4723-li.pdf"
pdf_path = "papers/li2025sieve.pdf"
txt_path = "papers/li2025sieve.txt"

cmd = ['curl.exe', '--ssl-no-revoke', '-L', '--max-time', '60', '-o', pdf_path, url]
subprocess.run(cmd)

if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
    reader = pypdf.PdfReader(pdf_path, strict=False)
    print(f"Downloaded {len(reader.pages)} pages ({os.path.getsize(pdf_path)} bytes).")
    text_pages = [f"--- PAGE {i+1} ---\n{p.extract_text() or ''}" for i, p in enumerate(reader.pages)]
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(text_pages))
    print(f"First page preview:\n{text_pages[0][:300]}")
else:
    print("Download failed.")
