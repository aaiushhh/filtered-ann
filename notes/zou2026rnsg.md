# zou2026rnsg — RNSG: A Range-Aware Graph Index for Efficient Range-Filtered Approximate Nearest Neighbor Search
Authors / Year / Venue / DOI: Zhiqiu Zou, Ziqi Yin, Rong-Hua Li, Hongchao Qin, Qiangqiang Dai, Guoren Wang / 2026 / Proceedings of the VLDB Endowment (PVLDB 2026) / 10.14778/3828612.3828636
Status: PUB (DOI: 10.14778/3828612.3828636)
PDF: papers/zou2026rnsg.pdf   Read fully: yes

## Problem addressed (p.)
Range-Filtered Approximate Nearest Neighbor (RFANN) search over multi-dimensional vector datasets with continuous or discrete 1D numerical scalar attributes (p. 1-2, §1). Existing methods either build multiple range-specific indices causing severe memory bloat or apply aggressive compression (like SeRF) that incurs high indexing time and connectivity loss, while lacking formal graph-theoretic guarantees that beam search remains monotonic over arbitrary induced range subgraphs (p. 1-2, §1).

## Method (core idea in ≤5 sentences) (p.)
Establishes the Range-Aware Relative Neighborhood Graph (RRNG) theory, proving that jointly incorporating spatial and attribute proximity produces graphs satisfying monotonic searchability and structural heredity over any range-induced subgraph (p. 1-2, §1; p. 3-5, §3). Translates this theory into a practical, scalable graph index called the Range-Aware Navigating Spread-out Graph (RNSG) (p. 5-8, §4). Implements a Fast Range-Aware Pruning strategy (Algorithm 1) that evaluates candidates in ascending order of scalar attribute distance, decomposing the pruning check into independent unilateral halves (p. 6, §4.1). Constructs RNSG from a spatial kNN graph candidate pool by applying range-aware edge selection and long-range routing edge augmentation (p. 7-8, §4.2; Algorithm 2). At query time, beam search navigates the unified graph by filtering out-of-range candidate neighbors during neighborhood expansion (p. 2-3, §2; p. 7-8, §4.3).

## Complexity / theoretical claims
- Theorem 3.3 & Theorem 3.5 (p. 4): Monotonic Searchability and Hereditary Property: For any valid range $[l, u]$, the range-induced subgraph $RRNG[V_{[l,u]}]$ is connected and contains a monotonic path between any two nodes.
- Theorem 3.6 (p. 5): The expected search cost of node-to-node monotone search in RRNG is $O(\log n)$.
- Theorem 3.7 (p. 5): The total number of edges in an RRNG is bounded by $O(n \cdot \bar{d}_{MRNG} \log n)$ where $\bar{d}_{MRNG}$ is the average degree of the base Monotonic RNG.
- Theorem 4.4 & Theorem 4.5 (p. 6, 7): Algorithm 1 constructs exact RRNG in $O(n^2 \log^2 n)$ time, and Algorithm 2 prunes a candidate graph of maximum degree $d$ in $O(n \cdot d^2 \log d)$ time.

## Filter type and selectivity regime handled (p.)
1D numerical scalar range constraints ($[l_q, u_q]$) (p. 1-2, §1; p. 2, §2.1). Evaluates low (1%), medium (10%), high (50%), and mixed range selectivity workloads (p. 9-11, §5; Table 1, p. 9; Fig. 5, p. 10).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Range-Aware Navigating Spread-out Graph (RNSG), a proximity graph rooted in Relative Neighborhood Graph (RNG / NSG) theory (p. 1-2, §1; p. 5-8, §4).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 1, p. 9): YT-Audio (1M, 128d), YT-RGB (1M, 1024d), WIT (1M, 2048d), TripClick (1M, 768d), SIFT1M (1M, 128d), GIST1M (1M, 960d), SpaceV10M (10M, 100d), SIFT-scale (10M–50M, 128d).
- Baselines (p. 10, §5): iRangeGraph, UNIFY, SuperPostfiltering (WST), SeRF (MaxLeap), DSG, ACORN-$\gamma$, Faiss-IVFPQ, Milvus-HNSW.
- Metrics (p. 10, §5): Recall@10, Queries per second (QPS), Index construction time (s, Fig. 6, p. 11), Deployed index size (MiB/GB, Fig. 6, p. 11).

## Key results (numbers exactly as reported, with Table/Fig locator)
- RNSG consistently achieves the highest QPS across recall levels from 0.8 to 1.0, delivering up to 4.2× higher QPS than state-of-the-art baselines iRangeGraph and UNIFY at $\ge 0.95$ recall (p. 10, Fig. 5).
- On YT-Audio, RNSG achieves $>10^4$ QPS at 0.95 recall on 1% and 10% selectivity, whereas SeRF and ACORN achieve lower throughput or fail to reach 0.95 recall (p. 10, Fig. 5).
- Indexing time of RNSG is 2–10× faster than SeRF and WST across all evaluated benchmark datasets (Fig. 6, p. 11).
- Scales effectively up to 50 million vectors on SIFT-scale while preserving linear construction scaling and high throughput (p. 9, Table 1; §5).

## Limitations (author-stated vs. observed)
- Author-stated: Focused on 1D continuous/discrete numerical range predicates; multi-dimensional compound range filters require multi-attribute graph extensions (p. 12, §7).
- Author-stated: Exact RRNG construction is $O(n^2 \log^2 n)$, necessitating the heuristic candidate-pool pruning of Algorithm 2 for million-scale datasets (p. 6-7, §4).
- Observed: Average node degree is higher than standard NSG due to maintaining range-aware edges across multiple scalar intervals.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Provides the definitive theoretical foundation for monotonic path existence and structural heredity in filtered proximity graphs. Offers a key PVLDB 2026 baseline to beat for range predicates and demonstrates how graph pruning can explicitly consider attribute gaps alongside vector distance. Directly informs our complexity analysis by showing that range-filtered graphs can maintain $O(\log n)$ search complexity.
Novelty check: yes for metadata predicate checks during graph traversal (in Section 2.1 and Section 4.3, candidate neighbors are evaluated against the query range $[l_q, u_q]$ during beam search traversal and out-of-range nodes are pruned, p. 2-3, §2; p. 7-8, §4.3), but no probabilistic membership filter (Bloom, Cuckoo, Xor) is used (p. 3-8, §3-4).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- patel2024acorn (ACORN: Performant and predicate-agnostic search over vector embeddings and structured data) (p. 13)
- zuo2024serf (SeRF: Segment graph for range-filtering approximate nearest neighbor search) (p. 14)
- malkov2020hnsw (Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 13)
- Fu et al. "Fast approximate nearest neighbor search with the navigating spreading-out graph (NSG)." (VLDB 2019) (p. 13)
