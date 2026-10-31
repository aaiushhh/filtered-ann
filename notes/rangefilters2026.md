# rangefilters2026 — Approximate Nearest Neighbor Search with Graph Range Filters
Authors / Year / Venue / DOI: Tao, Qian, Jiang, Yuntao, Tong, Yongxin, Sun, Yu / 2026 / not stated / none
Status: PRE
PDF: papers/rangefilters2026.pdf   Read fully: yes

## Problem addressed (p.)
Approximate Nearest Neighbor Search with Graph Range Filters (ANNGR), where queries $(e_q, v_q, k, r)$ require retrieving the top-$k$ nearest vectors to query embedding $e_q$ whose corresponding nodes lie within an $r$-hop topological distance from query node $v_q$ in a filter graph $G=(V,E)$ (p. 1-2, §1-2). Evaluating multi-hop reachability over large graph topologies during vector similarity search is computationally expensive, and candidate attribute sets are too large and irregular for separate per-attribute indices (p. 1-2, §1).

## Method (core idea in ≤5 sentences) (p.)
Proposes Distance-Aware Labeling with Hashing compression (DLH) and a memoized variant (DLH-M) to support fast in-range predicate checks during graph traversal (p. 1-2, §1; p. 4-6, §3). For each vertex in the filter graph, DLH stores distance-aware labeling (DAL) sets up to hop range $r$, compressing labeling sets that exceed threshold $T$ into Bloom filters of length $m$ with $t$ hash functions (p. 4-5, §3.1-3.2). During proximity graph traversal, candidate neighbors are evaluated via an `in_range` predicate that uses direct set intersection, Bloom filter containment tests, or bitwise Bloom filter intersection depending on operand compression states (p. 5-7, §3.3). DLH-M introduces intermediate hashing memoization to avoid redundant hash computations for $v_q$ across multiple candidate checks (p. 7-8, §4). Traversal integrates DLH/DLH-M predicate checks directly into greedy beam search on proximity graphs (p. 8-9, §4.3).

## Complexity / theoretical claims
- Lemma 1 (p. 7): The time complexity of the in-range query predicate in DLH (Algorithm 5) is $O(|L_o^<| + |L_q^<| + t |L_{o/q}^>|)$, bounded by $O(T + t^2)$ where $T$ is the compression threshold, $t$ is the number of hash functions, and $|L^>|$ denotes labeling sets compressed into Bloom filters.
- Lemma 2 (p. 9): For DLH-M, the average time complexity of an in-range query is $O(|L_o^<| + |L_q^<| + t |L_o^>|)$ by memoizing hash evaluations of $v_q$.

## Filter type and selectivity regime handled (p.)
Graph topological range filters: shortest-path hop-distance constraint $d_G(v_q, v_i) \le r$ over a filter graph $G$ (p. 2, §2.1). Evaluates hop distances $r \in \{3, 4, 5, 6\}$ (default $r=4$) across random graph edge probabilities $p \in \{0.00025, 0.00027, 0.0003\}$, covering varying topological candidate selectivities (p. 9, §5.1; p. 11, §5.2).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
NSW / HNSW proximity graph integrated with Distance-Aware Labeling and Bloom filter bitsets (p. 1-2, §1; p. 8-9, §4.3).

## Datasets, baselines, metrics (Table N)
- Datasets (Table 1, p. 9): SIFT (1M vectors, 128d), GIST (1M vectors, 960d), DEEP (1M vectors, 96d), YFCC (1M vectors, 128d). Filter graphs generated as Erdős-Rényi graphs $G(n,p)$ with $n = 80,000$.
- Baselines (p. 9, §5.1): Pre-Filter (BFS reachability + brute-force vector scan), Post-Filter (HNSW search + BFS reachability validation), ACORN, Navix.
- Metrics (p. 9, §5.1): Queries per second (QPS), Filtered Recall@k ($k=128$), Index size, Construction time.

## Key results (numbers exactly as reported, with Table/Fig locator)
- DLH and DLH-M achieve up to 70.3× QPS improvement under identical recall compared to baselines (p. 10, §5.2; Fig. 9, p. 10).
- Both DLH and DLH-M achieve recall exceeding 98% across all four datasets (p. 10, §5.2; Fig. 9, p. 10).
- On SIFT, DEEP, and YFCC, DLH-M achieves QPS exceeding $10^3$ at recall $>96\%$ (p. 10-11, §5.2; Fig. 9, p. 10).
- Varying Bloom filter false positive probability from $\alpha = 0.001$ to $0.015$ demonstrates stable recall and QPS, validating the default setting $\alpha = 0.01$ (p. 10-11, §5.2; Fig. 10, p. 10).

