# zhang2025dynamic — Efficient Dynamic Indexing for Range Filtered Approximate Nearest Neighbor Search
Authors / Year / Venue / DOI: Fangyuan Zhang, Mengxu Jiang, Guanhao Hou, Jieming Shi, Hua Fan, Wenchao Zhou, Feifei Li, Sibo Wang / 2025 / Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2025) / 10.1145/3725401
Status: PUB (DOI: 10.1145/3725401)
PDF: papers/zhang2025dynamic.pdf   Read fully: yes

## Problem addressed (p.)
Range-Filtered Approximate Nearest Neighbor Search over dynamic datasets where objects undergo continuous insertions and deletions (p. 1-3, §1). Existing graph-based range indices (such as SeRF) are static and cannot handle arbitrary object insertions or deletions without expensive complete graph re-indexing, while multi-index methods incur excessive memory footprints and high update overheads (p. 2-3, §1).

## Method (core idea in ≤5 sentences) (p.)
Proposes RangePQ and RangePQ+, dynamic index structures that integrate weight-balanced binary search trees (BSTs) with Inverted File Product Quantization (IVFPQ) (p. 3-4, §1; p. 8-16, §3). RangePQ organizes objects ordered by scalar attribute values into a weight-balanced BST ($BB[\alpha]$ tree), maintaining coarse cluster distribution summaries within internal nodes (p. 8-10, §3.1). At query time, Algorithm 1 decomposes the query range $[l_q, u_q]$ into $O(\log n)$ canonical tree nodes to identify candidate coarse clusters, followed by asymmetric distance computation over quantized vectors (p. 10-11, §3.2). RangePQ+ optimizes this by collapsing internal tree nodes into a two-layer structure with B-tree-like leaf buckets, achieving linear space and improved cache locality (p. 13-16, §3.3). Insertions and deletions are handled dynamically via weight-balanced tree rotations and lazy tombstone deletions in amortized logarithmic time (p. 12-16, §3.2-3.3).

## Complexity / theoretical claims
- Theorem 3.1 & Lemma 3.4 (p. 8, 10): The weight-balanced BST index $T$ has height $O(\log n)$ and decomposes any query range $[l_q, u_q]$ into $O(\log n)$ canonical nodes.
- Theorem 3.6 (p. 11): RangePQ query time complexity is $O(\log n + |C_q| \cdot \text{cost})$, where $|C_q|$ is the number of coarse clusters evaluated.
- Theorem 3.8 & Theorem 3.9 (p. 13-14): RangePQ handles object insertion in $O(\log n)$ amortized expected time and deletion in $O(\log n)$ amortized expected time.
- Theorem 3.11, 3.13, 3.14 (p. 16-17): RangePQ+ maintains query time $O(\log n + |C_q| \cdot \text{cost})$, amortized insertion time $O(\log n)$, and amortized deletion time $O(\log n)$ within linear $O(n)$ space.

## Filter type and selectivity regime handled (p.)
1D numerical scalar range constraints ($[l_q, u_q]$) (p. 4-5, §2). Evaluates query range coverage percentiles spanning from tiny ranges (0.1%, 0.5%, 1%) up to wide range coverage (20%, 40%, 80%) under both uniform and skewed Zipfian attribute distributions (p. 18-20, §5; Fig. 3–6).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Weight-balanced binary search tree ($BB[\alpha]$ tree) integrated with Inverted File Product Quantization (RangePQ / RangePQ+) (p. 8-16, §3).

## Datasets, baselines, metrics (Table N)
- Datasets (p. 18, §5): SIFT (1M vectors, 128d), GIST (1M vectors, 960d), WIT (1M subset, 2048d), SIFT-ZIP (1M vectors, 128d with Zipfian skew $\alpha=2$).
- Baselines (p. 18, §5): Milvus (IVF_PQ), RII, VBase, SeRF, SuperPostFilter, ACORN.
- Metrics (p. 18, §5): Recall@10, Queries per second (QPS), Insertion latency (ms/object, Fig. 7, p. 21), Deletion latency (ns/object, Fig. 8, p. 21), Index size (MB/GB, Fig. 9, p. 21).
- Note: Experimental results are reported in text (§5) and Figures 3–13 (p. 19–22); Table N is not stated.

## Key results (numbers exactly as reported, with Table/Fig locator)
- RangePQ+ achieves index sizes of only 0.13 GB on GIST and 0.12 GB on WIT, compared to 0.39 GB / 0.38 GB for SeRF, 4.3 GB / 4.1 GB for ACORN, and 10.6 GB / 15.2 GB for SuperPostFilter (p. 21, §5.2).
- RangePQ+ delivers stable QPS maintaining Recall@10 above 0.9 across coverage percentages from 0.1% to 80% (Fig. 3–6, p. 19–20; Fig. 12, p. 21).
- SeRF and ACORN fail to achieve $>0.9$ recall within 100ms on narrow ranges ($<1\%$ coverage) on WIT due to structural information loss during graph edge pruning (p. 21, §5.2).
- Insertion costs average 1–10 ms per object and deletion costs average 10–100 ns per object across all datasets (Fig. 7–8, p. 21).

## Limitations (author-stated vs. observed)
- Author-stated: Product quantization introduces quantization distortion, which limits peak recall compared to exact uncompressed vector distance calculations unless expensive full-vector re-ranking is applied (p. 3, §1; p. 23, §6).
- Author-stated: Restricted to 1D scalar attributes; multi-attribute range filtering requires multi-dimensional tree partitioning (p. 23, §6).
- Observed: Tree-based range decomposition on quantized partitions exhibits lower peak throughput than pure graph traversal when selectivity is high and graphs are well-connected.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Highlights the vulnerability of graph methods (SeRF and ACORN) on extreme low-selectivity range queries ($<1\%$), where graph connectivity breakdown causes severe recall loss. Provides rigorous theoretical complexity proofs for range filtering operations and dynamic update models. Demonstrates an alternative non-graph architectural paradigm combining tree-based membership pruning with vector quantization.
Novelty check: no; RangePQ is a tree- and quantization-based index (weight-balanced BST + Product Quantization), performing range filtering via canonical tree node decomposition before scanning quantized postings, without graph traversal (p. 3-4, §1; p. 8-11, §3.1-3.2).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- zuo2024serf (SeRF: Segment Graph for Range-Filtering Approximate Nearest Neighbor Search) (p. 26)
- patel2024acorn (ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data) (p. 26)
- wang2021milvus (Milvus: A Purpose-Built Vector Data Management System) (p. 26)
- zhang2023vbase (VBase: Unifying high-dimensional vector similarity search and relational queries via relaxed monotonicity) (p. 26)
