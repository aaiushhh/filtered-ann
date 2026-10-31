import csv
import os

rows = []
fieldnames = []

with open('manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    if 'pdf_source' not in fieldnames:
        # insert pdf_source right after full_text_status
        idx = fieldnames.index('full_text_status') + 1 if 'full_text_status' in fieldnames else len(fieldnames)
        fieldnames.insert(idx, 'pdf_source')

    for r in reader:
        bibkey = r['bibkey']
        status = r.get('full_text_status', '')
        pdf_file = os.path.join('papers', f"{bibkey}.pdf")

        if bibkey == 'kraska2018learned':
            r['full_text_status'] = 'OK'
            r['pdf_source'] = 'arxiv'
            r['source_url'] = 'https://arxiv.org/pdf/1712.01208'
            r['file_size_bytes'] = str(os.path.getsize(pdf_file))
            r['text_version'] = 'arXiv-1712.01208'
        elif bibkey == 'zou2026rnsg':
            r['full_text_status'] = 'OK'
            r['pdf_source'] = 'publisher'
            r['source_url'] = 'https://www.vldb.org/pvldb/vol19/p2839-zou.pdf'
            r['file_size_bytes'] = str(os.path.getsize(pdf_file))
            r['text_version'] = 'published'
        elif bibkey in ['cai2024navigating', 'shaikh2026annex']:
            r['full_text_status'] = 'PAYWALLED'
            r['pdf_source'] = 'manual'
        elif r.get('relevance') == 'PROPOSED-DROP':
            r['full_text_status'] = 'SKIPPED'
            r['pdf_source'] = 'none'
        else:
            # If not yet set, determine based on source_url or arxiv_id
            if 'pdf_source' not in r or not r['pdf_source']:
                src = r.get('source_url', '')
                if 'downloaded_paper' in src:
                    r['pdf_source'] = 'manual'
                elif 'arxiv' in src or r.get('arxiv_id'):
                    r['pdf_source'] = 'arxiv'
                elif os.path.exists(pdf_file):
                    r['pdf_source'] = 'publisher'
                else:
                    r['pdf_source'] = 'none'

        rows.append(r)

with open('manifest.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Updated manifest.csv successfully.")
