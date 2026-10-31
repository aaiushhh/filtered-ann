import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import time
import ssl
import os
import glob
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Load notes to find who cites what
notes = {}
for p in glob.glob("notes/*.md"):
    k = os.path.basename(p)[:-3]
    with open(p, "r", encoding="utf-8") as f:
        notes[k] = f.read()

# Load survey text as well
survey_path = "papers/survey2025filtered.txt"
survey_text = ""
if os.path.exists(survey_path):
    with open(survey_path, "r", encoding="utf-8", errors="ignore") as f:
        survey_text = f.read()

candidate_defs = [
    # Topic 1: AMQ filters in graph / vector search / core filter variants
    {
        "bibkey": "breslow2018morton", "topic": 1, 
        "name": "Morton Filters",
        "doi": "10.14778/3229863.3229875",
        "kw": ["Morton filter", "Morton Filters", "Breslow", "Jayasena"]
    },
    {
        "bibkey": "dillinger2021ribbon", "topic": 1,
        "name": "Ribbon Filter",
        "arxiv_id": "2103.02515",
        "kw": ["Ribbon filter", "Ribbon Filter", "Dillinger", "Walzer"]
    },
    {
        "bibkey": "wang2019vacuum", "topic": 1,
        "name": "Vacuum Filters",
        "doi": "10.14778/3364376.3364384",
        "kw": ["Vacuum filter", "Vacuum Filter", "Vacuum Filters"]
    },
    {
        "bibkey": "pagh2004cuckoo", "topic": 1,
        "name": "Cuckoo Hashing",
        "doi": "10.1016/j.jalgor.2003.12.002",
        "kw": ["Cuckoo hashing", "Cuckoo Hashing", "Pagh", "Rodler"]
    },
    {
        "bibkey": "broder2004network", "topic": 1,
        "name": "Network Applications of Bloom Filters",
        "doi": "10.1080/15427951.2004.10129096",
        "kw": ["Network Applications of Bloom Filters", "Broder"]
    },
    {
        "bibkey": "mitzenmacher2018model", "topic": 1,
        "name": "A Model for Learned Bloom Filters",
        "neurips_url": "https://proceedings.neurips.cc/paper/2018/hash/71e0c50d481b28807d95b5ba6646875b-Abstract.html",
        "arxiv_id": "1802.08881",
        "kw": ["A Model for Learned Bloom Filters", "Sandwiching", "Learned Bloom Filters"]
    },
    {
        "bibkey": "zhang2018surf", "topic": 1,
        "name": "SuRF: Practical Range Query Filtering with Fast Succinct Tries",
        "doi": "10.1145/3183713.3196931",
        "kw": ["SuRF", "Succinct Tries"]
    },
    
    # Topic 2: Selectivity-aware cost models / complexity analysis for filtered ANN
    {
        "bibkey": "gupta2023caps", "topic": 2,
        "name": "CAPS",
        "arxiv_id": "2308.15014",
        "kw": ["CAPS", "Partition-based Index for Filtered Similarity Search"]
    },
    {
        "bibkey": "zuo2023arkgraph", "topic": 2,
        "name": "ARKGraph",
        "doi": "10.14778/3587136.3587143",
        "kw": ["ARKGraph", "All-Range Approximate K-Nearest-Neighbor Graph"]
    },
    {
        "bibkey": "zheng2025digra", "topic": 2,
        "name": "DIGRA",
        "doi": "10.1145/3709675",
        "kw": ["DIGRA", "Directed Graph-based Range-filtered", "Range-filtered Approximate Nearest Neighbor"]
    },
    {
        "bibkey": "li2025sieve", "topic": 2,
        "name": "SIEVE",
        "query": "SIEVE: A Framework for Efficient Filtered Vector Search",
        "arxiv_id": "2411.08271",
        "kw": ["SIEVE", "Filtered Vector Search"]
    },

    # Topic 3: Set-membership / access-control predicates in vector search
    {
        "bibkey": "zhang2023vbase", "topic": 3,
        "name": "VBASE",
        "usenix_url": "https://www.usenix.org/conference/osdi23/presentation/zhang-qianxi",
        "arxiv_id": "2307.03986",
        "kw": ["VBASE", "Relaxed Monotonicity"]
    },
    {
        "bibkey": "xu2024multifilterann", "topic": 3,
        "name": "Multi-Filter ANN Search",
        "query": "Multi-Filter Approximate Nearest Neighbor Search",
        "arxiv_id": "2408.08502",
        "kw": ["MultiFilterANN", "Multi-Filter", "MultiFilter"]
    },

    # Topic 4: Cache-miss / memory-latency analysis of HNSW / graph traversal
    {
        "bibkey": "johnson2019billion", "topic": 4,
        "name": "FAISS (Billion-scale similarity search with GPUs)",
        "doi": "10.1109/TBDATA.2019.2921572",
        "arxiv_id": "1702.08734",
        "kw": ["Billion-scale similarity search with GPUs", "Johnson", "Douze"]
    },
    {
        "bibkey": "ren2020hmann", "topic": 4,
        "name": "HM-ANN",
        "neurips_url": "https://proceedings.neurips.cc/paper/2020/hash/a78b05615797300c14457e937d1ec02a-Abstract.html",
        "arxiv_id": "2006.12028",
        "kw": ["HM-ANN", "Heterogeneous Memory"]
    },
    
    # Topic 5: Theory of graph-based ANN search (expected hops, search-cost bounds, LSH)
    {
        "bibkey": "fu2019nsg", "topic": 5,
        "name": "NSG",
        "doi": "10.14778/3305387.3305392",
        "arxiv_id": "1707.00143",
        "kw": ["Navigating Spreading-out Graph", "NSG", "Cong Fu"]
    },
    {
        "bibkey": "prokhorenkova2020graph", "topic": 5,
        "name": "Graph-based nearest neighbor search: From practice to theory",
        "arxiv_id": "2006.05942",
        "kw": ["Prokhorenkova", "From practice to theory"]
    },
    {
        "bibkey": "indyk2023worst", "topic": 5,
        "name": "Worst-case performance of popular approximate nearest neighbor search implementations",
        "arxiv_id": "2310.17030",
        "kw": ["Indyk", "Xu", "Worst-case performance of popular approximate nearest neighbor"]
    },
    {
        "bibkey": "diwan2024navigable", "topic": 5,
        "name": "Navigable graphs for high-dimensional nearest neighbor search",
        "arxiv_id": "2406.07770",
        "kw": ["Diwan", "Navigable graphs for high-dimensional nearest neighbor"]
    },
    {
        "bibkey": "datar2004locality", "topic": 5,
        "name": "Locality-sensitive hashing scheme based on p-stable distributions",
        "doi": "10.1145/997817.997857",
        "kw": ["p-stable", "Locality-sensitive hashing scheme based on p-stable", "Datar"]
    },
    {
        "bibkey": "lv2007multiprobe", "topic": 5,
        "name": "Multi-probe LSH",
        "doi": "10.14778/1456536.1456631",
        "kw": ["Multi-probe LSH", "Multi-Probe LSH", "Qin Lv"]
    }
]

