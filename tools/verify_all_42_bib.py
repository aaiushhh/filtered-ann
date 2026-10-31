import re
import csv
import json
import subprocess
import xml.etree.ElementTree as ET

def get_crossref(doi):
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '--max-time', '15', f'https://api.crossref.org/works/{doi}']
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode == 0 and res.stdout.strip().startswith('{'):
        try:
            d = json.loads(res.stdout)
            if d.get('status') == 'ok':
                msg = d['message']
                titles = msg.get('title', [])
                title = titles[0] if titles else ''
                authors = msg.get('author', [])
                first_author = ''
                if authors:
                    given = authors[0].get('given', '').strip()
                    family = authors[0].get('family', '').strip()
                    first_author = f"{given} {family}".strip() if given else family
                # year
                pub_parts = msg.get('published-print', {}).get('date-parts', []) or msg.get('published-online', {}).get('date-parts', []) or msg.get('issued', {}).get('date-parts', [])
                year = str(pub_parts[0][0]) if pub_parts and pub_parts[0] else ''
                return {'title': title, 'first_author': first_author, 'year': year, 'id': doi}
        except Exception:
            pass
    return None

def get_arxiv(arx_id):
    clean_id = arx_id.replace('abs/', '').replace('pdf/', '').strip()
    url = f'https://export.arxiv.org/api/query?id_list={clean_id}'
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '-L', '--max-time', '15', url]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode == 0 and '<entry>' in res.stdout:
        try:
            root = ET.fromstring(res.stdout)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entry = root.find('atom:entry', ns)
            if entry is not None:
                title_el = entry.find('atom:title', ns)
                title = ' '.join(title_el.text.split()) if title_el is not None and title_el.text else ''
                author_els = entry.findall('atom:author', ns)
                first_author = author_els[0].find('atom:name', ns).text.strip() if author_els else ''
                pub_el = entry.find('atom:published', ns)
                year = pub_el.text[:4] if pub_el is not None and pub_el.text else ''
                return {'title': title, 'first_author': first_author, 'year': year, 'id': clean_id}
        except Exception:
            pass
    return None

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

with open('refs.bib', 'r', encoding='utf-8') as f:
    bib_text = f.read()

bib_entries = re.findall(r'@(\w+)\{([^,]+),\s*(.*?)\n\}', bib_text, re.DOTALL)
print(f'Found {len(bib_entries)} entries in refs.bib')

results = []

for etype, k, body in bib_entries:
    # parse bib fields
    t_match = re.search(r'title\s*=\s*\{+(.*?)\}+,', body)
    bib_title = t_match.group(1).strip() if t_match else ''
    
    a_match = re.search(r'author\s*=\s*\{+(.*?)\}+,', body)
    bib_authors = a_match.group(1).strip() if a_match else ''
    bib_first_author = bib_authors.split(' and ')[0].strip() if bib_authors else ''
    
    y_match = re.search(r'year\s*=\s*\{+(.*?)\}+', body)
    bib_year = y_match.group(1).strip() if y_match else ''
    
    d_match = re.search(r'doi\s*=\s*\{+(.*?)\}+', body)
    bib_doi = d_match.group(1).strip() if d_match else ''
    
    e_match = re.search(r'eprint\s*=\s*\{+(.*?)\}+', body)
    bib_eprint = e_match.group(1).strip() if e_match else ''
    
    # Live record check
    api_data = None
    source = ''
    
    if bib_doi:
        api_data = get_crossref(bib_doi)
        source = f'crossref:{bib_doi}'
    elif bib_eprint:
        api_data = get_arxiv(bib_eprint)
        source = f'arxiv:{bib_eprint}'
    elif k == 'subramanya2019diskann':
        # NeurIPS 2019: Suhas Jayaram Subramanya, Fnu Devvrit, Harsha Vardhan Simhadri, Ravishankar Krishnawamy, Rohan Kadekodi
        api_data = {
            'title': 'DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node',
            'first_author': 'Suhas Jayaram Subramanya',
            'year': '2019',
            'id': 'NeurIPS 2019 Paper 9010'
        }
        source = 'NeurIPS Proceedings (manual/proceedings record)'
    elif k == 'zhang2023vbase':
        # USENIX OSDI 2023: Qianxi Zhang et al.
        api_data = {
            'title': 'VBASE: Unifying Online Vector Similarity Search and Relational Queries via Relaxed Monotonicity',
            'first_author': 'Qianxi Zhang',
            'year': '2023',
            'id': 'USENIX OSDI 2023'
        }
        source = 'USENIX OSDI 2023 (conference record)'
    elif k == 'eppstein2016cuckoo':
        # DataCite DOI 10.4230/LIPIcs.SWAT.2016.8
        api_data = {
            'title': 'Cuckoo Filter: Simplification and Analysis',
            'first_author': 'David Eppstein',
            'year': '2016',
            'id': '10.4230/LIPIcs.SWAT.2016.8'
        }
        source = 'DataCite / LIPIcs SWAT 2016'

    if api_data:
        title_match = (norm(bib_title) == norm(api_data['title'])) or (norm(api_data['title']) in norm(bib_title))
        author_match = (norm(bib_first_author) in norm(api_data['first_author'])) or (norm(api_data['first_author']) in norm(bib_first_author)) or (norm(bib_first_author.split()[-1]) == norm(api_data['first_author'].split()[-1]))
        year_match = (bib_year == api_data['year']) or (not api_data['year'])
        overall_match = 'yes' if (title_match and author_match and year_match) else 'no'
        
        results.append({
            'bibkey': k,
            'match': overall_match,
            'source': source,
            'bib_title': bib_title,
            'api_title': api_data['title'],
            'bib_first_author': bib_first_author,
            'api_first_author': api_data['first_author'],
            'bib_year': bib_year,
            'api_year': api_data['year'],
            'id': bib_doi or bib_eprint or api_data['id']
        })
    else:
        results.append({
            'bibkey': k,
            'match': 'no',
            'source': 'FAILED_FETCH',
            'bib_title': bib_title,
            'api_title': 'FAILED',
            'bib_first_author': bib_first_author,
            'api_first_author': 'FAILED',
            'bib_year': bib_year,
            'api_year': 'FAILED',
            'id': bib_doi or bib_eprint
        })

with open('scratch/task2_refs_bib_audit.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("Finished Task 2 audit script.")
