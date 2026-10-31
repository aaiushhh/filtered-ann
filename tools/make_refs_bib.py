import csv
import re

def escape_bib(s):
    if not s:
        return ""
    return s.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')

entries = []
with open('manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        bibkey = r['bibkey']
        title = escape_bib(r.get('title', ''))
        year = r.get('verified_year', '') or 'not stated'
        venue = escape_bib(r.get('verified_venue', ''))
        doi = r.get('doi', '')
        arxiv_id = r.get('arxiv_id', '')
        status = r.get('verified_status', '')

        # Determine BibTeX entry type
        if status == 'PRE' or (not doi and not venue and arxiv_id):
            # Preprint
            entry = f"@article{{{bibkey},\n"
            entry += f"  title = {{{{{title}}}}},\n"
            entry += f"  author = {{not stated}},\n" # Manifest does not have author column
            entry += f"  year = {{{year}}},\n"
            entry += f"  archivePrefix = {{arXiv}},\n"
            entry += f"  eprint = {{{arxiv_id}}},\n"
            entry += f"  journal = {{arXiv preprint arXiv:{arxiv_id}}}\n"
            entry += "}"
        else:
            # Published paper
            # Check if proceedings or journal
            is_conf = any(term in venue.lower() for term in ['conference', 'proceedings', 'symposium', 'workshop', 'icde', 'sigmod', 'vldb', 'neurips', 'cikm'])
            entry_type = "inproceedings" if is_conf else "article"
            venue_field = "booktitle" if is_conf else "journal"
            
            entry = f"@{entry_type}{{{bibkey},\n"
            entry += f"  title = {{{{{title}}}}},\n"
            entry += f"  author = {{not stated}},\n"
            entry += f"  {venue_field} = {{{{{venue}}}}},\n"
            entry += f"  year = {{{year}}}"
            if doi:
                entry += f",\n  doi = {{{doi}}}"
            if arxiv_id:
                entry += f",\n  eprint = {{{arxiv_id}}},\n  archivePrefix = {{arXiv}}"
            entry += "\n}"
            
        entries.append(entry)

with open('paper/refs.bib', 'w', encoding='utf-8') as f:
    f.write("\n\n".join(entries) + "\n")

print(f"Generated paper/refs.bib with {len(entries)} entries.")
