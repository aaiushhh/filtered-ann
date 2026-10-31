import csv

# True full titles and relevance for the 4 mismatched papers
phase1_updates = {
    'filtered2026system': {
        'title': 'Filtered Approximate Nearest Neighbor Search in Vector Databases: System Design and Performance Analysis',
        'relevance': 'KEEP',
        'relevance_reason': 'Directly benchmarks and evaluates filtered ANN search execution strategies across modern vector database engines including graph-based HNSW.'
    },
    'filteraware2025': {
        'title': 'Learning Filter-Aware Distance Metrics for Nearest Neighbor Search with Multiple Filters',
        'relevance': 'KEEP',
        'relevance_reason': 'Optimizes graph construction and traversal distance metrics specifically for vector search under multiple discrete attribute filter constraints.'
    },
    'cftrag2025': {
        'title': 'CFT-RAG: An Entity Tree Based Retrieval Augmented Generation Algorithm With Cuckoo Filter',
        'relevance': 'PROPOSED-DROP',
        'relevance_reason': 'Focuses on entity localization in hierarchical tree structures for RAG rather than predicate-constrained vector similarity search in proximity graphs.'
    },
    'bridgerag2026': {
        'title': 'Bridge-RAG: An Abstract Bridge Tree Based Retrieval Augmented Generation Algorithm',
        'relevance': 'PROPOSED-DROP',
        'relevance_reason': 'Applies Cuckoo filters to abstract bridge trees for document chunk retrieval in LLMs, not to predicate pruning in graph-based ANN search.'
    }
}

