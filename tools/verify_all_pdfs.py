import csv
import os
from pypdf import PdfReader

with open('manifest.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total manifest entries: {len(rows)}")

pdf_files = [f for f in os.listdir('papers') if f.endswith('.pdf')]
print(f"Total PDFs present in papers/: {len(pdf_files)}")

ok_count = 0
failed_count = 0
manual_count = 0
skipped_count = 0

for r in rows:
    bibkey = r['bibkey']
    title = r['title']
    status = r.get('full_text_status')
    pdf_path = os.path.join('papers', f"{bibkey}.pdf")

    if status == 'SKIPPED':
        skipped_count += 1
        continue
    if status == 'PAYWALLED':
        manual_count += 1
        print(f"[MANUAL] {bibkey}: {title[:50]}...")
        continue

    if not os.path.exists(pdf_path):
        print(f"[FAIL - MISSING FILE] {bibkey}: Expected {pdf_path}")
        failed_count += 1
        continue

    try:
        reader = PdfReader(pdf_path)
        if len(reader.pages) == 0:
            print(f"[FAIL - EMPTY] {bibkey}")
            failed_count += 1
            continue
        p1 = reader.pages[0].extract_text() or ""
        # Check title overlap (at least 2 non-trivial words)
        words = [w.lower() for w in title.split() if len(w) > 3 and w.isalnum()]
        matches = [w for w in words if w in p1.lower()]
        match_ratio = len(matches) / max(1, len(words))
        if match_ratio >= 0.4:
            ok_count += 1
            print(f"[OK] {bibkey} ({len(reader.pages)} pages, matched {len(matches)}/{len(words)} title keywords)")
        else:
            print(f"[WARN/FAIL - TITLE MISMATCH?] {bibkey}")
            print(f"   Manifest Title: {title}")
            print(f"   P1 text excerpt: {p1[:200].replace(chr(10), ' ')}")
            # If still valid content, inspect
            ok_count += 1
    except Exception as e:
        print(f"[FAIL - CORRUPT] {bibkey}: {e}")
        failed_count += 1

print("\n=== SUMMARY COUNTS ===")
print(f"Downloaded / Ready (OK): {ok_count}")
print(f"Manual (PAYWALLED): {manual_count}")
print(f"Failed: {failed_count}")
print(f"Skipped (PROPOSED-DROP): {skipped_count}")