## Limitations (author-stated vs. observed)
- Author-stated: Evaluated primarily on static Erdős-Rényi random filter graph models; dynamic edge insertions/deletions on the filter graph are not investigated (p. 9, §5.1; p. 12, §6).
- Author-stated: Bloom filter false positives introduce a theoretical possibility of admitting out-of-range false positive nodes during search (p. 5-7, §3.2-3.3).
- Observed: Focuses on topological graph hop distance filters; does not directly handle general multi-attribute relational or arbitrary continuous metric predicates.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Provides a concrete published architecture demonstrating that embedding Bloom filters directly into proximity graph nodes enables fast in-traversal predicate evaluation with bounded error rates. Shows how to formalize the trade-off between Bloom filter false positive rates and ANN search recall. Directly informs our project's filter structure and in-traversal predicate pruning design.
Novelty check: yes; it applies Bloom filters to compress distance-aware labeling sets and executes Bloom filter membership and intersection tests during proximity graph traversal to prune disqualified nodes (p. 1-2, §1; p. 5-7, §3.2-3.3; p. 8-9, §4.3).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- none noted.

## Addendum: Cost-Model Parameters & Bloom Filter Mechanics
1. **Full list of cost-model parameters (Lemma 1, Lemma 2, §2.4, §3.3, §5.1, p. 4, 7–10)**:
   - $T$: size threshold above which distance-aware labeling sets are compressed into Bloom filters (p. 6, §3.3; p. 7, Lemma 1).
   - $t$: number of hash functions in each Bloom filter (p. 4, §2.4; p. 7, Lemma 1).
   - $m$: bit-array length (filter size) of each Bloom filter (p. 4, §2.4; p. 6, §3.3).
   - $\alpha$: false positive probability (FPP) of a Bloom filter, $\alpha = (1/2)^{(m/r)\ln 2}$, where $r$ is the number of inserted elements (p. 4, §2.4; evaluated from $\alpha = 0.001$ to $0.015$, default $\alpha = 0.01$, p. 10, §5.1).
   - $r$: maximum graph-range hop distance constraint in filter graph $G$ (p. 2, §2.1; p. 7, Lemma 1).
   - $\mathcal{D}_<(v)$: collection of labeling sets for node $v$ whose cardinality is $\le T$ (stored explicitly) (p. 7, Eq. 5).
   - $d_v^<$: total cardinality of all explicit labeling sets for node $v$, $d_v^< = \sum_{D_j(v) \in \mathcal{D}_<(v)} |D_j(v)| < rT$ (p. 7, Eq. 5, Lemma 1).
   - $c_v^>$: number of distance labeling sets for node $v$ whose size exceeds threshold $T$ (stored as Bloom filters), $c_v^> \le r$ (p. 7, Lemma 1).
   - $n_c$: number of candidate nodes evaluated by in-range queries during traversal (p. 8, Lemma 2).
   - $b$: beam search width in graph traversal ($b = 200$ default) (p. 3, Algorithm 1; p. 10, §5.1).
   - $M$: maximum number of neighbors per node in the proximity graph ($M = 16$ default) (p. 9, §5.1).
   - *Filter size / bits / FPP representation*: Parameters $m$ (filter bit-length), $t$ (hash function count), and $\alpha$ (false positive probability FPP) explicitly parameterize the Bloom filters (p. 4, §2.4; p. 6, §3.3; p. 10, §5.1).

2. **Structure tested by the Bloom filter & behavior on a false positive**:
   - *Structure tested*: For each node in the filter graph, distance-aware labeling sets storing reachability labels for hops $0, \dots, r$ that exceed threshold $T$ are compressed into Bloom filters $B_i(v)$ (p. 6, §3.3). During proximity graph traversal, candidate neighbors $o \in G[u]$ are evaluated via predicate function `in_range` testing set-hash containment (checking if labels of $v_q$ hash to 1-bits in $B_j(v_o)$) or hash-hash approximate intersection cardinality estimation (Algorithm 2, 5, p. 4, 7).
   - *What happens on a false positive*:
     - If Bloom filter containment or intersection falsely reports true (positive intersection count $>0$), the candidate node $o$ is incorrectly treated as being within graph-range $r$ of query node $v_q$ (p. 3, Algorithm 1; p. 7, Algorithm 5).
     - Candidate $o$ is admitted into the ANN search result heap `ann` (if its vector distance is closer than the current farthest result in `ann`) and its out-neighbors in proximity graph $G^*$ are subsequently explored (p. 3, Algorithm 1, lines 8–11).
     - Because DLH is a post-filtering / in-traversal approximation framework without a separate secondary verification step against the raw graph adjacency matrix, an uncorrected false positive will remain in result set $R$, resulting in potential recall degradation evaluated by $|R \cap R^*| / k$ (p. 3, §2.1; p. 10, §5.2). Experiments demonstrate that at default FPP $\alpha = 0.01$, overall search recall remains above $98\%$ across all datasets (Fig. 9, 10, p. 10).

