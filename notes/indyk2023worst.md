# indyk2023worst — Worst-case Performance of Popular Approximate Nearest Neighbor Search Implementations: Guarantees and Limitations
Authors / Year / Venue / DOI: Piotr Indyk, Haike Xu / 2023 / Advances in Neural Information Processing Systems 36 (NeurIPS 2023) / 10.52202/075280-2891 (arXiv:2310.19126)
Status: PUB (NeurIPS 2023)
PDF: papers/indyk2023worst.pdf   Read fully: yes

## Problem addressed (p.)
Worst-case theoretical guarantees and algorithmic limitations of popular proximity graph indexes (DiskANN/Vamana, HNSW, and NSG) (p. 1-3, §1). While prior theoretical analyses focused on average-case random data (e.g., uniform spherical distributions), this paper investigates worst-case performance under adversarial or clustered metric configurations with bounded doubling dimension.

## Method (core idea in ≤5 sentences) (p.)
The paper evaluates two regimes of graph-based approximate nearest neighbor search: provable guarantees under global pruning versus worst-case failure modes under heuristic approximations (p. 1-4, §1-§3). For DiskANN under "slow preprocessing" (where robust pruning is evaluated globally across all vertices with $U=V, R=n$), the authors prove that greedy search ($L=1$) guarantees an $(\frac{\alpha+1}{\alpha-1} + \epsilon)$-approximation ratio in $O(\log_\alpha \frac{\Delta(\alpha-1)}{\epsilon})$ steps on metric spaces with doubling dimension $d$ and aspect ratio $\Delta$ (p. 1, 4-5, §3, Theorem 3.4). They prove that this approximation ratio is tight by constructing a 2D instance under $l_1$ metric where greedy search scans $\ge n$ vertices before reaching an approximation ratio smaller than $\frac{\alpha+1}{\alpha-1}$ (p. 5-6, §3.5, Theorem 3.6). Furthermore, they prove a lower bound showing that greedy search must scan $\Omega(\log \Delta)$ or $\Omega(n)$ vertices on a 1D line with $\Delta = O(\alpha^n)$ (p. 5, §3.4, Theorem 3.5). Conversely, for the practical "fast preprocessing" variants of DiskANN, HNSW, and NSG, the authors construct explicit metric counterexamples where heuristic local edge selection traps greedy routing into long cycles, forcing linear query times ($\ge 0.1n$ distance evaluations) to find the nearest neighbors (p. 1, 6-8, §4).

