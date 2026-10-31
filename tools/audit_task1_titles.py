"""
Audit Task 1: For every row in manifest.csv, fetch title from Crossref/arXiv
by stored DOI/arXiv ID and compare with stored title.
"""
import csv
import json
import subprocess
import re
import sys

def fetch_crossref_title(doi):
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '--max-time', '15',
           f'https://api.crossref.org/works/{doi}']
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode == 0 and res.stdout.strip().startswith('{'):
        try:
            data = json.loads(res.stdout)
            if data.get('status') == 'ok':
                titles = data['message'].get('title', [])
                return titles[0] if titles else None
        except Exception:
            pass
    return None

def fetch_arxiv_title(arxiv_id):
    clean_id = arxiv_id.replace('abs/', '').replace('pdf/', '').strip()
    url = f'https://export.arxiv.org/api/query?id_list={clean_id}'
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '-L', '--max-time', '15', url]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode == 0 and '<entry>' in res.stdout:
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(res.stdout)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entry = root.find('atom:entry', ns)
            if entry is not None:
                title_el = entry.find('atom:title', ns)
                if title_el is not None and title_el.text:
                    return ' '.join(title_el.text.split())
        except Exception:
            pass
    return None

def normalize(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

with open('manifest.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

results = []
for r in rows:
    bk = r['bibkey']
    stored = r.get('title', '')
    doi = r.get('doi', '').strip()
    arxiv = r.get('arxiv_id', '').strip()
    
    api_title = None
    source = ''
    
    if doi:
        api_title = fetch_crossref_title(doi)
        source = f'crossref:{doi}'
    
    if api_title is None and arxiv:
        api_title = fetch_arxiv_title(arxiv)
        source = f'arxiv:{arxiv}'
    
    if api_title is None and not doi and not arxiv:
        source = 'NO_ID'
        api_title = '(no DOI or arXiv ID stored)'
    elif api_title is None:
        api_title = '(API fetch failed)'
    
    match = 'yes' if api_title and normalize(stored) == normalize(api_title) else 'no'
    
    results.append({
        'bibkey': bk,
        'stored_title': stored[:80],
        'api_title': (api_title or '')[:80],
        'match': match,
        'source': source
    })

with open('scratch/audit_task1_titles.md', 'w', encoding='utf-8') as out:
    out.write('# Audit Task 1: Title Verification via Crossref/arXiv API\n\n')
    out.write(f'Total rows checked: {len(results)}\n\n')
    out.write('| bibkey | stored title | API title | match | source |\n')
    out.write('|---|---|---|---|---|\n')
    for r in results:
        out.write(f"| {r['bibkey']} | {r['stored_title']} | {r['api_title']} | {r['match']} | {r['source']} |\n")
    
    mismatches = [r for r in results if r['match'] == 'no']
    out.write(f'\n## Summary\n- Total rows: {len(results)}\n- Matches: {len(results) - len(mismatches)}\n- Mismatches: {len(mismatches)}\n\n')
    if mismatches:
        out.write('### Mismatches detail:\n')
        for r in mismatches:
            out.write(f"- **{r['bibkey']}** ({r['source']})\n  - Stored: {r['stored_title']}\n  - API: {r['api_title']}\n\n")

print(f"Done. {len(results)} rows checked, {len([r for r in results if r['match'] == 'no'])} mismatches.")