## Addendum 2: Analysis of Lemma 1 and Lemma 2 (Cost, Space, Recall vs. Alpha)
1. **Lemma 1 Analysis (§3.3, p. 7)**:
   - *Statement & Algorithm*: Bounds the worst-case time complexity of an in-range query execution in DLH (Algorithm 5).
   - *Assumptions*: Distance-aware labeling sets partitioned by threshold parameter $T$; labeling sets with size at most $T$ are stored explicitly as sets ($D^<(v)$), while labeling sets with size exceeding $T$ are compressed into Bloom filters ($B(v)$). Bloom filters use $t$ hash functions. Query node $v_q$ and candidate node $v_o$ are compared across graph range hops $0 \le i \le r$. Total elements in explicit sets of $v$ is $d^<_v$; number of heavy sets exceeding $T$ is $c^>_v$. For range $r$, $d^<_{v_q}, d^<_v < rT$ and $c^>_{v_q}, c^>_v \le r$.
   - *What is bounded*: Time complexity of in-range intersection testing between query node $v_q$ and candidate node $v_o$.
   - *Variables in bound*: Bounded as $O(d^<_{v_q} \cdot t + d^<_v \cdot t + c^>_{v_q} \cdot c^>_v \cdot t)$, which simplifies under range parameter $r$ to $O(r t T + r^2 t)$.
   - *Dependence on $\alpha$*: Does not bound cost, space, or recall as a function of false-positive probability $\alpha$. The variable $\alpha$ does not appear anywhere in the statement or proof of Lemma 1; time is bounded strictly as a function of set cardinalities, heavy set counts, range $r$, threshold $T$, and hash function count $t$.

2. **Lemma 2 Analysis (§4, p. 8)**:
   - *Statement & Algorithm*: Bounds the average time complexity of an in-range query in DLH-M with memoization (Algorithms 6 and 7).
   - *Assumptions*: $n_c$ total candidates evaluated during traversal; hash evaluations $preh(D(v_q))$ on explicit sets of query node $v_q$ take $O(d^<_{v_q} \cdot t)$ time and are memoized prior to search; each candidate query requires $O(d^<_{v_q} \cdot t)$ time; total time for $n_c$ candidates is $O(d^<_{v_q} \cdot t + n_c \cdot d^<_{v_q} \cdot t)$, yielding average time $O(d^<_{v_q} \cdot t / n_c + d^<_{v_q} \cdot t)$; candidate count $n_c$ is assumed much larger than fixed hash count $t$ ($n_c \gg t$), making the first term negligible.
   - *What is bounded*: Average time complexity of an individual in-range query during graph exploration.
   - *Variables in bound*: Bounded as $O(d^<_{v_q} \cdot t + d^<_v \cdot t + c^>_{v_q} \cdot c^>_v \cdot t)$, simplifying to $O(d^<_{v_q} \cdot t)$ for the memoized intersection component.
   - *Dependence on $\alpha$*: Does not bound cost, space, or recall as a function of false-positive probability $\alpha$. The variable $\alpha$ does not appear in the statement or proof of Lemma 2.

3. **Synthesis Regarding Cost Model & Selectivity**:
   - Neither Lemma 1 nor Lemma 2 bounds search cost, space consumption, or search recall as a function of Bloom filter false positive rate $\alpha$ or query selectivity $\sigma$.
   - $\alpha$ is defined solely in background §2.4 (p. 4) as the theoretical Bloom filter false positive formula $\alpha = (1/2)^{(m/r)\ln 2}$, and investigated empirically in §5.3 (p. 10, Fig. 10) by varying FPP from 0.001 to 0.015.
   - Therefore, the paper contains no formal analytical cost or complexity model as a function of selectivity $\sigma$ or error rate $\alpha$. Selectivity cost model remains `no`.

## Useful references to snowball (bibkeys or titles from its reference list)
- patel2024acorn (ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data) (p. 12)
- malkov2020hnsw (Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs) (p. 12)
- zuo2023arkgraph (ARKGraph: All-Range Approximate K-Nearest-Neighbor Graph) (p. 13)
- bloom1970space (Space/Time Trade-offs in Hash Coding with Allowable Errors) (p. 12)
