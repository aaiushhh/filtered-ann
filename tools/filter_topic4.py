import json

with open("tools/topic4_candidates_raw.json", "r", encoding="utf-8") as f:
    items = json.load(f)

keywords = ["cache", "prefetch", "memory", "hnsw", "graph", "traversal", "latency"]

filtered = []
for it in items:
    title = it["title"]
    summary = it.get("summary", "")
    full = (title + " " + summary).lower()
    if ("hnsw" in full or "nearest neighbor" in full or "vector search" in full or "graph" in full) and \
       ("cache" in full or "prefetch" in full or "memory" in full or "latency" in full):
        filtered.append(it)

print(f"Filtered {len(filtered)} items:")
for it in filtered[:15]:
    print(f"- [{it['source']}] {it['title']} ({it['year']}) | {it.get('venue', '')}")
    if "arxiv_id" in it:
        print(f"  arXiv: {it['arxiv_id']}")
    if "doi" in it:
        print(f"  DOI: {it['doi']}")
