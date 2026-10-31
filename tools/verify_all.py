import subprocess
import json
import re
import urllib.parse
import html

SEEDS = [
    {
        "bibkey": "bloom1970space",
        "group": "A",
        "seed_status": "PUB",
        "seed_title": "Space/Time Trade-offs in Hash Coding with Allowable Errors",
        "link": "https://dl.acm.org/doi/10.1145/362686.362692",
        "doi": "10.1145/362686.362692",
        "arxiv_id": None
    },
    {
        "bibkey": "fan2014cuckoo",
        "group": "A",
        "seed_status": "PUB",
        "seed_title": "Cuckoo Filter: Practically Better Than Bloom",
        "link": "https://dl.acm.org/doi/10.1145/2674005.2674994",
        "doi": "10.1145/2674005.2674994",
        "arxiv_id": None
    },
    {
        "bibkey": "eppstein2016cuckoo",
        "group": "A",
        "seed_status": "PUB",
        "seed_title": "Cuckoo Filter: Simplification and Analysis",
        "link": "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SWAT.2016.8",
        "doi": "10.4230/LIPIcs.SWAT.2016.8",
        "arxiv_id": None
    },
    {
        "bibkey": "graf2020xor",
        "group": "A",
        "seed_status": "PUB (journal: ACM JEA, DOI 10.1145/3376122) / PRE copy",
        "seed_title": "Xor Filters: Faster and Smaller Than Bloom and Cuckoo Filters",
        "link": "https://arxiv.org/abs/1912.08258",
        "doi": "10.1145/3376122",
        "arxiv_id": "1912.08258"
    },
    {
        "bibkey": "mitzenmacher2017adaptive",
        "group": "A",
        "seed_status": "PRE?",
        "seed_title": "Adaptive Cuckoo Filters",
        "link": "https://arxiv.org/abs/1704.06818",
        "doi": None,
        "arxiv_id": "1704.06818"
    },
    {
        "bibkey": "maplets2025",
        "group": "A",
        "seed_status": "PRE",
        "seed_title": "Time To Replace Your Filter: How Maplets Simplify System Design",
        "link": "https://arxiv.org/abs/2510.05518",
        "doi": None,
        "arxiv_id": "2510.05518"
    },
    {
        "bibkey": "kraska2018learned",
        "group": "B",
        "seed_status": "PUB",
        "seed_title": "The Case for Learned Index Structures",
        "link": "https://dl.acm.org/doi/10.1145/3183713.3196909",
        "doi": "10.1145/3183713.3196909",
        "arxiv_id": None
    },
    {
        "bibkey": "indyk1998approximate",
        "group": "B",
        "seed_status": "PUB",
        "seed_title": "Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality",
        "link": "https://dl.acm.org/doi/10.1145/276698.276876",
        "doi": "10.1145/276698.276876",
        "arxiv_id": None
    },
    {
        "bibkey": "pla2025learned",
        "group": "B",
        "seed_status": "PRE",
        "seed_title": "Piecewise Linear Approximation in Learned Index Structures: Theoretical and Empirical Analysis",
        "link": "https://arxiv.org/abs/2506.20139",
        "doi": None,
        "arxiv_id": "2506.20139"
    },
    {
        "bibkey": "superseding2019learning",
        "group": "B",
        "seed_status": "PRE?",
        "seed_title": "Superseding Traditional Indexes by Orchestrating Learning and Geometry",
        "link": "https://arxiv.org/abs/1903.00507",
        "doi": None,
        "arxiv_id": "1903.00507"
    },
    {
        "bibkey": "lshlowerbounds2005",
        "group": "B",
        "seed_status": "PRE?",
        "seed_title": "Lower Bounds on Locality Sensitive Hashing",
        "link": "https://arxiv.org/abs/cs/0510088",
        "doi": None,
        "arxiv_id": "cs/0510088"
    },
    {
        "bibkey": "malkov2020hnsw",
        "group": "C",
        "seed_status": "PUB",
        "seed_title": "Efficient and Robust ANN Search Using Hierarchical Navigable Small World Graphs",
        "link": "https://dl.acm.org/doi/10.1109/TPAMI.2018.2889473",
        "doi": "10.1109/TPAMI.2018.2889473",
        "arxiv_id": "1603.09320"
    },
    {
        "bibkey": "subramanya2019diskann",
        "group": "C",
        "seed_status": "PUB",
        "seed_title": "DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node",
        "link": "https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html",
        "doi": None,
        "arxiv_id": None
    },
    {
        "bibkey": "chen2021spann",
        "group": "C",
        "seed_status": "PUB?",
        "seed_title": "SPANN: Highly-efficient Billion-scale Approximate Nearest Neighbor Search",
        "link": "https://arxiv.org/abs/2111.08566",
        "doi": None,
        "arxiv_id": "2111.08566"
    },
    {
        "bibkey": "beam2025distance",
        "group": "C",
        "seed_status": "PRE",
        "seed_title": "Distance Adaptive Beam Search for Provably Accurate Graph-Based Nearest Neighbor Search",
        "link": "https://arxiv.org/abs/2505.15636",
        "doi": None,
        "arxiv_id": "2505.15636"
    },
    {
        "bibkey": "manohar2025range",
        "group": "C",
        "seed_status": "PRE",
        "seed_title": "Range Retrieval with Graph-Based Indices",
        "link": "https://arxiv.org/abs/2502.13245",
        "doi": None,
        "arxiv_id": "2502.13245"
    },
    {
        "bibkey": "survey2025filtered",
        "group": "D",
        "seed_status": "PRE",
        "seed_title": "Survey of Filtered Approximate Nearest Neighbor Search over the Vector-Scalar Hybrid Data",
        "link": "https://arxiv.org/abs/2505.06501",
        "doi": None,
        "arxiv_id": "2505.06501"
    },
    {
        "bibkey": "filtered2026system",
        "group": "D",
        "seed_status": "PRE",
        "seed_title": "Filtered ANN Search in Vector Databases: System Design and Performance Analysis",
        "link": "https://arxiv.org/abs/2602.11443",
        "doi": None,
        "arxiv_id": "2602.11443"
    },
    {
        "bibkey": "routing2026query",
        "group": "D",
        "seed_status": "PRE",
        "seed_title": "Query-aware Routing for Filtered Approximate Nearest Neighbors Search",
        "link": "https://arxiv.org/abs/2606.19898",
        "doi": None,
        "arxiv_id": "2606.19898"
    },
    {
        "bibkey": "curator2026",
        "group": "D",
        "seed_status": "PRE",
        "seed_title": "Curator: Efficient Vector Search with Low-Selectivity Filters",
        "link": "https://arxiv.org/abs/2601.01291",
        "doi": None,
        "arxiv_id": "2601.01291"
    },
    {
        "bibkey": "filteraware2025",
        "group": "D",
        "seed_status": "PRE",
        "seed_title": "Learning Filter-Aware Distance Metrics for NN Search with Multiple Filters",
        "link": "https://arxiv.org/abs/2511.04073",
        "doi": None,
        "arxiv_id": "2511.04073"
    },
    {
        "bibkey": "rangefilters2026",
        "group": "D",
        "seed_status": "PRE",
        "seed_title": "Approximate Nearest Neighbor Search with Graph Range Filters",
        "link": "https://arxiv.org/abs/2607.00727",
        "doi": None,
        "arxiv_id": "2607.00727"
    },
    {
        "bibkey": "matsui2025lotusfilter",
        "group": "E",
        "seed_status": "PUB",
        "seed_title": "LotusFilter: Fast Diverse Nearest Neighbor Search via a Learned Cutoff Table",
        "link": "https://openaccess.thecvf.com/content/CVPR2025/papers/Matsui_LotusFilter_Fast_Diverse_Nearest_Neighbor_Search_via_a_Learned_Cutoff_CVPR_2025_paper.pdf",
        "doi": "10.1109/cvpr52734.2025.02833",
        "arxiv_id": None
    },
    {
        "bibkey": "pipeannfilter2026",
        "group": "E",
        "seed_status": "PRE",
        "seed_title": "PipeANN-Filter: An Efficient Filtered Vector Search System on SSD",
        "link": "https://arxiv.org/abs/2605.17992",
        "doi": None,
        "arxiv_id": "2605.17992"
    },
    {
        "bibkey": "cftrag2025",
        "group": "E",
        "seed_status": "PRE",
        "seed_title": "CFT-RAG: An Entity Tree Based RAG Algorithm With Cuckoo Filter",
        "link": "https://arxiv.org/abs/2501.15098",
        "doi": None,
        "arxiv_id": "2501.15098"
    },
    {
        "bibkey": "bridgerag2026",
        "group": "E",
        "seed_status": "PRE",
        "seed_title": "Bridge-RAG: An Abstract Bridge Tree Based RAG Algorithm",
        "link": "https://arxiv.org/abs/2603.26668",
        "doi": None,
        "arxiv_id": "2603.26668"
    },
    {
        "bibkey": "cuckoogpu2026",
        "group": "E",
        "seed_status": "PRE",
        "seed_title": "Cuckoo-GPU: Accelerating Cuckoo Filters on Modern GPUs",
        "link": "https://arxiv.org/abs/2603.15486",
        "doi": None,
        "arxiv_id": "2603.15486"
    }
]

