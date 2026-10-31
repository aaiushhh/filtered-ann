import json
import csv
import re
import os
import glob
import urllib.request
import xml.etree.ElementTree as ET
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Load notes
notes = {}
for p in glob.glob("notes/*.md"):
    k = os.path.basename(p)[:-3]
    with open(p, "r", encoding="utf-8") as f:
        notes[k] = f.read()

# Load survey text
with open("papers/survey2025filtered.txt", "r", encoding="utf-8", errors="ignore") as f:
    survey_text = f.read()

# Candidate list
candidates = [
    # TOPIC 1: Bloom / Cuckoo / Xor / AMQ filters in graph / vector search or core AMQ algorithms
    {
        "bibkey": "dillinger2021ribbon",
        "topic": 1,
        "topic_name": "AMQ filters in graph/vector search & core filter algorithms",
        "title": "Ribbon filter: practically smaller than Bloom and Xor",
        "authors": "Peter C. Dillinger, Stefan Walzer",
        "venue": "arXiv preprint",
        "year": "2021",
        "doi": "",
        "arxiv_id": "2103.02515",
        "link": "https://arxiv.org/abs/2103.02515",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/2103.02515.pdf",
        "oa_status": "OK",
        "kw": ["Ribbon filter", "Ribbon Filter", "Dillinger", "Walzer"]
    },
    {
        "bibkey": "breslow2018morton",
        "topic": 1,
        "topic_name": "AMQ filters in graph/vector search & core filter algorithms",
        "title": "Morton Filters: Faster, Space-Efficient Cuckoo Filters via Biasing, Compression, and Decoupled Logical Sparsity",
        "authors": "Alex D. Breslow, Nuwan S. Jayasena",
        "venue": "Proceedings of the VLDB Endowment",
        "year": "2018",
        "doi": "10.14778/3213880.3213884",
        "arxiv_id": "",
        "link": "https://doi.org/10.14778/3213880.3213884",
        "pdf_source": "vldb.org",
        "source_url": "https://www.vldb.org/pvldb/vol11/p1041-breslow.pdf",
        "oa_status": "OK",
        "kw": ["Morton filter", "Morton Filters", "Breslow", "Jayasena"]
    },
    {
        "bibkey": "wang2019vacuum",
        "topic": 1,
        "topic_name": "AMQ filters in graph/vector search & core filter algorithms",
        "title": "Vacuum Filters: More Space-Efficient and Faster Replacement for Bloom and Cuckoo Filters",
        "authors": "Min Wang, Mingxun Zhou, Shouqian Shi, Chenqian Gao",
        "venue": "Proceedings of the VLDB Endowment",
        "year": "2019",
        "doi": "10.14778/3364324.3364333",
        "arxiv_id": "",
        "link": "https://doi.org/10.14778/3364324.3364333",
        "pdf_source": "vldb.org",
        "source_url": "https://www.vldb.org/pvldb/vol13/p197-wang.pdf",
        "oa_status": "OK",
        "kw": ["Vacuum filter", "Vacuum Filter", "Vacuum Filters"]
    },
    {
        "bibkey": "mitzenmacher2018model",
        "topic": 1,
        "topic_name": "AMQ filters in graph/vector search & core filter algorithms",
        "title": "A Model for Learned Bloom Filters, and Optimizing by Sandwiching",
        "authors": "Michael Mitzenmacher",
        "venue": "Advances in Neural Information Processing Systems (NeurIPS 2018)",
        "year": "2018",
        "doi": "",
        "arxiv_id": "1901.00902",
        "link": "https://arxiv.org/abs/1901.00902",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/1901.00902.pdf",
        "oa_status": "OK",
        "kw": ["A Model for Learned Bloom Filters", "Sandwiching", "Learned Bloom Filters"]
    },
    {
        "bibkey": "pagh2004cuckoo",
        "topic": 1,
        "topic_name": "AMQ filters in graph/vector search & core filter algorithms",
        "title": "Cuckoo hashing",
        "authors": "Rasmus Pagh, Flemming Friche Rodler",
        "venue": "Journal of Algorithms",
        "year": "2004",
        "doi": "10.1016/j.jalgor.2003.12.002",
        "arxiv_id": "",
        "link": "https://doi.org/10.1016/j.jalgor.2003.12.002",
        "pdf_source": "manual",
        "source_url": "https://doi.org/10.1016/j.jalgor.2003.12.002",
        "oa_status": "PAYWALLED",
        "kw": ["Cuckoo hashing", "Cuckoo Hashing", "Pagh", "Rodler"]
    },
    {
        "bibkey": "broder2004network",
        "topic": 1,
        "topic_name": "AMQ filters in graph/vector search & core filter algorithms",
        "title": "Network Applications of Bloom Filters: A Survey",
        "authors": "Andrei Broder, Michael Mitzenmacher",
        "venue": "Internet Mathematics",
        "year": "2004",
        "doi": "10.1080/15427951.2004.10129096",
        "arxiv_id": "",
        "link": "https://doi.org/10.1080/15427951.2004.10129096",
        "pdf_source": "manual",
        "source_url": "https://doi.org/10.1080/15427951.2004.10129096",
        "oa_status": "PAYWALLED",
        "kw": ["Network Applications of Bloom Filters", "Broder"]
    },
    {
        "bibkey": "zhang2018surf",
        "topic": 1,
        "topic_name": "AMQ filters in graph/vector search & core filter algorithms",
        "title": "SuRF: Practical Range Query Filtering with Fast Succinct Tries",
        "authors": "Huanchen Zhang, Hyeontaek Lim, Viktor Leis, David G. Andersen, Michael Kaminsky, Kimberly Keeton, Andrew Pavlo",
        "venue": "Proceedings of the 2018 International Conference on Management of Data (SIGMOD 2018)",
        "year": "2018",
        "doi": "10.1145/3183713.3196931",
        "arxiv_id": "",
        "link": "https://doi.org/10.1145/3183713.3196931",
        "pdf_source": "manual",
        "source_url": "https://doi.org/10.1145/3183713.3196931",
        "oa_status": "PAYWALLED",
        "kw": ["SuRF", "Succinct Tries"]
    },

    # TOPIC 2: Selectivity-aware cost models or complexity analysis for filtered ANN
    {
        "bibkey": "gupta2023caps",
        "topic": 2,
        "topic_name": "Selectivity-aware cost models / complexity analysis for filtered ANN",
        "title": "CAPS: A Partition-based Index for Filtered Similarity Search",
        "authors": "Gaurav Gupta, Tharun Medini, Anshumali Shrivastava",
        "venue": "arXiv preprint",
        "year": "2023",
        "doi": "",
        "arxiv_id": "2308.15014",
        "link": "https://arxiv.org/abs/2308.15014",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/2308.15014.pdf",
        "oa_status": "OK",
        "kw": ["CAPS", "Partition-based Index for Filtered Similarity Search"]
    },
    {
        "bibkey": "zuo2023arkgraph",
        "topic": 2,
        "topic_name": "Selectivity-aware cost models / complexity analysis for filtered ANN",
        "title": "ARKGraph: All-Range Approximate K-Nearest-Neighbor Graph",
        "authors": "Chaoji Zuo, Miao Qiao, Wenchao Zhou, Feifei Li, Dong Deng",
        "venue": "Proceedings of the VLDB Endowment",
        "year": "2023",
        "doi": "10.14778/3587136.3587143",
        "arxiv_id": "",
        "link": "https://doi.org/10.14778/3587136.3587143",
        "pdf_source": "vldb.org",
        "source_url": "https://www.vldb.org/pvldb/vol16/p1431-zuo.pdf",
        "oa_status": "OK",
        "kw": ["ARKGraph", "All-Range Approximate K-Nearest-Neighbor Graph"]
    },
    {
        "bibkey": "li2025sieve",
        "topic": 2,
        "topic_name": "Selectivity-aware cost models / complexity analysis for filtered ANN",
        "title": "SIEVE: A Framework for Efficient Filtered Vector Search",
        "authors": "Rui Li, Yuming Xu, Jiayi Wang, Feifei Li",
        "venue": "arXiv preprint",
        "year": "2024",
        "doi": "",
        "arxiv_id": "2411.08271",
        "link": "https://arxiv.org/abs/2411.08271",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/2411.08271.pdf",
        "oa_status": "OK",
        "kw": ["SIEVE", "Filtered Vector Search"]
    },
    {
        "bibkey": "zheng2025digra",
        "topic": 2,
        "topic_name": "Selectivity-aware cost models / complexity analysis for filtered ANN",
        "title": "DIGRA: A Directed Graph-based Approach for Range-filtered Approximate Nearest Neighbor Search",
        "authors": "Bolong Zheng, Cong Fu, Feifei Li, Christian S. Jensen",
        "venue": "Proceedings of the ACM on Management of Data (PACMMOD 2025)",
        "year": "2025",
        "doi": "10.1145/3709675",
        "arxiv_id": "",
        "link": "https://doi.org/10.1145/3709675",
        "pdf_source": "manual",
        "source_url": "https://doi.org/10.1145/3709675",
        "oa_status": "PAYWALLED",
        "kw": ["DIGRA", "Directed Graph-based Range-filtered", "Range-filtered Approximate Nearest Neighbor"]
    },

    # TOPIC 3: Set-membership or access-control predicates in vector search
    {
        "bibkey": "zhang2023vbase",
        "topic": 3,
        "topic_name": "Set-membership / access-control predicates in vector search",
        "title": "VBASE: Unifying Online Vector Similarity Search and Relational Queries via Relaxed Monotonicity",
        "authors": "Qianxi Zhang, Hantao Wang, Haodong Duan, Cong Fu",
        "venue": "17th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2023)",
        "year": "2023",
        "doi": "",
        "arxiv_id": "2307.03986",
        "link": "https://arxiv.org/abs/2307.03986",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/2307.03986.pdf",
        "oa_status": "OK",
        "kw": ["VBASE", "Relaxed Monotonicity"]
    },
    {
        "bibkey": "xu2024multifilterann",
        "topic": 3,
        "topic_name": "Set-membership / access-control predicates in vector search",
        "title": "Multi-Filter Approximate Nearest Neighbor Search",
        "authors": "Chen Xu, Peng Wang, Chaokun Wang",
        "venue": "arXiv preprint",
        "year": "2024",
        "doi": "",
        "arxiv_id": "2408.08502",
        "link": "https://arxiv.org/abs/2408.08502",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/2408.08502.pdf",
        "oa_status": "OK",
        "kw": ["MultiFilterANN", "Multi-Filter", "MultiFilter"]
    },

    # TOPIC 4: Cache-miss / memory-latency analysis of HNSW / graph traversal
    {
        "bibkey": "johnson2019billion",
        "topic": 4,
        "topic_name": "Cache-miss / memory-latency analysis of HNSW traversal",
        "title": "Billion-Scale Similarity Search with GPUs",
        "authors": "Jeff Johnson, Matthijs Douze, Hervé Jégou",
        "venue": "IEEE Transactions on Big Data",
        "year": "2019",
        "doi": "10.1109/TBDATA.2019.2921572",
        "arxiv_id": "1702.08734",
        "link": "https://arxiv.org/abs/1702.08734",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/1702.08734.pdf",
        "oa_status": "OK",
        "kw": ["Billion-scale similarity search with GPUs", "Johnson", "Douze", "8733051"]
    },
    {
        "bibkey": "ren2020hmann",
        "topic": 4,
        "topic_name": "Cache-miss / memory-latency analysis of HNSW traversal",
        "title": "HM-ANN: Efficient Billion-Point Nearest Neighbor Search on Heterogeneous Memory",
        "authors": "Jie Ren, Minjia Zhang, Dong Li",
        "venue": "Advances in Neural Information Processing Systems (NeurIPS 2020)",
        "year": "2020",
        "doi": "",
        "arxiv_id": "2006.12028",
        "link": "https://arxiv.org/abs/2006.12028",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/2006.12028.pdf",
        "oa_status": "OK",
        "kw": ["HM-ANN", "Heterogeneous Memory"]
    },

    # TOPIC 5: Theory of graph-based ANN search (expected hops, search-cost bounds)
    {
        "bibkey": "fu2019nsg",
        "topic": 5,
        "topic_name": "Theory of graph-based ANN search (expected hops, search-cost bounds)",
        "title": "Fast Approximate Nearest Neighbor Search With The Navigating Spreading-out Graph",
        "authors": "Cong Fu, Chao Xiang, Changxu Wang, Deng Cai",
        "venue": "Proceedings of the VLDB Endowment",
        "year": "2019",
        "doi": "10.14778/3305387.3305392",
        "arxiv_id": "1707.00143",
        "link": "https://doi.org/10.14778/3305387.3305392",
        "pdf_source": "vldb.org",
        "source_url": "https://www.vldb.org/pvldb/vol12/p461-fu.pdf",
        "oa_status": "OK",
        "kw": ["Navigating Spreading-out Graph", "NSG", "Cong Fu"]
    },
    {
        "bibkey": "prokhorenkova2020graph",
        "topic": 5,
        "topic_name": "Theory of graph-based ANN search (expected hops, search-cost bounds)",
        "title": "Graph-based nearest neighbor search: From practice to theory",
        "authors": "Liudmila Prokhorenkova, Aleksandr Shekhovtsov",
        "venue": "Proceedings of the 37th International Conference on Machine Learning (ICML 2020)",
        "year": "2020",
        "doi": "",
        "arxiv_id": "2006.05942",
        "link": "https://arxiv.org/abs/2006.05942",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/2006.05942.pdf",
        "oa_status": "OK",
        "kw": ["Prokhorenkova", "From practice to theory"]
    },
    {
        "bibkey": "indyk2023worst",
        "topic": 5,
        "topic_name": "Theory of graph-based ANN search (expected hops, search-cost bounds)",
        "title": "Worst-case performance of popular approximate nearest neighbor search implementations: Guarantees and limitations",
        "authors": "Piotr Indyk, Haike Xu",
        "venue": "Advances in Neural Information Processing Systems (NeurIPS 2023)",
        "year": "2023",
        "doi": "",
        "arxiv_id": "2310.17030",
        "link": "https://arxiv.org/abs/2310.17030",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/2310.17030.pdf",
        "oa_status": "OK",
        "kw": ["Indyk", "Xu", "Worst-case performance of popular approximate nearest neighbor"]
    },
    {
        "bibkey": "diwan2024navigable",
        "topic": 5,
        "topic_name": "Theory of graph-based ANN search (expected hops, search-cost bounds)",
        "title": "Navigable graphs for high-dimensional nearest neighbor search: Constructions and limits",
        "authors": "Aditi Diwan, Piotr Indyk, Sandeep Silwal, Haike Xu",
        "venue": "Advances in Neural Information Processing Systems (NeurIPS 2024)",
        "year": "2024",
        "doi": "",
        "arxiv_id": "2406.07770",
        "link": "https://arxiv.org/abs/2406.07770",
        "pdf_source": "arxiv",
        "source_url": "https://arxiv.org/pdf/2406.07770.pdf",
        "oa_status": "OK",
        "kw": ["Diwan", "Navigable graphs for high-dimensional nearest neighbor"]
    },
    {
        "bibkey": "lv2007multiprobe",
        "topic": 5,
        "topic_name": "Theory of graph-based ANN search (expected hops, search-cost bounds)",
        "title": "Multi-probe LSH: efficient indexing for high-dimensional similarity search",
        "authors": "Qin Lv, William K. Josephson, Zhe Wang, Moses Charikar, Kai Li",
        "venue": "Proceedings of the 33rd International Conference on Very Large Data Bases (VLDB 2007)",
        "year": "2007",
        "doi": "",
        "arxiv_id": "",
        "link": "http://www.vldb.org/conf/2007/papers/research/p950-lv.pdf",
        "pdf_source": "vldb.org",
        "source_url": "http://www.vldb.org/conf/2007/papers/research/p950-lv.pdf",
        "oa_status": "OK",
        "kw": ["Multi-probe LSH", "Multi-Probe LSH", "Qin Lv"]
    },
    {
        "bibkey": "datar2004locality",
        "topic": 5,
        "topic_name": "Theory of graph-based ANN search (expected hops, search-cost bounds)",
        "title": "Locality-sensitive hashing scheme based on p-stable distributions",
        "authors": "Mayur Datar, Nicole Immorlica, Piotr Indyk, Vahab S. Mirrokni",
        "venue": "Proceedings of the twentieth annual symposium on Computational geometry (SoCG 2004)",
        "year": "2004",
        "doi": "10.1145/997817.997857",
        "arxiv_id": "",
        "link": "https://doi.org/10.1145/997817.997857",
        "pdf_source": "manual",
        "source_url": "https://doi.org/10.1145/997817.997857",
        "oa_status": "PAYWALLED",
        "kw": ["p-stable", "Locality-sensitive hashing scheme based on p-stable", "Datar"]
    }
]

# Calculate exact citing notes for each candidate
for c in candidates:
    citing = set()
    for nk, text in notes.items():
        if c["bibkey"] in text.lower():
            citing.add(nk)
            continue
        for pat in c.get("kw", []):
            if re.search(r'\b' + re.escape(pat) + r'\b', text, re.IGNORECASE):
                citing.add(nk)
                break
    c["cited_by"] = sorted(list(citing))
    c["cite_count"] = len(citing)

# Sort candidates by cite_count descending
candidates.sort(key=lambda x: (x["cite_count"], -x["topic"]), reverse=True)

print("RANKED CANDIDATES:")
for c in candidates:
    print(f"[{c['cite_count']} citations] {c['bibkey']:22} | Topic {c['topic']} | OA: {c['oa_status']:9} | Cited by: {', '.join(c['cited_by'][:3])}")

with open("tools/snowball_ranked.json", "w", encoding="utf-8") as f:
    json.dump(candidates, f, indent=2)
