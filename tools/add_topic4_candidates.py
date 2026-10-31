import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import csv
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

topic4_candidates = [
    {
        "bibkey": "wang2025anncache",
        "title": "ANN-Cache: Accelerating Approximate Nearest Neighbor Search via Caching",
        "doi": "10.1109/TKDE.2026.3700562",
        "arxiv_id": "",
        "query": "ANN-Cache: Accelerating Approximate Nearest Neighbor Search via Caching",
        "note": "Topic 4: Caching framework to accelerate graph ANN / HNSW queries by exploiting spatial/temporal locality"
    },
    {
        "bibkey": "liu2025tieredcache",
        "title": "Tiered Cache-HNSW: Using Hierarchical Caching System in HNSW",
        "doi": "10.1109/icct-pacific63901.2025.11012786",
        "arxiv_id": "",
        "query": "Tiered Cache-HNSW: Using Hierarchical Caching System in HNSW",
        "note": "Topic 4: Hierarchical tiered caching system to reduce cache misses during HNSW traversal"
    },
    {
        "bibkey": "zhang2026io",
        "title": "I/O Optimizations for Graph-Based Disk-Resident Approximate Nearest Neighbor Search: A Design Space Exploration",
        "doi": "",
        "arxiv_id": "2602.21514",
        "query": "2602.21514",
        "note": "Topic 4: Memory-access, page caching, and I/O access pattern optimizations for disk-resident graph ANN"
    },
    {
        "bibkey": "huang2025dhnsw",
        "title": "Efficient Vector Search on Disaggregated Memory with d-HNSW",
        "doi": "",
        "arxiv_id": "2505.11783",
        "query": "2505.11783",
        "note": "Topic 4: Disaggregated memory traversal, remote memory access latency, and cache prefetching in HNSW"
    },
    {
        "bibkey": "liu2025shine",
        "title": "SHINE: A Scalable HNSW Index in Disaggregated Memory",
        "doi": "",
        "arxiv_id": "2507.17647",
        "query": "2507.17647",
        "note": "Topic 4: Memory access patterns and caching index partitions for HNSW traversal in disaggregated memory"
    },
    {
        "bibkey": "wu2025inmemory",
        "title": "Toward Efficient and Scalable Design of In-Memory Graph-Based Vector Search",
        "doi": "",
        "arxiv_id": "2509.05750",
        "query": "2509.05750",
        "note": "Topic 4: Architectural characterization of CPU memory hierarchy and cache-miss bottlenecks during in-memory graph ANN"
    }
]

# Fetch metadata
def fetch_doi_meta(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0 (mailto:researcher@test.edu)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            msg = data.get("message", {})
            title = msg.get("title", [""])[0]
            authors_list = msg.get("author", [])
            auth_str = ", ".join([f"{a.get('family', '')}, {a.get('given', '')}".strip(', ') for a in authors_list])
            venue = msg.get("container-title", [""])[0] or msg.get("publisher", "")
            issued = msg.get("issued", {}).get("date-parts", [[None]])[0][0]
            link = msg.get("URL", f"https://doi.org/{doi}")
            return {"title": title, "authors": auth_str, "venue": venue, "year": str(issued), "link": link}
    except Exception as e:
        print(f"DOI fetch failed for {doi}: {e}")
        return None

def fetch_arxiv_meta(aid):
    url = f"https://export.arxiv.org/api/query?id_list={aid}"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            root = ET.fromstring(resp.read().decode('utf-8'))
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            entry = root.find("atom:entry", ns)
            if entry is None:
                return None
            title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
            title = " ".join(title.split())
            auths = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
            published = entry.find("atom:published", ns).text[:4]
            link = f"https://arxiv.org/abs/{aid}"
            return {"title": title, "authors": ", ".join(auths), "venue": "arXiv preprint", "year": published, "link": link}
    except Exception as e:
        print(f"arXiv fetch failed for {aid}: {e}")
        return None

# Load manifest
with open("manifest.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

manifest_keys = set(r["bibkey"] for r in rows)

new_rows = []
for cand in topic4_candidates:
    k = cand["bibkey"]
    if k in manifest_keys:
        print(f"Already in manifest: {k}")
        continue
    meta = None
    if cand["doi"]:
        meta = fetch_doi_meta(cand["doi"])
    elif cand["arxiv_id"]:
        meta = fetch_arxiv_meta(cand["arxiv_id"])
    
    if not meta:
        print(f"Could not resolve metadata for {k}")
        continue
    
    new_r = {
        "bibkey": k,
        "group": "C", # Graph ANN / hardware architecture
        "seed_status": "",
        "verified_status": "PUB" if cand["doi"] else "PRE",
        "title": meta["title"],
        "link": meta["link"],
        "doi": cand["doi"],
        "arxiv_id": cand["arxiv_id"],
        "verified_venue": meta["venue"],
        "verified_year": meta["year"],
        "origin": "snowball",
        "verification_result": "OK",
        "notes": cand["note"],
        "relevance": "KEEP",
        "relevance_reason": "Topic 4: Memory-access, cache-miss, or prefetching in graph ANN",
        "added_in_gate": "5",
        "review_status": "SNOWBALL-CANDIDATE",
        "full_text_status": "PENDING-DOWNLOAD",
        "pdf_source": "arxiv" if cand["arxiv_id"] else "doi",
        "text_version": "arXiv" if cand["arxiv_id"] else "published",
        "source_url": meta["link"],
        "file_size_bytes": "",
        "cited_by": "search_topic_4"
    }
    # Ensure all fieldnames covered
    for fn in fieldnames:
        if fn not in new_r:
            new_r[fn] = ""
    rows.append(new_r)
    new_rows.append(new_r)
    print(f"Added {k}: {meta['title']} ({meta['year']})")

with open("manifest.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated manifest.csv: added {len(new_rows)} Topic 4 candidate papers (total rows: {len(rows)}).")

with open("tools/topic4_resolved.json", "w", encoding="utf-8") as f:
    json.dump(new_rows, f, indent=2)
