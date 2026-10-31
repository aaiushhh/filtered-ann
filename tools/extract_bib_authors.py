import json

with open('tools/verification_complete.json', 'r', encoding='utf-8', errors='replace') as f:
    data = json.load(f)

for item in data[:10]:
    bibkey = item['seed']['bibkey']
    meta = item.get('meta', {})
    doi_data = meta.get('doi_data', {}) if meta else {}
    authors = []
    if doi_data and 'author' in doi_data:
        for a in doi_data['author']:
            name = f"{a.get('given', '')} {a.get('family', '')}".strip()
            if name: authors.append(name)
    arxiv_meta = meta.get('arxiv_meta', {}) if meta else {}
    if not authors and arxiv_meta and 'authors' in arxiv_meta:
        authors = arxiv_meta['authors']
    print(f"{bibkey} -> {' and '.join(authors)}")
