import csv

with open('manifest.csv', 'r', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        k = r['bibkey']
        doi = r.get('doi', '')
        arxiv = r.get('arxiv_id', '')
        status = r.get('verified_status', '')
        venue = r.get('verified_venue', '')
        print(f"{k} | DOI: {doi} | arXiv: {arxiv} | Status: {status} | Venue: {venue}")
