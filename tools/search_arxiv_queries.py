import urllib.request
import json
import urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (mailto:researcher@example.org)'}

queries = [
    ('NHQ', 'Navigating in a Hierarchical Query Space for Filtered Nearest Neighbor Search'),
    ('CAPS', 'CAPS: A Partition-based Index for Filtered Similarity Search'),
    ('VBase', 'VBase: Unifying High-Dimensional Vector Similarity Search and Relational Queries'),
    ('Stitched-Vamana', 'Filtered-DiskANN'),
    ('PARIS', 'PARIS: Partition-based Search for Filtered Vector Retrieval')
]

for tag, q in queries:
    url = f'https://export.arxiv.org/api/query?search_query=ti:%22{urllib.parse.quote(q)}%22&max_results=2'
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
