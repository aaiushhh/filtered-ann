# filtered2026system — Filtered Approximate Nearest Neighbor Search in Vector Databases: System Design and Performance Analysis
Authors / Year / Venue / DOI: Amanbayev, Abylay, Tsan, Brian, Dang, Tri, Rusu, Florin / 2026 / not stated / none
Status: PRE
PDF: papers/filtered2026system.pdf   Read fully: yes

## Problem addressed (p.)
Evaluates how end-to-end vector database management systems (VDBMS) and relational extensions handle Filtered Approximate Nearest Neighbor Search (FANNS) across varying selectivity regimes (p. 1-2, §1). While algorithmic innovations propose standalone indexing structures, production systems rely on query optimizers and execution engines whose internal adaptations and planning decisions often dominate raw index performance (p. 1, §1; p. 12, §5.1.4).

## Method (core idea in ≤5 sentences) (p.)
Establishes a unified taxonomy of filtering strategies in vector databases: pre-filtering, in-filtering (in-traversal filtering), post-filtering, and hybrid adaptive strategies (p. 3-4, §2.2). Proposes the Global-Local Selectivity (GLS) correlation metric to quantify independence between predicate filters and high-dimensional vector clusters (p. 6-8, §4). Introduces MoReVec, a multi-table relational dataset with 768-dimensional text embeddings and structured scalar attributes designed for filtered similarity queries (p. 2, §1; p. 15-16, §7). Extends the standard ANN-Benchmarks framework to systematically benchmark filtered similarity search (p. 14, §6). Evaluates execution trade-offs and query optimizer planning choices across three major engines: FAISS, Milvus, and pgvector (p. 12-14, §5.2; §8, p. 17-26).

## Complexity / theoretical claims
- none stated (empirical systems study) (p. 1-35).

## Filter type and selectivity regime handled (p.)
Relational scalar metadata constraints including categorical equality, discrete sets, and 1D numerical range filters (p. 6, §4; p. 15-16, §7). Evaluates wide selectivity regimes from extremely low ($\sigma \approx 10^{-4}$) to full collection ($\sigma = 1.0$) (p. 1, §1; §8, p. 17-26).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
HNSW (graph-based proximity index), IVFFlat / IVFPQ (inverted file clustering partitions), and Flat (exact brute-force sequential scan) across FAISS, Milvus, and pgvector (p. 1, §1; p. 12, §5.1; p. 14, §5.2).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 4, p. 14; §7, p. 15-16): MoReVec (relational movie/review text embeddings, 768d), SIFT-1M (1M, 128d), GIST-1M (1M, 960d), GloVe-100 (1.18M, 100d), ArXiv (2.7M, 768d).
- Baselines / Systems (Table 3, p. 12; §5.2, p. 12-14): FAISS (C++ library), Milvus (distributed vector database), pgvector (PostgreSQL vector extension).
- Metrics (p. 6, §4; p. 14, §6.1): Filtered Recall@k, Queries Per Second (QPS), Query Latency (ms), Query Optimization overhead, GLS correlation score.

## Key results (numbers exactly as reported, with Table/Fig locator)
- IVFFlat outperforms HNSW in latency and recall stability when filter selectivity is low ($\sigma \le 1\%$) across evaluated systems (p. 1, §1; Fig. 7, p. 19).
- In pgvector, the cost-based optimizer frequently selects approximate index scans over sequential scans despite sequential scans achieving 1.0 recall at equivalent latency (p. 1, §1; p. 23, §8.3.2).
- Milvus achieves robust recall by implementing an adaptive hybrid fallback mechanism that switches between graph exploration and exact brute-force scans (p. 1, §1; p. 20, §8.2).
- On MoReVec, high GLS correlation significantly skews local cluster density, reducing HNSW recall unless search beam width is expanded by up to 4× (p. 8, §4.2; Fig. 11, p. 24).

## Limitations (author-stated vs. observed)
- Author-stated: Benchmarking is restricted to single-node evaluation; distributed partitioning and network communication overheads are not explored (p. 26, §9).
- Author-stated: Query workloads evaluate static datasets; concurrent real-time graph updates under continuous filtering workloads are left for future work (p. 26, §9).
- Observed: Focuses on engine-level execution policies of standard indices (HNSW, IVFFlat) rather than proposing novel graph traversal algorithms or compressed edge data structures.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Validates that naive in-traversal filtering in HNSW degrades severely at low selectivity ($\sigma \le 1\%$), forcing modern systems to rely on crude sequential scan fallbacks. Directly supports our project's goal of designing probabilistic membership filters embedded within HNSW nodes to avoid graph fragmentation. Informs our cost model by showing where the optimizer transition threshold ($\sigma^*$) should theoretically and practically lie.
Novelty check: yes for metadata predicate checks during graph traversal (evaluated as "in-filtering" in HNSW within Milvus and FAISS, p. 3-4, §2.2; p. 12, §5.1), but no probabilistic membership filter (Bloom, Cuckoo, Xor) is implemented or evaluated (p. 3-14, §2-5).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- wang2021milvus (Milvus: A Purpose-Built Vector Data Management System) (p. 29)
- zhang2023vbase (VBase: Unifying high-dimensional vector similarity search and relational queries via relaxed monotonicity) (p. 30)
- J. Johnson, M. Douze, H. Jégou. "Billion-scale similarity search with GPUs." (IEEE TBD 2019) (p. 28)
- gollapudi2023filtereddiskann (Filtered-DiskANN: Graph algorithms for approximate nearest neighbor search with filters) (p. 28)
