# wu2022hqann — HQANN: Efficient and Robust Similarity Search for Hybrid Queries with Structured and Unstructured Constraints
Authors / Year / Venue / DOI: Wei Wu, Junlin He, Yu Qiao, Guoheng Fu, Li Liu, Jin Yu / 2022 / Proceedings of the 31st ACM International Conference on Information & Knowledge Management (CIKM 2022) / 10.1145/3511808.3557610
Status: PUB (DOI: 10.1145/3511808.3557610)
PDF: papers/wu2022hqann.pdf   Read fully: yes

## Problem addressed (p.)
Hybrid similarity search combining unstructured vector embeddings with structured metadata attribute constraints (p. 1-2, §1). Traditional two-stage frameworks (pre-filtering exhaustive bitmap scans or post-filtering) suffer high latency or severe recall loss, while existing hybrid proximity graphs (e.g., NHQ) treat vector distance as dominant and fail when the number of attributes scales (p. 1-2, §1-2).

## Method (core idea in ≤5 sentences) (p.)
Proposes HQANN, an attribute-centric composite proximity graph framework that fuses structured attribute constraints and unstructured vector distances into a unified traversal metric (p. 1-2, §1-3). Defines a composite distance function where attribute matching is given dominant priority over vector distance, ensuring that points with identical attributes are prioritized in routing (p. 2-3, §3; Eq. 4, p. 3). Incorporates a scaled Manhattan attribute distance mapping with a scaling factor $\beta$ to preserve the navigation sense among differing attribute combinations (p. 3, §3). Constructs and traverses standard proximity graphs (HNSW) directly using the fused composite distance without requiring separate subquery execution engines (p. 2-3, §3).

## Complexity / theoretical claims
- none stated (purely empirical) (p. 1-5).

## Filter type and selectivity regime handled (p.)
Structured categorical attribute constraints represented as integer attribute vectors (p. 2-3, §3). Evaluates workloads ranging from small attribute sets (10 attributes) up to massive attribute spaces (over 800,000 attribute constraints on merchandise dataset) (p. 4, §4; Table 1, p. 4).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
HNSW proximity graph adapted with composite attribute-vector distance metric (HQANN-HNSW) (p. 2-4, §3-4).

## Datasets, baselines, metrics (Table N)
- Datasets (p. 3-4, §4): GLOVE-1.2M (1.18M vectors, 100d), SIFT-1M (1M vectors, 128d), GIST-1M (1M vectors, 960d), DEEP-1B (10M subset evaluated, 96d), Merchandise-0.2B (200M internal e-commerce dataset with 0.8M attribute constraints).
- Baselines (p. 4, §4): Vearch, AnalyticDB-V (ADBV), Milvus, NHQ-HNSW, and standard HNSW.
- Metrics (p. 4, §4): Recall@10, Queries Per Second (QPS), Performance scaling over varying attribute constraint counts.

## Key results (numbers exactly as reported, with Table/Fig locator)
- HQANN-HNSW achieves up to an order-of-magnitude higher QPS at $\ge 0.9$ Recall@10 compared to two-stage frameworks (Vearch, ADBV, Milvus) across GLOVE, SIFT, GIST, and DEEP (Fig. 3, p. 4).
- On GLOVE-1.2M with 100 attribute constraints, HQANN-HNSW maintains Recall@10 of 0.950 across $\beta \in [0.10, 0.25]$ (Table 1, p. 4).
- On the 200M merchandise dataset with 800,000 attribute constraints, tuning $\beta=0.25$ boosts Recall@10 from 0.727 (at $\beta=1.0$) to 0.999 (Table 1, p. 4).
- As the number of attribute constraints increases from 32 to 10,000, HQANN maintains stable high Recall@10 ($\approx 0.95$) and high QPS, whereas NHQ and Vearch experience sharp recall drops (Fig. 4, p. 4).

## Limitations (author-stated vs. observed)
- Author-stated: Requires careful manual tuning of the scale factor parameter $\beta$ to balance attribute distance magnitude against vector distance magnitude across different datasets (p. 3, §3; Table 1, p. 4).
- Author-stated: Attribute vectors must be integer-encoded or mapped to discrete representation spaces; arbitrary continuous floating-point range inequalities are not directly supported (p. 3, §3).
- Observed: 5-page short conference paper lacks detailed formal complexity derivations and provides limited analysis of index build times and memory footprints.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Early precursor to in-traversal graph filtering that establishes the principle of prioritizing metadata matching over metric distance during graph search. Serves as a baseline to beat and illustrates the limitations of scalar-weighted distance heuristics compared to exact or probabilistic filter membership. Informs how graph traversal routing behaves when metadata constraints are evaluated at every hop.
Novelty check: yes for metadata predicate checks during graph traversal (it evaluates fused attribute Manhattan distances during greedy HNSW edge exploration, p. 2-3, §3; Eq. 4, p. 3), but no probabilistic membership filter (Bloom, Cuckoo, Xor) is used (p. 2-4, §3-4).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- malkov2020hnsw (Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 5)
- wang2021milvus (Milvus: A purpose-built vector data management system) (p. 5)
- J. Johnson, M. Douze, H. Jégou. "Billion-scale similarity search with GPUs." (IEEE TBD 2019) (p. 5)