def fetch_doi(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0 (mailto:research@example.org)"})
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
            return {
                "status": "OK",
                "title": title,
                "authors": auth_str,
                "venue": venue,
                "year": str(issued),
                "doi": doi,
                "link": link
            }
    except Exception as e:
        return {"status": "ERR", "error": str(e)}

def fetch_arxiv(aid):
    url = f"https://export.arxiv.org/api/query?id_list={aid}"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            root = ET.fromstring(resp.read().decode('utf-8'))
            ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
            entry = root.find("atom:entry", ns)
            if entry is None:
                return {"status": "ERR", "error": "Not found in arXiv"}
            title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
            title = " ".join(title.split())
            auths = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
            published = entry.find("atom:published", ns).text[:4]
            doi_elem = entry.find("arxiv:doi", ns)
            doi = doi_elem.text if doi_elem is not None else ""
            link = f"https://arxiv.org/abs/{aid}"
            return {
                "status": "OK",
                "title": title,
                "authors": ", ".join(auths),
                "venue": "arXiv preprint",
                "year": published,
                "doi": doi,
                "arxiv_id": aid,
                "link": link
            }
    except Exception as e:
        return {"status": "ERR", "error": str(e)}

results = []

for c in candidate_defs:
    bibkey = c["bibkey"]
    print(f"Resolving {bibkey}...")
    meta = None
    if "doi" in c and c["doi"]:
        meta = fetch_doi(c["doi"])
        if meta["status"] != "OK" and "arxiv_id" in c:
            meta = fetch_arxiv(c["arxiv_id"])
    elif "arxiv_id" in c:
        meta = fetch_arxiv(c["arxiv_id"])
    
    # Calculate citing notes
    citing = set()
    for nk, text in notes.items():
        if bibkey in text.lower():
            citing.add(nk)
            continue
        for pat in c.get("kw", []):
            if re.search(r'\b' + re.escape(pat) + r'\b', text, re.IGNORECASE):
                citing.add(nk)
                break
    
    # Check survey
    in_survey = False
    for pat in c.get("kw", []):
        if re.search(r'\b' + re.escape(pat) + r'\b', survey_text, re.IGNORECASE):
            in_survey = True
            break
    
    # Determine OA status
    # PVLDB (10.14778) is diamond open access!
    # arXiv is open access!
    # ACM, IEEE, Springer, Elsevier may be paywalled unless author posted on arXiv or open access.
    oa_status = "UNKNOWN"
    pdf_source = ""
    source_url = ""
    
    if meta and meta.get("status") == "OK":
        doi_val = meta.get("doi", "")
        aid_val = meta.get("arxiv_id", c.get("arxiv_id", ""))
        
        if "10.14778" in doi_val: # PVLDB is completely open access
            oa_status = "OK"
            pdf_source = "vldb.org"
            source_url = f"https://www.vldb.org/pvldb/vol{doi_val.split('.')[1] if '.' in doi_val else ''}"
        elif aid_val:
            oa_status = "OK"
            pdf_source = "arxiv"
            source_url = f"https://arxiv.org/pdf/{aid_val}.pdf"
        elif "neurips.cc" in c.get("neurips_url", ""):
            oa_status = "OK"
            pdf_source = "neurips.cc"
            source_url = c["neurips_url"]
        elif "usenix.org" in c.get("usenix_url", ""):
            oa_status = "OK"
            pdf_source = "usenix.org"
            source_url = c["usenix_url"]
        else:
            # Paywalled / needs manual download if publisher is ACM, IEEE, Elsevier
            oa_status = "PAYWALLED"
            pdf_source = "manual"
            source_url = meta.get("link", "")
            
        c_res = {
            "bibkey": bibkey,
            "topic": c["topic"],
            "title": meta.get("title"),
            "authors": meta.get("authors"),
            "venue": meta.get("venue"),
            "year": meta.get("year"),
            "doi": doi_val,
            "arxiv_id": aid_val,
            "link": meta.get("link"),
            "cited_by": sorted(list(citing)),
            "cite_count": len(citing),
            "in_survey": in_survey,
            "oa_status": oa_status,
            "pdf_source": pdf_source,
            "source_url": source_url
        }
        results.append(c_res)
    else:
        print(f"Failed to resolve {bibkey}: {meta}")
    time.sleep(0.5)

with open("tools/snowball_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Successfully resolved {len(results)} candidates.")