## Complexity / theoretical claims
- Lemma 2.1 (Doubling dimension covering, p. 3, §2): For point set $P$ with doubling dimension $d$, any ball $B(p, r) \cap P$ can be covered by $m \le O(k^d)$ balls of diameter $< r/k$.
- Definition 3.1 ($\alpha$-shortcut reachability, p. 4, §3.2): Let $\alpha \ge 1$. A graph $G=(V, E)$ is $\alpha$-shortcut reachable from vertex $p$ if for any other vertex $q$, either $(p, q) \in E$, or $\exists p'$ s.t. $(p, p') \in E$ and $D(p', q) \cdot \alpha \le D(p, q)$. $G$ is $\alpha$-shortcut reachable if it is $\alpha$-shortcut reachable from any vertex $v \in V$.
- Lemma 3.2 (p. 4, §3.2): Connecting each vertex $p$ to the output of `RobustPruning(p, V, \alpha)` forms an $\alpha$-shortcut reachable graph.
- Lemma 3.3 (Sparsity / degree bound, p. 4, §3.2): For any vertex $p$, $|RobustPruning(p, V, \alpha)| \le O((4\alpha)^d \log \Delta)$, where $d$ is the doubling dimension and $\Delta = D_{max}/D_{min}$ is the aspect ratio of $P$.
- Theorem 3.4 (Provable Upper Bound for Slow-Preprocessing DiskANN, p. 5, §3.3): Let $G=(V, E)$ be an $\alpha$-shortcut reachable graph constructed using the slow preprocessing method. `GreedySearch(s, q, L=1)` starting from any vertex $s \in V$ and $L=1$ finds an $\left(\frac{\alpha+1}{\alpha-1} + \epsilon\right)$-approximate nearest neighbor in $O\left(\log_\alpha \frac{\Delta (\alpha-1)}{\epsilon}\right)$ steps.
- Theorem 3.5 (Hop Lower Bound on 1D Line, p. 5, §3.4): For any choice of $\alpha > 1$, there exists a set of $n = 2^k - 1$ points on a 1D line with aspect ratio $\Delta = O(\alpha^n)$, and a query $q$, such that after the slow preprocessing version of DiskANN, greedy search must scan at least $\Omega(\log \Delta)$ or $\Omega(n)$ vertices before reaching an $O(1)$-approximate nearest neighbor of $q$.
- Theorem 3.6 (Tight Approximation Lower Bound in 2D $l_1$, p. 6, §3.5): For any $\alpha > 1$, there exists a set of $n+2$ points in the 2D plane under $l_1$ distance where the slow preprocessing version of DiskANN will scan at least $n$ vertices before getting to a vertex with an approximation ratio smaller than $\frac{\alpha+1}{\alpha-1}$.
- Lemma 3.7 (Properties of Tight Instance, p. 6, §3.5): Formal structural properties of the 2D grid instance in Figure 1 proving that induced subgraph on $P$ is strongly connected and $(p, a) \notin E$, forcing greedy routing through $n$ points before reaching $a$.
- Section 4 Worst-Case Hardness (Empirical, p. 6-8, §4): Explicit families of 2D instances showing that heuristic fast preprocessing in DiskANN, HNSW, and NSG requires $\ge 0.1n$ steps to find any of the 5 true nearest neighbors.
- selectivity_cost_model: not stated; the paper investigates unconstrained metric graph ANN search and provides no cost model or complexity formulation as a function of filter selectivity (p. 1-17).

## Filter type and selectivity regime handled (p.)
- Filter type: None (unconstrained ANN search in metric spaces) (p. 1, 3, §1, §2).
- Selectivity regime handled: Not applicable / 100% selectivity (unfiltered) (p. 1-3, §1).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- DiskANN (Vamana graph with $\alpha$-robust pruning), HNSW (Hierarchical Navigable Small World), and NSG (Navigating Spreading-out Graph) (p. 1-4, 6-8, §1-§4).

## Datasets, baselines, metrics (Table N)
- Synthetic worst-case geometric datasets: 2D spiral point configurations, concentric circles, and multi-scale grid clusters in $\mathbb{R}^2$ ($n \in [10^3, 10^5]$) (p. 5-8, §4).
- Real-world benchmark: SIFT1M (1M 128-d vectors) (p. 8-9, §5).
- Baselines: DiskANN (slow and fast preprocessing), HNSW, NSG, and exact linear scan (p. 1-3, 6-8, §1, §4).
- Metrics: Query hop count, number of distance evaluations vs. Recall@5, maximum out-degree (p. 1, 6-9, §1, §4, §5).

## Key results (numbers exactly as reported, with Table/Fig locator)
- On worst-case 2D instances ($n=10^4$), DiskANN (fast) requires $>1000$ steps ($\ge 0.1n$) before encountering any of the 5 true nearest neighbors (p. 1, 6-7, §1, §4, Figure 2).
- On SIFT1M, global robust pruning yields maximum degree 64 and reaches 0.95 recall with $O(\log n)$ hops, validating doubling-dimension predictions (p. 8-9, §5, Figure 4).

## Limitations (author-stated vs. observed)
- Author-stated (p. 1, 4, §1, §3.1): Provable polylogarithmic query guarantees require "slow preprocessing" ($O(n^3)$ construction time), which is computationally intractable for billion-scale datasets.
- Observed: Analyzes unconstrained metric vector search exclusively; contains no analysis of predicate filtering, hybrid routing, or probabilistic membership structures.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
- Demonstrates that heuristic edge selection in proximity graphs can induce catastrophic linear-time worst-case traversals ($0.1n$ hops) when graph shortcuts fail.
- Direct mathematical justification for why predicate filtering degrades graph ANN: removing non-matching nodes induces artificial dead ends analogous to the worst-case instances shown here.
- Provides rigorous proof that robust pruning requires degree scaling as $O((4\alpha)^{d} \log \Delta)$ to maintain connectivity across metric bottlenecks.
Novelty check: no; investigates pure metric ANN search without evaluating metadata predicates or membership filters during graph traversal (p. 1-17).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- The theoretical $(\frac{\alpha+1}{\alpha-1} + \epsilon)$ approximation bound applies strictly to the impractical $O(n^3)$ slow preprocessing model; practical fast preprocessing is shown empirically to suffer from linear worst-case queries (p. 1, 4, 6-8).

## Useful references to snowball (bibkeys or titles from its reference list)
- subramanya2019diskann (Subramanya et al., 2019: DiskANN: Fast accurate billion-point nearest neighbor search on a single node) (p. 10)
- malkov2020hnsw (Malkov & Yashunin, 2020: Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 10)
- fu2019nsg (Fu et al., 2019: Fast approximate nearest neighbor search with the navigating spreading-out graph) (p. 9)
