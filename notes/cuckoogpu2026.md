# cuckoogpu2026 — Cuckoo-GPU: Accelerating Cuckoo Filters on Modern GPUs
Authors / Year / Venue / DOI: Dortmann, Tim, Vieth, Markus, Schmidt, Bertil / 2026 / ICPP 2026 (Proceedings of the 55th International Conference on Parallel Processing) / 10.1145/3832810.3832822
Status: PUB
PDF: papers/cuckoogpu2026.pdf   Read fully: yes

## Problem addressed (p.)
Designing dynamic Approximate Membership Query (AMQ) data structures supporting high-throughput insertions, queries, and deletions on modern GPU accelerators (p. 1, §1). Existing GPU dynamic filters (e.g., Two-Choice Filter [TCF], GPU Quotient Filter [GQF]) over-prioritize memory locality through serial element shifting or cooperative group synchronization, incurring severe latency bottlenecks and failing to saturate the massive global memory bandwidth of modern high-bandwidth memory (HBM3) architectures (p. 1, 3, §1, §3).

## Method (core idea in ≤5 sentences) (p.)
Cuckoo-GPU implements a lock-free, parallel Cuckoo filter for modern GPUs that embraces the uncoalesced random memory access pattern of Cuckoo hashing to fully saturate global memory bandwidth (p. 1, 3-4, §1, §4.1-§4.3). It utilizes atomic compare-and-swap (CAS) operations on 64-bit words tightly packing 8-bit or 16-bit fingerprints, avoiding coarse-grained locks (p. 3-4, §4.2, §4.3, Algorithm 1). A novel Breadth-First Search (BFS) eviction heuristic inspects candidate alternate buckets during insertion to locate shallow displacement paths, bounding eviction chain lengths and suppressing tail thread divergence at high load factors (p. 1-2, 5-6, §4.6.1). Read-only queries are accelerated using vectorized 128-bit/256-bit memory loads combined with SIMD Within A Register (SWAR) bitwise tag comparisons (p. 4-5, §4.4, Algorithm 2). An optional offset-based bucket placement policy using a choice-bit decouples filter sizing from strict powers of two, eliminating memory over-provisioning (p. 6, §4.6.2).

## Complexity / theoretical claims
- Theoretical False Positive Rate (FPR) approximation (Eq. 4, p. 2, §2.1): $\epsilon \approx 1 - (1 - 2^{-f})^{2 b \alpha}$, where $f$ is fingerprint bits, $b$ is bucket capacity (slots per bucket), and $\alpha$ is load factor (cited from Lang et al., 2019 [19]).
- Algorithmic operation complexity (p. 2, 7, §2.1, §4.6): Queries and deletions inspect at most two candidate buckets ($O(1)$ operations). No formal asymptotic theorems proven (`empirical performance analysis; theoretical FPR formula cited from literature (p. 2, Eq. 4)`).

## Filter type and selectivity regime handled (p.)
- Filter type: Dynamic Cuckoo filter supporting concurrent insertions, positive/negative membership queries, and deletions (p. 1-2, §2.1).
- Selectivity regime handled: Evaluated at target load factor $\alpha = 0.95$ ($95\%$ occupancy), with empirical FPR of $\approx 0.045\%$ for 16-bit fingerprints and bucket size $b=16$ (p. 6-7, §5.2-§5.3). Selectivity in predicate ANN terms is `not stated` (evaluated as a standalone AMQ filter).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- `none; standalone AMQ data structure`: Flat array of fixed-size buckets in GPU global memory, organized hierarchically into 64-bit words containing packed fingerprints, with no proximity graph or vector index (p. 3-4, §4.2).

## Datasets, baselines, metrics (Table N)
- Datasets (p. 6, 9, §5.2, §5.5):
  - Synthetic: Uniformly distributed 64-bit integers in L2-resident ($2^{22}$ slots / 8 MiB) and DRAM-resident ($2^{28}$ slots / 512 MiB) scenarios.
  - Real-world genomic: T2T-CHM13 human genome (20 GB packed 31-mers extracted via KMC3).
- Baselines (p. 6, §5.1): GPU Blocked Bloom filter (GBBF / cuCollections), Bulk Two-Choice filter (TCF), GPU Counting Quotient filter (GQF), Partitioned CPU Cuckoo filter (PCF, 120 threads on 60-core Intel Xeon W9-3595X), Bucketed Cuckoo Hash Table (BCHT).
- Hardware (p. 6, §5.1): System A (RTX PRO 6000 Blackwell, 96 GB GDDR7, 1.8 TB/s), System B (NVIDIA GH200 Grace Hopper, 96 GB HBM3, 3.4 TB/s), System C (60-core Xeon W9-3595X, 256 GB DDR5).
- Metrics (p. 6-7, §5.2): Throughput in billions of elements per second (B elem/s) for insertion, query (+/-), and deletion; False Positive Rate (FPR) (%); Eviction chain length percentiles (p90, p95, p99).

