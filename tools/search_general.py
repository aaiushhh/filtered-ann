import urllib.request
import json
import urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (mailto:researcher@example.org)'}

queries = [
    'Milvus: A Purpose-Built Vector Data Management System',
    'Navigating in a Hierarchical Query Space for Filtered Nearest Neighbor Search',
    'CAPS: A Partition-based Index for Filtered Similarity Search',
    'VBase: Unifying High-Dimensional Vector Similarity Search and Relational Queries',
    'Towards High-Performance Range-Filtered Approximate Nearest Neighbor Search'
]

for q in queries:
    url = f'https://api.crossref.org/works?query={urllib.parse.quote(q)}&rows=3'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))['message']['items']
            print(f"=== Search: {q[:30]}... ===")
            for it in data:
                t = it.get('title', [''])[0]
                doi = it.get('DOI', '')
                venue = it.get('container-title', [''])[0]
                year = it.get('issued', {}).get('date-parts', [[None]])[0][0]
                authors = [a.get('family', '') for a in it.get('author', [])]
                print(f"  -> {t} | {venue} ({year}) | DOI: {doi} | {authors[:3]}")
    except Exception as e:
        print(f"Error {e}")
