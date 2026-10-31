# routing2026query — Query-aware Routing for Filtered Approximate Nearest Neighbors Search
Authors / Year / Venue / DOI: Xiong, Qianqian, Zhang, Mengxuan / 2026 / not stated / none
Status: PRE
PDF: papers/routing2026query.pdf   Read fully: yes

## Problem addressed (p.)
Filtered Approximate Nearest Neighbors Search (FANNS) across categorical predicates where no single indexing method or parameter setting consistently dominates (p. 1-2, §1). Performance varies sharply across datasets, predicate types, and query selectivities, making manual selection of algorithms and hyperparameters suboptimal (p. 1-2, §1).

## Method (core idea in ≤5 sentences) (p.)
Proposes a query-aware routing framework that dynamically selects the optimal FANNS method and execution parameters on a per-query basis (p. 1-2, §1). Constructs an offline benchmark table capturing empirical recall and QPS across candidate methods and configurations (p. 6, §4.3). Employs a lightweight Multi-Layer Perceptron regression model (MLP-Reg) to predict candidate methods' recall using only three features: query selectivity $\sigma$, mean local intrinsic dimensionality ($LID_{mean}$), and predicate type (p. 5, §4.2; p. 9, §6.2). Queries the offline benchmark table with predicted recall to select the configuration that satisfies the target recall threshold while maximizing QPS (p. 6, §4.3). Also formulates a rule-based decision tree (RuleRouter) as a lightweight static baseline (p. 3-4, §3).

## Complexity / theoretical claims
- none stated (empirical machine learning routing study) (p. 1-12).

## Filter type and selectivity regime handled (p.)
Three categorical filter predicate types: Equality ($L_i = L_q$), Containment / AND ($L_q \subseteq L_i$), and Overlap / OR ($L_q \cap L_i \ne \emptyset$) (p. 2, §2.1). Handles broad selectivity regimes spanning low to high selectivity ($\sigma \in [10^{-4}, 1.0]$) (p. 5, §4.2; p. 8, §6.1.2).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Routes across heterogeneous index structures: HNSW (Post-filtering), UNG, SIEVE, ACORN-$\gamma$, and FilteredVamana (p. 7, §6.1.1).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 2, p. 8; Table 4, p. 9): 6 training datasets (Arxiv, Paper, Audio, Book, Video, YFCC) and 5 unseen evaluation datasets (yahoo800k, dbpedia560k, synth_100d_lc, synth_768d_mc, synth_768d_hc).
- Baselines (p. 7, §6.1.1): Pre-filter, Post-filter (HNSW), UNG, SIEVE, ACORN-$\gamma$, ACORN-1, NHQ, CAPS, FilteredVamana, StitchedVamana, RuleRouter.
- Metrics (p. 8, §6.1.1): Recall@10, Queries Per Second (QPS) over 16 threads, Routing overhead latency ($\mu\text{s}$).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Feature ablation successfully narrows 22 candidate features down to 3 minimal features without sacrificing routing precision (p. 9, §6.2).
- Routing decision inference latency is only 41 $\mu\text{s}$ per query for 5 candidate methods on CPU (p. 11, §6.2).
- The ML Router consistently tracks the empirical Pareto frontier across all 5 unseen datasets, outperforming static methods and RuleRouter (p. 11, §6.2; Fig. 4, p. 10).

## Limitations (author-stated vs. observed)
- Author-stated: Requires an offline profiling phase on benchmark workloads to construct the performance lookup table (p. 6, §4.3; p. 12, §7).
- Author-stated: Restricted to categorical predicates; does not support continuous numerical range queries (p. 2, §2.1; p. 12, §7).
- Observed: Deploying routing across heterogeneous index structures requires keeping multiple indexing engines (e.g., UNG, ACORN, Vamana) co-located in memory, incurring high RAM overhead.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Demonstrates empirically that query selectivity ($\sigma$) is the single most dominant factor determining whether post-filtering or in-traversal graph filtering wins. Validates the theoretical motivation for our project's selectivity crossover point ($\sigma^*$) and cost model. Serves as a comparative framework showing the performance boundaries of ACORN and post-filter HNSW.
Novelty check: no; routing operates prior to search by predicting recall and dispatching the query to external algorithms, without modifying graph traversal itself (p. 1-2, §1; p. 5-6, §4).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- patel2024acorn (ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data) (p. 12)
- gollapudi2023filtereddiskann (Filtered-DiskANN: Graph Algorithms for Approximate Nearest Neighbor Search with Filters) (p. 12)
- li2025sieve (SIEVE: A Workload-Adaptive Sub-Index Framework for Filtered Vector Search) (p. 12)
- zhao2023airship (AIRSHIP: Attribute-constrained approximate nearest neighbor search on proximity graph) (p. 12)
