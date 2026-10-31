import csv
import os
import subprocess
import pypdf
import datetime
import time

os.makedirs('papers', exist_ok=True)
os.makedirs('logs', exist_ok=True)

rows = []
with open('manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    for r in reader:
        rows.append(r)

new_fields = ['full_text_status', 'text_version', 'source_url', 'file_size_bytes']
for nf in new_fields:
    if nf not in fieldnames:
        fieldnames.append(nf)

for idx, r in enumerate(rows, 1):
    bibkey = r['bibkey']
    relevance = r.get('relevance', 'KEEP')
    
    pdf_path = os.path.join('papers', f'{bibkey}.pdf')
    txt_path = os.path.join('papers', f'{bibkey}.txt')
    
    if os.path.exists(pdf_path) and os.path.exists(txt_path) and os.path.getsize(pdf_path) > 1000:
        r['full_text_status'] = 'OK'
        r['file_size_bytes'] = str(os.path.getsize(pdf_path))
        if not r.get('text_version'):
            r['text_version'] = f"arXiv-{r['arxiv_id']}" if r.get('arxiv_id') else 'published'
        print(f"[{idx}/{len(rows)}] Already present: {bibkey}", flush=True)
        continue

    if relevance == 'PROPOSED-DROP':
        r['full_text_status'] = 'SKIPPED'
        r['text_version'] = ''
        r['source_url'] = ''
        r['file_size_bytes'] = '0'
        print(f"[{idx}/{len(rows)}] Skipped (PROPOSED-DROP): {bibkey}", flush=True)
        continue

    url_to_try = None
    version_label = None
    
    if bibkey == 'eppstein2016cuckoo':
        url_to_try = 'https://drops.dagstuhl.de/storage/00lipics/lipics-vol053-swat2016/LIPIcs.SWAT.2016.8/LIPIcs.SWAT.2016.8.pdf'
        version_label = 'published'
    elif bibkey == 'matsui2025lotusfilter':
        url_to_try = r['link']
        version_label = 'published'
    elif r.get('arxiv_id'):
        url_to_try = f"https://arxiv.org/pdf/{r['arxiv_id']}"
        version_label = f"arXiv-{r['arxiv_id']}"
    
    if not url_to_try:
        r['full_text_status'] = 'PAYWALLED'
        r['text_version'] = 'published'
        r['source_url'] = r.get('link', '')
        r['file_size_bytes'] = '0'
        print(f"[{idx}/{len(rows)}] PAYWALLED: {bibkey}", flush=True)
        continue

    print(f"[{idx}/{len(rows)}] Downloading {bibkey} from {url_to_try}...", flush=True)
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Run curl to download
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '-L', '--max-time', '45', '-o', pdf_path, '-w', '%{http_code}', url_to_try]
    res = subprocess.run(cmd, capture_output=True, text=True)
    http_code = res.stdout.strip()
    
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
        # Check if actually PDF
        with open(pdf_path, 'rb') as f_check:
            header = f_check.read(4)
        if header == b'%PDF':
            size_bytes = os.path.getsize(pdf_path)
            r['full_text_status'] = 'OK'
            r['text_version'] = version_label
            r['source_url'] = url_to_try
            r['file_size_bytes'] = str(size_bytes)
            
            with open('logs/fetch_log.csv', 'a', newline='', encoding='utf-8') as fl:
                csv.writer(fl).writerow([ts, bibkey, url_to_try, f"OK ({size_bytes}B)"])
                
            try:
                reader = pypdf.PdfReader(pdf_path)
                text_pages = []
                for p_idx, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ''
                    text_pages.append(f"--- PAGE {p_idx+1} ---\n{page_text}")
                with open(txt_path, 'w', encoding='utf-8') as tf:
                    tf.write("\n\n".join(text_pages))
                print(f"    Extracted {len(reader.pages)} pages ({size_bytes} bytes)", flush=True)
            except Exception as te:
                print(f"    Text extraction error: {te}", flush=True)
        else:
            os.remove(pdf_path)
            r['full_text_status'] = 'PAYWALLED'
            r['text_version'] = version_label
            r['source_url'] = url_to_try
            r['file_size_bytes'] = '0'
            print(f"    Downloaded non-PDF content (HTTP {http_code})", flush=True)
    else:
        status_label = 'PAYWALLED' if http_code in ['401', '403'] else 'FAILED'
        r['full_text_status'] = status_label
        r['text_version'] = version_label
        r['source_url'] = url_to_try
        r['file_size_bytes'] = '0'
        with open('logs/fetch_log.csv', 'a', newline='', encoding='utf-8') as fl:
            csv.writer(fl).writerow([ts, bibkey, url_to_try, f"HTTP {http_code}"])
        print(f"    HTTP {http_code}", flush=True)

with open('manifest.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

missing_rows = [r for r in rows if r.get('full_text_status') in ['PAYWALLED', 'FAILED']]
with open('papers/MISSING.md', 'w', encoding='utf-8') as mf:
    mf.write("# Missing Full-Text Papers (PAYWALLED or FAILED)\n\n")
    mf.write("Please download these PDFs through your institutional access and place them in `papers/<bibkey>.pdf`.\n\n")
    mf.write("| bibkey | Title | Status | DOI | Source / Link |\n")
    mf.write("|---|---|---|---|---|\n")
    for mr in missing_rows:
        mf.write(f"| {mr['bibkey']} | {mr['title']} | {mr['full_text_status']} | {mr.get('doi','')} | {mr.get('link','')} |\n")

print(f"\nAll complete! Manifest updated. {len(missing_rows)} missing papers listed in papers/MISSING.md.", flush=True)
