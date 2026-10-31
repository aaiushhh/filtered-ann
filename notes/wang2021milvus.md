# wang2021milvus — Milvus: A Purpose-Built Vector Data Management System
Authors / Year / Venue / DOI: Jianguo Wang, Xiaomeng Yi, Rentong Guo, Hai Jin, Peng Xu, Shengjun Li, Xiangyu Wang, Xiangzhou Guo, Chengming Li, Xiaohai Xu, Kun Yu, Yuxing Yuan, Yinghao Zou, Jiquan Long, Yudong Cai, Zhenxiang Li, Zhifeng Zhang, Yihua Mo, Jun Gu, Ruiyi Jiang, Yi Wei, Charles Xie / 2021 / Proceedings of the 2021 International Conference on Management of Data (SIGMOD 2021) / 10.1145/3448016.3457550
Status: PUB (DOI: 10.1145/3448016.3457550)
PDF: papers/wang2021milvus.pdf   Read fully: yes

## Problem addressed (p.)
Managing massive, dynamic high-dimensional vector data in production AI applications (p. 1-2, §1). Algorithmic vector search libraries (FAISS, SPTAG) assume static, in-memory vectors and lack distributed storage, dynamic update mechanisms, and advanced hybrid query capabilities like attribute filtering and multi-vector search (p. 1-2, §1; Table 1, p. 2).

## Method (core idea in ≤5 sentences) (p.)
Presents Milvus, a purpose-built, distributed, open-source vector database management system (VDBMS) supporting billion-scale dynamic vector collections (p. 1-3, §1-2). Employs a cloud-native disaggregated storage-and-compute architecture with data sharding into immutable segments and dynamic LSM-tree-like log merging (p. 3-4, §2). Optimizes heterogeneous CPU/GPU computing via SQ8H quantization and PCIe data pipelining (p. 4-6, §3). Categorizes hybrid attribute filtering into five execution strategies: Strategy A (pre-filtering brute-force scan), Strategy B (pre-filtering generating an entity ID bitmap checked during vector search), Strategy C (post-filtering), Strategy D (cost-based optimizer), and Strategy E (partition-based filtering) (p. 6-7, §4.1; Fig. 4, p. 7). Implements an iterative merging algorithm to support multi-vector similarity queries (p. 7-8, §4.2; Algorithm 2).

## Complexity / theoretical claims
- none stated (empirical systems and architecture paper) (p. 1-14).

## Filter type and selectivity regime handled (p.)
Relational scalar metadata range constraints ($c_1 \le A \le c_2$) and categorical equality constraints (p. 6-7, §4.1). Evaluated across fine-grained selectivity regimes from highly selective ($\sigma = 0, 0.1$) to unselective ($\sigma = 0.9, 0.95, 0.99$) (p. 12, §7.5; Fig. 14, p. 12).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Supports diverse vector indexing algorithms including HNSW, IVF_FLAT, IVF_SQ8, and IVF_SQ8H on CPU/GPU, with scalar B-trees and ID bitmaps (p. 3, §2.2; p. 4-6, §3; p. 10, §7.1).

## Datasets, baselines, metrics (Table N)
- Datasets (p. 10, §7.1): SIFT1B (1 billion vectors, 128d, 512 GB) and Deep1B (1 billion vectors, 96d, 384 GB), evaluated in 1M, 10M, 100M, and 1B configurations.
- Baselines (Table 1, p. 2; p. 10, §7.1): Faiss, SPTAG, ElasticSearch, Vearch, AnalyticDB-V, PASE (PostgreSQL).
- Metrics (p. 10, §7.1): Throughput (QPS), Query execution time (s), Recall@k ($k=50, 500$), Indexing throughput, Speedup ratio.

## Key results (numbers exactly as reported, with Table/Fig locator)
- Strategy E (partition-based filtering) is up to 13.7× faster than Strategy D (cost-based pre/post filtering) at low query selectivities (p. 7, §4.1; Fig. 14, p. 12).
- On SIFT10M and Deep10M with HNSW indexes, Milvus achieves up to 20,000 QPS at high recall (0.8–0.98), outperforming Vearch and commercial systems (Fig. 9, p. 11).
- Scales near-linearly from 1M to 1 billion vectors on distributed nodes, answering queries on 1 billion vectors in under 1.5 seconds (p. 11, §7.3; Fig. 10, p. 11).
- In real-world chemical structure search at Apptech, Milvus reduced drug candidate similarity analysis time from hours to less than a minute (p. 10, §6.2).

## Limitations (author-stated vs. observed)
- Author-stated: Attribute partitioning (Strategy E) requires prior knowledge of frequently queried attributes to define partitions; it degrades if query attributes do not align with partition keys (p. 7, §4.1).
- Author-stated: Strategy B (bitmap-guided vector index traversal) still incurs index search overhead when selectivity is very low, where sequential scanning (Strategy A) is faster (p. 7, §4.1; Fig. 14, p. 12).
- Observed: Focuses on systems-level architecture and query execution planning rather than designing dedicated graph-theoretic pruning algorithms.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Serves as the milestone systems paper that formalized the modern execution taxonomy for filtered vector search (Strategies A–E) in vector databases. Directly demonstrates Strategy B (checking an exact candidate bitmap during vector index traversal), which our project generalizes by embedding probabilistic membership filters directly into graph nodes. Provides the foundational systems baseline and selectivity cost model context for filtered ANN.
Novelty check: yes for metadata/ID checks during search traversal (Strategy B generates an entity ID bitmap from attribute pre-filtering and checks bitmap membership on candidate vectors during index traversal, p. 7, §4.1), but it uses an exact candidate bitmap rather than a probabilistic membership filter (Bloom, Cuckoo, Xor) (p. 6-7, §4.1).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- malkov2020hnsw (Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 13)
- J. Johnson, M. Douze, H. Jégou. "Billion-scale similarity search with GPUs." (IEEE TBD 2019) (p. 13)
- wu2022hqann (HQANN: Efficient and Robust Similarity Search for Hybrid Queries with Structured and Unstructured Constraints) (cited via related work on hybrid queries, p. 12)
- zhan2020analyticdbv (AnalyticDB-V: A hybrid analytical engine towards query fusion for structured and unstructured data) (p. 14)
