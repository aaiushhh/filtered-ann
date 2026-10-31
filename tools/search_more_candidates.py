import urllib.request
import json
import urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (mailto:researcher@example.org)'}

queries = [
    ('Milvus SIGMOD', 'Milvus: A Purpose-Built Vector Data Management System'),
    ('CAPS VLDB', 'CAPS: A Partition-based Index for Filtered Similarity Search'),
    ('VBase OSDI', 'VBase: Unifying High-Dimensional Vector Similarity Search and Relational Queries'),
    ('NHQ VLDB', 'Navigating in a Hierarchical Query Space for Filtered Nearest Neighbor Search'),
    ('MultiFilterANN', 'MultiFilterANN'),
    ('VBase SOSP', 'VBase'),
    ('UniFiltered', 'UniFiltered: A Unified Framework for Filtered Approximate Nearest Neighbor Search')
]

for tag, q in queries:
    url = f'https://api.crossref.org/works?query.title={urllib.parse.quote(q)}&rows=3'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('message', {}).get('items', [])
            print(f'=== Query: {tag} ===')
            for it in items:
                title = it.get('title', [''])[0]
                doi = it.get('DOI', '')
                venue = it.get('container-title', [''])[0]
                issued = it.get('issued', {}).get('date-parts', [[None]])[0][0]
                authors = [a.get('family', '') for a in it.get('author', [])]
                print(f'  Match: {title} | {venue} ({issued}) | DOI: {doi} | Authors: {authors[:3]}')
    except Exception as e:
        print(f'=== {tag} ERROR: {e} ===')
