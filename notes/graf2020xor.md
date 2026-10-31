# graf2020xor — Xor Filters: Faster and Smaller Than Bloom and Cuckoo Filters
Authors / Year / Venue / DOI: Thomas Mueller Graf, Daniel Lemire / 2020 / ACM Journal of Experimental Algorithmics / 10.1145/3376122
Status: PUB
PDF: papers/graf2020xor.pdf   Read fully: yes

## Problem addressed (p.)
Approximate set membership queries over static/immutable sets that achieve smaller memory footprints and faster lookup speeds than Bloom and cuckoo filters (p. 1). Standard Bloom filters require many random memory accesses (e.g., $-\log_2 \epsilon \approx 7$ accesses at $\epsilon = 1\%$) and consume 44% more memory than the theoretical lower bound, while cuckoo filters incur higher CPU instruction counts and lower space efficiency at moderate false-positive rates (p. 1–2).

## Method (core idea in ≤5 sentences) (p.)
The paper introduces the xor filter, a practical approximate set membership structure for immutable sets based on 3-partite hypergraph peeling and XOR fingerprint assignment (p. 1, 3, §3). For a set $S$, it allocates an array $B$ of capacity $c = \lfloor 1.23 |S| \rfloor + 32$ storing $k$-bit fingerprints, divided into three equal ranges indexed by independent hash functions $h_0, h_1, h_2$ (p. 4, §3). Construction iteratively identifies keys that map uniquely to an entry, pushes them onto a stack, and assigns fingerprint values in reverse stack order such that $B[h_0(x)] \oplus B[h_1(x)] \oplus B[h_2(x)] = \text{fingerprint}(x)$ for every $x \in S$ (p. 4–6, §3.2). Membership queries check this exact XOR condition using exactly 3 memory accesses that execute concurrently via CPU memory-level parallelism (MLP), requiring no branch instructions (p. 4, §3.1; p. 12, §4.4). An enhanced "xor+ filter" variant concentrates empty entries into the last third of the table and compresses them with Rank9, reducing space to $1.0824k + 0.5125$ bits per key (p. 7, §3.3).

## Complexity / theoretical claims
- Space complexity: Standard xor filter requires $c = \lfloor 1.23 |S| \rfloor + 32$ entries of $k$ bits, giving $1.23 k = 1.23 \log_2(1/\epsilon)$ bits per key (p. 4, 7, 8).
- Compressed xor+ filter requires $1.0824 k + 0.5125$ bits per key (p. 7, §3.3).
- Construction time: Linear time $O(|S|)$, as each key is added to 3 sets and removed at most once during peeling (p. 5, §3.2).
- Construction success probability: Exceeds 0.8 for small sets and approaches 1.0 asymptotically for large sets (e.g., almost 1 for $|S| = 10^7$) when $c = 1.23 |S| + 32$ (p. 5, Fig. 1).
- Query complexity: Exactly 3 memory accesses and $\approx 48$ instructions per query, independent of target false-positive probability $\epsilon$ (p. 4, 12, §3.1, §4.4).
- Statement, assumptions, theorem number, page: none stated as formal numbered theorems; theoretical space bounds and hypergraph peelability derived from Botelho et al. [6] and Dietzfelbinger & Pagh [17] under uniform independent hashing assumptions (§3, p. 3–7).

## Filter type and selectivity regime handled (p.)
- Filter type: Xor filter (8-bit and 16-bit fingerprints) and compressed Xor+ filter (with Rank9) (p. 4, 7, 10, §3).
- Selectivity regime handled: Designed for approximate set membership queries across false-positive rates $\epsilon \in [10^{-5}, 0.1]$; requires less memory than space-optimized Bloom filters across all regimes, and less memory than cuckoo filters for all $\epsilon > 5.6 \times 10^{-6}$ (p. 7, 8, Fig. 2).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- Index structure used: other (flat 3-way partitioned array of $k$-bit fingerprints; no proximity graph or vector index) (p. 4, §3).

## Datasets, baselines, metrics (Table N)
- Datasets: Synthetic 64-bit random keys and sequential keys evaluated at 10M and 100M keys, queried with 10M keys under varying match fractions (0%, 25%, 50%, 75%, 100%) (p. 7–8, §4).
- Baselines: Standard Bloom filter (8, 12, 16 bits/key), Blocked Bloom filter (Apache Impala AVX2), Cuckoo filter (12 and 16 bits), Cuckoo semi-sorted (13 bits), Golomb-compressed sequence (GCS), Counting Quotient Filter (CQF), and Morton filter (p. 9–10, 13–14, §4.1, App. B, Tables 3, 5).
- Metrics: Construction time (ns/key) (Table 2, p. 10; Table 4, p. 13); query time (ns/query), space usage (bits/key), false-positive probability (%) (Table 3, p. 11; Table 5, p. 14; Figs. 3, 4, 5).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Construction time (Table 2, p. 10):
  - 10M keys: Blocked Bloom 10 ns/key; Bloom 8/12/16: 40/60/90 ns/key; Cuckoo 12/16: 80/90 ns/key; Cuckoo semiSort 13: 130 ns/key; Xor 8/16: 110/120 ns/key; Xor+ 8/16: 160/160 ns/key; GCS: 160 ns/key.
  - 100M keys: Blocked Bloom 20 ns/key; Bloom 8/12/16: 70/90/130 ns/key; Cuckoo 12/16: 130/120 ns/key; Cuckoo semiSort 13: 200 ns/key; Xor 8/16: 130/130 ns/key; Xor+ 8/16: 180/180 ns/key; GCS: 190 ns/key.
