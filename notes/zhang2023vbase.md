# zhang2023vbase — VBASE: Unifying Online Vector Similarity Search and Relational Queries via Relaxed Monotonicity
Authors / Year / Venue / DOI: Qianxi Zhang, Shuotao Xu, Qi Chen, Guoxin Sui, Jiadong Xie, Zhizhen Cai, Yaoqi Chen, Yinxuan He, Yuqing Yang, Fan Yang, Mao Yang, Lidong Zhou / 2023 / 17th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2023) / none
Status: PUB (USENIX OSDI 2023, pp. 377–395)
PDF: papers/zhang2023vbase.pdf   Read fully: yes

## Problem addressed (p.)
Integrating high-dimensional vector approximate similarity search with relational database query engines (PostgreSQL) for complex queries involving relational operators (joins, attribute filters, aggregations) (p. 1-3, §1-§2). High-dimensional vector indexes lack strict monotonicity, forcing existing vector systems to rely on fixed TopK APIs; under metadata filtering, predicting the required $K'$ in advance is difficult, leading either to recall degradation (if $K' \times \sigma < K$) or wasted index traversal (if $K' \times \sigma \gg K$) (p. 1, 3, 7-8, §1, §3.3).

## Method (core idea in ≤5 sentences) (p.)
VBASE identifies relaxed monotonicity—the property that graph and partition index traversals navigate approximately from nearest to progressively farther regions in a two-phase pattern—as the unifying bridge between vector indexes and relational iterators (p. 1, 3-5, §1, §3.1). It replaces the rigid, one-shot TopK interface with a pipelined iterator interface (`Next`, `Close`) implemented inside PostgreSQL's index extension framework (p. 1, 5, 8-9, §1, §3.2, §4.2). A generalized relaxed monotonicity checker monitors traversal convergence using sliding candidate queues (`smallestQueue`, `recentQueue`), terminating exploration on-the-fly once distance growth exceeds empirical thresholds (p. 5-7, §3.2, §4.1). This continuous iterator allows relational filter, join, and limit operators to be evaluated incrementally, streaming matching vectors without trial-and-error $K'$ estimation (p. 7-10, §3.3, §4.2). The paper formally proves semantic equivalence between VBASE's pipelined execution and ideal TopK relational filtering (p. 7–8, §3.3; formal definition is Definition 1 on p. 5 / p. 380).

## Complexity / theoretical claims
- Semantic Equivalence Proof (§3.3, p. 7–8 / pp. 382–383; formal property is Definition 1 on p. 5 / p. 380): Proves that for filtered queries $r_1 = \text{Filter}(\text{Limit}_K(\text{Sort}(R_1)))$, VBASE produces identical results to ideal TopK filtering ($r_1 = r_2$) while visiting the minimal required candidate count $R_2$ satisfying $\tilde{K} \times \sigma = K$ on-the-fly.
- No Formal Complexity Formula: The paper presents no asymptotic runtime theorems or closed-form cost bounds parameterized by selectivity $\sigma$ (`purely empirical systems and algebraic query rewrite analysis`).
- selectivity_cost_model: no; notes the relation $K' \times \sigma = K$ in query plan formulation (p. 8, §3.3), but provides no closed-form analytical cost or search complexity model as a function of filter selectivity $\sigma$ (p. 1-16).

## Filter type and selectivity regime handled (p.)
- Filter type: Arbitrary relational SQL predicates, including numerical ranges, categorical equality, multi-attribute conjunctions/disjunctions, and relational join predicates (p. 3-4, 8-10, §2, §4.2).
- Selectivity regime handled: Broad selectivity from highly selective ($0.01\%$) to dense ($>50\%$), adapting traversal depth dynamically on-the-fly (p. 8, 12-14, §3.3, §6.3).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- Evaluated over multiple underlying vector indexes: HNSW, DiskANN/Vamana, and SPANN, integrated into PostgreSQL (p. 2, 5, 8, 11, §1, §3.2, §6.1).

## Datasets, baselines, metrics (Table N)
- Datasets (§6.1, p. 11, Table 2):
  - SIFT1B (subset 100M 128-d vectors).
  - Deep1B (subset 100M 96-d vectors).
  - SpaceV (100M 100-d vectors).
  - Multi-attribute e-commerce dataset (10M 64-d vectors with price and category scalar columns).
- Baselines (§6.1, p. 11-12): pgvector (PostgreSQL HNSW/IVFFlat extension), Milvus v2.2 (in-filtering and trial-and-error TopK), and native PostgreSQL sequential scan.
- Metrics (§6.1, p. 11-12): Query latency (ms), throughput (QPS), and Recall@10.

## Key results (numbers exactly as reported, with Table/Fig locator)
- Latency on Filtered Queries (Figure 10, p. 12-13, §6.3):
  - On SIFT100M with scalar attribute filtering, VBASE achieves $2.5\times\text{--}4.1\times$ lower latency than pgvector and $1.8\times\text{--}3.2\times$ lower latency than Milvus trial-and-error across selectivities from $0.1\%$ to $10\%$.
  - On Vector Join queries (Figure 12, p. 13-14, §6.4), VBASE outperforms PostgreSQL table join by up to $37.4\times$ by pruning distance computations via early iterator termination.

## Limitations (author-stated vs. observed)
- Author-stated (p. 7, 10, 15, §3.2, §4.3, §7): Relaxed monotonicity parameters (window size $w$, queue capacity $E$, distance threshold $\delta$) are configured empirically; suboptimal thresholds can terminate traversal prematurely on highly clustered or non-uniform metrics.
- Observed: Focuses on relational engine pipelining and iterator abstractions; does not embed probabilistic filters into the vector index graph structure itself.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
- Demonstrates the practical failure of fixed TopK interfaces and pre/post filtering in vector-relational databases.
- Highlights why stopping criteria must adapt to selectivity on-the-fly, connecting directly to our dynamic traversal cost model.
Novelty check: no; VBASE implements a relational iterator interface in PostgreSQL where scalar filters operate outside or after vector index scan steps, rather than evaluating probabilistic membership filters during graph traversal (p. 5, 8-10, §3-§4).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Relaxed monotonicity termination relies on deterministic sequential traversal of the vector index (p. 8, footnote 1), which may not hold under multi-threaded parallel graph traversals.

## Useful references to snowball (bibkeys or titles from its reference list)
- malkov2020hnsw (Malkov & Yashunin, 2020: Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 17)
- subramanya2019diskann (Subramanya et al., 2019: DiskANN: Fast accurate billion-point nearest neighbor search on a single node) (p. 17)
- chen2021spann (Chen et al., 2021: SPANN: Highly-efficient billion-scale approximate nearest neighbor search) (p. 16)
- wang2021milvus (Wang et al., 2021: Milvus: A purpose-built vector data management system) (p. 17)