# The 10 verified additions for Phase 2
additions = [
    {
        'bibkey': 'gollapudi2023filtereddiskann',
        'group': 'D',
        'seed_status': 'PUB',
        'verified_status': 'PUB',
        'title': 'Filtered-DiskANN: Graph Algorithms for Approximate Nearest Neighbor Search with Filters',
        'link': 'https://doi.org/10.1145/3543507.3583552',
        'doi': '10.1145/3543507.3583552',
        'arxiv_id': '',
        'verified_venue': 'Proceedings of the ACM Web Conference 2023',
        'verified_year': '2023',
        'origin': 'snowball',
        'verification_result': 'ok',
        'notes': 'Verified via Crossref. Key baseline for filtered graph traversal.',
        'relevance': 'KEEP',
        'relevance_reason': 'Foundational filtered graph ANN algorithm introducing Filtered-Vamana and Stitched-Vamana.',
        'added_in_gate': '0.5',
        'review_status': 'ADDED-PENDING-USER-REVIEW'
    },
    {
        'bibkey': 'patel2024acorn',
        'group': 'D',
        'seed_status': 'PUB',
        'verified_status': 'PUB',
        'title': 'ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data',
        'link': 'https://doi.org/10.1145/3654923',
        'doi': '10.1145/3654923',
        'arxiv_id': '',
        'verified_venue': 'Proceedings of the ACM on Management of Data',
        'verified_year': '2024',
        'origin': 'snowball',
        'verification_result': 'ok',
        'notes': 'Verified via Crossref. State-of-the-art predicate-agnostic HNSW extension.',
        'relevance': 'KEEP',
        'relevance_reason': 'Extends HNSW traversal to perform predicate-agnostic filtered search using multi-hop routing.',
        'added_in_gate': '0.5',
        'review_status': 'ADDED-PENDING-USER-REVIEW'
    },
    {
        'bibkey': 'luo2025tagfiltered',
        'group': 'D',
        'seed_status': 'PUB',
        'verified_status': 'PUB',
        'title': 'Tag-Filtered Approximate Nearest Neighbor Search',
        'link': 'https://doi.org/10.1109/icde65448.2025.00272',
        'doi': '10.1109/icde65448.2025.00272',
        'arxiv_id': '',
        'verified_venue': '2025 IEEE 41st International Conference on Data Engineering (ICDE)',
        'verified_year': '2025',
        'origin': 'snowball',
        'verification_result': 'ok',
        'notes': 'Verified via Crossref.',
        'relevance': 'KEEP',
        'relevance_reason': 'Directly targets tag-filtered similarity search on graph indexes under low selectivity.',
        'added_in_gate': '0.5',
        'review_status': 'ADDED-PENDING-USER-REVIEW'
    },
    {
        'bibkey': 'wu2022hqann',
        'group': 'D',
        'seed_status': 'PUB',
        'verified_status': 'PUB',
        'title': 'HQANN: Efficient and Robust Similarity Search for Hybrid Queries with Structured and Unstructured Constraints',
        'link': 'https://doi.org/10.1145/3511808.3557610',
        'doi': '10.1145/3511808.3557610',
        'arxiv_id': '',
        'verified_venue': 'Proceedings of the 31st ACM International Conference on Information & Knowledge Management',
        'verified_year': '2022',
        'origin': 'snowball',
        'verification_result': 'ok',
        'notes': 'Verified via Crossref.',
        'relevance': 'KEEP',
        'relevance_reason': 'Pioneering work in hybrid queries combining scalar constraints with graph ANN search.',
        'added_in_gate': '0.5',
        'review_status': 'ADDED-PENDING-USER-REVIEW'
    },
    {
        'bibkey': 'cai2024navigating',
        'group': 'D',
        'seed_status': 'PUB',
        'verified_status': 'PUB',
        'title': 'Navigating Labels and Vectors: A Unified Approach to Filtered Approximate Nearest Neighbor Search',
        'link': 'https://doi.org/10.1145/3698822',
        'doi': '10.1145/3698822',
        'arxiv_id': '',
        'verified_venue': 'Proceedings of the ACM on Management of Data',
        'verified_year': '2024',
        'origin': 'snowball',
        'verification_result': 'ok',
        'notes': 'Verified via Crossref.',
        'relevance': 'KEEP',
        'relevance_reason': 'Unifies label navigation and vector graph traversal for predicate-constrained nearest neighbor search.',
        'added_in_gate': '0.5',
        'review_status': 'ADDED-PENDING-USER-REVIEW'
    },
    {
        'bibkey': 'zuo2024serf',
        'group': 'D',
        'seed_status': 'PUB',
        'verified_status': 'PUB',
        'title': 'SeRF: Segment Graph for Range-Filtering Approximate Nearest Neighbor Search',
        'link': 'https://doi.org/10.1145/3639324',
        'doi': '10.1145/3639324',
        'arxiv_id': '',
        'verified_venue': 'Proceedings of the ACM on Management of Data',
        'verified_year': '2024',
        'origin': 'snowball',
        'verification_result': 'ok',
        'notes': 'Verified via Crossref.',
        'relevance': 'KEEP',
        'relevance_reason': 'Segment graph architecture designed to handle range filter predicates during proximity graph routing.',
        'added_in_gate': '0.5',
        'review_status': 'ADDED-PENDING-USER-REVIEW'
    },
    {
        'bibkey': 'zhang2025dynamic',
        'group': 'D',
        'seed_status': 'PUB',
        'verified_status': 'PUB',
        'title': 'Efficient Dynamic Indexing for Range Filtered Approximate Nearest Neighbor Search',
        'link': 'https://doi.org/10.1145/3725401',
        'doi': '10.1145/3725401',
        'arxiv_id': '',
        'verified_venue': 'Proceedings of the ACM on Management of Data',
        'verified_year': '2025',
        'origin': 'snowball',
        'verification_result': 'ok',
        'notes': 'Verified via Crossref.',
        'relevance': 'KEEP',
        'relevance_reason': 'Dynamic graph indexing strategy for handling updates in range-filtered vector similarity search.',
        'added_in_gate': '0.5',
        'review_status': 'ADDED-PENDING-USER-REVIEW'
    },
    {
        'bibkey': 'zou2026rnsg',
        'group': 'D',
        'seed_status': 'PUB',
        'verified_status': 'PUB',
        'title': 'RNSG: A Range-Aware Graph Index for Efficient Range-Filtered Approximate Nearest Neighbor Search',
        'link': 'https://doi.org/10.14778/3828612.3828636',
        'doi': '10.14778/3828612.3828636',
        'arxiv_id': '',
        'verified_venue': 'Proceedings of the VLDB Endowment',
        'verified_year': '2026',
        'origin': 'snowball',
        'verification_result': 'ok',
        'notes': 'Verified via Crossref.',
        'relevance': 'KEEP',
        'relevance_reason': 'Range-aware graph index specifically tailored to filter predicates in graph ANN search.',
        'added_in_gate': '0.5',
        'review_status': 'ADDED-PENDING-USER-REVIEW'
    },
    {
        'bibkey': 'wang2021milvus',
        'group': 'D',
        'seed_status': 'PUB',
        'verified_status': 'PUB',
        'title': 'Milvus: A Purpose-Built Vector Data Management System',
        'link': 'https://doi.org/10.1145/3448016.3457550',
        'doi': '10.1145/3448016.3457550',
        'arxiv_id': '',
        'verified_venue': 'Proceedings of the 2021 International Conference on Management of Data',
        'verified_year': '2021',
        'origin': 'snowball',
        'verification_result': 'ok',
        'notes': 'Verified via Crossref.',
        'relevance': 'MAYBE',
        'relevance_reason': 'High-impact vector database architecture paper detailing systems-level hybrid filtered query execution.',
        'added_in_gate': '0.5',
        'review_status': 'ADDED-PENDING-USER-REVIEW'
    },
    {
        'bibkey': 'shaikh2026annex',
        'group': 'D',
        'seed_status': 'PUB',
        'verified_status': 'PUB',
        'title': 'ANNex: Efficient Filtered Approximate Nearest Neighbor Search via Graph-Traversal Metadata Filtering',
        'link': 'https://doi.org/10.61927/igmin365',
        'doi': '10.61927/igmin365',
        'arxiv_id': '',
        'verified_venue': 'IgMin Research',
        'verified_year': '2026',
        'origin': 'snowball',
        'verification_result': 'ok',
        'notes': 'Verified via Crossref.',
        'relevance': 'KEEP',
        'relevance_reason': 'Directly analyzes graph-traversal metadata filtering techniques for filtered ANN search.',
        'added_in_gate': '0.5',
        'review_status': 'ADDED-PENDING-USER-REVIEW'
    }
]

# Read existing manifest
rows = []
with open('manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    for r in reader:
        rows.append(r)

# Ensure new columns exist
new_cols = ['relevance', 'relevance_reason', 'added_in_gate', 'review_status']
for c in new_cols:
    if c not in fieldnames:
        fieldnames.append(c)

# Update existing rows
for r in rows:
    b = r['bibkey']
    if b in phase1_updates:
        r['title'] = phase1_updates[b]['title']
        r['relevance'] = phase1_updates[b]['relevance']
        r['relevance_reason'] = phase1_updates[b]['relevance_reason']
        r['verification_result'] = 'ok'  # resolved mismatch
    else:
        # Default relevance for existing seed papers
        r['relevance'] = 'KEEP'
        r['relevance_reason'] = 'Core literature pipeline seed paper.'
    r['added_in_gate'] = '0'
    r['review_status'] = 'SEED-CONFIRMED'

# Append new additions
for add in additions:
    row_dict = {col: add.get(col, '') for col in fieldnames}
    rows.append(row_dict)

with open('manifest.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated manifest.csv: total {len(rows)} rows, {len(fieldnames)} columns.")
