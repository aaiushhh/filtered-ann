# li2025sieve — SIEVE: Effective Filtered Vector Search with Collection of Indexes
Authors / Year / Venue / DOI: Zhaoheng Li, Silu Huang, Wei Ding, Yongjoo Park, Jianjun Chen / 2025 / Proceedings of the VLDB Endowment (PVLDB 2025) / 10.14778/3749646.3749725
Status: PUB (PVLDB Vol. 18, No. 11, pp. 4723–4736, 2025)
PDF: papers/li2025sieve.pdf   Read fully: yes

## Problem addressed (p.)
Filtered vector search under hard metadata predicates across arbitrary selectivity regimes (p. 1-2, §1). Existing graph-based solutions fail across broad selectivity ranges: partition-based indexes (e.g. CAPS) restrict filter formats; data-attribute-aware graphs (e.g. Filtered-DiskANN) limit attribute cardinality ($<200$); intra-search filtering (e.g. ACORN) causes excessive traversal time inflation (up to $219\times$ HNSW latency at low selectivity); and exhaustive single-predicate indexing incurs prohibitive memory overhead (p. 1-2, §1, Table 1).

## Method (core idea in ≤5 sentences) (p.)
Instead of constraining traversal on a single global graph, SIEVE builds an index collection containing a root index and multiple specialized HNSW subindexes, each dedicated to high-frequency or low-selectivity predicate subsets (p. 1-3, §1-§3). To construct this collection under a fixed memory budget, SIEVE formulates a three-dimensional analytical cost model that relates subindex size, search time, target recall, and filter selectivity (p. 1, 4-6, §2.3, §4.2). Subindexes are downscaled in connectivity ($M_\downarrow$) and beam width ($S_\downarrow$) because smaller point subsets require substantially smaller degree to achieve high recall (p. 4-6, §2.3, §4.2, Figure 3). Candidate subindexes are selected using greedy submodular optimization that maximizes marginal search time reduction over historical query workloads (p. 4, 6-7, §3.1, §4.3). At query time, SIEVE dynamically routes queries to the optimal subindex or falls back to exact brute-force scan when filter selectivity is extremely low ($card(f) \le \text{threshold}$) (p. 4, 7-8, §3.2, §5.2).

## Complexity / theoretical claims
- Analytical Cost Model (§4.2, PDF p. 5–6 / printed pp. 4727–4728, Table 2, Table 3): Formulates closed-form equations for memory size and query latency as a function of filter cardinality $card(f)$ (selectivity $\sigma = card(f)/N$):
  - Brute-force search cost: $C_{bf}(f) = \gamma \cdot card(f)$ (Table 3, PDF p. 6 / printed p. 4728; defined in Table 2, PDF p. 5 / printed p. 4727).
  - Indexed search cost: $C(I_h, sef, w, f) := \log(card(h)) \cdot sef \cdot \left(\frac{card(h)}{card(f)}\right)^{cor(w, f, h)}$ if $h$ subsumes $f$ else $\infty$ (Definition 4.7, PDF p. 5 / printed p. 4727; Table 3, PDF p. 6 / printed p. 4728).
  - Subindex $M$ downscaling function: $M_\downarrow(I_h) := M_\infty \frac{\log(card(h))}{\log(N)}$ (Definition 4.6, PDF p. 5 / printed p. 4727).
  - In-memory subindex size: $S(I_h) = M \cdot card(h) = \frac{M_\infty \log(card(h))}{\log(N)} card(h)$ (Table 3, PDF p. 6 / printed p. 4728; §4.2, PDF p. 5 / printed p. 4727).
- Submodular Optimization Guarantee (§4.3, PDF p. 7 / printed p. 4729): States that the greedy subindex selection algorithm achieves a $(1 - 1/e)$-approximation ratio to the NP-hard index collection problem under budget $B$ (citing Nemhauser et al. [49, 70]; note: there is no theorem numbered 4.6 in the paper; Definition 4.6 on PDF p. 5 / printed p. 4727 is the $M_\downarrow$ downscaling function).
- selectivity_cost_model: yes; explicitly models both brute-force scan cost $C_{bf}(f) = \gamma \cdot card(f)$ and indexed graph search latency $C(I_h, sef, w, f)$ as mathematical functions of filter cardinality/selectivity $card(f)/N$, routing queries between subindexes and brute force (PDF pp. 5–7 / printed pp. 4727–4729, §4.2, Table 2, Table 3, Definitions 4.6 & 4.7).

