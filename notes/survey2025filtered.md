# survey2025filtered — Survey of Filtered Approximate Nearest Neighbor Search over the Vector-Scalar Hybrid Data
Authors / Year / Venue / DOI: Lin, Yanjun, Zhang, Kai, He, Zhenying, Jing, Yinan, Wang, X. Sean / 2025 / not stated / none
Status: PRE
PDF: papers/survey2025filtered.pdf   Read fully: yes

## Problem addressed (p.)
Lack of systematic survey, unified problem definitions, and principled algorithm classification for Filtered Approximate Nearest Neighbor Search (FANNS) over vector-scalar hybrid data (p. 1, §1). Identifies key challenges including inconsistent search problem formulations, incomplete analysis of query difficulty, and lack of standardized hybrid datasets (p. 1-2, §1; p. 11, §4.1).

## Method (core idea in ≤5 sentences) (p.)
Formulates a formal mathematical model for vector-scalar hybrid datasets, queries, and evaluation metrics (p. 3-4, §2). Proposes a pruning-focused taxonomy categorizing 17 FANNS algorithms into four distinct pruning paradigms: Vector-Sequential Pruning (VSP), Vector-centric Joint Pruning (VJP), Scalar-Sequential Pruning (SSP), and Scalar-centric Joint Pruning (SJP) (p. 6-7, §3.1; Fig. 1-2, p. 7). Classifies algorithms based on whether vector pruning or scalar pruning takes precedence, and whether pruning operates sequentially or jointly during index traversal (p. 6-10, §3). Analyzes hybrid dataset construction across synthetic and organic scalar domains (p. 11-12, §4). Evaluates the distribution factor and selectivity regimes governing query difficulty, presenting an agenda of open research challenges (p. 12-17, §5-6).

## Complexity / theoretical claims
- none stated (survey paper) (p. 1-26).

## Filter type and selectivity regime handled (p.)
Covers diverse filter types across the literature: equality filters, discrete label/set filters, and 1D/multi-dimensional numerical range filters (p. 3-4, §2.2). Discusses query selectivity across high, medium, and low regimes, highlighting how query difficulty is jointly governed by scalar selectivity and the spatial vector distribution of matching candidates (p. 12-16, §5).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Surveys across all major vector index families: graph-based (NSW, HNSW, Vamana/DiskANN), inverted partition-based (IVF, IVFFlat, IVFPQ), tree-based (kd-tree, qd-tree, prefix tree, segment tree), and hybrid composite structures (p. 4-6, §2.3; p. 7-11, §3).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 2, p. 12): SIFT-1M (1M, 128d), GIST-1M (1M, 960d), Deep-10M (10M, 96d), MNIST-8M (8.1M, 784d), MTG (40k, 1152d), GloVe-Twitter (1.18M, 25-200d), GloVe-Crawl (1.99M, 300d), LAION-1M (1M, 512d), YouTube (6.13M, 1024d/128d).
- Baselines (surveyed algorithms A1-A17, p. 6-11, §3): Post-Filtering, VBase, AIRSHIP, ACORN, Filtered-DiskANN, SeRF, Milvus-Partition, HQI, MA-NSW, iRangeGraph, WST, etc.
- Metrics (p. 4, §2.4): Filtered Recall@K, Normalized Cumulative Information Gain (NCG), Queries Per Second (QPS), Query Latency, Index Construction Time, Index Size.

## Key results (numbers exactly as reported, with Table/Fig locator)
- Provides structured taxonomy categorizing 17 FANNS algorithms across 4 pruning paradigms (Fig. 1-2, p. 7; §3, p. 6-11).
- Surveys 9 major hybrid datasets, classifying data size, vector source, dimensionality, and number of organic scalar attributes (Table 2, p. 12).
- Highlights that under extreme low selectivity, VSP (post-filtering) suffers severe degradation because the probability of encountering valid candidates drops proportionally to selectivity (p. 7, §3.2).
- Identifies that VJP algorithms like ACORN and Filtered-DiskANN achieve higher efficiency across selectivity levels but may produce lower recall when graph connectivity breaks down (p. 8-9, §3.3).

## Limitations (author-stated vs. observed)
- Author-stated: Comprehensive standardized hybrid benchmark datasets are still lacking in the community, limiting unified experimental cross-comparison (p. 11, §4.1; p. 17, §6).
- Author-stated: Effective quantitative metrics to measure the spatial correlation between scalar filters and vector distribution remain an open problem (p. 12, §5.2; p. 17, §6).
- Observed: Purely qualitative and taxonomic review without new empirical experimental benchmarks executed under a uniform hardware/software testbed.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Provides the overarching taxonomic foundation that classifies our project as a Vector-centric Joint Pruning (VJP) approach operating inside HNSW traversal. Notes that existing VJP graph indexes lack formal theoretical guarantees and rely on empirical heuristics or degree inflation. Directly motivates Section 6.1's open question: how to integrate traditional probabilistic data structures to support general filter indexing without structural graph degradation.
Novelty check: unclear / no; as a survey paper, it categorizes existing in-traversal predicate check algorithms (e.g., ACORN, AIRSHIP, Filtered-DiskANN under VJP, p. 7-10, §3.3), but identifies that none of the surveyed graph methods utilize probabilistic membership filters (Bloom, Cuckoo, Xor) during traversal (p. 6-11, §3; p. 17, §6.1).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Useful references to snowball (bibkeys or titles from its reference list)
- patel2024acorn (ACORN: Performant and predicate-agnostic search over vector embeddings and structured data) (p. 23)
- gollapudi2023filtereddiskann (Filtered-DiskANN: Graph algorithms for approximate nearest neighbor search with filters) (p. 20)
- zuo2024serf (SeRF: Segment graph for range-filtering approximate nearest neighbor search) (p. 25)
- zhao2023airship (AIRSHIP: Attribute-constrained approximate nearest neighbor search on proximity graph) (p. 25)
- zhang2023vbase (VBase: Unifying high-dimensional vector similarity search and relational queries via relaxed monotonicity) (p. 25)