def check_link(url):
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '-I', '-L', '--max-time', '15', url]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    # Parse status code from last HTTP block
    codes = re.findall(r'HTTP/\d(?:\.\d)?\s+(\d{3})', res.stdout)
    if codes:
        return int(codes[-1]), codes
    # Try non-HEAD if HEAD failed or empty
    cmd2 = ['curl.exe', '--ssl-no-revoke', '-s', '-o', 'NUL', '-w', '%{http_code}', '--max-time', '15', url]
    res2 = subprocess.run(cmd2, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res2.stdout.strip().isdigit():
        return int(res2.stdout.strip()), [res2.stdout.strip()]
    return -1, [res.stderr.strip()[:100]]

def get_doi_metadata(doi):
    url = f"https://doi.org/{doi}"
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '-L', '-H', 'Accept: application/vnd.citationstyles.csl+json', '--max-time', '15', url]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    try:
        data = json.loads(res.stdout)
        return data
    except Exception:
        # Fallback to Crossref API
        cr_url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
        cr_cmd = ['curl.exe', '--ssl-no-revoke', '-s', '--max-time', '15', cr_url]
        cr_res = subprocess.run(cr_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        try:
            cr_data = json.loads(cr_res.stdout)
            return cr_data.get('message', {})
        except Exception:
            return None

def get_arxiv_metadata(arxiv_id):
    url = f"https://arxiv.org/abs/{arxiv_id}"
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '-L', '--max-time', '15', url]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    html_text = res.stdout
    if not html_text or "404 Not Found" in html_text or "<title>Error</title>" in html_text:
        return {"found": False, "raw_html": html_text[:200]}
    
    # Extract metadata tags
    title_match = re.search(r'<meta name="citation_title" content="(.*?)"', html_text)
    authors = re.findall(r'<meta name="citation_author" content="(.*?)"', html_text)
    date_match = re.search(r'<meta name="citation_date" content="(.*?)"', html_text)
    doi_match = re.search(r'<meta name="citation_doi" content="(.*?)"', html_text)
    journal_match = re.search(r'<meta name="citation_journal_title" content="(.*?)"', html_text)
    
    # Also check page text for DOI or journal ref if not in meta
    if not doi_match:
        page_doi = re.search(r'doi\.org/(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)', html_text)
        doi_val = page_doi.group(1) if page_doi else None
    else:
        doi_val = doi_match.group(1)
        
    return {
        "found": bool(title_match),
        "title": html.unescape(title_match.group(1)) if title_match else None,
        "authors": [html.unescape(a) for a in authors],
        "date": date_match.group(1) if date_match else None,
        "doi": doi_val,
        "journal_title": journal_match.group(1) if journal_match else None
    }

