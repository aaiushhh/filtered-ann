import subprocess
import pypdf
import os

url = "https://www.usenix.org/system/files/osdi23-zhang-qianxi.pdf"
pdf_path = "papers/zhang2023vbase.pdf"
txt_path = "papers/zhang2023vbase.txt"

cmd = [
    'curl.exe', '--ssl-no-revoke', '-L',
    '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    '--max-time', '60',
    '-o', pdf_path, url
]
subprocess.run(cmd)

with open(pdf_path, 'rb') as f:
    hdr = f.read(10)
print("Header:", hdr, "Size:", os.path.getsize(pdf_path))

if hdr[:4] == b'%PDF':
    r = pypdf.PdfReader(pdf_path, strict=False)
    t_pages = [f"--- PAGE {i+1} ---\n{p.extract_text() or ''}" for i, p in enumerate(r.pages)]
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(t_pages))
    print(f"zhang2023vbase: {len(r.pages)} pages, first page preview:\n{t_pages[0][:300]}")
