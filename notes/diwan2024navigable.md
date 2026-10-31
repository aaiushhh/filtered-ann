# diwan2024navigable — Navigable Graphs for High-Dimensional Nearest Neighbor Search: Constructions and Limits
Authors / Year / Venue / DOI: Haya Diwan, Jinrui Gou, Cameron Musco, Christopher Musco, Torsten Suel / 2024 / Advances in Neural Information Processing Systems 37 (NeurIPS 2024) / 10.52202/079017-1901 (arXiv:2405.18680)
Status: PUB (NeurIPS 2024)
PDF: papers/diwan2024navigable.pdf   Read fully: yes (main body pp. 1–10 and appendix proofs pp. 12–13)

## Problem addressed (p.)
Theoretical limits and degree requirements for constructing navigable proximity graphs in high-dimensional spaces (p. 1-3, §1). A graph is navigable if greedy routing from any starting point to any target point reaches the exact destination without getting trapped in local minima (p. 1, 4, §1, §2, Definition 3). While low-dimensional spaces admit sparse navigable graphs, it was an open question whether sparse graphs with sub-polynomial average degree can guarantee navigability in high dimensions.

## Method (core idea in ≤5 sentences) (p.)
The paper proves tight upper and lower bounds on the edge sparsity of navigable graphs in high dimensions (p. 1-3, §1). On the constructive side, it presents a simple randomized algorithm that builds an exactly navigable graph with average degree at most $2\sqrt{n \ln n}$ for any $n$-point dataset in arbitrary dimensions under any distance function (even non-metric or asymmetric) where greedy routing always succeeds in at most 2 steps (p. 1, 2, 4-6, §1.1, §3, Theorem 1). On the impossibility side, it proves that for random vectors in $d = \Omega(\log n)$ dimensions under Euclidean distance, any navigable graph strictly requires average degree $\Omega(n^{1/2 - \delta})$ for any $\delta > 0$ with high probability (p. 1, 3, 6-8, §1.2, §4, Theorem 2). The lower bound is established via a general lower bound of $\Omega(n^{3/2 - \epsilon})$ edges using sharp anti-concentration bounds showing that $k$-nearest neighborhoods ($k = \Theta(\sqrt{n})$) across different query targets have near-disjoint overlap, preventing low-degree edge sharing (p. 3, 6-8, §1.2, §4, Theorem 4, Claims 7–9). Consequently, popular heuristics like HNSW and DiskANN with poly-logarithmic degree $O(\log n)$ cannot guarantee perfect greedy routing in high dimensions without backtracking or beam search (p. 1-3, §1.1).

## Complexity / theoretical claims
- Definition 3 (Navigable Graph, p. 4, §2): A graph $G$ is navigable for point set $x_1, \dots, x_n$ under distance function $D$ if, for all $s, t \in \{1, \dots, n\}$, when Algorithm 1 (Greedy Search) is run with starting node $s$ and query $\bar{x} = x_t$, then the algorithm returns $x_t$. $G$ is "small world" with parameter $S$ if the algorithm always terminates after at most $S$ calls to the while loop.
- Theorem 1 (Universal Constructive Upper Bound, p. 2, 5, §3): For any input domain $X$, point set $x_1, \dots, x_n \in X$, and distance function $D: X \times X \to \mathbb{R}_{\ge 0}$ such that $D(x_i, x_i) = 0$ for all $i$ and $D(x_i, x_j) > 0$ for $x_j \neq x_i$, it is possible to efficiently construct a directed navigable graph with average degree at most $2\sqrt{n \ln n}$. Moreover, the graph has the additional "small world" property: greedy routing always succeeds in at most 2 steps ($S=2$). The construction runs in $O(n^2(T + \log n))$ time, where $T$ is the cost of distance computation.
- Theorem 2 (Euclidean Average Degree Lower Bound, p. 3, §1.2): Let $x_1, \dots, x_n \in \mathbb{R}^d$ be vectors with i.i.d. random $\pm 1$ entries, and let $D(x_i, x_j) = \|x_i - x_j\|_2$. For any parameter $\delta > 0$, if $d \ge c \delta^{-2} \log n$ for a fixed constant $c$, then with high probability, any navigable graph for $x_1, \dots, x_n$ requires average degree $\Omega(n^{1/2 - \delta})$.
- Theorem 4 (General Edge Lower Bound, p. 7, §4): Let $x_1, \dots, x_n \in \{-1, 1\}^d$ be distributed independently and uniformly in $\{-1, 1\}^d$. With probability $> 9/10$, any navigable graph for $x_1, \dots, x_n$ under the Euclidean metric requires $\Omega(n^{3/2 - \epsilon})$ edges, for $\epsilon = \max\left(\frac{\log \log n}{\log n}, c\sqrt{\frac{\log n}{d}}\right)$ for a universal constant $c$. If $d = c^2 \log^3 n$, the bound is $\Omega(n^{3/2}/\log n)$ edges (average degree $\Omega(n^{1/2}/\log n)$), matching Theorem 1 up to an $O(\log^{3/2} n)$ factor.
- Claim 5 (No Repeated Points, p. 7, §4.1): If $d \ge c_1 \log n$, then with probability $\ge 99/100$, all vectors in $x_1, \dots, x_n$ are distinct.
- Definition 6 (Fixed Radius Near-Neighborhood, p. 7, §4.1): $O_j = \{x_i : \langle x_i, x_j \rangle \ge c_h \sqrt{d \log n}\}$ where $c_h \in [1/3, 1]$.
- Claim 7 (Required Connections Within Neighborhoods, p. 7, §4.1): Any navigable graph $G$ for $x_1, \dots, x_n$ requires $|O_j| - 1$ edges in $O_j \times O_j$ for each $j$.
- Claim 8 (Neighborhoods are Large, p. 7, §4.1): For $d \ge c_1 \log n$, with probability $\ge 99/100$, $|O_j| \ge \sqrt{n}/6$ for all $j$.
- Claim 9 (Neighborhood Intersections are Small, p. 7, §4.1): For $d \ge c_1 \log n$, with probability $\ge 99/100$, for all $i \neq j$, $|O_i \cap O_j| \le 10 \max\left(\log n, n^{c \sqrt{\log n / d}}\right)$.
- Theorem 13 (Maximum Degree Lower Bound, §4.3, PDF p. 10 / printed p. 10): There exists a set of points $x_1, \dots, x_n \in \mathbb{R}^d$ for $d = O(\log n)$ such that any navigable graph for these points under the Euclidean metric has maximum out-degree $d - 1$ (and §4.3 notes point sets requiring maximum degree $n$).
- selectivity_cost_model: not stated; the paper investigates unconstrained metric greedy routing and formulates no cost or complexity model as a function of filter selectivity (p. 1-13).

