# fan2014cuckoo — Cuckoo Filter: Practically Better Than Bloom
Authors / Year / Venue / DOI: Bin Fan, Dave G. Andersen, Michael Kaminsky, Michael D. Mitzenmacher / 2014 / CoNEXT 2014 / 10.1145/2674005.2674994
Status: PUB
PDF: papers/fan2014cuckoo.pdf   Read fully: yes

## Problem addressed (p.)
Approximate set membership testing supporting dynamic addition and deletion of items without degrading space efficiency or query lookup throughput (p. 1–2). Standard Bloom filters cannot delete items without rebuilding the entire filter, and existing deletion-capable extensions (counting Bloom filters, d-left counting Bloom filters, quotient filters) introduce large space or latency penalties (p. 1–2).

## Method (core idea in ≤5 sentences) (p.)
The paper introduces the Cuckoo Filter, an approximate set membership data structure based on multi-way associative cuckoo hash tables storing short fingerprints instead of full keys (p. 1, §1). To enable dynamic displacements during insertion without retaining original keys, it proposes partial-key cuckoo hashing, deriving an item's alternate candidate bucket index via $h_2(x) = h_1(x) \oplus \text{hash}(\text{fingerprint})$ (p. 4, §3.1). Lookups probe at most two candidate buckets (at most $2b$ fingerprint entries), incurring at most two cache line misses regardless of whether the query is positive or negative (p. 5, §3.2; p. 9, §6). Deletions simply locate and remove one matching fingerprint copy from either candidate bucket without complex rebalancing or false deletion hazards (p. 5, §3.3). A semi-sorting optimization sorts fingerprints in 4-entry buckets to compress bucket state, saving 1 bit per item (p. 8, §5.2).

## Complexity / theoretical claims
- Fingerprint size lower bound: $f = \Omega(\log(n)/b)$ bits to ensure non-trivial probability of avoiding $2b + 1$ items colliding into the same two buckets (eq. 3, p. 6–7).
- False-positive probability upper bound: bounded by $1 - (1 - 1/2^f)^{2b} \approx 2b / 2^f \le \epsilon$ across $2b$ fingerprint comparisons (eq. 5, p. 8).
- Minimal fingerprint size for target false-positive rate $\epsilon$: $f \ge \lceil \log_2(1/\epsilon) + \log_2(2b) \rceil$ bits (eq. 6, p. 8).
- Amortized space cost per item: $C \le \lceil \log_2(1/\epsilon) + \log_2(2b) \rceil / \alpha$ bits (eq. 7, p. 8).
- Space cost for bucket size $b = 4$ ($\alpha \approx 95.5\%$): $(\log_2(1/\epsilon) + 3)/\alpha$ bits/item for basic cuckoo filter, and $(\log_2(1/\epsilon) + 2)/\alpha$ bits/item with semi-sorting (Table 2, p. 8).
- Statement, assumptions, theorem number, page: asymptotic lower bound derived in §4 (eq. 3, p. 6–7) under uniform hashing assumptions; no formal numbered theorems.

## Filter type and selectivity regime handled (p.)
- Filter type: Cuckoo filter (basic CF with $b=4$ entries/bucket, and semi-sorted ss-CF) (p. 4–8, §3, §5).
- Selectivity regime handled: Designed for approximate set membership queries across false-positive rates $\epsilon \in [10^{-5}, 0.1]$; specifically achieves superior space efficiency over space-optimized Bloom filters when target error rate $\epsilon < 3\%$ (p. 1, p. 8–9, Fig. 4).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- Index structure used: other (multi-way cuckoo hash table organized into an array of buckets; no proximity graph or vector index) (p. 3–4, §2.2, §3).

