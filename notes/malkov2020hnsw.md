# malkov2020hnsw — Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs
Authors / Year / Venue / DOI: Yu A. Malkov, D. A. Yashunin / 2020 / IEEE Transactions on Pattern Analysis and Machine Intelligence / 10.1109/TPAMI.2018.2889473
Status: PUB
PDF: papers/malkov2020hnsw.pdf   Read fully: yes

## Problem addressed (p.)
Approximate $K$-nearest neighbor search ($K$-ANNS) in high-dimensional and general metric spaces, resolving the power-law search routing scaling and severe performance degradation on clustered or low-dimensional data exhibited by flat Navigable Small World (NSW) proximity graphs (p. 1–2).

## Method (core idea in ≤5 sentences) (p.)
Hierarchical NSW (HNSW) constructs an incremental multi-layer graph index where stored elements are assigned to a maximum layer selected randomly from an exponentially decaying geometric distribution, generalizing 1D skip lists to metric proximity graphs (p. 1, 3). The upper layers contain sparser graphs with long-range links for coarse "zoom-in" greedy navigation, while lower layers contain denser short-range links for fine-grained convergence (p. 3). During index construction, an edge-selection heuristic connects elements in diverse directions to approximate relative neighborhood graphs, maintaining connectivity across isolated clusters (p. 3–4, 5–6). Query search initiates at the top layer with candidate queue size $ef=1$ until reaching a local minimum, descending layer by layer until layer 0, where beam search with priority queue size $ef$ executes (p. 4–5).

## Complexity / theoretical claims
- Statement, assumptions, theorem number, page:
  - Search complexity: Under the assumption that exact Delaunay graphs are formed on every layer and the average node degree is bounded by constant $C$, the expected number of greedy steps in each layer is bounded by $S = 1 / (1 - \exp(-m_L))$ independent of dataset size $N$ (§4.2.1, p. 7). Since the expected maximum layer scales as $O(\log N)$, total search complexity scales as $O(\log N)$ (§4.2.1, p. 7).
  - Practical heuristic scaling: In practical HNSW with bounded degree $M$, the authors claim empirical backtracking complexity on layer 0 saturates with dataset size, acting as an additive term that does not alter logarithmic scaling (§4.2.1, p. 7).
  - Construction complexity: Scales as $O(N \log N)$ for low-dimensional data, because each element insertion executes searches across an expected constant number of layers $1 + m_L$ (§4.2.2, p. 7).
  - Memory cost: Average memory consumption per element is $(M_{\max 0} + m_L \cdot M_{\max}) \cdot \text{bytes\_per\_link}$, yielding approximately 60–450 bytes per object for typical $M \in [6, 48]$ (§4.2.3, p. 8).
  - Theorem number: none stated (asymptotic derivations based on Delaunay assumptions and empirical validations) (§4.2.1–4.2.2, p. 7).

## Filter type and selectivity regime handled (p.)
not stated (pure vector/metric similarity search without metadata predicate filtering or selectivity regimes) (p. 1–11).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
HNSW (multi-layer hierarchical proximity graph) (p. 1, 3–5).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 1, Table 2, p. 9; Table 3, p. 10):
  - Vector datasets (Table 1, p. 9): SIFT (1M, 128d, $L_2$), GloVe (1.2M, 100d, cosine), CoPhIR (2M, 272d, $L_2$), Random hypercube (30M, 4d, $L_2$; 10M, 4d; 100k, 1024d), DEEP (1M, 96d, $L_2$), MNIST (60k, 784d, $L_2$), SIFT subset of 1B (200M, 128d, $L_2$, Table 3, p. 10).
  - Non-metric datasets (Table 2, p. 9): Wiki-sparse (4M, sparse cosine), Wiki-8 (2M, JS divergence), Wiki-128 (2M, JS divergence), ImageNet (1M, SQFD distance), DNA (1M, Levenshtein edit distance).
- Baselines (§5.1–5.4, p. 8–10): Flat NSW (sw-graph in nmslib), FLANN 1.8.4, Annoy (2016-02-02), VP-tree, FALCONN 1.2 (LSH), NAPP permutation index, brute-force filtering, NNDescent-produced proximity graphs, Faiss (OPQ64+IMI2x14+PQ64 and OPQ32+IMI2x14+PQ32).
- Metrics (§1, p. 1; §5, p. 8–10): Recall (ratio of found true nearest neighbors to $K$), raw query time (ms), distance computations per query, build time (minutes/hours), peak memory (GB).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Outperforms baseline NSW by nearly three orders of magnitude in distance computations on Wiki-8 with JS-divergence (§5.3, p. 10; Fig. 14, p. 10).
- For 10M SIFT dataset with $efConstruction=100$, creates high-quality index in 3 minutes on a 4X 10-core Xeon E5-4650 v2 server (§4.1, p. 7; Fig. 10, p. 7).
- On 10M 4D random vectors at recall 0.9 (1-NN), query time is under 0.02 ms using autoselected $m_L = 1/\ln(M)$ (Fig. 3, p. 6).
- On 200M SIFT, HNSW achieves higher recall and faster query times than Faiss: HNSW builds in 5.6 hours (efConstruction=500) or 42 minutes (efConstruction=40) using 64 GB peak memory, while Faiss requires 11–12 hours with 23.5–30 GB peak memory (Table 3, p. 10; Fig. 15, p. 10).

## Limitations (author-stated vs. observed)
- Author-stated: Exact Delaunay graph assumption breaks down in high dimensions because average Delaunay vertex degree scales exponentially with dimensionality, so formal logarithmic scalability proof does not strictly generalize to high dimensions (§4.2.1, p. 7); index consumes 60–450 bytes per object, which is substantially higher memory than quantized compression methods (§4.2.3, p. 8; §5.4, p. 10); centralized entry point at the top layer creates a congestion bottleneck that hinders distributed sharding (§6, p. 11); native index deletions and updates are not supported (§6, p. 11).
- Observed: Pure metric similarity search; does not handle predicate constraints or metadata filtering during traversal.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
HNSW provides the core multi-layer graph architecture and greedy search procedure (`SEARCH-LAYER`) that our project aims to augment by embedding probabilistic membership filters into traversal. The trade-offs established between candidate list size $ef$, layer descent, and degree $M$ define the structural cost baseline for our filter-augmented traversal and selectivity crossover model.
Novelty check: Novelty check: no (p. 1–11; purely metric vector similarity search without metadata predicates or probabilistic membership filters).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Theoretical search complexity of $O(\log N)$ in §4.2.1 (p. 7) relies on the existence of an exact Delaunay graph with bounded degree $C$, but in high dimensions Delaunay degree grows exponentially ($2^{\Omega(d)}$), leaving high-dimensional logarithmic scaling dependent solely on empirical observations.

## Useful references to snowball (bibkeys or titles from its reference list)
- Malkov et al. (2014) [26]: Approximate nearest neighbor algorithm based on navigable small world graphs (Information Systems)
- Arya & Mount (1993) [18]: Approximate Nearest Neighbor Queries in Fixed Dimensions (SODA)
- Harwood & Drummond (2016) [47]: FANNG: fast approximate nearest neighbour graphs (CVPR)
- Dong et al. (2011) [29]: Efficient k-nearest neighbor graph construction for generic similarity measures (WWW)
- Pugh (1990) [27]: Skip lists: a probabilistic alternative to balanced trees (CACM)
