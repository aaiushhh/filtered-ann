# Gate 1 — Batch Report 1 (Group D: Filtered ANN)

## 1. Summary of Completed Papers
Batch 1 evaluated 5 open-access papers in Group D (Filtered ANN):

| bibkey | Full Title | Status | Verbatim Quotes Verified |
|---|---|---|---|
| `curator2026` | Curator: Efficient Vector Search with Low-Selectivity Filters | OK | 2 / 2 PASS |
| `filteraware2025` | Learning Filter-Aware Distance Metrics for Approximate Nearest Neighbor Search with Multiple Filters | OK | 2 / 2 PASS |
| `filtered2026system` | Filtered ANN Search in Vector Databases: A Performance and Architecture Study | OK | 2 / 2 PASS |
| `rangefilters2026` | Approximate Nearest Neighbor Search with Graph Range Filters | OK | 2 / 2 PASS |
| `routing2026query` | Query-aware Routing for Filtered Approximate Nearest Neighbors Search | OK | 3 / 3 PASS |

All 5 reading notes have been generated in `notes/<bibkey>.md` following the mandatory 6-section template.

## 2. Blocked Papers
- **None** in Batch 1. All 5 papers had full text available in `papers/*.txt`.

## 3. Programmatic Quote-Check Failures
- **Zero failures** across all 5 notes.
- Every quoted string was verified programmatically against `papers/<bibkey>.txt` using single-space whitespace normalization via `tools/verify_quotes.py`.
- Exact quote details:
  - `curator2026`:
    - (p. 2): "the sub-graph of qualifying vectors becomes increasingly sparse and disconnected." (10 words) — PASS
    - (p. 1): "approximate nearest neighbor search (ANNS) queries are often combined with filters on labels such as dates and price ranges." (19 words) — PASS
  - `filteraware2025`:
    - (p. 2): "learns the optimal trade-off between vector distance and filter match directly from the data, rather than relying on fixed penalties." (20 words) — PASS
    - (p. 2): "These learned weights guide both the search process and index construction, leading to graph structures that more effectively capture the underlying filter" (22 words) — PASS
  - `filtered2026system`:
    - (p. 1): "algorithmic adaptations within the engine often override raw index performance." (10 words) — PASS
    - (p. 1): "partition-based indexes (IVFFlat) outperform graph-based indexes (HNSW) for low-selectivity queries." (10 words) — PASS
  - `rangefilters2026`:
    - (p. 2): "DLH compresses extensive labeling sets into fixed-size bit vectors using Bloom filters, thereby enabling approximate set intersections with bounded error rates." (21 words) — PASS
    - (p. 1): "Large labeling sets are further compressed into Bloom filters to improve query efficiency in DLH." (15 words) — PASS
  - `routing2026query`:
    - (p. 1): "A lightweight ML model predicts each candidate method’s recall on the query" (12 words) — PASS
    - (p. 1): "Our ablation study narrows 22 candidate features to a minimal set of three" (13 words) — PASS
    - (p. 8): "We report recall@10 and average QPS over 16 threads as the primary metrics;" (13 words) — PASS

## 4. Newly Discovered Literature Gaps (Recorded in `gaps.md`)
Cross-referencing the citation graphs of these 5 papers revealed important candidate systems for future snowballing:
1. `shi2025benchmark`: Shi, Cai, Zheng. "Filtered Approximate Nearest Neighbor Search on High-Dimensional Data: A Benchmark" (arXiv:2509.07789, 2025) — benchmark covering Pre-filter, Post-filter, UNG, ACORN, Vamana.
2. `li2025sieve`: Li, Huang, Ding, Park, Chen. "SIEVE: A Workload-Adaptive Sub-Index Framework for Filtered Vector Search" (SIGMOD 2025) — workload-adaptive sub-index selection.
3. `gan2026efficient`: Gan & Wang. "Efficient Filtered-ANN via Learning-based Execution Planning" (2026) — per-query learned execution planner between pre-filtering and post-filtering; highly relevant to crossover selectivity analysis ($\sigma^*$).
4. `zuo2023arkgraph`: Zuo & Deng. "ARKGraph: All-Range Approximate K-Nearest-Neighbor Graph" (PVLDB 16(11): 3034-3047, 2023) — foundation for proximity graph range filtering.

## 5. Synthesis Progress
- Created `observations.md` with one-line takeaways and key supporting references for all 5 papers.
- Updated `gaps.md` with discovered literature and context.
- Appended all actions to `LOG.md`.

## 6. Next Batch (Batch 2)
Pending your approval, Batch 2 will process the next 5 open-access papers in order (remaining Group D paper, followed by Group C graph ANN papers):
1. `[D] survey2025filtered`: Survey of Filtered Approximate Nearest Neighbor Search over Vector-Scalar Hybrid Data
2. `[C] beam2025distance`: Distance Adaptive Beam Search for Provably Accurate Graph-Based Nearest Neighbor Search
3. `[C] chen2021spann`: SPANN: Highly-efficient Billion-scale Approximate Nearest Neighbor Search
4. `[C] malkov2020hnsw`: Efficient and Robust Approximate Nearest Neighbors Using Hierarchical Navigable Small World Graphs
5. `[C] manohar2025range`: Range Retrieval with Graph-Based Indices
