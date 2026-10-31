import os
import subprocess
import pypdf
import datetime
import csv

os.makedirs('papers', exist_ok=True)
os.makedirs('logs', exist_ok=True)

targets = [
    {"bibkey": "prokhorenkova2020graph", "url": "https://arxiv.org/pdf/2006.05942", "version": "arXiv-2006.05942"},
    {"bibkey": "diwan2024navigable", "url": "https://arxiv.org/pdf/2406.07770", "version": "arXiv-2406.07770"},
    {"bibkey": "indyk2023worst", "url": "https://arxiv.org/pdf/2310.17030", "version": "arXiv-2310.17030"},
    {"bibkey": "li2025sieve", "url": "https://arxiv.org/pdf/2411.08271", "version": "arXiv-2411.08271"},
    {"bibkey": "gupta2023caps", "url": "https://arxiv.org/pdf/2308.15014", "version": "arXiv-2308.15014"},
    {"bibkey": "xu2024multifilterann", "url": "https://arxiv.org/pdf/2408.08502", "version": "arXiv-2408.08502"},
    {"bibkey": "zhang2023vbase", "url": "https://arxiv.org/pdf/2307.03986", "version": "arXiv-2307.03986"},
    {"bibkey": "mitzenmacher2018model", "url": "https://arxiv.org/pdf/1901.00902", "version": "arXiv-1901.00902"}
]

# Read manifest rows to update full_text_status
manifest_rows = []
fieldnames = []
with open("manifest.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    manifest_rows = list(reader)

manifest_dict = {r["bibkey"]: r for r in manifest_rows}

for t in targets:
    k = t["bibkey"]
    pdf_path = os.path.join("papers", f"{k}.pdf")
    txt_path = os.path.join("papers", f"{k}.txt")
    
    if os.path.exists(pdf_path) and os.path.exists(txt_path) and os.path.getsize(pdf_path) > 1000:
        print(f"Already exists: {k}")
        continue
    
    url = t["url"]
    print(f"Downloading {k} from {url}...")
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '-L', '--max-time', '60', '-o', pdf_path, '-w', '%{http_code}', url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    http_code = res.stdout.strip()
    
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
        with open(pdf_path, 'rb') as f_check:
            header = f_check.read(4)
        if header == b'%PDF':
            size_bytes = os.path.getsize(pdf_path)
            print(f"  Downloaded {size_bytes} bytes (HTTP {http_code})")
            with open('logs/fetch_log.csv', 'a', newline='', encoding='utf-8') as fl:
                csv.writer(fl).writerow([ts, k, url, f"OK ({size_bytes}B)"])
            
            # Extract text
            try:
                reader = pypdf.PdfReader(pdf_path)
                text_pages = []
                for p_idx, page in enumerate(reader.pages):
                    pt = page.extract_text() or ''
                    text_pages.append(f"--- PAGE {p_idx+1} ---\n{pt}")
                with open(txt_path, 'w', encoding='utf-8') as tf:
                    tf.write("\n\n".join(text_pages))
                print(f"  Extracted {len(reader.pages)} pages to {txt_path}")
            except Exception as e:
                print(f"  Text extraction failed: {e}")
            
            if k in manifest_dict:
                manifest_dict[k]["full_text_status"] = "OK"
                manifest_dict[k]["text_version"] = t["version"]
                manifest_dict[k]["source_url"] = url
                manifest_dict[k]["file_size_bytes"] = str(size_bytes)
        else:
            print(f"  Invalid PDF header: {header}")
            os.remove(pdf_path)
    else:
        print(f"  Download failed (HTTP {http_code})")

# Write back manifest.csv
with open("manifest.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(manifest_rows)

print("Target download process completed.")
