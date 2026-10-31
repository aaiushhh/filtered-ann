# curator2026 — Curator: Efficient Vector Search with Low-Selectivity Filters
Authors / Year / Venue / DOI: Jin, Yicheng, Wu, Yongji, Hu, Wenjun, Maggs, Bruce M., Yang, Jun, Zhang, Xiao, Zhuo, Danyang / 2026 / Proceedings of the ACM on Management of Data (PACMMOD) / 10.1145/3786635
Status: PUB (DOI: 10.1145/3786635)
PDF: papers/curator2026.pdf   Read fully: yes

## Problem addressed (p.)
Filtered approximate nearest neighbor search (ANNS) combining dense vectors with discrete label filters under low-selectivity regimes ($\sigma \le 1\%$, e.g., $10^{-4}$ to $10^{-2}$) (p. 1-2, §1). Graph-based indexes like HNSW encounter graph connectivity breakdown on low-selectivity queries because qualifying vectors become sparse and their induced subgraph fragments, while existing graph workarounds (e.g., degree expansion in ACORN) incur severe index construction overheads (p. 1-2, §1).

## Method (core idea in ≤5 sentences) (p.)
Curator introduces a dual-index architecture that uses a partition-based index tailored for low selectivity alongside proximity graphs for high selectivity (p. 1-2, §1). It builds specialized indexes for individual labels within a shared hierarchical clustering tree generated via recursive k-means (p. 4-5, §3.2). For each label, Curator creates a virtual inverted posting list of partitions, compacting posting entries to eliminate redundancy (p. 5-6, §3.3). At query time, Curator dynamically chooses search parameters using an offline profiling-based query planner (p. 7, §4). Queries with low selectivity are routed to Curator, whereas high-selectivity queries run on graph indexes (p. 7-8, §4.3).

## Complexity / theoretical claims
- none stated (purely empirical) (p. 1-15).

## Filter type and selectivity regime handled (p.)
Discrete categorical label filters (single label and conjunctions/disjunctions of labels) (p. 2-3, §2.1). Handles low-selectivity regimes where $\sigma \le 1\%$ (e.g., $10^{-4}$ to $10^{-2}$) (p. 1-2, §1; Table 2, p. 9).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Hierarchical partition-based index (recursive k-means clustering tree) paired in a dual-index setup with graph indexes (ACORN / HNSW) (p. 1-2, §1; p. 4, §3.1).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 2, p. 9): YFCC-10M (10M vectors, 192d, 1000 labels), arXiv (2M vectors, 384d, 100 labels).
- Baselines (p. 9, §6.1): ACORN-10, ACORN-40, Milvus (HNSW-based), Filtered-DiskANN, IVFFlat, Pre-Filtering (Flat scan), Post-Filtering.
- Metrics (p. 9, §6.1): 10-recall@10, QPS, query latency (ms), index build time, memory footprint.

## Key results (numbers exactly as reported, with Table/Fig locator)
- Curator achieves up to 20.9× speedup over ACORN at low selectivity ($\sigma < 0.1\%$) (p. 2, §1; Fig. 2, p. 2).
- Vector insertion throughput is 4.4×–58.7× faster than shared graph index approaches like ACORN (§6.4, p. 12, Figure 13).
- Curator index construction takes 0.44 hours on arXiv (vs. 1.25 hours for ACORN-10) and 2.12 hours on YFCC-10M (vs. 18.23 hours for ACORN-10) (§6.4, p. 12, Figure 12).
- Memory overhead of adding Curator to ACORN is 4.3% on YFCC-10M and 5.5% on arXiv (§6.4, p. 12, Figure 12).

## Limitations (author-stated vs. observed)
- Author-stated: Tailored specifically to low-selectivity queries ($\sigma \le 1\%$) and relies on a dual-index architecture routing high-selectivity queries back to graph indexes (p. 1-2, §1; p. 7-8, §4.3).
- Author-stated: Evaluated primarily on discrete labels rather than continuous multi-dimensional numerical range predicates (p. 2-3, §2.1).
- Observed: Dual-index setup increases operational complexity by requiring separate tuning and maintenance for both the partition index and proximity graph.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Demonstrates that HNSW traversal suffers severe connectivity breakdown below $\sigma \approx 1\%$, motivating architectural alternatives. Directly serves as a baseline to beat when demonstrating that in-traversal filtering with probabilistic membership filters can preserve graph navigability without maintaining dual indices. Informs the selectivity regime boundary ($\sigma^*$) where pure graph traversal should transition or be augmented.
Novelty check: no; Curator is an external partition-based index complementing graph traversal in a dual-index system, not an in-traversal filter (p. 1-2, §1; p. 4, §3.1).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- patel2024acorn (ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data) (p. 14)
- gollapudi2023filtereddiskann (Filtered-DiskANN: Graph Algorithms for Approximate Nearest Neighbor Search with Filters) (p. 14)
- wang2021milvus (Milvus: A Purpose-Built Vector Data Management System) (p. 15)
- J. Johnson, M. Douze, H. Jégou. "Billion-scale similarity search with GPUs." (IEEE TBD 2019) (p. 14)