## Datasets, baselines, metrics (Table N)
- Datasets: Synthetic 64-bit random integer keys generated via random number generators (up to 128 million items in 192 MB filters, and up to $2^{30}$ buckets / 4 billion items in scaling tests) (p. 6, 9–10, §4, §7).
- Baselines: Standard Bloom filter (BF), Blocked Bloom filter (blk-BF), Quotient filter (QF), and d-left counting Bloom filter (dl-CBF) (p. 9–10, §7, Table 3).
- Metrics: Number of items stored, bits per item, achieved false-positive rate (%), construction speed (million keys/sec) (Table 3, p. 10); lookup throughput (MOPS) vs positive query fraction (Fig. 5, p. 11); lookup throughput vs occupancy (Fig. 6, p. 12); insert throughput vs occupancy (Fig. 7, p. 11); delete throughput vs occupancy (Fig. 8, p. 12).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Table 3 (192 MB filter budget, p. 10):
  - CF: 127.78 million items, 12.60 bits/item, 0.19% false-positive rate, construction speed 5.00 million keys/sec.
  - ss-CF: 128.04 million items, 12.58 bits/item, 0.09% false-positive rate, construction speed 3.13 million keys/sec.
  - BF: 123.89 million items, 13.00 bits/item, 0.19% false-positive rate, construction speed 3.91 million keys/sec.
  - blk-BF: 123.89 million items, 13.00 bits/item, 0.43% false-positive rate, construction speed 7.64 million keys/sec.
  - QF: 120.80 million items, 13.33 bits/item, 0.18% false-positive rate, construction speed 1.91 million keys/sec.
  - dl-CBF: 103.82 million items, 15.51 bits/item, 0.76% false-positive rate, construction speed 4.78 million keys/sec.
- Space crossover threshold: Cuckoo filter beats space-optimized Bloom filter space at false-positive rates below 3% (7.2 bits per item) (Fig. 4, p. 9).
- Memory access cost: CF incurs at most 2 memory references per lookup for both positive and negative queries, whereas space-optimized BF requires $\log_2(1/\epsilon)$ references on positive queries and 2 references on negative queries (Table 2, p. 8).
- Table occupancy: Achieves $\alpha = 95.5\%$ occupancy for $b=4$ and up to 98% for $b=8$ with fingerprints $\ge 6$ bits (p. 6, 8, Fig. 2).

## Limitations (author-stated vs. observed)
- Author-stated: Required fingerprint size grows as $\Omega(\log(n)/b)$ bits, which is asymptotically worse than Bloom filter's constant bits per item (p. 1, p. 6–7, §4); cannot insert identical items more than $2b$ times without causing bucket overflow and insertion failure (p. 5, §3.1); insertion throughput decreases significantly as occupancy approaches maximum capacity due to longer displacement chains (p. 11–12, Fig. 7).
- Observed: Designed strictly for 1D membership queries; contains no spatial distance metrics, vector embeddings, or graph traversal mechanisms.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Serves as an essential AMQ filter structure offering dynamic deletion capability and strictly bounded (at most two) cache misses per lookup. Its deterministic two-bucket probe pattern makes it a compelling candidate for in-traversal predicate pruning where memory latency dominates. Forms a primary baseline filter structure in our theoretical cost model and empirical benchmarks.
Novelty check: Novelty check: no (evaluates standalone approximate set membership algorithms for networking and key-value systems; §1, p. 1–2).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- The derivation in Eq. (3) assumes that the failure probability is dominated by groups of $2b+1$ items colliding, which the authors explicitly state they "believe" but "do not prove" (§4, p. 6).
- In Table 3, BF and blk-BF store identical numbers of items (123.89 million) at 13.00 bits/item, but blk-BF achieves more than double the false-positive rate (0.43% vs 0.19%) due to block load imbalance (§7.1, p. 10).

## Useful references to snowball (bibkeys or titles from its reference list)
- Bender, M. A. et al. (2012). Don't thrash: How to cache your hash on flash. PVLDB 5(11), 1627–1637.
- Bonomi, F. et al. (2006). An improved construction for counting bloom filters. ESA, LNCS 4168, 684–695.
- Pagh, R. and Rodler, F. (2004). Cuckoo hashing. Journal of Algorithms 51(2), 122–144.
- Putze, F., Sanders, P., and Johannes, S. (2007). Cache-, hash- and space-efficient bloom filters. Experimental Algorithms, 108–121.
