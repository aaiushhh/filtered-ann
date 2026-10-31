# prokhorenkova2020graph — Graph-based Nearest Neighbor Search: From Practice to Theory
Authors / Year / Venue / DOI: Liudmila Prokhorenkova, Aleksandr Shekhovtsov / 2020 / Proceedings of the 37th International Conference on Machine Learning (ICML 2020), PMLR 119:7803-7813 / arXiv:1907.00845
Status: PUB (ICML 2020, PMLR 119)
PDF: papers/prokhorenkova2020graph.pdf   Read fully: main body read in full (pp. 1–8); supplementary proofs (pp. 12–31) surveyed for formal mechanics, not read line-by-line.

## Problem addressed (p.)
Theoretical foundations and complexity guarantees of graph-based approximate nearest neighbor search (NNS) algorithms, specifically analyzing greedy search, long-range links, and beam search on proximity graphs for points uniformly distributed on a $d$-dimensional sphere $S^d$ (p. 1-3, §1-§3). Prior works established state-of-the-art empirical performance (e.g., HNSW, NSW) but lacked rigorous mathematical performance bounds on query path length, convergence, and degree trade-offs.

## Method (core idea in ≤5 sentences) (p.)
The paper analyzes greedy routing on proximity graphs under dense ($d = \log(n)/\omega, \omega \to \infty$) and sparse ($d = \omega \log(n), \omega \to \infty$) regimes on $S^d$ (p. 1-4, §1-§4.2). For plain nearest-neighbor graphs in the dense regime, greedy search requires $\Theta(n^{1/d})$ steps, each step checking $\Theta(d^{1/2} M^d)$ neighbors (p. 4, §4.2, Theorem 1). In the sparse regime, it proves that greedy search converges in at most two steps, solving $c, R$-ANN with time $\Theta(n^{1-M+o(1)})$ and space $\Theta(n^{2-M+o(1)})$ (p. 5, §4.2, Theorem 2). To accelerate dense graphs without dimensionality dependence, it proves that augmenting nodes with Kleinberg-style long-range links reduces the number of steps to $O(\log^2 n)$ with one link (Theorem 3) and $O(\log n)$ with $\Theta(\log n)$ links (Corollary 2), with a rank-based sampling heuristic avoiding explicit dimension knowledge (p. 5-6, §4.3). Finally, it provides the first theoretical analysis of beam search in graph NNS, proving that expanding $C L^d \sqrt{d}$ candidates circumvents local minima traps and reduces the required graph degree to $O(L^d M^d)$ (p. 6, §4.4, Theorem 4).

## Complexity / theoretical claims
- Dense Regime Greedy Search (Theorem 1, p. 4, §4.2): Assume $d \gg \log \log n$ and constant $c \ge 1$. Let $M$ be a constant such that $M > \sqrt{\frac{4c^2}{3c^2 - 1}}$. Graph $G(M)$ connects $x_i, x_j$ iff $\rho(x_i, x_j) \le \arcsin(M n^{-1/d})$. With probability $1 - o(1)$, $G(M)$-based NNS solves $c, R$-ANN for any $R$ (or exact NN if $c=1$ with $M > \sqrt{2}$). Time complexity is $\Theta(d^{1/2} n^{1/d} M^d) = n^{o(1)}$; space complexity is $\Theta(n d^{-1/2} M^d \log n) = n^{1+o(1)}$. Step count is $\Theta(n^{1/d})$; per-step complexity is $\Theta(d^{1/2} M^d)$.
- Sparse Regime Greedy Search (Theorem 2, p. 5, §4.2): For any $c > 1$, let $\alpha_c = \cos(\frac{\pi}{2c})$ and $M < \frac{\alpha_c^2}{\alpha_c^2 + 1}$. Graph $G(M)$ connects $x_i, x_j$ iff $\rho(x_i, x_j) \le \arccos(\sqrt{\frac{2M \ln n}{d}})$. With probability $1 - o(1)$, $G(M)$-based NNS solves $c, R$-ANN in at most 2 steps; time complexity is $\Theta(n^{1 - M + o(1)})$ and space complexity is $\Theta(n^{2 - M + o(1)})$.
- Corollary 1 (Euclidean Sparse Regime, p. 5, §4.2): Holds for Euclidean distance with $\alpha_c = 1 - 1/c^2$, yielding time complexity $n^\phi$ and space complexity $n^{1+\phi}$ where $\phi \approx \frac{1}{(1 - 1/c^2)^2 + 1}$.
- Long-Range Shortcuts (Theorem 3, p. 5, §4.3): Under the conditions of Theorem 1, sampling one long-range edge per node according to $P(u \to v) \propto \rho(u, v)^{-d}$ reduces the number of search steps to $O(\log^2 n)$ with probability $1 - o(1)$.
- Multiple Long-Range Shortcuts (Corollary 2, p. 6, §4.3): If for each node $\Theta(\log n)$ long-range edges are added, the number of steps becomes $O(\log n)$, yielding time complexity $O(d^{1/2} \log n \cdot M^d)$ while asymptotic space complexity remains unchanged compared to Theorem 1.
- Dimension-Free Rank-Based Sampling (Lemma 1, p. 6, §4.3): Sampling according to rank $P(k\text{-th neighbor}) \propto 1/k$ with pre-sampling of $n^\phi$ candidates ($0 < \phi < 1$) preserves link probabilities within $\Theta(1/\phi)$ for $k > n^{1-\phi}$ while reducing construction time to $\Theta(n^{1+\phi}(d + \log n^\phi))$.
- Beam Search Complexity (Theorem 4, p. 6, §4.4): Let $M > 1, L > 1$ such that $M^2(1 - \frac{M^2}{4L^2}) > 1$ and $\log \log n \ll d \ll \log n$. Using beam search with $C L^d \sqrt{d}$ candidates and $\Theta(\log n)$ long-range edges, $G(M)$-based NNS solves exact NN with probability $1 - o(1)$ in time $O(L^d M^d)$.
- Optimal Beam Search Trade-Off (Corollary 3, p. 6, §4.4): Setting $M = \sqrt{3/2}$ and $L > \sqrt{9/8}$ reduces the dominant time complexity term to $(27/16)^{d/2}$, which is strictly less than $2^{d/2}$ from Theorem 1.
- selectivity_cost_model: not stated; the paper investigates unconstrained metric nearest neighbor search and provides no cost model or complexity formulation as a function of predicate selectivity (p. 1-8).

