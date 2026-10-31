# gupta2023caps — CAPS: A Practical Partition Index for Filtered Similarity Search
Authors / Year / Venue / DOI: Gaurav Gupta, Jonah Yi, Benjamin Coleman, Chen Luo, Vihan Lakshman, Anshumali Shrivastava / 2023 / arXiv preprint / none (arXiv:2308.15014)
Status: PRE (arXiv:2308.15014)
PDF: papers/gupta2023caps.pdf   Read fully: yes

## Problem addressed (p.)
Filtered approximate nearest neighbor search (ANNS) over high-dimensional vector embeddings with structured metadata constraints (p. 1-3, §1-§3). Prior filtered ANN systems primarily adapt graph indexes (e.g. Filtered-DiskANN, AIRSHIP, NHQ), which incur severe random memory access, high cache-miss overheads, and high index build costs (p. 1-2, §1, Table 1). Furthermore, existing methods suffer from the "unhappy middle" phenomenon: pre-filtering is optimal only for very sparse attributes (low selectivity), post-filtering is optimal only for very dense attributes (high selectivity), and both fail severely in the intermediate selectivity regime (p. 3-4, §3, Figure 1).

## Method (core idea in ≤5 sentences) (p.)
CAPS proposes a space-partitioning framework (hierarchical IVF clustering) that interleaves attribute filtering directly with inverted list lookups instead of traversing a proximity graph (p. 1, 4-6, §1, §5). Data points are first clustered into primary metric partitions based on vector similarity, and points within each partition are subsequently sub-partitioned into disjoint buckets based on attribute frequencies (p. 5-7, §5.1-§5.2, Figure 2, 3). For conjunctive queries (multi-attribute AND constraints), CAPS evaluates posting list intersections across sub-partitions in $O(1)$ amortized lookup time per cluster before computing vector distances (p. 5, 7, §5.1, §5.3). By avoiding graph hops, CAPS enables cache-friendly contiguous SIMD memory scans and straightforward parallelization across partitions (p. 2, 5, §1, §5). The overall index footprint requires only $\sim 10\%$ of graph index sizes while maintaining high recall (p. 1, 8-10, §1, §6).

## Complexity / theoretical claims
- Theoretical claims: Purely empirical query formulation (`no formal asymptotic complexity theorems proven`).
- Query Cost Formulation (§5.1, p. 5-6): Total query cost over $m$ inspected clusters is formulated as $\sum_{bin=1}^m \sum_{j=1}^{h+1} C(b, p, bin, j) |p_{bin,j}|$, where $C(b, p, bin, j)$ evaluates sub-partition validity against query filter $b$.
- "Unhappy Middle" Trade-off (§3, p. 4, Figure 1): Empirically characterizes the transition where pre-filtering and post-filtering degrade, but does not formulate an analytical closed-form crossover equation.
- selectivity_cost_model: not stated; characterizes the empirical trade-off between pre-filtering and post-filtering across attribute density (Figure 1, p. 4), but derives no formal closed-form mathematical cost or complexity model as a function of filter selectivity $\sigma$ (p. 1-13).

## Filter type and selectivity regime handled (p.)
- Filter type: Categorical label filtering, conjunctive multi-attribute AND constraints, and sparse high-cardinality attributes (p. 1-3, 7, §1, §3, §5.3, Table 1).
- Selectivity regime handled: Dense attributes ($>50\%$), sparse attributes ($<1\%$), and the intermediate "unhappy middle" selectivity regime ($1\%\text{--}20\%$) (p. 1, 3-4, 8-10, §1, §3, §6, Figure 1).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- Space-partitioning / Inverted File (IVF) index with attribute-based sub-partitioning (CAPS), compared against graph indexes (HNSW in Milvus, Filtered-DiskANN/Vamana, AIRSHIP) and IVF-Flat (p. 1-2, 5, 8-9, §1, §5, §6).

## Datasets, baselines, metrics (Table N)
- Datasets (§6.1, p. 8, Table 2):
  - YFCC10M: 10M 192-d vectors, average 10.8 labels/vector.
  - Paper: 2M 128-d vectors, 34K unique labels.
  - ImageNet: 1.2M 512-d vectors, 1K classes.
  - MNIST: 70K 784-d vectors, 10 labels (exploratory benchmark).
- Baselines (§6.1, p. 8-9): Milvus (IVF-Flat, HNSW), Filtered-DiskANN, AIRSHIP, NHQ.
- Metrics (§6.1, p. 8-9): Query latency (ms), QPS at 0.90 and 0.95 Recall@10, index build time (hours), index size (GB).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Recall vs. Latency (Figure 4, 5, p. 9-10, §6.2):
  - On YFCC10M at 0.90 recall: CAPS achieves $4.8\times$ lower latency than Filtered-DiskANN and $6.2\times$ lower latency than Milvus-HNSW.
  - On Paper dataset at 0.95 recall: CAPS achieves 12.3 ms latency compared to 38.5 ms for Milvus-HNSW ($3.1\times$ speedup) (Figure 5b, p. 10).
- Index Footprint (Table 3, p. 10, §6.3): On YFCC10M, CAPS requires 4.2 GB memory, compared to 48.6 GB for Filtered-DiskANN and 41.2 GB for Milvus-HNSW (an $\sim 10\times$ space reduction).

## Limitations (author-stated vs. observed)
- Author-stated (p. 2, 7, 12, §1, §5.3, §7): Relies on attribute frequency skew; performance degrades on high-entropy or perfectly uniform attribute distributions where sub-partitions cannot isolate active points; conjunctive filters with many clauses incur higher intersection overhead.
- Observed: Is an IVF partition index rather than a graph index; does not support graph traversal or fine-grained hop pruning.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
- Provides the clearest empirical characterization of the "unhappy middle" failure mode that motivates in-traversal predicate pruning.
- Demonstrates why graph-based methods suffer cache-miss bottlenecks during traversal, underscoring the necessity of lightweight in-cache probabilistic filter evaluation.
Novelty check: no; CAPS is an IVF space-partitioning index that performs exact attribute set checks on cluster sub-partitions, rather than evaluating probabilistic membership filters during graph traversal (p. 1-6).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Query complexity expression $\sum |p_{bin,j}|$ in §5.1 (p. 6) assumes $O(1)$ hash table sub-partition lookup, but omits posting list pointer traversal overheads in multi-attribute conjunctive queries (p. 6-7).

## Useful references to snowball (bibkeys or titles from its reference list)
- gollapudi2023filtereddiskann (Gollapudi et al., 2023: Filtered-DiskANN: Graph algorithms for approximate nearest neighbor search with filters) (p. 13)
- malkov2020hnsw (Malkov & Yashunin, 2020: Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 13)
- subramanya2019diskann (Subramanya et al., 2019: DiskANN: Fast accurate billion-point nearest neighbor search on a single node) (p. 14)
