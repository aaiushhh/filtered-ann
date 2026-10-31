import urllib.request
import json
import urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (mailto:researcher@example.org)'}

dois = [
    '10.14778/3828612.3828636', # RNSG VLDB 2026
    '10.1145/3448016.3457550', # Milvus SIGMOD 2021
    '10.61927/igmin365'          # ANNex 2026
]

for doi in dois:
    url = f'https://api.crossref.org/works/{doi}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))['message']
            print(f"Title: {data.get('title', [''])[0]}")
            print(f"Venue: {data.get('container-title', [''])[0]}")
            print(f"Year: {data.get('issued', {}).get('date-parts', [[None]])[0][0]}")
            print(f"DOI: {doi}")
            authors = [f"{a.get('given','')} {a.get('family','')}".strip() for a in data.get('author', [])]
            print(f"Authors: {', '.join(authors)}")
            print()
    except Exception as e:
        print(f"Error {doi}: {e}")
