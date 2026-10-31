import csv
import json
import os
import re
import subprocess
import xml.etree.ElementTree as ET

# Load manifest and notes
with open('manifest.csv', 'r', encoding='utf-8') as f:
    manifest = {r['bibkey']: r for r in csv.DictReader(f)}

notes_keys = sorted([f.replace('.md', '') for f in os.listdir('notes') if f.endswith('.md')])
print(f"Total notes found: {len(notes_keys)}")

def get_crossref(doi):
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', f'https://api.crossref.org/works/{doi}']
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode == 0 and res.stdout.strip().startswith('{'):
        try:
            data = json.loads(res.stdout)
            if data.get('status') == 'ok':
                return data['message']
        except Exception:
            pass
    return None

def get_arxiv(arxiv_id):
    clean_id = arxiv_id.replace('abs/', '').replace('pdf/', '').strip()
    url = f'https://export.arxiv.org/api/query?id_list={clean_id}'
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '-L', url]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode == 0 and '<feed' in res.stdout:
        try:
            root = ET.fromstring(res.stdout)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entry = root.find('atom:entry', ns)
            if entry is not None:
                title = ' '.join(entry.find('atom:title', ns).text.split())
                authors = [a.find('atom:name', ns).text.strip() for a in entry.findall('atom:author', ns)]
                published = entry.find('atom:published', ns).text[:4]
                summary = entry.find('atom:summary', ns).text.strip() if entry.find('atom:summary', ns) is not None else ''
                return {
                    'title': title,
                    'authors': authors,
                    'year': published,
                    'arxiv_id': clean_id,
                    'summary': summary
                }
        except Exception as e:
            print(f"Error parsing arxiv {arxiv_id}: {e}")
    return None

def get_note_title(bibkey):
    note_path = os.path.join('notes', f"{bibkey}.md")
    with open(note_path, 'r', encoding='utf-8') as fp:
        first_line = fp.readline().strip()
    if '—' in first_line:
        return first_line.split('—', 1)[1].strip()
    elif '-' in first_line:
        return first_line.split('-', 1)[1].strip()
    return first_line

bib_entries = []
title_mismatches = []
validation_records = []