## Filter type and selectivity regime handled (p.)
- Filter type: Arbitrary predicate formats including categorical labels, multi-attribute conjunctions (AND), disjunctions (OR), and range predicates (p. 1-2, 4, §1, §4.1).
- Selectivity regime handled: All regimes from ultra-low selectivity ($0.01\%$) to high selectivity ($>50\%$), routing ultra-low to brute force and medium/low to dedicated subindexes (p. 1-2, 8, §1, §5.2, Table 1).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- Collection of downscaled HNSW graphs ($I_\infty$ and subindexes $I_h$), with comparison against IVF, Flat brute-force scan, ACORN, CAPS, and Filtered-DiskANN (p. 2-5, 8-9, §2, §4, §5).

## Datasets, baselines, metrics (Table N)
- Datasets (§6.1, p. 9-10, Table 3):
  - Paper: 2M 128-d vectors, 34K unique category labels.
  - Video: 1M 256-d vectors, 1.2K multi-label tags.
  - E-Commerce: 10M 64-d vectors, 50K hierarchical product categories.
  - Bio: 5M 512-d vectors, continuous numerical attributes.
- Baselines (§6.1, p. 10): Milvus (IVF-Flat, HNSW), hnswlib (result-filtering), ACORN-1, ACORN- $\gamma$, CAPS, Filtered-DiskANN, Exhaustive Indexing.
- Metrics (§6.1, p. 10): Query latency (ms at 0.90 and 0.95 Recall@10), QPS, index build time, memory footprint (GB).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Latency and Throughput (Figure 8, 9, p. 10-11, §6.2):
  - On Paper dataset at 0.90 recall: SIEVE achieves $3.8\times$ lower latency than ACORN and $8.2\times$ lower latency than Milvus-HNSW.
  - On E-Commerce dataset at low selectivity ($<1\%$): ACORN experiences traversal inflation ($>120$ ms), whereas SIEVE serves queries in $<8.5$ ms (Figure 9b, p. 11).
  - Under memory budget $1.5\times$ HNSW, SIEVE covers $>80\%$ of query workload with specialized subindexes, reducing average latency by $62.4\%$ compared to global HNSW (Figure 10, p. 11, §6.3).

## Limitations (author-stated vs. observed)
- Author-stated (p. 2, 4, 13, §1, §4.1, §7): Requires a representative historical query workload $H$ during offline indexing; performance degrades on unseen predicate patterns that lack specialized subindexes, defaulting to global root index or brute-force scan.
- Observed: Memory consumption increases linearly with the number of materialized subindexes (up to $2.15\times$ base HNSW); does not support dynamic online insertion of new predicates without index rebuilding.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
- Directly relevant to our cost-modeling framework: provides an established baseline formula parameterizing brute-force and graph-traversal crossover points by filter selectivity ($card(f)/N$).
- Illustrates the architectural trade-off: SIEVE chooses to duplicate data across multiple materialized sub-graphs, whereas our approach retains a single graph and embeds probabilistic membership filters to prune traversal without multiplying index storage.
Novelty check: no; does not prune graph edges during traversal with Bloom/Cuckoo/Xor membership filters, but instead routes queries across a collection of separate materialized sub-graphs (p. 1-4, §1-§3).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Cost model assumes subindex $M$ scales strictly as $M_\infty \frac{\log(card(h))}{\log(N)}$ without accounting for degree saturation in dense clusters, and $C(I_h, sef, w, f)$ assumes query correlation $cor(w, f, h)$ can be estimated accurately from historical queries (PDF pp. 5–6 / printed pp. 4727–4728, §4.2).

## Useful references to snowball (bibkeys or titles from its reference list)
- patel2024acorn (Patel et al., 2024: ACORN: Performant and predicate-agnostic search over vector embeddings and structured data) (p. 13)
- gupta2023caps (Gupta et al., 2023: CAPS: A practical partition index for filtered similarity search) (p. 13)
- malkov2020hnsw (Malkov & Yashunin, 2020: Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 14)
- gollapudi2023filtereddiskann (Gollapudi et al., 2023: Filtered-DiskANN: Graph algorithms for approximate nearest neighbor search with filters) (p. 13)
