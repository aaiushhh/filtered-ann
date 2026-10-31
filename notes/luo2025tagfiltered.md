# luo2025tagfiltered — Tag-Filtered Approximate Nearest Neighbor Search
Authors / Year / Venue / DOI: Jiarui Luo, Miao Qiao, Chaoji Zuo, Dong Deng / 2025 / 2025 IEEE 41st International Conference on Data Engineering (ICDE 2025) / 10.1109/icde65448.2025.00272
Status: PUB (DOI: 10.1109/icde65448.2025.00272)
PDF: papers/luo2025tagfiltered.pdf   Read fully: yes

## Problem addressed (p.)
Tag-Filtered Approximate Nearest Neighbor Search (TFANNS), where high-dimensional vectors are associated with arbitrary sets of discrete categorical tags and queries require retrieving vectors containing all query tags ($t(q) \subseteq t(p)$) (p. 1-2, §I-II). State-of-the-art graph methods like Filtered-DiskANN suffer low recall on low-to-medium frequency tags because small tag subgraphs suffer connectivity breakdown, while separate pre-filtering indices lead to an excessive memory footprint (p. 1, §I).

## Method (core idea in ≤5 sentences) (p.)
Proposes a tag-frequency-aware proximity graph indexing framework with three graph construction strategies: Local Method, Global Method, and Packing Strategy (p. 1-2, §I; p. 3-7, §IV-V). The Local Method allocates node out-degrees across associated tags using a logarithmic frequency priority scheme to prevent frequent tags from monopolizing edges (p. 3, §IV.A; Algorithm 2). The Global Method partitions tags into high-frequency and low-frequency sets based on a threshold $\theta$, building independent HNSW graphs for frequent tags and routing rare tags to inverted lists (p. 5-6, §IV.B; Algorithm 5). The Packing Strategy merges related low-frequency tags into packed super-nodes to preserve edge budget and structural navigation efficiency (p. 6-7, §V; Algorithm 7). At query time, Algorithm 3 executes greedy search starting from random entry vectors of the rarest query tag and checks full tag set containment ($t(q) \subseteq t(r)$) during neighbor expansion (p. 4, §III.B).

## Complexity / theoretical claims
- Lemma 1 (Space Complexity, p. 6): For the Global Method graph $G$, the total edge allocation across all tags $t \in T$ with frequency $f(t) \ge \theta$ satisfies $\sum_{t \in T, f(t) \ge \theta} f(t) m(t) \le M_0 \min\{f, 2n\}$, establishing an overall space complexity of $O(n M_0)$.

## Filter type and selectivity regime handled (p.)
Multi-tag discrete categorical containment filters ($t(q) \subseteq t(p)$) (p. 2, §II). Handles wide tag frequency and selectivity regimes ranging from extremely low selectivity (1st percentile $\sigma \approx 10^{-7}$ on YFCC) up to high frequency (50th–100th percentiles $\sigma \approx 0.01$ to $0.70$) (Table II, p. 8; §VI.A).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Tag-aware proximity graphs based on HNSW / NSW, augmented with per-tag degree allocation and super-node packing (p. 2-7, §III-V).

## Datasets, baselines, metrics (Table N)
- Datasets (Table I & Table II, p. 8): SIFT Zipf Attr (1M, 128d), GIST Zipf Attr (1M, 960d), SIFT Uniform Attr (1M, 128d), GIST Uniform Attr (1M, 960d), SIFT Zipf Tag (1M, 128d), Paper Uniform Attr (2M, 200d), YFCC (10M, 192d, 200k tags), YouTube-Audio (1M, 128d), YouTube-Video (1M, 1024d), LAION (960k, 768d).
- Baselines (p. 8-9, §VI.A): Post-filter IVF, Post-filter HNSW, Faiss-IVF, ACORN, StitchedVamana, FilteredVamana, NHQ.
- Metrics (p. 8, §VI.A): Recall@k, Queries per second (QPS), Index Size (GB, Table III, p. 11), Index Construction Time (s, Table III, p. 11).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Packing Strategy achieves superior QPS across high-recall regimes on YFCC Single Filter, YouTube-Video, YouTube-Audio, and LAION (p. 11, Fig. 12).
- On YFCC (10M vectors), Packing Strategy index size is 8.60 GB with 7,980s build time, compared to 7.46 GB / 8,777s for StitchedVamana (Table III, p. 11).
- On SIFT Zipf Tag, Packing Strategy scales effectively up to 50M vectors while maintaining $>90\%$ recall and high QPS (p. 11, Fig. 11).
- Outperforms FilteredVamana and ACORN on datasets with heavy-tailed Zipf tag distributions by allocating sufficient routing edges to rare tags (p. 9-11, §VI.B-C; Fig. 12, p. 11).

## Limitations (author-stated vs. observed)
- Author-stated: Packing Strategy requires determining the optimal frequency threshold $\theta$ and super-node clustering hyperparameters, which depend on tag frequency distribution (p. 6-7, §V; p. 10, §VI.C).
- Author-stated: When query tags have extremely low co-occurrence in base data, fallback to sequential scan is invoked when estimated candidates fall below threshold $\theta$ (p. 4, §III.B, Algorithm 3).
- Observed: Tag-aware degree allocation substantially increases graph index complexity compared to standard uniform HNSW graphs.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Serves as an essential ICDE 2025 baseline for multi-tag filtered ANN search under heavy-tailed label distributions. Directly addresses graph connectivity failure on low-selectivity tags through degree reallocation and super-node packing. Informs our project's graph traversal design by illustrating how in-traversal predicate checking interacts with tag frequency skews.
Novelty check: yes for metadata predicate checks during graph traversal (in Algorithm 3 SEARCH, candidate neighbors along rarest tag subgraphs are tested for tag containment $t(q) \subseteq t(r)$ during search expansion, p. 4, §III.B), but no probabilistic membership filter (Bloom, Cuckoo, Xor) is used (p. 3-7, §IV-V).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Table II lists YFCC 100th percentile base dataset tag selectivity as 1e-07 and 1st percentile as 0.339, which indicates the table header sorts tags in ascending order of selectivity rather than standard descending percentile convention (Table II, p. 8).

## Useful references to snowball (bibkeys or titles from its reference list)
- patel2024acorn (ACORN: Performant and predicate-agnostic search over vector embeddings and structured data) (p. 13)
- gollapudi2023filtereddiskann (Filtered-DiskANN: Graph algorithms for approximate nearest neighbor search with filters) (p. 12)
- malkov2020hnsw (Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 13)
- zuo2024serf (SeRF: Segment graph for range-filtering approximate nearest neighbor search) (p. 13)
