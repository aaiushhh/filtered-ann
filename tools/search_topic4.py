import urllib.request
import urllib.parse
import json
import ssl
import xml.etree.ElementTree as ET

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

queries = [
    "HNSW cache prefetching",
    "graph nearest neighbor memory access cache",
    "approximate nearest neighbor search prefetching memory",
    "graph-based vector search cache miss",
    "HNSW memory hierarchy cache efficiency",
    "SIMD prefetching graph ANN search"
]

def search_cr(q):
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(q)}&rows=5"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0 (mailto:researcher@test.edu)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get("message", {}).get("items", [])
    except Exception as e:
        print("CR Err:", e)
        return []

def search_arxiv(q):
    url = f"https://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(q)}&max_results=5"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            root = ET.fromstring(resp.read().decode('utf-8'))
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            items = []
            for e in root.findall("atom:entry", ns):
                title = e.find("atom:title", ns).text.strip().replace("\n", " ")
                title = " ".join(title.split())
                id_url = e.find("atom:id", ns).text.strip()
                aid = id_url.split("/abs/")[-1]
                published = e.find("atom:published", ns).text[:4]
                summary = e.find("atom:summary", ns).text.strip().replace("\n", " ")[:200]
                items.append({"title": title, "arxiv_id": aid, "year": published, "summary": summary})
            return items
    except Exception as e:
        print("arXiv Err:", e)
        return []

all_found = {}

for q in queries:
    print(f"Querying: {q}")
    for item in search_cr(q):
        title = item.get("title", [""])[0]
        doi = item.get("DOI", "")
        if title and doi and title.lower() not in all_found:
            all_found[title.lower()] = {
                "source": "Crossref",
                "title": title,
                "doi": doi,
                "venue": item.get("container-title", [""])[0],
                "year": str(item.get("issued", {}).get("date-parts", [[None]])[0][0]),
                "link": f"https://doi.org/{doi}"
            }
    for item in search_arxiv(q):
        title = item["title"]
        if title and title.lower() not in all_found:
            all_found[title.lower()] = {
                "source": "arXiv",
                "title": title,
                "arxiv_id": item["arxiv_id"],
                "venue": "arXiv preprint",
                "year": item["year"],
                "link": f"https://arxiv.org/abs/{item['arxiv_id']}",
                "summary": item["summary"]
            }

with open("tools/topic4_candidates_raw.json", "w", encoding="utf-8") as f:
    json.dump(list(all_found.values()), f, indent=2)

print(f"Total raw items found: {len(all_found)}")
