import subprocess
import pypdf
import os
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. diwan2024navigable
print("--- Downloading diwan2024navigable (arXiv:2405.18680) ---")
cmd = ['curl.exe', '--ssl-no-revoke', '-L', '--max-time', '60', '-o', 'papers/diwan2024navigable.pdf', 'https://arxiv.org/pdf/2405.18680.pdf']
subprocess.run(cmd)
r = pypdf.PdfReader('papers/diwan2024navigable.pdf', strict=False)
t_pages = [f"--- PAGE {i+1} ---\n{p.extract_text() or ''}" for i, p in enumerate(r.pages)]
with open('papers/diwan2024navigable.txt', 'w', encoding='utf-8') as f:
    f.write("\n\n".join(t_pages))
print(f"diwan: {len(r.pages)} pages, first page: {t_pages[0][:200]}...")

# 2. indyk2023worst
print("--- Downloading indyk2023worst (arXiv:2310.19126) ---")
cmd = ['curl.exe', '--ssl-no-revoke', '-L', '--max-time', '60', '-o', 'papers/indyk2023worst.pdf', 'https://arxiv.org/pdf/2310.19126.pdf']
subprocess.run(cmd)
r = pypdf.PdfReader('papers/indyk2023worst.pdf', strict=False)
t_pages = [f"--- PAGE {i+1} ---\n{p.extract_text() or ''}" for i, p in enumerate(r.pages)]
with open('papers/indyk2023worst.txt', 'w', encoding='utf-8') as f:
    f.write("\n\n".join(t_pages))
print(f"indyk: {len(r.pages)} pages, first page: {t_pages[0][:200]}...")

# 3. zhang2023vbase
print("--- Downloading zhang2023vbase (USENIX OSDI 2023) ---")
cmd = ['curl.exe', '--ssl-no-revoke', '-L', '--max-time', '60', '-o', 'papers/zhang2023vbase.pdf', 'https://www.usenix.org/system/files/osdi23-zhang-qianxi.pdf']
subprocess.run(cmd)
r = pypdf.PdfReader('papers/zhang2023vbase.pdf', strict=False)
t_pages = [f"--- PAGE {i+1} ---\n{p.extract_text() or ''}" for i, p in enumerate(r.pages)]
with open('papers/zhang2023vbase.txt', 'w', encoding='utf-8') as f:
    f.write("\n\n".join(t_pages))
print(f"zhang: {len(r.pages)} pages, first page: {t_pages[0][:200]}...")
