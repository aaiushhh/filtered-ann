# beam2025distance — Distance Adaptive Beam Search for Provably Accurate Graph-Based Nearest Neighbor Search
Authors / Year / Venue / DOI: Al-Jazzazi, Yousef, Diwan, Haya, Gou, Jinrui, Musco, Cameron, Musco, Christopher, Suel, Torsten / 2025 / NeurIPS 2025 (Advances in Neural Information Processing Systems 38) / 10.52202/085713-3346
Status: PUB
PDF: papers/beam2025distance.pdf   Read fully: yes

## Problem addressed (p.)
Addressing the theory-practice gap in graph-based approximate nearest neighbor search (ANNS); standard beam search parameterized by a fixed beam width $b$ lacks formal approximation guarantees on navigable graphs and enforces a rigid stopping condition that cannot adapt to variable query difficulty (p. 1–3).

## Method (core idea in ≤5 sentences) (p.)
The paper decouples beam search into candidate traversal ordering and termination criteria, replacing the fixed beam-width stopping condition with a distance-adaptive termination rule (p. 2, 4–5). The proposed Adaptive Beam Search terminates traversal when candidate node $x$ selected for expansion satisfies $d(q, x) \ge (1 + \gamma) \cdot \max_{j \in B} d(q, j)$, where $B$ is the current set of $k$ closest discovered items and $\gamma > 0$ is a user-controlled slack parameter (p. 5). This criterion dynamically terminates early on easy queries while naturally expanding more candidate nodes on difficult queries with dense false nearest neighbors (p. 5). The modification integrates into existing graph ANNS libraries with minimal lines of code (p. 2, 8).

## Complexity / theoretical claims
- Statement, assumptions, theorem number, page:
  - Navigable Graph Definition (Definition 1, p. 3): A directed graph $G=(V, E)$ is navigable under metric $d$ if for all $x, y \in V$ with $d(x,y) > 0$, there exists $z \in N_G(x)$ with $d(z, y) < d(x, y)$.
  - Approximation Guarantee (Theorem 1, p. 6): Suppose $d$ is a metric on $\mathcal{X}$ and $G$ is navigable under $d$. For any query $q \in \mathcal{X}$, Adaptive Beam Search with parameter $0 < \gamma \le 2$ returns a set $B$ of $k$ points such that for all $v \in \{1, \dots, n\} \setminus B$, $d(q, v) \ge \frac{\gamma}{2} \max_{j \in B} d(q, j)$. When $\gamma = 2$, it provably solves the exact $k$-NN problem; for smaller $\gamma$, it guarantees a $2/\gamma$ approximation factor (§4, p. 6–7).
  - Impossibility for Standard Beam Search (Claim 2, p. 6; Appendix A.2): Standard beam search with fixed beam width $b \le n-3$ fails to solve approximate nearest neighbor search on navigable graphs for any finite approximation factor.
  - Worst-case runtime complexity: none stated (the authors note the result links accuracy to navigability but falls short of proving worst-case runtime bounds) (§4, p. 6).

## Filter type and selectivity regime handled (p.)
not stated (pure metric vector similarity search without metadata predicate filtering or selectivity constraints) (p. 1–10).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Navigable graphs (constructed via Diwan et al. 2024 with degree $O(\sqrt{n \log n})$ and pruned) and heuristic proximity graphs: HNSW, Vamana, NSG, EFANNA (p. 1, 8).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 1, p. 8): MNIST (60K, 784d, $L_2$; 50K for navigable graphs), SIFT1M (1M, 128d, $L_2$; 100K for navigable graphs), DEEP96 (1M, 96d, $L_2$; 100K for navigable graphs), DEEP256 (1M, 256d, $L_2$), GloVe (1M, 200d, $L_2$), GIST (1M, 960d, $L_2$).
- Baselines (§5.1, p. 8; Fig. 3–4): Standard beam search (beam width $b \ge k$), Adaptive Beam Search V2 ($d(q, x) \ge d_1 + \gamma d_k$), tested across HNSW, Vamana, NSG, EFANNA, and pruned navigable graphs.
- Metrics (§5.1, p. 8): Recall (average fraction of true $k$ nearest neighbors found), average number of distance computations per query.

## Key results (numbers exactly as reported, with Table/Fig locator)
- Adaptive Beam Search yields a 10–50% reduction in distance computations required for a given recall level compared to standard beam search across various datasets and graph constructions (§1, p. 2; §5.1, p. 8).
- On navigable graphs across SIFT1M, DEEP96, and MNIST for $k=1$ and $k=10$, Adaptive Beam Search achieves up to 30–40% decrease in distance computations for equivalent recall (Fig. 3, p. 9; §5.2, p. 9).
- On heuristic graphs (NSG, Vamana, EFANNA, HNSW) with $k=10$, Adaptive Beam Search consistently outperforms standard beam search across all datasets, achieving more than a $2\times$ reduction in distance computations on MNIST (§5.2, p. 9; Fig. 4, p. 10).

## Limitations (author-stated vs. observed)
- Author-stated: Theorem 1 guarantees solution quality but does not provide worst-case running time bounds (§4, p. 6); constructing truly sparse navigable graphs is computationally expensive, restricting navigable experiments to subsampled datasets of $\le 100K$ points (§5.1, p. 8); heuristic variant Adaptive Beam Search V2 underperforms significantly when $d_1 \ll d_k$ due to premature termination (§5.1, p. 8; §5.2, p. 9).
- Observed: Pure metric similarity search; does not incorporate metadata attributes or membership filtering into the traversal or stopping rule.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
This paper provides the foundational theoretical proof connecting graph navigability to distance-adaptive beam search stopping conditions, offering mathematical tools directly applicable to bounding traversal depth in filter-augmented HNSW. Its decoupled traversal-and-termination framework suggests that probabilistic membership filters could be cleanly integrated into candidate expansion priority queues alongside distance slack thresholds.
Novelty check: Novelty check: no (p. 1–10; pure metric ANN search without predicate evaluations or probabilistic membership filter data structures).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Table 1 (p. 8) lists dataset DEEP96 (96 dimensions), whereas Figure 3 and Figure 4 captions and discussions refer to DEEP256 (256 dimensions) for heuristic graphs; the text does not clarify whether DEEP96 was used exclusively for navigable graphs or if both variants were evaluated interchangeably.

## Useful references to snowball (bibkeys or titles from its reference list)
- Diwan et al. (2024) [12]: Navigable graphs for high-dimensional nearest neighbor search: Constructions and limits (NeurIPS)
- Indyk & Xu (2023) [19]: Worst-case performance of popular approximate nearest neighbor search implementations: Guarantees and limitations (NeurIPS)
- Gollapudi et al. (2023) [17]: Filtered-DiskANN: Graph algorithms for approximate nearest neighbor search with filters (WWW)
- Manohar et al. (2025) [39]: Range retrieval with graph-based indices (arXiv:2502.13245)