## Key results (numbers exactly as reported, with Table/Fig locator)
- On NVIDIA GH200 (System B, HBM3, 95% target load factor, Fig. 3, p. 7-8):
  - L2-resident (8 MiB, Fig. 3a): Insertion throughput is $378\times$ higher than GQF and $4.1\times$ higher than TCF; query (+) throughput is $6\times$ higher than GQF and $34.7\times$ higher than TCF (exceeds static GBBF by $1.25\times$); deletion throughput is $258\times$ higher than GQF and $107\times$ higher than TCF.
  - DRAM-resident (512 MiB, Fig. 3b): Insertion throughput is $10\times$ higher than GQF ($4.3\times$ on System A) and $2.1\times$ higher than TCF ($1.4\times$ on System A); query (+) throughput is $2.6\times$ GQF and $9.9\times$ TCF (matches GBBF at $0.90\times$ on System B, $0.86\times$ on System A).
  - Multi-threaded CPU comparison (p. 7, §5.2): Delivers $32.4\times$ speedup over 120-thread CPU PCF for DRAM insertions on System A, up to $350\times$ speedup for L2-resident positive queries on System B.
  - T2T-CHM13 genomic 31-mers (Fig. 8, p. 9, §5.5): Cuckoo-GPU achieves 34.13 B elem/s positive queries, 13.51 B elem/s insertions, and 13.41 B elem/s deletions; outperforming TCF by $2.4\times$ (insert), $10.3\times$ (query), $39.2\times$ (delete), and GQF by $6.2\times$ (insert), $1.68\times$ (query), $2.1\times$ (delete).
  - BFS eviction optimization (Fig. 5, Fig. 6, p. 8-9, §5.4.1): Suppresses exponential tail eviction growth at $\ge 90\%$ load factor, boosting insertion throughput by up to $25\%$ over DFS.

## Limitations (author-stated vs. observed)
- Author-stated (p. 5, 10, §4.4, §6): (1) Vectorized non-atomic memory loads in queries risk torn reads if executed concurrently with insertions or deletions without external synchronization; (2) At extreme load factors, insertions can fail, requiring table rebuilds or secondary stashes; (3) FPR tuning is constrained to coarse, hardware-friendly bucket and fingerprint widths (e.g., 8, 16, 32 bits); (4) Negative queries face a compute bottleneck because both candidate buckets must be searched via SWAR bitwise arithmetic.
- Observed: Evaluates only raw AMQ operations in isolation; does not integrate the filter with vector embeddings, similarity search, or graph traversal pipelines.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
- Provides a high-throughput hardware accelerator building block for GPU-accelerated predicate filtering, demonstrating that dynamic Cuckoo filters can sustain tens of billions of queries per second on modern HBM3 architectures.
- Offers algorithmic insights (lock-free CAS concurrency, SWAR vectorization, BFS eviction) applicable to implementing fast dynamic membership filters in vector databases.
- Novelty check: no; this is a pure hardware acceleration study of standalone Cuckoo filter data structures on GPUs, with no vector graph traversal or predicate ANN search evaluated (p. 1-2, §1).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Abstract (p. 1) and Section 1 (p. 2) state deletion throughput is "258× (107×) higher than GQF (TCF)", but Section 5.2 (p. 7) text states "258× speedup over GQF and 107× over TCF", whereas elsewhere the parenthetical numbers map conversely between the two baselines.
- The query kernel uses non-atomic, non-coherent vectorized loads (§4.4, p. 5) which prevents safe concurrent reads and writes, limiting true dynamic multi-threaded streaming updates.

## Useful references to snowball (bibkeys or titles from its reference list)
- [10] Bin Fan, Dave G. Andersen, Michael Kaminsky, Michael D. Mitzenmacher. Cuckoo filter: practically better than bloom. CoNEXT 2014.
- [7] Alex D. Breslow and Nuwan S. Jayasena. Morton filters: faster, space-efficient cuckoo filters via biasing, compression, and decoupled logical sparsity. PVLDB 2018.
- [9] Peter C. Dillinger and Stefan Walzer. Ribbon filter: practically smaller than Bloom and Xor. arXiv:2103.02515, 2021.
- [13] Thomas Mueller Graf and Daniel Lemire. Xor filters: Faster and smaller than bloom and cuckoo filters. ACM JEA 2020.
- [19] Harald Lang, Thomas Neumann, Alfons Kemper, Peter Boncz. Performance-optimal filtering: Bloom overtakes Cuckoo at high throughput. PVLDB 2019.
- [20] Hunter McCoy, Steven Hofmeyr, Katherine Yelick, Prashant Pandey. High-performance filters for GPUs. PPoPP 2023.
- [25] Johanna Elena Schmitz, Jens Zentgraf, Sven Rahmann. Smaller and more flexible cuckoo filters. ALENEX 2026.
