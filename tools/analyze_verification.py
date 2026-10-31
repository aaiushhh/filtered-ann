import json
import re

with open("tools/verification_complete.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for idx, item in enumerate(data, 1):
    seed = item["seed"]
    bibkey = seed["bibkey"]
    code = item["http_code"]
    meta = item.get("meta", {})
    doi_data = meta.get("doi_data")
    arxiv_data = meta.get("arxiv_data")
    neurips_data = meta.get("neurips_data")
    pub_crossref = item.get("pub_crossref")
    
    print(f"[{idx}] {bibkey}")
    print(f"  Seed Title: {seed['seed_title']}")
    print(f"  Seed Status: {seed['seed_status']}")
    print(f"  Link: {seed['link']} (HTTP {code})")
    
    if doi_data:
        t = doi_data.get('title')
        if isinstance(t, list): t = t[0]
        c = doi_data.get('container-title')
        if isinstance(c, list): c = c[0]
        y = None
        if 'issued' in doi_data and 'date-parts' in doi_data['issued']:
            y = doi_data['issued']['date-parts'][0][0]
        elif 'publicationYear' in doi_data:
            y = doi_data['publicationYear']
        d = doi_data.get('DOI', seed.get('doi'))
        print(f"  DOI Meta: Title='{t}', Venue='{c}', Year={y}, DOI={d}")
        
    if arxiv_data and arxiv_data.get("found"):
        print(f"  arXiv Meta: Title='{arxiv_data.get('title')}', Authors={arxiv_data.get('authors')[:2]}..., Date={arxiv_data.get('date')}, DOI={arxiv_data.get('doi')}")
        
    if neurips_data:
        print(f"  NeurIPS Meta: Title='{neurips_data.get('title')}', Venue='{neurips_data.get('venue')}', Date={neurips_data.get('date')}")
        
    if pub_crossref:
        t = pub_crossref.get('title', [''])[0]
        c = pub_crossref.get('container-title', [''])[0]
        d = pub_crossref.get('DOI')
        print(f"  Pub Match: Title='{t}', Venue='{c}', DOI={d}")
    print()