def search_crossref_for_preprint(title, author=None):
    q = urllib.parse.quote(title)
    url = f"https://api.crossref.org/works?query.title={q}&rows=3"
    if author:
        url += f"&query.author={urllib.parse.quote(author)}"
    cmd = ['curl.exe', '--ssl-no-revoke', '-s', '--max-time', '15', url]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    try:
        data = json.loads(res.stdout)
        items = data.get('message', {}).get('items', [])
        # Find item with closest title match
        for item in items:
            cr_title = item.get('title', [''])[0]
            # Normalize comparison
            t1 = re.sub(r'[^a-z0-9]', '', title.lower())
            t2 = re.sub(r'[^a-z0-9]', '', cr_title.lower())
            if t1 in t2 or t2 in t1:
                return item
    except Exception:
        pass
    return None

def main():
    results = []
    print(f"=== Starting Comprehensive Verification of {len(SEEDS)} Seed Papers ===", flush=True)
    
    for i, seed in enumerate(SEEDS, 1):
        bibkey = seed["bibkey"]
        print(f"\n[{i}/{len(SEEDS)}] Processing {bibkey}...", flush=True)
        
        # 1. URL check
        code, history = check_link(seed["link"])
        print(f"  Link: {seed['link']} -> HTTP {code}", flush=True)
        
        meta = {}
        pub_crossref = None
        
        # 2. DOI metadata
        if seed.get("doi"):
            doi_data = get_doi_metadata(seed["doi"])
            if doi_data:
                meta["doi_data"] = doi_data
                print(f"  Fetched DOI metadata for {seed['doi']}", flush=True)
                
        # 3. arXiv metadata
        if seed.get("arxiv_id"):
            ar_data = get_arxiv_metadata(seed["arxiv_id"])
            meta["arxiv_data"] = ar_data
            if ar_data.get("found"):
                print(f"  Fetched arXiv metadata: '{ar_data.get('title')}'", flush=True)
                # Check for published version on Crossref
                first_author = ar_data['authors'][0] if ar_data.get('authors') else None
                if first_author and ',' in first_author:
                    first_author = first_author.split(',')[0]
                cr_match = search_crossref_for_preprint(ar_data.get('title', seed['seed_title']), first_author)
                if cr_match:
                    pub_crossref = cr_match
                    print(f"  Found published version in Crossref: DOI {cr_match.get('DOI')} ({cr_match.get('container-title')})", flush=True)
            else:
                print(f"  WARNING: arXiv ID {seed['arxiv_id']} NOT FOUND or unreachable!", flush=True)
                
        # Special case: NeurIPS proceedings
        if "proceedings.neurips.cc" in seed["link"]:
            cmd = ['curl.exe', '--ssl-no-revoke', '-s', '-L', seed["link"]]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            t_m = re.search(r'<meta name="citation_title" content="(.*?)"', res.stdout)
            a_m = re.findall(r'<meta name="citation_author" content="(.*?)"', res.stdout)
            d_m = re.search(r'<meta name="citation_publication_date" content="(.*?)"', res.stdout)
            meta["neurips_data"] = {
                "title": t_m.group(1) if t_m else None,
                "authors": a_m,
                "date": d_m.group(1) if d_m else "2019",
                "venue": "Advances in Neural Information Processing Systems 32 (NeurIPS 2019)"
            }
            print("  Fetched NeurIPS page metadata", flush=True)
            
        record = {
            "seed": seed,
            "http_code": code,
            "meta": meta,
            "pub_crossref": pub_crossref
        }
        results.append(record)
        
    with open("tools/verification_complete.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print("\n=== Verification finished. Saved tools/verification_complete.json ===", flush=True)

if __name__ == "__main__":
    main()