- Query performance at 25% find rate (Table 3, p. 11):
  - 10M keys: Xor 8: 23 ns, 9.8 bits/key, FPP 0.389%; Xor 16: 27 ns, 19.7 bits/key, FPP 0.002%; Xor+ 8: 36 ns, 9.2 bits/key, FPP 0.390%; Xor+ 16: 43 ns, 17.8 bits/key, FPP 0.002%; Cuckoo 12: 31 ns, 12.8 bits/key, FPP 0.183%; Cuckoo 16: 32 ns, 17.0 bits/key, FPP 0.012%; Bloom 8: 31 ns, 8.0 bits/key, FPP 2.161%; Bloom 12: 40 ns, 12.0 bits/key, FPP 0.313%; Blocked Bloom: 16 ns, 10.7 bits/key, FPP 0.939%; GCS: 137 ns, 10.0 bits/key, FPP 0.389%.
  - 100M keys: Xor 8: 32 ns, 9.8 bits/key, FPP 0.391%; Xor 16: 33 ns, 19.7 bits/key, FPP 0.001%; Xor+ 8: 64 ns, 9.2 bits/key, FPP 0.389%; Xor+ 16: 65 ns, 17.8 bits/key, FPP 0.002%; Cuckoo 12: 38 ns, 12.8 bits/key, FPP 0.184%; Cuckoo 16: 37 ns, 17.0 bits/key, FPP 0.011%; Bloom 8: 53 ns, 8.0 bits/key, FPP 2.205%; Bloom 12: 58 ns, 12.0 bits/key, FPP 0.339%.
- CQF and Morton filters (Table 5, p. 14): CQF query time 64 ns (10M) and 88 ns (100M); Morton filter query time 47 ns (10M) and 65 ns (100M), both significantly slower than Xor 8 (23 ns and 32 ns).
- Instruction count: Xor filter executes exactly 3 memory accesses and $\approx 48$ instructions per query, compared to 66–68 instructions for Cuckoo filters and 41–105 for Bloom filters (p. 12, §4.4).

## Limitations (author-stated vs. observed)
- Author-stated: Xor filters are completely immutable; they do not support dynamic addition or deletion of keys without reconstructing the filter from scratch (p. 1, 13, §1, §4.4); construction time is roughly $2\times$ slower than Bloom filter construction (p. 10, 13, §4.2, §5).
- Observed: Purely 1D approximate set membership data structure; lacks any concept of vector distance metrics, high-dimensional similarity, or graph traversal.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Provides an ultra-fast, branchless AMQ filter baseline requiring only 3 memory accesses and minimal instruction overhead ($\approx 48$ instructions). Highly relevant for static or immutable metadata predicates where filters can be pre-built on graph nodes to maximize in-traversal throughput. Serves as our primary static AMQ baseline in space and query latency comparisons against Bloom and Cuckoo filters.
Novelty check: Novelty check: no (focuses on standalone approximate set membership data structures for LSM trees and networking systems; §1, §2, p. 1–3).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- In Table 3(a), Xor 16 bits/key is listed as 19.7 ($1.23 \times 16 = 19.68$), and empirical FPP is reported as 0.002%, whereas theoretical $1/2^{16} = 0.001526\%$.
- The authors observe that Fan et al.'s original cuckoo filter reference implementation wastes up to 50% of memory due to power-of-two size constraints (p. 9, §4.1; Table 4, p. 13), prompting their non-power-of-two cuckoo modification.

## Useful references to snowball (bibkeys or titles from its reference list)
- Botelho, F. C., Pagh, R., and Ziviani, N. (2007). Simple and space-efficient minimal perfect hash functions. WADS 2007, 139–150.
- Breslow, A. D. and Jayasena, N. S. (2018). Morton filters: Faster, space-efficient cuckoo filters via biasing, compression, and decoupled logical sparsity. PVLDB 11(9), 1041–1055.
- Dietzfelbinger, M. and Pagh, R. (2008). Succinct data structures for retrieval and approximate membership. ICALP 2008, 385–396.
- Pandey, P., Bender, M. A., Johnson, R., and Patro, R. (2017). A general-purpose counting filter: Making every bit count. SIGMOD 2017, 775–787.
