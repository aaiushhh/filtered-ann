import urllib.request
import json
import urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (mailto:researcher@example.org)'}

queries = [
    ('NHQ', 'Navigating in a Hierarchical Query Space'),
    ('CAPS', 'Partition-based Index for Filtered Similarity Search'),
    ('VBase', 'High-Dimensional Vector Similarity Search and Relational Queries'),
    ('Graph Filtered', 'Graph-Based Approximate Nearest Neighbor Search with Filters'),
    ('Filtered HNSW', 'Filtered HNSW')
]

for tag, q in queries:
    url = f'https://export.arxiv.org/api/query?search_query=all:%22{urllib.parse.quote(q)}%22&max_results=3'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8')
            print(f"=== arXiv Query: {tag} ===")
            import xml.etree.ElementTree as ET
            root = ET.fromstring(content)
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip().replace('\n', ' ')
                id_val = entry.find('{http://www.w3.org/2005/Atom}id').text
                print(f"  -> Title: {title} | ID: {id_val}")
    except Exception as e:
        print(f"=== {tag} ERROR: {e} ===")