## Filter type and selectivity regime handled (p.)
- Filter type: None (unconstrained ANN search over continuous vectors on $S^d$) (p. 1, §1).
- Selectivity regime handled: Not applicable / 100% selectivity (unfiltered) (p. 1, 3, §1, §3).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- Plain $k$-NN graphs, Kleinberg-augmented random graphs, and HNSW (Hierarchical Navigable Small World graphs) (p. 2-3, 7-8, §2, §4, §5).

## Datasets, baselines, metrics (Table N)
- Datasets (§5, p. 7-8, Table 1): Synthetic uniform spherical vectors in $\mathbb{R}^{d+1}$ ($d \in [2, 16], n = 10^6$); SIFT (1M 128-d, Euclidean); GIST (1M 960-d, Euclidean); GloVe (1.2M 300-d, Angular); DEEP (1M 96-d, Euclidean).
- Baselines (§5, p. 7-8): Plain $k$-NN graph greedy search, $k$-NN + KL (Kleinberg shortcuts), $k$-NN + KL + LLF (long links first), $k$-NN + beam search, and HNSW.
- Metrics (§5, p. 7-8, Table 2, Figure 2): Number of distance computations vs. Error = $1 - \text{Recall}@1$; average step count vs. degree.

## Key results (numbers exactly as reported, with Table/Fig locator)
- On synthetic data ($n=10^6, d=2$), greedy search requires 200 steps with degree 20 to achieve 0.998 Recall@1; for $d=16$, it requires 4 steps but degree 2000 for 0.99 Recall@1 (Table 2, p. 7, §5.1).
- On synthetic data ($d=16$), using beam search with beam size 100 reduces required degree from 2000 down to 20 while achieving 0.995 Recall@1 in 106 steps (Table 2, p. 7, §5.1).
- On SIFT and DEEP, $k$-NN + beam + KL + LLF achieves competitive query performance matching or approaching HNSW (Figure 3, p. 8, §5.3).

## Limitations (author-stated vs. observed)
- Author-stated (p. 2-3, 7, §1, §5.3): Theoretical step bounds assume uniform data distribution over the unit sphere $S^d$; empirical real-world datasets exhibit non-uniform clustering and intrinsic low dimensionality where neighbor diversification heuristics are required.
- Observed: Analyzes unconstrained vector search only; contains no mechanisms for metadata predicates, hybrid graph traversals, or probabilistic filtering.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
- Provides fundamental theoretical baseline establishing that standard greedy traversal over navigable graphs requires $O(\log^2 n)$ hops.
- Serves as the mathematical anchor for our theoretical traversal cost model, proving that graph navigation step bounds depend directly on neighbor density and coverage.
- Demonstrates how adding non-local edges (analogous to false-positive bridge nodes) exponentially reduces search diameter across sparse regions.
Novelty check: no; evaluates pure metric vector similarity search without membership filters or metadata predicate constraints during traversal (p. 1-8).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Theoretical claims rely on uniform spherical density, whereas Section 5 acknowledges real feature embeddings have severe cluster skew requiring empirical heuristic uniformization (p. 3, 7-8).

## Useful references to snowball (bibkeys or titles from its reference list)
- malkov2020hnsw (Malkov & Yashunin, 2018: Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 8)
- fu2019nsg (Fu et al., 2019: Fast approximate nearest neighbor search with the navigating spreading-out graph) (p. 8)
- Kleinberg, J. (2000). Navigation in a small world. Nature 406(6798):845. (p. 8)
