import urllib.request
import json
import urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (mailto:researcher@example.org)'}

dois = [
    ('10.1145/3543507.3583552', 'Filtered-DiskANN'),
    ('10.1145/3654923', 'ACORN'),
    ('10.1109/icde65448.2025.00272', 'Tag-Filtered ICDE 2025'),
    ('10.1145/3511808.3557610', 'HQANN CIKM 2022'),
    ('10.1145/3698822', 'Navigating Labels and Vectors PACMMOD 2024'),
    ('10.1145/3639324', 'SeRF PACMMOD 2024'),
    ('10.1145/3725401', 'Range Filtered PACMMOD 2025')
]

for doi, tag in dois:
    url = f'https://api.crossref.org/works/{doi}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))['message']
            title = data.get('title', [''])[0]
            venue = data.get('container-title', [''])[0]
            year = data.get('issued', {}).get('date-parts', [[None]])[0][0]
            authors = [f"{a.get('given','')} {a.get('family','')}".strip() for a in data.get('author', [])]
            print(f"=== {tag} ===")
            print(f"Title: {title}")
            print(f"Venue: {venue} ({year})")
            print(f"DOI: {doi}")
            print(f"Authors: {', '.join(authors)}")
            print()
    except Exception as e:
        print(f"=== {tag} ERROR: {e} ===")
