# maplets2025 — Time To Replace Your Filter: How Maplets Simplify System Design
Authors / Year / Venue / DOI: Bender, Michael A., Conway, Alex, Farach-Colton, Martín, Johnson, Rob, Pandey, Prashant / 2025 / not stated / none
Status: PRE
PDF: papers/maplets2025.pdf   Read fully: yes

## Problem addressed (p.)
Architectural mismatch and performance degradation caused by using approximate set-membership filters (Bloom, quotient, cuckoo) in data systems that fundamentally require key-value associations (maps) rather than simple set membership (p. 1). When systems need to associate small auxiliary values (such as SSTable IDs, $k$-mer counts, or experiment bitmasks) with keys, relying on filters forces designers into complex workarounds—such as multiple filter queries, parallel filter arrays, or secondary hash tables—that degrade latency, inflate memory footprint, and reduce throughput (p. 1–2).

## Method (core idea in ≤5 sentences) (p.)
The paper introduces the maplet, a space-efficient data structure for approximate key-value mappings that provides the space efficiency of probabilistic filters while natively supporting value associations with one-sided error guarantees (p. 1, §1). A maplet is constructed from a perfect-hashing filter (such as a quotient, cuckoo, or Morton filter) that maps fingerprints injectively to array slots, expanding internal slots to store associated values directly alongside fingerprints for high cache locality (p. 2, §2). For key $k$, the maplet returns an approximation $m[k]$ such that $m[k] = M[k]$ with probability $\ge 1 - \epsilon$, guaranteeing the one-sided ordering property $M[k] \preceq m[k]$ with respect to an associative/commutative operator $\oplus$ (p. 1–2, §1, §2). It proves the "strong maplet property," guaranteeing that when errors occur, the returned value is merged with at most $\ell$ extraneous keys with probability $\Pr[\ell \ge L] \le \epsilon^L$ (exponential decay in error magnitude) (p. 2–3, §2). It surveys maplet applications across LSM-tree storage engines (SplinterDB), computational genomics (Squeakr, Mantis), and network routing (p. 3–6, §3–§6).

## Complexity / theoretical claims
- Space complexity: Storing $v$-bit values requires $O(\log(1/\epsilon) + v)$ bits per item using quotient or cuckoo filters, adding exactly $v$ bits of overhead over the underlying filter (p. 2, §2).
- Error probability: Overall error rate is at most $\epsilon$; for any key $k$, $m[k] = M[k]$ unless a fingerprint collision occurs under $h$, which occurs with probability at most $\epsilon$ by the union bound (p. 2, §2).
- Strong Maplet Property: $m[k] = M[k] \oplus (\bigoplus_{i=1}^\ell M[k_i])$ where $\Pr[\ell \ge L] \le \epsilon^L$ (p. 2–3, §2).
- Statement, assumptions, theorem number, page: theoretical space and error guarantees derived analytically in §2 (p. 2–3); no formal numbered theorems.

## Filter type and selectivity regime handled (p.)
- Filter type: Maplets constructed on top of perfect-hashing filters: Counting Quotient Filters (CQF), Cuckoo filters, Morton filters, and Vector Quotient Filters (p. 1–3, §1, §2).
- Selectivity regime handled: Approximate mapping with tunable one-sided error rate $\epsilon$ (e.g., standard AMQ operating range $\epsilon \in [10^{-3}, 10^{-1}]$); evaluated conceptually across storage engines, genomic search, and networking (§2–§6, p. 2–6).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- Index structure used: other (perfect-hashing filter arrays, quotient filter compact slots, LSM-tree node indices, inverted index CQF; no vector index, HNSW, or proximity graph) (p. 2–5, §2–§5).

## Datasets, baselines, metrics (Table N)
- Datasets: Case study analyses referencing external published systems:
  - SplinterDB on NVMe key-value workloads (p. 3–4, §3);
  - Squeakr on genomic $k$-mer sequencing data (p. 4, §4);
  - Mantis on the Sequence Read Archive (SRA) with over 50 petabases / 40,000 RNA-Seq experiments (100 TB sequencing data) (p. 4–5, §5);
  - Broder & Mitzenmacher networking applications (p. 5–6, §6).
