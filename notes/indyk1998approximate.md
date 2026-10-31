# indyk1998approximate — Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality
Authors / Year / Venue / DOI: Piotr Indyk, Rajeev Motwani / 1998 / STOC 1998 / 10.1145/276698.276876
Status: PUB
PDF: papers/indyk1998approximate.pdf   Read fully: yes

## Problem addressed (p.)
Overcoming the "curse of dimensionality" in high-dimensional nearest neighbor search (NNS) under $l_p$ norms, where existing exact algorithms suffer either query time linear in dataset size $n$ or preprocessing space/time severely exponential in dimension $d$ ($n^d$ or $2^d$) (p. 1–2 / pp. 604–605).

## Method (core idea in ≤5 sentences) (p.)
The paper relaxes exact search to $\epsilon$-approximate nearest neighbor search ($\epsilon$-NNS) and reduces it to $\epsilon$-Point Location in Equal Balls ($\epsilon$-PLEB) using a hierarchical tree structure called a ring-cover tree (p. 2–5 / pp. 605–608). To solve $\epsilon$-PLEB in sublinear query time without exponential dependence on dimension, it introduces Locality-Sensitive Hashing (LSH), a randomized hashing framework where collisions are far more probable for close points than distant ones (p. 2–3, 5–7 / pp. 605–606, 608–610). Points in $\mathbb{R}^d$ under $l_p$ norms ($p \in [1, 2]$) are embedded into a Hamming cube, where an $(r_1, r_2, p_1, p_2)$-sensitive hash family constructed from coordinate projections maps points into hash buckets (p. 5–7 / pp. 608–610). Queries search buckets indexed by $l$ independent composite hash functions, returning qualifying points in time bounded by $O(dn^\rho)$ where $\rho = \frac{\ln(1/p_1)}{\ln(1/p_2)}$ (p. 6–7 / pp. 609–610). An alternative bucketing method based on uniform grid decomposition is also proposed for $0 < \epsilon < 1$ with $O(d)$ query time and $O(n) \times O(1/\epsilon)^d$ preprocessing (p. 6 / p. 609).

## Complexity / theoretical claims
- Theorem 4 (§4.2, p. 6 / p. 609): Given a $(r_1, r_2, p_1, p_2)$-sensitive hash family $\mathcal{H}$ for distance measure $D$, there exists a randomized algorithm for $(r_1, r_2)$-PLEB using $O(dn + n^{1+\rho})$ space and $O(n^\rho)$ evaluations of hash functions per query, where $\rho = \frac{\ln(1/p_1)}{\ln(1/p_2)}$.
- Proposition 1 (§1, p. 2 / p. 604): For $\epsilon > 1$, there is an algorithm for $\epsilon$-NNS in $\mathbb{R}^d$ under $l_p$ norm ($p \in [1, 2]$) using $\tilde{O}(n^{1 + 1/\epsilon} + dn)$ preprocessing space and $\tilde{O}(dn^{1/\epsilon})$ query time.
- Proposition 2 (§1, p. 2 / p. 605; §4.1, p. 6 / p. 609): For $0 < \epsilon < 1$, there is an algorithm for $\epsilon$-NNS in $\mathbb{R}^d$ under any $l_p$ norm using $\tilde{O}(n) \times O(1/\epsilon)^d$ preprocessing space and $\tilde{O}(d)$ query time.
- Proposition 3 (§1, p. 2 / p. 604): For any $\epsilon > 0$, there is an algorithm for $\epsilon$-NNS in $\mathbb{R}^d$ under $l_p$ norm ($p \in [1, 2]$) using $(nd)^{O(1/\epsilon^2)}$ preprocessing and $\tilde{O}(d)$ query time.
- Ring-Cover Tree Bounds (Lemma 1–4, Corollary 1–2, §3, p. 4–5 / pp. 607–608): Depth is $O(\log^2 n)$, query overhead is $O(\log^2 n \cdot \log(1/\epsilon))$ PLEB tests, and total space is $O(n \text{ polylog } n)$ plus underlying PLEB storage.

## Filter type and selectivity regime handled (p.)
`not stated` (the paper addresses unconditional approximate nearest neighbor search; no metadata predicates or probabilistic membership filters are handled).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Locality-Sensitive Hashing (LSH) hash tables and Ring-Cover Trees over equal balls (§3, p. 3–5 / pp. 606–608; §4.2, p. 5–7 / pp. 608–610). Proximity graphs (HNSW, IVF, Vamana) are not used.

## Datasets, baselines, metrics (Table N)
`none stated` (pure theoretical conference paper; mentions preliminary empirical results from external citation [36] on p. 1 and p. 3 / pp. 604, 606, but contains no experimental tables, datasets, empirical baselines, or quantitative metrics).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Theoretical asymptotic bounds: Establishes the first sublinear query time $\tilde{O}(dn^{1/\epsilon})$ for $\epsilon$-approximate nearest neighbor search with polynomial preprocessing $\tilde{O}(n^{1+1/\epsilon} + dn)$ for $\epsilon > 1$ under $l_p$ norms ($p \in [1, 2]$) (Proposition 1, p. 2 / p. 604).
- Establishes LSH parameter $\rho \le \frac{1}{1+\epsilon}$ for $(r, (1+\epsilon)r)$-PLEB in Hamming space, yielding query time bounded by $O(dn^{1/(1+\epsilon)})$ (§4.2, p. 6–7 / pp. 609–610).

## Limitations (author-stated vs. observed)
- Author-stated: Truly sublinear query time with polynomial preprocessing in Proposition 1 requires $\epsilon > 1$ (p. 1–2 / p. 604); Proposition 2 preprocessing cost is exponential in dimension $d$ ($O(1/\epsilon)^d$) (p. 1–2 / p. 604); Proposition 3 has an exponent growing as $O(1/\epsilon^2)$, making it impractical for small $\epsilon$ (p. 1, 3 / pp. 604, 606).
- Observed: Randomized algorithm with constant success probability requiring independent repetitions to boost confidence; unconstrained similarity search with no support for scalar predicates or attribute filters; applies strictly to metric spaces.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Foundational paper introducing Locality-Sensitive Hashing (LSH) and proving sublinear query bounds for approximate nearest neighbor search. Serves as the primary theoretical baseline for sublinear hashing-based ANN, contrasting with graph-based search models like HNSW.
Novelty check: No. The paper does not use proximity graph traversal and does not apply metadata predicate checks or probabilistic membership filters during search (p. 1–8 / pp. 604–611).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Page numbering dual citation: The conference proceedings pagination is pp. 604–613, whereas the paper itself has internal page numbering 1–10; both are indicated across section locators for unambiguous reference.

## Useful references to snowball (bibkeys or titles from its reference list)
- Broder et al. (1997) [9]: Syntactic clustering of the web (resemblance measure / min-wise hashing)
- Dolev et al. (1995) [24]: Neighborhood search in Hamming space
- Frankl & Maehara (1987) [32] / Johnson & Lindenstrauss (1984) [41]: Dimension reduction random projection lemma
- Gionis, Indyk, Motwani (1999) [36]: Similarity search in high dimensions via hashing (VLDB 1999)
- Kleinberg (1997) [45]: Two algorithms for nearest-neighbor search in high dimensions
- Kushilevitz, Ostrovsky, Rabani (1998) [46]: Efficient search for approximate nearest neighbor in high dimensions
