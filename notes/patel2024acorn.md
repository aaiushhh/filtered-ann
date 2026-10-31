# patel2024acorn — ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data
Authors / Year / Venue / DOI: Liana Patel, Peter Kraft, Carlos Guestrin, Matei Zaharia / 2024 / Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2024) / 10.1145/3654923
Status: PUB (DOI: 10.1145/3654923)
PDF: papers/patel2024acorn.pdf   Read fully: yes

## Problem addressed (p.)
Filtered approximate nearest neighbor search (ANNS) combining high-dimensional dense vectors with arbitrary structured metadata predicates (p. 1-2, §1). Existing graph methods suffer severe performance breakdown when query selectivity is low or when predicates exhibit high query correlation (predicate clustering), while constructing per-predicate subgraphs is computationally intractable when predicate combinations have high cardinality (p. 1-2, §1; p. 5-6, §3-4).

## Method (core idea in ≤5 sentences) (p.)
Introduces ACORN, a predicate-agnostic proximity graph indexing framework built on HNSW that approximates search over the theoretically ideal "oracle partition index" without explicitly constructing separate indices per predicate (p. 1-2, §1; p. 6-7, §4-5). ACORN-$\gamma$ constructs a denser variant of HNSW parameterized by an expansion factor $\gamma$ and a compressed base level, ensuring connectivity within arbitrary induced predicate subgraphs (p. 7, §5; p. 9-10, §5.2). ACORN-1 reduces construction cost by maintaining standard HNSW degree bounds and expanding neighbor lists dynamically on-the-fly via multi-hop traversal during query search (p. 7, §5; p. 10-11, §5.3). During search (Algorithm 2), greedy traversal evaluates predicate matching on candidate neighbors and routes over the induced predicate subgraph, ignoring disqualified nodes in the candidate result set (p. 7-8, §5.1).

## Complexity / theoretical claims
- Section 4 (p. 6): An oracle partition index built specifically for predicate $P$ over matching subset $X_P$ achieves search complexity $O(\log |X_P| + k)$.
- Section 3.2 (p. 6): Pre-filtering scales linearly with matching subset size: $O(|X_P|)$.
- Section 3.2 (p. 6): Post-filtering has expected search complexity $O(\log |X| + k/\sigma)$, with worst-case search complexity $O(|X|)$ when qualifying vectors cluster far from the query vector under negative query correlation.

## Filter type and selectivity regime handled (p.)
Arbitrary structured metadata predicates: single/multi-label categorical equality, range predicates (`between(a, b)`), list containment (`contains(...)`), and regex pattern matching (`regex-match()`) (p. 4-5, §3.1; Table 2, p. 15). Evaluated across varied selectivity percentiles from low to high selectivity ($\sigma \in [0.001, 1.0]$) and varying query correlation regimes (p. 15, Table 2; p. 19-20, §7.3.2).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
HNSW augmented with neighbor list expansion factor $\gamma$ and compression factor $M_{comp}$, evaluated as ACORN-$\gamma$ and ACORN-1 (p. 4, §2; p. 7-11, §5).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 2, p. 15): SIFT1M (1M, 128d), Paper (2.03M, 200d), TripClick (1.06M, 768d), LAION-1M (1M, 512d), LAION-25M (24.65M, 512d).
- Baselines (p. 16, §7.2): Pre-filtering (Flat scan), Post-filtering (standard HNSW), NHQ, FilteredDiskANN (FilteredVamana, StitchedVamana), and Oracle Partition Index.
- Metrics (p. 16, §7.2): Recall@10, Queries per second (QPS), Time-to-index (TTI in seconds, Table 4, p. 21), Index Size (GB, Table 5, p. 21), Average out-degree (Table 6, p. 21).

## Key results (numbers exactly as reported, with Table/Fig locator)
- On low-cardinality datasets (SIFT1M, Paper), ACORN-$\gamma$ achieves 2–10× higher QPS at fixed recall compared to FilteredDiskANN and NHQ (p. 18, §7.3.1; Fig. 7, p. 18).
- On high-cardinality datasets (TripClick, LAION-1M), ACORN outperforms baselines by 30–50× higher QPS at 0.9 recall (p. 19, §7.3.2; Fig. 8, p. 19).
- Robust to negative query correlation on LAION-1M, attaining 28–100× higher QPS at 0.9 recall than post-filtering (p. 19, §7.3.2; Fig. 10, p. 20).
- Time-to-index on LAION-25M is 38,007.5s for ACORN-$\gamma$, 705.3s for ACORN-1, and 1,147.2s for HNSW (Table 4, p. 21).
- Index size on LAION-25M is 59 GB for ACORN-$\gamma$ and ACORN-1 vs. 54 GB for HNSW and 47 GB for Flat (Table 5, p. 21).

## Limitations (author-stated vs. observed)
- Author-stated: ACORN-$\gamma$ requires significantly higher time-to-index (TTI) and increased edge degrees during construction, making it heavy for resource-constrained build environments (p. 7, §5; p. 20-21, §7.4.1; Table 4, p. 21).
- Author-stated: ACORN-1 avoids heavy indexing costs but suffers lower search QPS (1.5–5× lower than ACORN-$\gamma$) due to online multi-hop edge generation overhead (p. 18, §7.3.1).
- Observed: Degree expansion creates substantial memory pressure, and filtering still relies on evaluating metadata checks on expanded neighbor lists during search.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Serves as the primary state-of-the-art graph-filtered baseline to beat and the most closely related HNSW traversal modification. Formulates the theoretical complexity bounds for pre-filtering, post-filtering, and oracle graph partitioning ($O(\log |X| + k/\sigma)$ vs. $O(\log |X_P| + k)$), which our cost model directly builds upon. Demonstrates that in-traversal filtering maintains navigability, where embedding probabilistic membership filters can prune edges without incurring ACORN's heavy degree expansion.
Novelty check: yes for metadata predicate checks during graph traversal (in ACORN-SEARCH-LAYER, candidate neighbors are evaluated against predicate $P$ and pruned during greedy graph routing, p. 7-8, §5.1, Algorithm 2), but no probabilistic membership filter (Bloom, Cuckoo, Xor) is used (p. 6-11, §4-5).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- malkov2020hnsw (Efficient and Robust Approximate Nearest Neighbors Using Hierarchical Navigable Small World Graphs) (p. 25)
- gollapudi2023filtereddiskann (Filtered-DiskANN: Graph Algorithms for Approximate Nearest Neighbor Search with Filters) (p. 24)
- wu2022hqann (HQANN: Efficient and Robust Similarity Search for Hybrid Queries with Structured and Unstructured Constraints) (p. 26)
- subramanya2019diskann (DiskANN: Fast accurate billion-point nearest neighbor search on a single node) (p. 26)