for k in notes_keys:
    r = manifest[k]
    doi = r.get('doi', '').strip()
    arxiv_id = r.get('arxiv_id', '').strip()
    status = r.get('verified_status', '').strip()
    note_title = get_note_title(k)

    api_title = ""
    authors = []
    year = ""
    venue = ""
    entry_type = "article"
    extra_fields = {}

    # Prefer published DOI if available
    is_published = bool(doi and status == 'PUB')
    crossref_data = get_crossref(doi) if doi else None

    # Handle DataCite DOI fallback (e.g. eppstein2016cuckoo)
    datacite_data = None
    if doi and not crossref_data:
        cmd = ['curl.exe', '--ssl-no-revoke', '-s', f'https://api.datacite.org/dois/{doi}']
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if res.returncode == 0 and '"attributes"' in res.stdout:
            try:
                d_json = json.loads(res.stdout)
                datacite_data = d_json.get('data', {}).get('attributes', {})
            except Exception:
                pass

    if crossref_data:
        # Title
        t_list = crossref_data.get('title', [])
        api_title = t_list[0] if t_list else r.get('title', '')
        # Authors
        for a in crossref_data.get('author', []):
            given = a.get('given', '').strip()
            family = a.get('family', '').strip()
            if family:
                name = f"{given} {family}".strip() if given else family
                authors.append(name)
        # Year
        pub_parts = crossref_data.get('published-print', {}).get('date-parts', []) or crossref_data.get('published-online', {}).get('date-parts', []) or crossref_data.get('issued', {}).get('date-parts', [])
        if pub_parts and pub_parts[0]:
            year = str(pub_parts[0][0])
        else:
            year = r.get('verified_year', 'not stated')
        # Venue
        c_title = crossref_data.get('container-title', [])
        venue = c_title[0] if c_title else r.get('verified_venue', 'not stated')
        
        # Determine inproceedings vs article
        work_type = crossref_data.get('type', '')
        if 'proceedings' in work_type or any(term in venue.lower() for term in ['conference', 'proceedings', 'symposium', 'icde', 'sigmod', 'vldb', 'neurips', 'cikm', 'conext', 'swat', 'cvpr', 'icpp']):
            entry_type = "inproceedings"
        else:
            entry_type = "article"

        extra_fields['doi'] = doi
        if arxiv_id:
            extra_fields['note'] = f"Preprint arXiv:{arxiv_id}"

    elif datacite_data:
        titles = datacite_data.get('titles', [])
        api_title = titles[0].get('title', '') if titles else r.get('title', '')
        for c in datacite_data.get('creators', []):
            given = c.get('givenName', '').strip()
            family = c.get('familyName', '').strip()
            name = f"{given} {family}".strip() if given else c.get('name', '').strip()
            if name:
                authors.append(name)
        year = str(datacite_data.get('publicationYear', '2016'))
        container = datacite_data.get('container', {})
        venue = container.get('title', 'LIPIcs, Volume 53, SWAT 2016')
        entry_type = "inproceedings"
        extra_fields['doi'] = doi
        if arxiv_id:
            extra_fields['note'] = f"Preprint arXiv:{arxiv_id}"

    elif arxiv_id:
        # Use arXiv API
        ar_data = get_arxiv(arxiv_id)
        if ar_data:
            api_title = ar_data['title']
            authors = ar_data['authors']
            year = ar_data['year']
            venue = f"arXiv preprint arXiv:{arxiv_id}"
            entry_type = "article"
            extra_fields['eprint'] = arxiv_id
            extra_fields['archivePrefix'] = "arXiv"
        else:
            print(f"Failed to fetch arXiv API for {k} ({arxiv_id})")
    else:
        # Fallback for papers without Crossref DOI or arXiv API (e.g. NeurIPS without DOI or USENIX OSDI)
        api_title = r.get('title', '')
        year = r.get('verified_year', '')
        venue = r.get('verified_venue', '')
        if k == 'subramanya2019diskann':
            authors = ['Suhas Jayaram Subramanya', 'Fnu Devvrit', 'Harsha Vardhan Simhadri', 'Ravishankar Krishnawamy', 'Rohan Kadekodi']
        elif k == 'zhang2023vbase':
            authors = ['Qianxi Zhang', 'Shuotao Xu', 'Qi Chen', 'Guorui Xie', 'Ke Cheng', 'Zhizhen Cai', 'Qiuping Lu', 'Zhihao Zhang', 'Chen Chen', 'Ningyi Xu', 'Fan Yang', 'Mao Yang']
        else:
            authors = [r.get('authors', 'not stated')]
        entry_type = "inproceedings"
        extra_fields['booktitle'] = venue

    # Check title comparison
    # Normalize for comparison
    clean_note_t = re.sub(r'[^a-zA-Z0-9]', '', note_title.lower())
    clean_api_t = re.sub(r'[^a-zA-Z0-9]', '', api_title.lower())
    if clean_note_t != clean_api_t:
        title_mismatches.append({
            'bibkey': k,
            'note_title': note_title,
            'api_title': api_title
        })

    # Format BibTeX entry
    author_str = " and ".join(authors) if authors else "not stated"
    lines = [f"@{entry_type}{{{k},"]
    lines.append(f"  title = {{{{{api_title}}}}},")
    lines.append(f"  author = {{{author_str}}},")
    if entry_type == "inproceedings":
        lines.append(f"  booktitle = {{{{{venue}}}}},")
    else:
        lines.append(f"  journal = {{{{{venue}}}}},")
    lines.append(f"  year = {{{year}}}")

    for ek, ev in extra_fields.items():
        if ek == 'doi':
            lines[-1] += ","
            lines.append(f"  doi = {{{ev}}}")
        elif ek == 'eprint':
            lines[-1] += ","
            lines.append(f"  eprint = {{{ev}}},")
            lines.append(f"  archivePrefix = {{{extra_fields.get('archivePrefix', 'arXiv')}}}")
        elif ek == 'note':
            lines[-1] += ","
            lines.append(f"  note = {{{ev}}}")

    lines.append("}")
    bib_entries.append("\n".join(lines))
    validation_records.append({
        'bibkey': k,
        'has_doi_or_arxiv': bool(doi or arxiv_id),
        'identifier': doi or f"arXiv:{arxiv_id}"
    })

# Write refs.bib
with open('refs.bib', 'w', encoding='utf-8') as f:
    f.write("\n\n".join(bib_entries) + "\n")

print(f"Generated refs.bib with {len(bib_entries)} entries.")
print(f"Title mismatches count: {len(title_mismatches)}")
for tm in title_mismatches:
    print(f"  [{tm['bibkey']}]:")
    print(f"    Note: {tm['note_title']}")
    print(f"    API:  {tm['api_title']}")

# Save title mismatches to tools/title_mismatches.json
with open('tools/title_mismatches.json', 'w', encoding='utf-8') as f:
    json.dump(title_mismatches, f, indent=2)
