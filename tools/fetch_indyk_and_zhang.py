import subprocess
import pypdf
import os

# 1. indyk2023worst (resume download from arXiv:2310.19126)
print("--- Resuming indyk2023worst ---")
cmd = ['curl.exe', '--ssl-no-revoke', '-L', '-C', '-', '--max-time', '180', '-o', 'papers/indyk2023worst.pdf', 'https://arxiv.org/pdf/2310.19126.pdf']
subprocess.run(cmd)

r = pypdf.PdfReader('papers/indyk2023worst.pdf', strict=False)
t_pages = [f"--- PAGE {i+1} ---\n{p.extract_text() or ''}" for i, p in enumerate(r.pages)]
with open('papers/indyk2023worst.txt', 'w', encoding='utf-8') as f:
    f.write("\n\n".join(t_pages))
print(f"indyk2023worst: {len(r.pages)} pages ({os.path.getsize('papers/indyk2023worst.pdf')} bytes).")

# 2. zhang2023vbase (from USENIX OSDI 2023)
print("--- Downloading zhang2023vbase ---")
cmd = ['curl.exe', '--ssl-no-revoke', '-L', '--max-time', '180', '-o', 'papers/zhang2023vbase.pdf', 'https://www.usenix.org/system/files/osdi23-zhang-qianxi.pdf']
subprocess.run(cmd)

r2 = pypdf.PdfReader('papers/zhang2023vbase.pdf', strict=False)
t_pages2 = [f"--- PAGE {i+1} ---\n{p.extract_text() or ''}" for i, p in enumerate(r2.pages)]
with open('papers/zhang2023vbase.txt', 'w', encoding='utf-8') as f:
    f.write("\n\n".join(t_pages2))
print(f"zhang2023vbase: {len(r2.pages)} pages ({os.path.getsize('papers/zhang2023vbase.pdf')} bytes).")