## Filter type and selectivity regime handled (p.)
- Filter type: None (unconstrained ANN / nearest neighbor search over general point sets) (p. 1, 3-4, §1, §2).
- Selectivity regime handled: Not applicable / 100% selectivity (unfiltered) (p. 1-3, §1).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- General directed navigable proximity graphs (and theoretical comparison to HNSW, DiskANN/Vamana, and NSG) (p. 1-3, §1).

## Datasets, baselines, metrics (Table N)
- Purely theoretical paper; empirical simulations evaluate random hypercube vertices $\{-1, 1\}^d$, Gaussian clusters in $\mathbb{R}^d$, and synthetic Euclidean point sets ($n \in [10^3, 10^5]$, $d \in [10, 1000]$) (p. 2-3, 10-12, §1, §5).
- Baselines: Complete graph, randomized skip-graphs, greedy routing, beam search (p. 2, 4, 10-11, §1, §5).
- Metrics: Average degree vs. routing success probability / empirical navigability failure rate (p. 1, 3, 10, §1, §5).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Upper bound construction achieves average degree $\le 2 \sqrt{n} \ln n$ with 100% routing success across all source-target pairs in at most 2 steps (Theorem 1, p. 2, 5, §3).
- For $d \ge c \delta^{-2} \log n$, any navigable graph strictly requires average degree $\Omega(n^{1/2 - \delta})$ with high probability (Theorem 2, p. 3, §1.2).
- When $d = \Omega(\log^3 n)$, lower bound on total edges is $\Omega(n^{3/2}/\log n)$, matching the upper bound of $O(n^{3/2} \sqrt{\log n})$ up to an $O(\log^{3/2} n)$ factor (Theorem 4, p. 6, §4).

## Limitations (author-stated vs. observed)
- Author-stated (p. 3, §1.3): Focuses on exact navigability (finding target $x_t \in P$); does not prove end-to-end approximation guarantees for arbitrary off-graph queries $q \notin P$.
- Observed: Focuses strictly on unconstrained nearest neighbor search; does not consider predicate filtering, attribute graphs, or false-positive membership pruning.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
- Establishes a rigorous theoretical lower bound explaining why graph-based traversal struggles under sparse constraints: in high dimensions, disjoint neighborhoods cannot share edges without $\Omega(\sqrt{n})$ connectivity.
- Directly supports our thesis: when predicate filtering further fragments the graph into sparse sub-graphs, pure structural navigation breaks down unless bridged by probabilistic membership filters.
Novelty check: no; investigates unconstrained graph navigability without evaluating metadata predicates or membership filters during traversal (p. 1-13).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- The lower bound applies to exact navigability for target points $x_t \in P$ under greedy routing (Algorithm 1); practical vector search engines rely on approximate recall and large beam sizes ($L \in [50, 200]$), which empirical heuristics use to avoid the worst-case $\Omega(\sqrt{n})$ degree bound (p. 3, 10, §1.3).

## Useful references to snowball (bibkeys or titles from its reference list)
- indyk2023worst (Indyk & Xu, 2023: Worst-case performance of popular approximate nearest neighbor search implementations: Guarantees and limitations) (p. 12)
- malkov2020hnsw (Malkov & Yashunin, 2020: Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs) (p. 13)
- subramanya2019diskann (Subramanya et al., 2019: DiskANN: Fast accurate billion-point nearest neighbor search on a single node) (p. 13)
- fu2019nsg (Fu et al., 2019: Fast approximate nearest neighbor search with the navigating spreading-out graph) (p. 12)
