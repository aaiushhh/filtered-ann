# Observations

- curator2026: Low-selectivity graph disconnection is addressed by stratified base clustering and multi-round greedy routing, outperforming ACORN and Post-filtering at selectivity < 10% (ref: Patel et al., ACORN, SIGMOD 2024).
- filteraware2025: Replaces static traversal penalties with learned metric weighting between vector distance and multi-filter satisfaction during HNSW construction and search, achieving superior Pareto curves on composite filters (ref: Malkov & Yashunin, HNSW, TPAMI 2020).
- filtered2026system: Engine-level query execution planning (iterative post-filtering vs pre-filtering in Milvus/Qdrant/pgvector) overrides raw index microbenchmarks, with IVFFlat outperforming HNSW under low selectivity regimes (ref: Wang et al., Milvus, SIGMOD 2021).
- rangefilters2026: Compresses high-cardinality multi-hop graph reachability labels into Bloom filters for in-traversal set containment and intersection testing, attaining up to 70.3x QPS gains over post-filtering with >98% recall (ref: Bloom, ACM 1970).
- routing2026query: Demonstrates no single filtered ANN method dominates across workloads; a 3-feature MLP regression router (selectivity, LID, predicate type) tracks the Pareto frontier across unseen datasets with 41 us decision overhead (ref: Patel et al., ACORN, SIGMOD 2024).
