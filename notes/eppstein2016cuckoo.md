# eppstein2016cuckoo — Cuckoo Filter: Simplification and Analysis
Authors / Year / Venue / DOI: David Eppstein / 2016 / SWAT 2016 (LIPIcs Vol 53) / 10.4230/LIPIcs.SWAT.2016.8
Status: PUB
PDF: papers/eppstein2016cuckoo.pdf   Read fully: yes

## Problem addressed (p.)
Lack of rigorous theoretical performance guarantees for cuckoo filters regarding insertion success probability, achievable load factors, and parameter sizing (p. 8:1–8:2). While Fan et al. (2014) showed empirical efficiency and established a necessary condition $f = \Omega((\log n)/b)$ for fingerprint length, no matching upper bounds or formal proofs of high-probability success had been established (p. 8:2).

## Method (core idea in ≤5 sentences) (p.)
The paper introduces a simplified variant of the cuckoo filter that removes the secondary hash function $h_2$, placing the two candidate locations of element $x$ directly at $h_1(x)$ and $h_1(x) \oplus \phi(x)$ (p. 8:2, 8:6, §3). This modification decomposes the cell dependency graph into $N/2^f$ disconnected components, where each component is an isolated clique (called a subtable) of $2^f$ cells (p. 8:6–8:7, §3). Because cell choices within each subtable are statistically independent, each subtable behaves as an independent blocked cuckoo hash table, making the structure amenable to formal analysis (p. 8:7–8:8, §4). It extends this simplified structure to incorporate a per-subtable stash without altering the query false-positive rate (p. 8:9–8:10, §5). Additionally, it describes a bit-parallel query algorithm using word-level SIMD arithmetic to evaluate all fingerprints within a block in $O(B)$ time (p. 8:11, §6).

## Complexity / theoretical claims
- Lemma 4.1: If $f = \log((\log n)/b) + \Omega(1)$, the probability that any subtable receives too many elements (becomes overfull) is polynomially small $\le 1/n^s$ (p. 8:8).
- Lemma 4.2: For sufficiently large constant block size $b$ and constant $s$, if $f > (s \log n)/b$, the insertion failure probability within a non-overfull subtable is at most $1/n^s$ (p. 8:9).
- Theorem 4.3: Creating a cuckoo filter for $n$ elements with block size $b$ and fingerprint size $f$ succeeds with high probability for load factor $1 - \delta - \delta^2$ whenever $f = \Omega((\log n)/b)$, with sufficient condition $f > (s + 1)(\log n)/b$ for failure probability $O(1/n^s)$ when $b \ge 1 + \frac{\ln(1/\delta)}{1 - \ln 2}$ (p. 8:9).
- Theorem 5.1: The false-positive rate with $b$ blocks, $n$ elements, $N$ cells, fingerprint size $f$, and load factor $1 - \delta = n/(Nb)$, with or without a stash, is at most $\frac{2n}{N(2^f - 1)} = \frac{2b(1-\delta)}{2^f - 1}$ (p. 8:10–8:11).
- Theorem 6.1: When each block of $b$ fingerprints is packed into $B$ machine words, membership queries execute in $O(B)$ time under the word-RAM model (p. 8:11).
- Statement, assumptions, theorem number, page: formal theorems and lemmas proved under the assumption of fully random hash functions and word-RAM operations (Lemmas 4.1, 4.2, Theorems 4.3, 5.1, 6.1, p. 8:8–8:11).

## Filter type and selectivity regime handled (p.)
- Filter type: Simplified cuckoo filter (without secondary hash function $h_2$, with or without per-subtable stash) and standard cuckoo filter (p. 8:2, 8:6, §3).
- Selectivity regime handled: Designed for approximate set membership queries across false-positive rates $\epsilon \le \frac{2b(1-\delta)}{2^f - 1}$; achieves storage cost $(1 + o(1))\log_2(1/\epsilon)$ bits per element matching the information-theoretic lower bound as $b$ grows (p. 8:2, 8:10).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- Index structure used: other (blocked cuckoo hash table partitioned into clique subtables; no proximity graph or vector index) (p. 8:2–8:3, §2).

