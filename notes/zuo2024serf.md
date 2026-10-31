# zuo2024serf — SeRF: Segment Graph for Range-Filtering Approximate Nearest Neighbor Search
Authors / Year / Venue / DOI: Chaoji Zuo, Miao Qiao, Wenchao Zhou, Feifei Li, Dong Deng / 2024 / Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2024) / 10.1145/3639324
Status: PUB (DOI: 10.1145/3639324)
PDF: papers/zuo2024serf.pdf   Read fully: yes

## Problem addressed (p.)
Range-Filtering Approximate Nearest Neighbor Search (RFANNS), where high-dimensional data points are associated with ordered 1D numerical scalar attributes and queries specify an arbitrary numerical range $[a_q, b_q]$ (p. 1-2, §1; p. 3-4, §2). Existing post-filtering and range-first pre-filtering methods break down either when range selectivity is low (graph connectivity failure) or high (exhaustive scanning overheads), while building separate proximity graphs for all possible ranges is combinatorially impossible (p. 1-2, §1).

## Method (core idea in ≤5 sentences) (p.)
Introduces the Segment Graph architecture for RFANNS, beginning with 1D Segment Graphs for half-bounded query ranges and extending to 2D Segment Graphs for arbitrary intervals (p. 2, §1; p. 6-15, §3-4). Demonstrates that inserting points sequentially in attribute order allows compact lossless compression of all $n^2$ possible interval-specific HNSW subgraphs into a unified graph structure (p. 7-8, §3; p. 12-14, §4). Edges in the 2D Segment Graph are annotated with 4-tuple validity boundaries $[a_{in}, a_{out}, b_{in}, b_{out}]$ indicating exactly which query intervals can navigate along the edge (p. 10-12, §4). At query time, Algorithm 7 (2DSegmentANNSearch) performs greedy beam search where candidate edges are checked against query bounds $[a_q, b_q]$ to emulate search over the exact induced HNSW graph of qualifying points (p. 11, §4). Implements Leap optimization strategies (MinLeap, MidLeap, MaxLeap) to accelerate index construction (p. 13-15, §4.3).

## Complexity / theoretical claims
- Lemma 5 (p. 12): The worst-case size of a 2D Segment Graph is $O(n^2 M)$ edges.
- Theorem 7 (p. 12): Under the assumption that attribute values are independent of vector distances, the average-case graph size of a 2D Segment Graph is $O(n M \ln n)$, the number of online search calls during construction is $O(n \log n)$, and construction time excluding online search is $O(n M^2 \log n)$.
- Theorem 8 (p. 13): The 2D Segment Graph produced by Algorithm 8 provides a lossless compression of all $n^2$ range-specific segment graphs $G_{i,j}$.

## Filter type and selectivity regime handled (p.)
Continuous or discrete 1D numerical range filters ($[a_q, b_q]$) (p. 3-4, §2). Evaluates half-bounded ($[1, b]$) and arbitrary range queries spanning selectivity percentiles from tiny fractions ($<1\%$) to wide windows ($>50\%$) (p. 17-19, §5.1-5.2; p. 20-22, §5.3).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Segment Graph / 2D Segment Graph based on HNSW, where edges are annotated with scalar interval validity intervals (p. 2, §1; p. 6-15, §3-4).

## Datasets, baselines, metrics (Table N)
- Datasets (p. 16, §5): DEEP (1M vectors, 96d), YouTube-Audio (1M vectors, 128d), WIT-Image (1M vectors, 2048d).
- Baselines (p. 20, §5.3): ANNS-first (HNSW post-filtering via nmslib), FAISS (IVFPQ), Rii, Filtered-DiskANN (bucketed), Milvus (HNSW-based), Range-first (pre-filtering brute-force scan).
- Metrics (p. 16, §5): Recall@10, Queries per second (QPS), Index Size (GB, Fig. 7, p. 17), Index Construction Time (s, Fig. 7, p. 17).
- Note: Experimental results are reported in text (§5) and Figures 7–13 (p. 17–23); Table N is not stated.

## Key results (numbers exactly as reported, with Table/Fig locator)
- On arbitrary query ranges with selectivity width $>1\%$, 2DSegmentGraph achieves higher QPS than all 6 baselines while maintaining recall $>95\%$ (p. 22, §5.3; Fig. 12, p. 22).
- When query selectivity is around 10%, 2DSegmentGraph QPS is roughly 1.5×, 2×, 5×, 10×, 35×, and 32× that of ANNS-first, Range-first, Milvus, Filtered-DiskANN, FAISS, and Rii respectively (p. 22, §5.3).
- On DEEP, YouTube-Audio, and WIT-Image, 2DSegmentGraph index sizes are 2.65 GB, 2.72 GB, and 8.29 GB, with index construction times of 1,562s, 983s, and 18,262s (p. 22, §5.3).
- Using 24 threads, 2DSegmentGraph indexing time drops to 313s for DEEP, 217s for YouTube-Audio, and 2,905s for WIT-Image (p. 22, §5.3).

## Limitations (author-stated vs. observed)
- Author-stated: Focused strictly on 1D numerical range attributes; extending segment graphs to multi-dimensional numerical ranges causes exponential dimensional expansion (p. 24, §7).
- Author-stated: Range-first pre-filtering still achieves higher QPS for extremely narrow ranges ($<1\%$) where candidate counts are very small (p. 22, §5.3).
- Observed: Storing 4 interval boundary values per edge increases memory footprint per node compared to standard proximity graphs.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Presents the primary theoretical framework for range-filtered HNSW graph navigation with formal $O(n M \ln n)$ average-case size bounds. Shows how edge-level metadata checks allow proximity graphs to emulate search over ideal subgraphs. Provides the exact baseline to beat for range-filtered graph search and serves as an important comparison point for embedding probabilistic membership filters.
Novelty check: yes for metadata predicate checks during graph traversal (in 2DSegmentANNSearch, candidate edges are verified against query range $[a_q, b_q]$ during greedy beam search traversal, p. 11, §4, Algorithm 7), but no probabilistic membership filter (Bloom, Cuckoo, Xor) is used (p. 6-15, §3-4).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- malkov2020hnsw (Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 25)
- gollapudi2023filtereddiskann (Filtered-DiskANN: Graph algorithms for approximate nearest neighbor search with filters) (p. 25)
- wang2021milvus (Milvus: A purpose-built vector data management system) (p. 25)
- zuo2023arkgraph (ARKGraph: All-Range Approximate K-Nearest-Neighbor Graph) (p. 26)
