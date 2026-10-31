import csv
import json

with open('tools/verification_complete.json', 'r', encoding='utf-8', errors='replace') as f:
    vc_data = {item['seed']['bibkey']: item for item in json.load(f)}

with open('manifest.csv', 'r', encoding='utf-8') as f:
    manifest_rows = {r['bibkey']: r for r in csv.DictReader(f)}

for k, r in manifest_rows.items():
    authors = []
    if k in vc_data:
        meta = vc_data[k].get('meta', {}) or {}
        doi_data = meta.get('doi_data', {}) or {}
        if 'author' in doi_data:
            for a in doi_data['author']:
                name = f"{a.get('given', '')} {a.get('family', '')}".strip()
                if name:
                    authors.append(name)
        arxiv_meta = meta.get('arxiv_meta', {}) or {}
        if not authors and 'authors' in arxiv_meta:
            authors = arxiv_meta['authors']
    print(f"{k} | {', '.join(authors) if authors else 'NEED AUTHORS'}")
