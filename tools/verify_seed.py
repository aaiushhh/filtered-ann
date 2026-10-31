import urllib.request
import urllib.parse
import urllib.error
import json
import xml.etree.ElementTree as ET
import time
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

SEEDS = [
    {
        "bibkey": "bloom1970space",
        "group": "A",
        "status_claim": "PUB",
        "title": "Space/Time Trade-offs in Hash Coding with Allowable Errors",
        "link": "https://dl.acm.org/doi/10.1145/362686.362692",
        "doi": "10.1145/362686.362692"
    },
    {
        "bibkey": "fan2014cuckoo",
        "group": "A",
        "status_claim": "PUB",
        "title": "Cuckoo Filter: Practically Better Than Bloom",
        "link": "https://dl.acm.org/doi/10.1145/2674005.2674994",
        "doi": "10.1145/2674005.2674994"
    },
    {
        "bibkey": "eppstein2016cuckoo",
        "group": "A",
        "status_claim": "PUB",
        "title": "Cuckoo Filter: Simplification and Analysis",
        "link": "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SWAT.2016.8",
        "doi": "10.4230/LIPIcs.SWAT.2016.8"
    },
    {
        "bibkey": "graf2020xor",
        "group": "A",
        "status_claim": "PUB (journal: ACM JEA, DOI 10.1145/3376122) / PRE copy",
        "title": "Xor Filters: Faster and Smaller Than Bloom and Cuckoo Filters",
        "link": "https://arxiv.org/abs/1912.08258",
        "arxiv_id": "1912.08258",
        "doi": "10.1145/3376122"
    },
    {
        "bibkey": "mitzenmacher2017adaptive",
        "group": "A",
        "status_claim": "PRE?",
        "title": "Adaptive Cuckoo Filters",
        "link": "https://arxiv.org/abs/1704.06818",
        "arxiv_id": "1704.06818"
    },
    {
        "bibkey": "maplets2025",
        "group": "A",
        "status_claim": "PRE",
        "title": "Time To Replace Your Filter: How Maplets Simplify System Design",
        "link": "https://arxiv.org/abs/2510.05518",
        "arxiv_id": "2510.05518"
    },
    {
        "bibkey": "kraska2018learned",
        "group": "B",
        "status_claim": "PUB",
        "title": "The Case for Learned Index Structures",
        "link": "https://dl.acm.org/doi/10.1145/3183713.3196909",
        "doi": "10.1145/3183713.3196909"
    },
    {
        "bibkey": "indyk1998approximate",
        "group": "B",
        "status_claim": "PUB",
        "title": "Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality",
        "link": "https://dl.acm.org/doi/10.1145/276698.276876",
        "doi": "10.1145/276698.276876"
    },
    {
        "bibkey": "pla2025learned",
        "group": "B",
        "status_claim": "PRE",
        "title": "Piecewise Linear Approximation in Learned Index Structures: Theoretical and Empirical Analysis",
        "link": "https://arxiv.org/abs/2506.20139",
        "arxiv_id": "2506.20139"
    },
    {
        "bibkey": "superseding2019learning",
        "group": "B",
        "status_claim": "PRE?",
        "title": "Superseding Traditional Indexes by Orchestrating Learning and Geometry",
        "link": "https://arxiv.org/abs/1903.00507",
        "arxiv_id": "1903.00507"
    },
    {
        "bibkey": "lshlowerbounds2005",
        "group": "B",
        "status_claim": "PRE?",
        "title": "Lower Bounds on Locality Sensitive Hashing",
        "link": "https://arxiv.org/abs/cs/0510088",
        "arxiv_id": "cs/0510088"
    },
    {
        "bibkey": "malkov2020hnsw",
        "group": "C",
        "status_claim": "PUB",
        "title": "Efficient and Robust ANN Search Using Hierarchical Navigable Small World Graphs",
        "link": "https://dl.acm.org/doi/10.1109/TPAMI.2018.2889473",
        "doi": "10.1109/TPAMI.2018.2889473",
        "arxiv_id": "1603.09320"
    },
    {
        "bibkey": "subramanya2019diskann",
        "group": "C",
        "status_claim": "PUB",
        "title": "DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node",
        "link": "https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html",
        "doi": None
    },
    {
        "bibkey": "chen2021spann",
        "group": "C",
        "status_claim": "PUB?",
        "title": "SPANN: Highly-efficient Billion-scale Approximate Nearest Neighbor Search",
        "link": "https://arxiv.org/abs/2111.08566",
        "arxiv_id": "2111.08566"
    },
    {
        "bibkey": "beam2025distance",
        "group": "C",
        "status_claim": "PRE",
        "title": "Distance Adaptive Beam Search for Provably Accurate Graph-Based Nearest Neighbor Search",
        "link": "https://arxiv.org/abs/2505.15636",
        "arxiv_id": "2505.15636"
    },
    {
        "bibkey": "manohar2025range",
        "group": "C",
        "status_claim": "PRE",
        "title": "Range Retrieval with Graph-Based Indices",
        "link": "https://arxiv.org/abs/2502.13245",
        "arxiv_id": "2502.13245"
    },
    {
        "bibkey": "survey2025filtered",
        "group": "D",
        "status_claim": "PRE",
        "title": "Survey of Filtered Approximate Nearest Neighbor Search over the Vector-Scalar Hybrid Data",
        "link": "https://arxiv.org/abs/2505.06501",
        "arxiv_id": "2505.06501"
    },
    {
        "bibkey": "filtered2026system",
        "group": "D",
        "status_claim": "PRE",
        "title": "Filtered ANN Search in Vector Databases: System Design and Performance Analysis",
        "link": "https://arxiv.org/abs/2602.11443",
        "arxiv_id": "2602.11443"
    },
    {
        "bibkey": "routing2026query",
        "group": "D",
        "status_claim": "PRE",
        "title": "Query-aware Routing for Filtered Approximate Nearest Neighbors Search",
        "link": "https://arxiv.org/abs/2606.19898",
        "arxiv_id": "2606.19898"
    },
    {
        "bibkey": "curator2026",
        "group": "D",
        "status_claim": "PRE",
        "title": "Curator: Efficient Vector Search with Low-Selectivity Filters",
        "link": "https://arxiv.org/abs/2601.01291",
        "arxiv_id": "2601.01291"
    },
    {
        "bibkey": "filteraware2025",
        "group": "D",
        "status_claim": "PRE",
        "title": "Learning Filter-Aware Distance Metrics for NN Search with Multiple Filters",
        "link": "https://arxiv.org/abs/2511.04073",
        "arxiv_id": "2511.04073"
    },
    {
        "bibkey": "rangefilters2026",
        "group": "D",
        "status_claim": "PRE",
        "title": "Approximate Nearest Neighbor Search with Graph Range Filters",
        "link": "https://arxiv.org/abs/2607.00727",
        "arxiv_id": "2607.00727"
    },
    {
        "bibkey": "matsui2025lotusfilter",
        "group": "E",
        "status_claim": "PUB",
        "title": "LotusFilter: Fast Diverse Nearest Neighbor Search via a Learned Cutoff Table",
        "link": "https://openaccess.thecvf.com/content/CVPR2025/papers/Matsui_LotusFilter_Fast_Diverse_Nearest_Neighbor_Search_via_a_Learned_Cutoff_CVPR_2025_paper.pdf",
        "doi": None
    },
    {
        "bibkey": "pipeannfilter2026",
        "group": "E",
        "status_claim": "PRE",
        "title": "PipeANN-Filter: An Efficient Filtered Vector Search System on SSD",
        "link": "https://arxiv.org/abs/2605.17992",
        "arxiv_id": "2605.17992"
    },
    {
        "bibkey": "cftrag2025",
        "group": "E",
        "status_claim": "PRE",
        "title": "CFT-RAG: An Entity Tree Based RAG Algorithm With Cuckoo Filter",
        "link": "https://arxiv.org/abs/2501.15098",
        "arxiv_id": "2501.15098"
    },
    {
        "bibkey": "bridgerag2026",
        "group": "E",
        "status_claim": "PRE",
        "title": "Bridge-RAG: An Abstract Bridge Tree Based RAG Algorithm",
        "link": "https://arxiv.org/abs/2603.26668",
        "arxiv_id": "2603.26668"
    },
    {
        "bibkey": "cuckoogpu2026",
        "group": "E",
        "status_claim": "PRE",
        "title": "Cuckoo-GPU: Accelerating Cuckoo Filters on Modern GPUs",
        "link": "https://arxiv.org/abs/2603.15486",
        "arxiv_id": "2603.15486"
    }
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def check_url(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            return resp.getcode(), resp.geturl()
    except urllib.error.HTTPError as e:
        return e.code, str(e)
    except Exception as e:
        return -1, str(e)

def get_crossref(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'FilteredANNLiteraturePipeline/1.0 (mailto:researcher@example.org)'
    })
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            if resp.getcode() == 200:
                data = json.loads(resp.read().decode('utf-8'))
                return data.get('message', {})
    except Exception as e:
        print(f"  [Crossref error for {doi}]: {e}", flush=True)
    return None

def get_arxiv(arxiv_id):
    clean_id = arxiv_id.strip()
    url = f"http://export.arxiv.org/api/query?id_list={clean_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            entry = root.find('atom:entry', ns)
            if entry is not None:
                title_elem = entry.find('atom:title', ns)
                title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else None
                if title == "Error" or (title and "Error" in title and len(title) < 20):
                    summary = entry.find('atom:summary', ns)
                    return {"found": False, "error": summary.text.strip() if summary is not None else "Not found"}
                
                authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
                published = entry.find('atom:published', ns).text if entry.find('atom:published', ns) is not None else None
                updated = entry.find('atom:updated', ns).text if entry.find('atom:updated', ns) is not None else None
                doi_elem = entry.find('arxiv:doi', ns)
                doi = doi_elem.text if doi_elem is not None else None
                journal_elem = entry.find('arxiv:journal_ref', ns)
                journal_ref = journal_elem.text if journal_elem is not None else None
                comment_elem = entry.find('arxiv:comment', ns)
                comment = comment_elem.text if comment_elem is not None else None
                
                return {
                    "found": True,
                    "title": title,
                    "authors": authors,
                    "published": published,
                    "updated": updated,
                    "doi": doi,
                    "journal_ref": journal_ref,
                    "comment": comment
                }
    except Exception as e:
        print(f"  [arXiv error for {arxiv_id}]: {e}", flush=True)
        return {"found": False, "error": str(e)}
    return {"found": False, "error": "unknown"}

def main():
    results = []
    print(f"Starting verification of {len(SEEDS)} seed papers...", flush=True)
    for idx, s in enumerate(SEEDS, 1):
        print(f"[{idx}/{len(SEEDS)}] Checking {s['bibkey']}...", flush=True)
        code, final_url = check_url(s['link'])
        print(f"  -> Link status: {code}", flush=True)
        res = {
            "bibkey": s['bibkey'],
            "group": s['group'],
            "seed_title": s['title'],
            "seed_status": s['status_claim'],
            "link": s['link'],
            "http_code": code,
            "final_url": final_url,
            "crossref_data": None,
            "arxiv_data": None
        }
        
        if s.get('doi'):
            print(f"  -> Fetching Crossref {s['doi']}...", flush=True)
            cr = get_crossref(s['doi'])
            res['crossref_data'] = cr
            time.sleep(0.2)
            
        if s.get('arxiv_id'):
            print(f"  -> Fetching arXiv {s['arxiv_id']}...", flush=True)
            ar = get_arxiv(s['arxiv_id'])
            res['arxiv_data'] = ar
            time.sleep(0.3)
            
        results.append(res)
        
    with open("tools/verification_raw.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Saved raw verification to tools/verification_raw.json", flush=True)

if __name__ == "__main__":
    main()
