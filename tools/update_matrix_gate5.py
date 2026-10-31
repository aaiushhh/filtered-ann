import csv

new_rows = [
    {
        "bibkey": "prokhorenkova2020graph",
        "year": "2020",
        "venue": "ICML 2020",
        "status": "PUB",
        "index_structure": "k-NN graph / Kleinberg / HNSW",
        "filter_type": "none",
        "selectivity_regime": "not stated",
        "strategy": "none",
        "formal_complexity": "yes",
        "complexity_form": "Theta(n^(1/d) * M^d) greedy k-NN; O(log^2 n) Kleinberg augmented; 2 steps for d >> log n (p. 2, 4-6)",
        "uses_probabilistic_filter": "no",
        "datasets": "synthetic uniform spherical, SIFT1M, GIST1M, GloVe (p. 7-8)",
        "main_baselines": "plain k-NN graph, uniform shortcuts, HNSW (p. 7-8)",
        "open_source_code": "none stated",
        "gap_note": "Assumes uniform spherical distribution; unconstrained search only without predicate filtering",
        "novelty_check": "no",
        "selectivity_cost_model": "no"
    },
    {
        "bibkey": "diwan2024navigable",
        "year": "2024",
        "venue": "NeurIPS 2024",
        "status": "PUB",
        "index_structure": "general directed navigable graph",
        "filter_type": "none",
        "selectivity_regime": "not stated",
        "strategy": "none",
        "formal_complexity": "yes",
        "complexity_form": "Upper bound O(sqrt(n) log n) average degree; lower bound Omega(n^(1/2-delta)) in d = Omega(log n) (p. 2-3, 5-9)",
        "uses_probabilistic_filter": "no",
        "datasets": "synthetic {-1, 1}^d, Gaussian clusters (p. 10-12)",
        "main_baselines": "complete graph, randomized skip-graphs, greedy routing (p. 4, 10-11)",
        "open_source_code": "none stated",
        "gap_note": "Proves Theta(sqrt(n)) degree lower bound for high-dimensional navigability; unconstrained search only",
        "novelty_check": "no",
        "selectivity_cost_model": "no"
    },
    {
        "bibkey": "indyk2023worst",
        "year": "2023",
        "venue": "NeurIPS 2023",
        "status": "PUB",
        "index_structure": "DiskANN (Vamana) / HNSW / NSG",
        "filter_type": "none",
        "selectivity_regime": "not stated",
        "strategy": "none",
        "formal_complexity": "yes",
        "complexity_form": "O(log Delta) query time with (alpha+1)/(alpha-1) approx for global robust pruning; >= 0.1n worst-case steps for fast preprocessing (p. 4-7)",
        "uses_probabilistic_filter": "no",
        "datasets": "synthetic 2D spiral, concentric circles, SIFT1M (p. 5-8)",
        "main_baselines": "DiskANN (slow/fast), HNSW, NSG, linear scan (p. 1-3, 6-8)",
        "open_source_code": "none stated",
        "gap_note": "First worst-case analysis of graph ANN; constructs linear-step instances; unconstrained search only",
        "novelty_check": "no",
        "selectivity_cost_model": "no"
    },
    {
        "bibkey": "li2025sieve",
        "year": "2025",
        "venue": "PVLDB 2025",
        "status": "PUB",
        "index_structure": "HNSW subindex collection / IVF / Flat",
        "filter_type": "categorical labels / conjunctive AND / disjunctive OR / range",
        "selectivity_regime": "arbitrary (0.01% to >50%)",
        "strategy": "partition",
        "formal_complexity": "yes",
        "complexity_form": "Closed-form cost model C_bf(f) = gamma * card(f) and C(I_h, f) for downscaled subindexes; (1-1/e) greedy submodular bound (p. 5-7)",
        "uses_probabilistic_filter": "no",
        "datasets": "Paper (2M), Video (1M), E-Commerce (10M), Bio (5M) (p. 9-10)",
        "main_baselines": "Milvus (HNSW, IVF), hnswlib, ACORN, CAPS, Filtered-DiskANN (p. 10)",
        "open_source_code": "none stated",
        "gap_note": "Materializes separate sub-graphs instead of pruning during single-graph traversal; requires historical query workload",
        "novelty_check": "no",
        "selectivity_cost_model": "yes"
    },
    {
        "bibkey": "gupta2023caps",
        "year": "2023",
        "venue": "arXiv preprint",
        "status": "PRE",
        "index_structure": "IVF / space-partitioning with attribute sub-partitions",
        "filter_type": "categorical labels / conjunctive AND / sparse attributes",
        "selectivity_regime": "dense (>50%), sparse (<1%), and unhappy middle (1%-20%)",
        "strategy": "partition",
        "formal_complexity": "no",
        "complexity_form": "none stated",
        "uses_probabilistic_filter": "no",
        "datasets": "YFCC10M, Paper (2M), ImageNet (1.2M), MNIST (70K) (p. 8)",
        "main_baselines": "Milvus (IVF-Flat, HNSW), Filtered-DiskANN, AIRSHIP, NHQ (p. 8-9)",
        "open_source_code": "none stated",
        "gap_note": "Partition-based approach avoiding graph traversal; degrades under uniform attribute distributions",
        "novelty_check": "no",
        "selectivity_cost_model": "no"
    },
    {
        "bibkey": "zhang2023vbase",
        "year": "2023",
        "venue": "USENIX OSDI 2023",
        "status": "PUB",
        "index_structure": "HNSW / DiskANN / SPANN inside PostgreSQL",
        "filter_type": "arbitrary SQL predicates (relational filter, range, join)",
        "selectivity_regime": "arbitrary (0.01% to >50%)",
        "strategy": "post",
        "formal_complexity": "yes",
        "complexity_form": "Theorem 1 semantic equivalence proof for relaxed monotonicity pipeline (p. 7-8)",
        "uses_probabilistic_filter": "no",
        "datasets": "SIFT100M, Deep100M, SpaceV100M, E-Commerce 10M (p. 11)",
        "main_baselines": "pgvector (PostgreSQL HNSW/IVFFlat), Milvus v2.2 (p. 11-12)",
        "open_source_code": "none stated",
        "gap_note": "Systems abstraction for relational-vector pipelines; does not embed probabilistic filters into graph edges",
        "novelty_check": "no",
        "selectivity_cost_model": "no"
    },
    {
        "bibkey": "mitzenmacher2018model",
        "year": "2018",
        "venue": "NeurIPS 2018",
        "status": "PUB",
        "index_structure": "other (Sandwiched Learned Bloom Filter)",
        "filter_type": "learned Bloom filter / standard Bloom filter / Bloomier filter",
        "selectivity_regime": "not stated",
        "strategy": "other",
        "formal_complexity": "yes",
        "complexity_form": "Theorem 4 generalization bound; optimal sandwiched false positive probability F_sand (p. 5, 8)",
        "uses_probabilistic_filter": "yes (Bloom filter)",
        "datasets": "synthetic oracle evaluations (p. 6-9)",
        "main_baselines": "standard Bloom filter, non-sandwiched learned Bloom filter (p. 1, 6-9)",
        "open_source_code": "none stated",
        "gap_note": "Evaluates set-membership queries; does not evaluate graph nearest neighbor traversal",
        "novelty_check": "no",
        "selectivity_cost_model": "no"
    }
]

with open("matrix.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

existing_keys = set(r["bibkey"] for r in rows)

added_count = 0
for nr in new_rows:
    if nr["bibkey"] not in existing_keys:
        rows.append(nr)
        added_count += 1
    else:
        # Update existing row if placeholder
        for idx, r in enumerate(rows):
            if r["bibkey"] == nr["bibkey"]:
                rows[idx] = nr

with open("matrix.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated matrix.csv: added {added_count} rows. Total rows now: {len(rows)}.")