- Baselines: Standard Bloom filters, Counting Bloom Filters (CBF), Sequence Bloom Trees (SBT, SSBT, HowDe-SBT), and dual Bloom-filter + hash-table systems (Jellyfish, BFCounter, Turtle) (p. 3–5, §3–§5).
- Metrics: none stated in dedicated tables (vision/conceptual paper citing performance numbers from prior literature: e.g., order-of-magnitude query speedup, $4\times$ faster construction, read multiplicity $g \log_g n$, write amplification) (p. 3–5, §3–§5).

## Key results (numbers exactly as reported, with Table/Fig locator)
- No empirical benchmark tables reported in the paper (`none stated` / vision paper).
- In SplinterDB, replacing separate SSTable filters with a single node maplet saves up to $g$ storage I/Os while matching collective filter memory usage (p. 3–4, §3).
- In Squeakr, using a CQF maplet achieves "order-of-magnitude faster queries and up to 4× faster construction compared to state-of-the-art k-mer counters" while yielding smaller index sizes (p. 4, §4).
- In Mantis, using a CQF maplet directly maps $k$-mers to experiment bit vectors, successfully indexing up to 40,000 SRA experiments (>100 TB data) with exact results, eliminating tree traversal and multi-level bitwise pruning of Sequence Bloom Trees (p. 5, §5).
- In networking, shows how maplets can streamline over half of the Bloom filter applications in Broder & Mitzenmacher (2004) into single-query lookups (p. 5–6, §6).

## Limitations (author-stated vs. observed)
- Author-stated: Building multiset maplets from cuckoo filters is constrained because cuckoo filters support at most $2b$ (e.g., 8) copies of a fingerprint, limiting duplicate value insertions when $\oplus$ does not form a mathematical group (p. 2, §2); in hardware-based routers, parallel Bloom filters can be evaluated simultaneously, so maplets primarily benefit software-based architectures (p. 5–6, §6).
- Observed: Conceptual vision paper synthesizing prior systems work (SplinterDB, Squeakr, Mantis); presents no newly gathered benchmark data or experimental tables. Does not evaluate high-dimensional vector search or proximity graph indexing.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Provides a foundational argument that approximate filters should be generalized to maplets when metadata attributes have multi-valued categorical labels or payload values. In HNSW graph traversal, if nodes need to evaluate multi-attribute or non-binary predicates, a maplet structure can map node IDs or edge predicates to attribute values rather than querying separate filters. Directly informs the structural design of metadata-augmented filter nodes in predicate-constrained ANN graphs.
Novelty check: Novelty check: no (evaluates storage engines, genomic search, and networking routing tables; mentions graph-like trees such as Sequence Bloom Trees in genomics and quad-trees in networking, but does not address vector proximity graphs or ANN traversal; §5, §6, p. 4–6).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- The paper is an unrefereed preprint (arXiv:2510.05518v1) with placeholder ACM metadata in the header/reference format ("Conference'17, July 2017, Washington, DC, USA", "ISBN 978-x-xxxx-xxxx-x/YYYY/MM", DOI "10.1145/nnnnnnn.nnnnnnn"; p. 1, 2, 4, 6).
- The paper contains no empirical experimental section or benchmark tables of its own; all quantitative performance claims are secondary citations from earlier papers (SplinterDB, Squeakr, Mantis).

## Useful references to snowball (bibkeys or titles from its reference list)
- Bender, M. A. et al. (2012). Don't Thrash: How to Cache Your Hash on Flash. PVLDB 5(11).
- Conway, A., Farach-Colton, M., and Johnson, R. (2023). SplinterDB and Maplets: Improving the Tradeoffs in Key-Value Store Compaction Policy. PACMMOD.
- Dillinger, P. C. et al. (2022). Fast Succinct Retrieval and Approximate Membership Using Ribbon. SEA.
- Pandey, P. et al. (2017). A general-purpose counting filter: Making every bit count. SIGMOD 2017.
- Pandey, P. et al. (2021). Vector Quotient Filters: Overcoming the Time/Space Trade-Off in Filter Design. SIGMOD 2021.