## Datasets, baselines, metrics (Table N)
- Datasets: none stated (pure theoretical paper; no empirical datasets or experimental benchmarks evaluated) (p. 8:1–8:12).
- Baselines: Standard Bloom filter [2], Blocked cuckoo hash table of Dietzfelbinger & Weidling [5], Cuckoo hashing with a stash of Kirsch et al. [12], and original cuckoo filter of Fan et al. [8] (p. 8:2–8:5, §2).
- Metrics: Failure probability $O(1/n^s)$, load factor $1 - \delta - \delta^2$, false-positive rate $\epsilon$, fingerprint length $f$ (bits), query time $O(B)$ (p. 8:8–8:11, §4–§6).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Establishes the first matching upper bound proving that $f = \Omega((\log n)/b)$ is both necessary and sufficient for high-probability insertion success ($1 - O(1/n^s)$) in cuckoo filters (p. 8:2, Theorem 4.3, p. 8:9).
- Proves maximum load factor of $1 - \delta - \delta^2$ with block size $b \ge 1 + \frac{\ln(1/\delta)}{1 - \ln 2}$ (Theorem 4.3, p. 8:9).
- Derives tight false-positive rate bound $\epsilon \le \frac{2b(1-\delta)}{2^f - 1}$, demonstrating that adding a stash does not increase the false-positive rate (Theorem 5.1, p. 8:10).
- Proves bit-parallel query evaluation runs in $O(B)$ time per query (Theorem 6.1, p. 8:11).
- No experimental tables or empirical benchmark numbers (`none stated` / purely theoretical).

## Limitations (author-stated vs. observed)
- Author-stated: Omitting $h_2$ degrades graph connectivity by fragmenting the cell graph into isolated cliques of size $2^f$, which is acknowledged as practically inferior to the original design of Fan et al. (p. 8:2, 8:6–8:7); analysis assumes fully random hash functions rather than explicit universal hash classes (p. 8:2, §1); reliability improvement of stashes in blocked cuckoo hashing remains conjectural (p. 8:4–8:5, 8:10).
- Observed: Pure theoretical paper containing no implementation, empirical benchmarks, or high-dimensional vector search applications.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Provides the rigorous theoretical foundation and exact closed-form FPR bound $\frac{2b(1-\delta)}{2^f - 1}$ required for parameter sizing in our analytical cost model. The bit-parallel query formulation (Theorem 6.1) provides a concrete algorithmic mechanism to evaluate multi-slot cuckoo buckets in constant time during node filtering. Directly validates theoretical guarantees on cuckoo filter capacity and failure rates when embedded in HNSW graphs.
Novelty check: Novelty check: no (focuses purely on theoretical simplification and asymptotic analysis of standalone cuckoo filters; §1, p. 8:1–8:2).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Page 8:4–8:5 notes an error in Kirsch et al. (2010), pointing out that their claimed failure probability bound $O(1/n^{(\sigma+1)(b-1)+1})$ for blocked cuckoo hashing with a stash of size $\sigma$ is incorrect because $\sigma + 2b + 1$ keys colliding in the same two cells causes a higher failure probability (footnote 1, p. 8:4–8:5).

## Useful references to snowball (bibkeys or titles from its reference list)
- Dietzfelbinger, M. and Weidling, C. (2007). Balanced allocation and dictionaries with tightly packed constant size bins. Theoret. Comput. Sci. 380(1-2), 47–68.
- Kirsch, A., Mitzenmacher, M., and Wieder, U. (2010). More robust hashing: cuckoo hashing with a stash. SIAM J. Comput. 39(4), 1543–1561.
- Pagh, A., Pagh, R., and Rao, S. S. (2005). An optimal Bloom filter replacement. SODA 2005, 823–829.
- Pagh, R. and Rodler, F. F. (2004). Cuckoo hashing. J. Algorithms 51(2), 122–144.
