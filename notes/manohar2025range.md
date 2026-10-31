# manohar2025range — Range Retrieval with Graph-Based Indices
Authors / Year / Venue / DOI: Manohar, Magdalen Dobson, Kim, Taekseung, Blelloch, Guy E. / 2025 / not stated / none
Status: PRE
PDF: papers/manohar2025range.pdf   Read fully: yes

## Problem addressed (p.)
Approximate high-dimensional range retrieval (retrieving all database vectors within a fixed metric distance radius $r$ of a query point, $\max_{p \in \mathcal{K}_q} d(p, q) \le r$) using graph-based indices; addressing the extreme query result skew (majority of queries have 0 results while outliers have thousands), which causes fixed-beam search to either waste computations on empty queries or fail to retrieve large result sets (p. 1–2, 4).

## Method (core idea in ≤5 sentences) (p.)
The authors adapt single-layer ANNS proximity graphs (specifically in-memory DiskANN / ParlayANN) to execute metric ball range retrieval without modifying the underlying graph index structure (p. 1–2, 4). They introduce an early stopping heuristic that evaluates the distance to the currently visited point ($d_{visited}$) after a minimum visit count ($v_l$) to terminate quickly when a query has no matching candidates within radius $r$ (p. 5–7). For queries containing matching candidates, search extends beyond standard beam search via two alternatives: Doubling Search (successively doubling beam width $b \leftarrow 2b$ if returned candidates are all valid range results), and Greedy Search (an unbounded queue that expands only neighbors falling strictly within radius $r$) (p. 5–7). Candidates identified under scalar quantization are exact-distance re-ranked to guarantee all returned items satisfy the radius constraint (p. 7).

## Complexity / theoretical claims
- Statement, assumptions, theorem number, page: none stated (purely empirical algorithm design and benchmarking across public vector datasets) (§1–6, p. 1–10).

## Filter type and selectivity regime handled (p.)
Metric ball distance range constraint ($d(p, q) \le r$), which the authors explicitly distinguish from metadata "range filtering" on numerical tags (§1.1, p. 2; §2, p. 2). Selectivity regimes span from 0 results (majority of queries, e.g. 70–99% depending on dataset) up to $>10^4$ matching vectors per query (Table 2, p. 4; p. 3–4).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Vamana (via in-memory DiskANN / ParlayANN implementation) and FAISS-IVF (inverted file with optional HNSW centroid coarse quantizer) (§4.1, p. 4; §5, p. 7). Multi-layer HNSW is noted as straightforwardly adaptable (§4.1, p. 4).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 1, p. 4):
  - Euclidean ($L_2$): BIGANN (128d uint8, 1M to 1B), DEEP (96d float, 1M), MSTuring (100d float, 1M), GIST (968d float, 1M), SSNPP (200d uint8, 1M to 1B), OpenAI (1536d float, 1M).
  - Inner Product (IP): Text2Image (200d float, 1M), Wikipedia (768d float, 1M and 10M), MSMARCO-WebSearch (768d float, 1M).
- Baselines (§1.1, p. 2; §4.1, p. 4; §5, p. 7): Standard beam search baseline on ANNS graph, in-memory Doubling Search (adapted from Starling system), FAISS-IVF range search.
- Metrics (Definition 2.2, p. 2; §5, p. 7; Fig. 4–6): Average Precision ($\sum_{q \in Q} |\mathcal{K}_q \cap \mathcal{K}'_q| / \sum_{q \in Q} |\mathcal{K}_q|$), QPS (queries per second), single-threaded search latency breakdown (s).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Achieves up to $100\times$ throughput (QPS) improvement over standard beam search and FAISS-IVF range search on DEEP, BIGANN, and MSTuring datasets (Abstract, p. 1; §5, p. 7; Fig. 4).
- Provides up to $10\times$ throughput speedup over in-memory doubling search without early stopping on large-scale datasets (Abstract, p. 1; §5, p. 7; Fig. 4–5).
- On OpenAI-1M, range search reaches ~10,000 QPS at 90% precision compared to ~5,000 QPS for top-10 search at 90% recall; on MSTuring-1M, achieves >100,000 QPS at 90% precision vs ~30,000 QPS for top-10 search (§5, p. 9).
- Demonstrated scalability on 100M and 1B datasets (BIGANN-1B, SSNPP-1B), where greedy range search increasingly outperforms doubling search as result density rises (Fig. 1, p. 3; Fig. 5, p. 9).

## Limitations (author-stated vs. observed)
- Author-stated: Early stopping heuristics can prematurely truncate queries with valid range results if cutoff thresholds are too aggressive, degrading average precision (§5, p. 9; Fig. 6); sensitivity to radius robustness varies across datasets (§3.1, p. 3); greedy search requires a larger initial beam width to discover entry points into dense clusters (§5, p. 8–9); lack of standard high-dimensional range retrieval benchmarks (§1, p. 1; §6, p. 10).
- Observed: Solves spatial/metric ball range retrieval ($d(p, q) \le r$), not predicate-constrained or metadata-filtered ANN search over relational/scalar attributes.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
The paper demonstrates that modifying graph traversal stopping rules and candidate filtering during search dynamically accommodates skewed selectivity without altering graph topology. Its analysis of early stopping ($d_{visited}$ cutoffs) and bounded greedy traversal provides an empirical reference for managing extreme selectivity variations during graph search.
Novelty check: Novelty check: no (p. 1–2, §1.1; explicitly focuses on metric ball distance range search $d(p,q) \le r$ and explicitly notes it does not evaluate metadata range filters or membership filter structures).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- §1.1 (p. 2) explicitly states that range search ($d(q, p) \le r$) is distinct from "range filtering" (predicates on external numerical attributes like timestamps); the paper deals solely with metric ball retrieval and does not evaluate metadata filtering.

## Useful references to snowball (bibkeys or titles from its reference list)
- Manohar et al. (2024) [20]: ParlayANN: Scalable and deterministic parallel graph-based approximate nearest neighbor search algorithms (PPoPP)
- Subramanya et al. (2019) [27]: DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node (NeurIPS)
- Engels et al. (2024) [11]: Approximate Nearest Neighbor Search with Window Filters (ICML)
- Szilvasy et al. (2024) [28]: Bulk range search with inverted files
- Wang et al. (2024) [30]: Starling: An I/O-Efficient Disk-Resident Graph Index (SIGMOD)
