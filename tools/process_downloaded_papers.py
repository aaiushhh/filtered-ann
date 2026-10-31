import os
import shutil
import csv
from pypdf import PdfReader

# Mapping of file in downloaded_paper to bibkey
MAPPING = {
    'bloom_cacm.pdf': 'bloom1970space',
    'DiskANN19.pdf': 'subramanya2019diskann',
    'Filtered-DiskANN23.pdf': 'gollapudi2023filtereddiskann',
    'ICDE25.pdf': 'luo2025tagfiltered'
}

print("=== 1. Copying PDFs and extracting text ===")
for src_name, bibkey in MAPPING.items():
    src_path = os.path.join('downloaded_paper', src_name)
    dst_pdf = os.path.join('papers', f"{bibkey}.pdf")
    dst_txt = os.path.join('papers', f"{bibkey}.txt")

    # Copy PDF
    shutil.copy2(src_path, dst_pdf)
    size = os.path.getsize(dst_pdf)
    print(f"Copied {src_name} -> {dst_pdf} ({size} bytes)")

    # Extract text
    reader = PdfReader(dst_pdf)
    text_parts = []
    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        text_parts.append(f"\n--- PAGE {idx+1} ---\n" + page_text)
    full_text = "".join(text_parts)

    with open(dst_txt, 'w', encoding='utf-8') as f:
        f.write(full_text)
    print(f"Extracted {len(reader.pages)} pages to {dst_txt} ({len(full_text)} chars)")

print("\n=== 2. Updating manifest.csv ===")
rows = []
fieldnames = []
with open('manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
        bibkey = r['bibkey']
        for src_name, target_key in MAPPING.items():
            if bibkey == target_key:
                dst_pdf = os.path.join('papers', f"{bibkey}.pdf")
                r['full_text_status'] = 'OK'
                r['text_version'] = 'published'
                r['source_url'] = f"downloaded_paper/{src_name}"
                r['file_size_bytes'] = str(os.path.getsize(dst_pdf))
                print(f"Updated manifest row for {bibkey}")
        rows.append(r)

with open('manifest.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("\n=== 3. Checking missing papers ===")
total = len(rows)
ok_count = sum(1 for r in rows if r.get('full_text_status') == 'OK')
paywalled_count = sum(1 for r in rows if r.get('full_text_status') == 'PAYWALLED')
skipped_count = sum(1 for r in rows if r.get('relevance') == 'PROPOSED-DROP')
failed_count = sum(1 for r in rows if r.get('full_text_status') == 'FAILED')

print(f"Total manifest entries: {total}")
print(f"  OK (full text available): {ok_count}")
print(f"  PAYWALLED / MISSING: {paywalled_count}")
print(f"  SKIPPED (PROPOSED-DROP): {skipped_count}")
print(f"  FAILED: {failed_count}")

missing_rows = [r for r in rows if r.get('full_text_status') == 'PAYWALLED']

# Write updated papers/MISSING.md
with open('papers/MISSING.md', 'w', encoding='utf-8') as f:
    f.write("# Missing (Paywalled) Papers Requiring Manual Download\n\n")
    f.write(f"Remaining Missing Count: {len(missing_rows)} / {total - skipped_count} eligible papers\n\n")
    f.write("| bibkey | group | title | DOI | Link |\n")
    f.write("|---|---|---|---|---|\n")
    for r in missing_rows:
        f.write(f"| `{r['bibkey']}` | {r['group']} | {r['title']} | {r.get('doi', 'none')} | {r['link']} |\n")

print(f"Updated papers/MISSING.md with {len(missing_rows)} remaining missing papers.")
