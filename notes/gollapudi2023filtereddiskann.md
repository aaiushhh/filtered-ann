# gollapudi2023filtereddiskann — Filtered-DiskANN: Graph Algorithms for Approximate Nearest Neighbor Search with Filters
Authors / Year / Venue / DOI: Siddharth Gollapudi, Neel Karia, Varun Sivashankar, Ravishankar Krishnaswamy, Nikit Begwani, Swapnil Raz, Yiyong Lin, Yin Zhang, Neelam Mahapatro, Premkumar Srinivasan, Amit Singh, Harsha Vardhan Simhadri / 2023 / Proceedings of the ACM Web Conference 2023 (WWW 2023) / 10.1145/3543507.3583552
Status: PUB (DOI: 10.1145/3543507.3583552)
PDF: papers/gollapudi2023filtereddiskann.pdf   Read fully: yes

## Problem addressed (p.)
Filtered Approximate Nearest Neighbor Search (ANNS) combining vector similarity with discrete metadata filter constraints (p. 1-2, §1). Traditional post-filtering fails when filter selectivity is low because too few qualifying candidates are retrieved, while pre-filtering over millions of items is computationally prohibitive or incurs excessive latency (p. 1-2, §1; p. 3, §2).

## Method (core idea in ≤5 sentences) (p.)
Proposes two proximity graph indexing algorithms tailored for filtered search based on DiskANN/Vamana: FilteredVamana and StitchedVamana (p. 1-2, §1; p. 3-5, §3-4). FilteredVamana builds a unified graph where out-neighbors are selected using FilteredRobustPrune to balance vector distance against label co-occurrence, and maintains designated label-specific medoid start nodes ($st(F)$) for routing (p. 3-4, §3; Algorithm 4, p. 4). StitchedVamana builds small standalone Vamana graphs independently for each label and stitches them together by taking their edge union before pruning the overlaid graph to a bounded maximum degree (p. 4-5, §4; Algorithm 5, p. 4). At query time, FilteredGreedySearch initiates graph exploration at the query label's medoid and explores only candidate neighbors matching the filter constraint (p. 3-4, §3.1; Algorithm 1, p. 3).

## Complexity / theoretical claims
- none stated (purely empirical) (p. 1-11).

## Filter type and selectivity regime handled (p.)
Discrete categorical filter labels (tested primarily on singleton filter label queries $F$, with support for multi-label sets) (p. 1, §1; p. 4, §3.1). Handles extreme low-selectivity regimes with filter specificity down to $10^{-4}$ to $10^{-6}$ (p. 3, §1; Table 1, p. 5).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Vamana proximity graph (from DiskANN), instantiated as FilteredVamana and StitchedVamana (p. 1, §1; p. 3-5, §3-4).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 1, p. 5): Turing (2.6M vectors, 100d, 3070 filters), Prep (1M vectors, 64d, 47 filters), DANN (3.3M vectors, 64d, 47 filters), SIFT (1M, 128d), GIST (1M, 960d), msong (992k, 420d), audio (53k, 192d), paper (2M, 200d).
- Baselines (p. 6, §5.2): FAISS IVF inline-processing, FAISS IVF post-processing, FAISS HNSW post-processing, NHQ, Milvus HNSW.
- Metrics (p. 5, §5; p. 8, §6): Recall@10, Queries Per Second (QPS), Index Build Time (s), Online ad click and revenue lift.

## Key results (numbers exactly as reported, with Table/Fig locator)
- StitchedVamana consistently offers better QPS for recall@90 by a factor of 2 compared to FilteredVamana (p. 7, §5.4.1).
- On PREP dataset at 90% recall, FilteredVamana achieves 2.5× higher QPS than the next best baseline (IVF inline), and StitchedVamana achieves 6× higher QPS (p. 7, §5.3.2; Fig. 2, p. 6).
- Index build time on Turing is 159.8s for FilteredVamana and 469.9s for StitchedVamana (Table 2, p. 7).
- In an online A/B test on a production sponsored ad search system with 47 regions, FilteredVamana increased user clicks by 34.61% and revenue by 48.95% over the baseline (Table 3, p. 8), with revenue gains reaching 79.77% on low-selectivity regions (<1% share) (Table 4, p. 8).

## Limitations (author-stated vs. observed)
- Author-stated: StitchedVamana build time scales with the number of unique labels, making it less practical when the number of labels is very large (p. 7, §5.4.1; Table 2, p. 7).
- Author-stated: Primarily benchmarks single-label equality queries; multi-label complex boolean predicates require further exploration (p. 4, §3.1).
- Observed: Pruning the stitched graph reduces edge coverage across rare label intersections, potentially impacting recall when queries specify combinations of rare filters.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Serves as one of the most important foundational graph-based filtered ANN baselines (FilteredVamana / StitchedVamana) to benchmark against. Demonstrates that label-guided pruning during index construction and traversal dramatically outperforms post-filtering at low selectivity. Shows how in-traversal predicate checking operates on proximity graphs, providing key empirical data for crossover selectivity analysis.
Novelty check: yes for metadata predicate check during graph traversal (in FilteredGreedySearch, neighbors are verified against query filter labels $F$ before being added to candidate set $L$, p. 3-4, §3.1, Algorithm 1), but no probabilistic membership filter (Bloom, Cuckoo, Xor) is used (p. 3-5, §3-4).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Authors state they were unable to reproduce the NHQ baseline results from prior literature (p. 6, §5.2; p. 9, Appendix A.1).

## Useful references to snowball (bibkeys or titles from its reference list)
- subramanya2019diskann (DiskANN: Fast accurate billion-point nearest neighbor search on a single node) (p. 11)
- malkov2020hnsw (Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 11)
- wang2021milvus (Milvus: A purpose-built vector data management system) (p. 11)
- wu2022hqann (HQANN: Efficient and Robust Similarity Search for Hybrid Queries with Structured and Unstructured Constraints) (p. 11)
