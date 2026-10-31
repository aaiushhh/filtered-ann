# filteraware2025 — Learning Filter-Aware Distance Metrics for Nearest Neighbor Search with Multiple Filters
Authors / Year / Venue / DOI: Sutradhar, Ananya, Gupta, Suryansh, Krishnaswamy, Ravishankar, Xu, Haiyang, Rastogi, Aseem, Srinivasa, Gopal / 2025 / not stated / none
Status: PRE
PDF: papers/filteraware2025.pdf   Read fully: yes

## Problem addressed (p.)
Filtered Approximate Nearest Neighbor (ANN) search over high-dimensional vector datasets subject to multi-label discrete attribute constraints (p. 1-2, §1). Existing graph-based methods rely on fixed, data-independent penalties during graph traversal or construction, which fail to generalize across diverse datasets where vector similarities and label distributions vary widely (p. 1-2, §1).

## Method (core idea in ≤5 sentences) (p.)
Proposes a data-driven approach that learns an optimal distance metric trading off vector similarity against filter mismatch penalty (p. 1-2, §1). Formulates the metric learning problem as a constrained linear program (LP) solved using PuLP (p. 4, §4). Derives optimal penalty weights ($w_m$) reflecting label rarity and metric spacing from a sample of training queries (p. 4, §4; p. 5, §7.1). Incorporates the learned distance metric into both index construction and beam-search traversal using Filtered-DiskANN as the base framework (p. 4, §5). Dynamically bypasses graph traversal to perform exact brute-force scan if estimated matching point cardinality falls below 100,000 (p. 4, §5; p. 9, Appendix A).

## Complexity / theoretical claims
- none stated (empirical machine learning optimization study) (p. 1-11).

## Filter type and selectivity regime handled (p.)
Multi-label discrete attribute containment filters where retrieved vectors must satisfy $S \subseteq L(v)$ (p. 1, §1; p. 3, §3). Evaluated across varied selectivity regimes, with penalty weights adapting according to whether filter matches are sparse or abundant (p. 1, §1; p. 5, §7.1; p. 6, §8).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Proximity graph based on Filtered-DiskANN / Vamana with learned distance metrics applied to edge construction and greedy routing (p. 4, §5; p. 8, Appendix A).

## Datasets, baselines, metrics (Table N)
- Datasets (p. 5, §7.1; p. 9-10, Appendix B): YFCC1M (1M image vectors, 11,865 train / 5,718 eval queries), Wikipedia (35M sentence embeddings, 308 train / 464 eval queries).
- Baselines (p. 5, §7.3): Post-Filtering, Fixed Penalty Search, Integrated Learning (Ours).
- Metrics (p. 5, §7.2): Recall@10, Average number of vector distance comparisons.
- Note: Table N is not stated; results are reported in text (§7) and Figures 1–2 (p. 5).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Improves Recall@10 accuracy by 5–10% over fixed-penalty baselines across evaluated datasets (p. 1, Abstract; p. 2, §1).
- On Wikipedia-35M, the learned penalty weight converges to $w_m = 0.204148$ (p. 5, Fig. 1).
- On YFCC1M, the learned penalty weight converges to $w_m = 0.017787$ (p. 5, Fig. 2).
- Shows that index construction with learned filter-aware edge weights does not degrade performance on unfiltered queries (p. 6, §7.3).

## Limitations (author-stated vs. observed)
- Author-stated: Formulated specifically for discrete multi-label containment ($S \subseteq L(v)$); does not support continuous numerical range or inequality predicates (p. 1, §1; p. 3, §3).
- Author-stated: Requires a representative training workload of sample queries to solve the linear program offline before index construction (p. 4, §4; p. 5, §7.1).
- Observed: Modifying distance functions during index construction binds the graph structure to specific training label distributions, potentially reducing robustness to workload drift.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Demonstrates that incorporating filter awareness into graph connectivity significantly outperforms post-filtering and static heuristics. Validates our hypothesis that traversal decisions must account for predicate selectivity. Contributes a useful comparison point showing how learned scalar weights differ from embedding probabilistic membership filters (Bloom/Cuckoo/Xor) directly inside graph nodes.
Novelty check: yes for metadata predicate checks during graph traversal (it evaluates filter overlap penalty during greedy graph routing, p. 4, §5), but no probabilistic membership filter (Bloom, Cuckoo, Xor) is used (p. 1-6, §1-5).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- gollapudi2023filtereddiskann (Filtered-diskann: Graph algorithms for approximate nearest neighbor search with filters) (p. 6)
- patel2024acorn (ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data) (p. 7)
- gupta2023caps (CAPS: A practical partition index for filtered similarity search) (p. 7)
- Datar et al. "Locality-sensitive hashing scheme based on p-stable distributions." (SoCG 2004) (p. 6)
