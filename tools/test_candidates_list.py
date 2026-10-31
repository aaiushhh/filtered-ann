import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import time
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

candidates = [
    # Topic 1: AMQ filters in graph / vector search / core filter variants
    {"bibkey": "breslow2018morton", "topic": 1, "query": "Morton Filters: Faster, Space-Efficient Cuckoo Filters via Biasing, Compression, and Decoupled Logical Sparsity", "target_doi": "10.14778/3229863.3229875"},
    {"bibkey": "dillinger2021ribbon", "topic": 1, "query": "Ribbon filter: practically smaller than Bloom and Xor", "arxiv_id": "2103.02515"},
    {"bibkey": "wang2019vacuum", "topic": 1, "query": "Vacuum Filters: More Space-Efficient and Faster Replacement for Bloom and Cuckoo Filters", "target_doi": "10.14778/3364376.3364384"},
    {"bibkey": "pagh2004cuckoo", "topic": 1, "query": "Cuckoo Hashing Pagh Rodler", "target_doi": "10.1016/j.jalgor.2003.12.002"},
    {"bibkey": "broder2004network", "topic": 1, "query": "Network Applications of Bloom Filters: A Survey Broder Mitzenmacher", "target_doi": "10.1080/15427951.2004.10129096"},
    {"bibkey": "mitzenmacher2018model", "topic": 1, "query": "A Model for Learned Bloom Filters and Optimizing by Sandwiching Mitzenmacher", "target_doi": ""},
    {"bibkey": "zhang2018surf", "topic": 1, "query": "SuRF: Practical Range Query Filtering with Fast Succinct Tries", "target_doi": "10.1145/3183713.3196931"},
    
    # Topic 2: Selectivity-aware cost models / complexity analysis for filtered ANN
    {"bibkey": "gupta2023caps", "topic": 2, "query": "CAPS: A Partition-based Index for Filtered Similarity Search", "arxiv_id": "2308.15014"},
    {"bibkey": "zuo2023arkgraph", "topic": 2, "query": "ARKGraph: All-Range Approximate K-Nearest-Neighbor Graph", "target_doi": "10.14778/3587136.3587143"},
    {"bibkey": "li2025sieve", "topic": 2, "query": "SIEVE: A Framework for Efficient Filtered Vector Search", "target_doi": ""},
    {"bibkey": "zheng2025digra", "topic": 2, "query": "DIGRA: A Directed Graph-based Approach for Range-filtered Approximate Nearest Neighbor Search", "target_doi": ""},

    # Topic 3: Set-membership / access-control predicates in vector search
    {"bibkey": "zhang2023vbase", "topic": 3, "query": "VBASE: Unifying Online Vector Similarity Search and Relational Queries via Relaxed Monotonicity", "target_doi": ""},
    {"bibkey": "multifilterann", "topic": 3, "query": "Multi-Filter Approximate Nearest Neighbor Search", "target_doi": ""},

    # Topic 4: Cache-miss / memory-latency analysis of HNSW / graph traversal
    {"bibkey": "johnson2019billion", "topic": 4, "query": "Billion-scale similarity search with GPUs Johnson Douze Jegou", "target_doi": "10.1109/TBDATA.2019.2921572"},
    {"bibkey": "ren2020hmann", "topic": 4, "query": "HM-ANN: Efficient Billion-Point Nearest Neighbor Search on Heterogeneous Memory", "target_doi": ""},
    
    # Topic 5: Theory of graph-based ANN search (expected hops, search-cost bounds, LSH)
    {"bibkey": "fu2019nsg", "topic": 5, "query": "Fast Approximate Nearest Neighbor Search With The Navigating Spreading-out Graph Fu", "target_doi": "10.14778/3305387.3305392"},
    {"bibkey": "prokhorenkova2020graph", "topic": 5, "query": "Graph-based nearest neighbor search: From practice to theory Prokhorenkova", "arxiv_id": "2006.05942"},
    {"bibkey": "indyk2023worst", "topic": 5, "query": "Worst-case performance of popular approximate nearest neighbor search implementations: Guarantees and limitations Indyk Xu", "arxiv_id": "2310.17030"},
    {"bibkey": "diwan2024navigable", "topic": 5, "query": "Navigable graphs for high-dimensional nearest neighbor search: Constructions and limits Diwan", "arxiv_id": "2406.07770"},
    {"bibkey": "datar2004locality", "topic": 5, "query": "Locality-sensitive hashing scheme based on p-stable distributions Datar", "target_doi": "10.1145/997817.997857"},
    {"bibkey": "lv2007multiprobe", "topic": 5, "query": "Multi-probe LSH: efficient indexing for high-dimensional similarity search Lv", "target_doi": "10.14778/1456536.1456631"}
]

print(f"Total candidate list: {len(candidates)}")
