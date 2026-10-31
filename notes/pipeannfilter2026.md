# pipeannfilter2026 — PipeANN-Filter: An Efficient Filtered Vector Search System on SSD
Authors / Year / Venue / DOI: Guo, Hao, Shu, Jiwu, Lu, Youyou / 2026 / not stated / none
Status: PRE
PDF: papers/pipeannfilter2026.pdf   Read fully: yes

## Problem addressed (p.)
Filtered approximate nearest neighbor search (filtered ANNS) over large-scale datasets residing on Solid-State Drives (SSDs) where both vectors and high-volume metadata attributes are stored on SSD (p. 1, §1). Existing strict in-filtering and pre-filtering require evaluating exact attributes from SSD for every encountered vector or neighbor, causing severe random I/O bottlenecks (<50 QPS throughput) or expensive attribute scans, while caching full metadata attributes in memory is memory-prohibitive (p. 1, 3-4, §1, §2.3).

## Method (core idea in ≤5 sentences) (p.)
PipeANN-Filter proposes speculative filtering: it explores a superset of valid vectors during graph search using lightweight in-memory probabilistic structures (e.g., Bloom filters for categorical labels, 1-byte quantized buckets for numerical ranges), deferring exact attribute verification to the final top-$k$ reranking stage (p. 1, 4-5, §3). Exact verification incurs minimal to zero additional SSD I/O by packing metadata attributes directly into the unaligned padding space of full-precision vector records fetched during reranking (p. 1, 4, §3). To maintain graph connectivity under low selectivity, each node record stores 10–20× additional 2-hop neighbors on SSD, repurposing false-positive explorations as bridge nodes across fragmented sub-graphs (p. 1-2, 5-6, §4.1). For label queries, it adopts a hybrid approach that pre-fetches SSD inverted lists for rare (low-selectivity) labels while relying on in-memory Bloom filters for frequent labels (p. 7, §4.3.1). A false-positive-aware analytical cost model dynamically routes queries between speculative pre-filtering, speculative in-filtering, and post-filtering based on estimated I/O and compute overhead (p. 5-7, §4.2, Table 1).

## Complexity / theoretical claims
- Analytical cost model (Table 1, p. 6, §4.2): No formal asymptotic theorems proven (`purely empirical cost model with analytical formulas`).
  - Pre-filtering: Est. I/O = $X_{pre} + L \frac{S_r}{p_{pre}}$, Est. Compute = $s \frac{N}{p_{pre}}$.
  - In-filtering (Low $s$, $s R_d / p_{in} \le R$): Est. I/O = $X_{in} + \frac{L}{s} \frac{R}{R_d} S_d$, Est. Compute = $(\frac{L}{s} \frac{R}{R_d} + \gamma \frac{L}{s}) R$.
  - In-filtering (High $s$, $s R_d / p_{in} > R$): Est. I/O = $X_{in} + \frac{L}{p_{in}} S_d$, Est. Compute = $\frac{L}{p_{in}} (R + \gamma R_d)$.
  - Post-filtering: Est. I/O = $\frac{L}{s} S_r$, Est. Compute = $\frac{L}{s} R$.
  - Total Cost = $\alpha \times \text{Est. I/O} + \beta \times \text{Est. Compute}$ ($\alpha=10, \beta=1$, relative compute cost $\gamma=0.05$).
  - Assumptions: Uniform distribution of valid vectors across the graph; independent attribute constraints (p. 6, 8, §4.2, §4.3.3).

## Filter type and selectivity regime handled (p.)
- Filter type: Categorical label filtering (Label, LabelAnd, LabelOr) using 4-byte in-memory Bloom filters per vector and inverted index lists (p. 7, 12, §4.3.1, §5.4); continuous range filtering using 1-byte quantized values (256 buckets) (p. 7-8, §4.3.2); Boolean combinations (AND/OR) (p. 8, §4.3.3).
- Selectivity regime handled: Arbitrary query selectivity from $0.001\%$ to $50\%$ (median $15.6\%$ on LAION100M) (p. 8, §5.1, Figure 2).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- On-SSD proximity graph based on Vamana (DiskANN layout with PipeANN traversal), storing full-precision vectors, out-neighbors ($R$), attributes, and dense 2-hop neighbors ($R_d$) on SSD, with in-memory PQ-compressed vectors and in-memory Bloom filters (p. 5, 8-9, §4.1, §5.1).
- Also evaluates against Milvus-HNSW, Milvus-IVFPQ, and Filtered-DiskANN (Filtered-Vamana) (p. 8-9, §5.1).

## Datasets, baselines, metrics (Table N)
- Datasets (p. 8, §5.1):
  - YFCC10M: 10M base, 100k query, 192-d uint8 vectors, average 10.8 labels/vector (BigANN benchmark).
  - YT5M (YouTube-8M): 5M base, 10k query, 1024-d float vectors, average 3.01 labels/vector.
  - LAION100M: 100M base, 10k query, 15 attributes (labels and image width range), 82,558 unique labels.
- Baselines (p. 8-9, §5.1): PipeANN-BaseFilter (heuristic pre/post routing at $1\%$ selectivity threshold), Milvus v2.6.11 (Milvus-HNSW and Milvus-IVF), Filtered-DiskANN (Filtered-Vamana).
- Metrics (p. 9, §5.1): Recall10@10, query latency (ms, single thread), query throughput (Op/s, multi-threaded SSD saturation), memory footprint (MB).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Throughput and latency at 0.9 recall:
  - On YT5M-LabelOr: PipeANN-Filter achieves $1.91\times$ throughput of PipeANN-BaseFilter, and latency is $72.7\%$ of BaseFilter (p. 9-10, §5.2, Fig. 5a, 6a).
  - On YFCC10M-LabelAnd: PipeANN-Filter achieves $1.71\times$ throughput of BaseFilter with $1.11\times$ latency; Milvus throughput remains $<150$ Op/s with latency $>10$ ms (p. 9-10, §5.2, Fig. 5b, 6b).
  - On LAION100M single-label: PipeANN-Filter achieves $1.44\times$ throughput and reduces average latency to $45.5\%$ of BaseFilter; Filtered-DiskANN fails to achieve recall $>0.8$ (p. 10, §5.3, Fig. 7).
  - On LAION100M Range filtering: PipeANN-Filter achieves $9.78\times$ throughput and reduces latency to $12.5\%$ of BaseFilter (p. 10-11, §5.3, Fig. 8b, 9b).
- False-positive exploration rate (p. 11, §5.4): ranges from $0.8\%$ to $69.4\%$, averaging $23.6\%$ (median $17.1\%$), reaching $63.5\%$ in LAION100M-1Label.
- Memory usage of probabilistic filters (Table 3, p. 12): 4-byte Bloom filters require 39 MB on YFCC10M ($3.5\%$ of SSD attribute index), 20 MB on YT5M ($28.9\%$), and 384 MB on LAION100M ($15.8\%$). Range 1-byte quantization consumes 96 MB ($12.5\%$).

## Limitations (author-stated vs. observed)
- Author-stated (p. 10-11, §5.2, §5.4): (1) Cost model overestimates I/O on LAION100M (up to $2.05\times$) due to early termination and non-uniform clustering of valid vectors; (2) Post-filtering cost model initially underestimates I/O at small candidate pool lengths $L$ because it omits the $\log(N)$ navigation hops; (3) In-filtering false-positive rate can reach up to $69.4\%$; (4) Under light SSD loads, speculative in-filtering has slightly higher latency than parallelized pre-filtering at high recall targets ($0.99$).
- Observed: Tailored specifically to SSD I/O minimization where DRAM is severely constrained; Bloom filters are held per vector (4 bytes/vector) in DRAM rather than embedded on graph edges.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
- Directly relevant to our project: provides the first working implementation of speculative in-filtering using in-memory Bloom filters during graph traversal.
- Offers an explicit analytical cost model quantifying the trade-off between false-positive rates ($1-p$), selectivity ($s$), and traversal overhead.
- Confirms our core hypothesis: bounded false-positive rates during traversal prevent early disconnection without requiring expensive exact predicate checks.
Novelty check: yes; in speculative in-filtering, in-memory Bloom filters (`is_member_approx`) are queried during graph traversal to filter out invalid neighbors before reading on-SSD node records (p. 1, 4, 6-7, §3, §4.1, §4.3.1, Figure 3b, Table 1).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Cost model relative compute weight $\gamma = 0.05$ (Table 1, p. 6) is configured empirically without a theoretical derivation.
- In Section 4.1 (p. 5), vector records store dense 2-hop neighbors that roughly double record size ($4056$ bytes to $8068$ bytes on LAION100M), yet the paper claims this extra read is ignored during pre- and post-filtering despite physical 4KB/8KB SSD page boundaries.

## Addendum: Cost-Model Parameters & Bloom Filter Mechanics
1. **Full list of cost-model parameters (Table 1, p. 6, §4.2)**:
   - $N$: total base vectors in dataset (p. 6, Table 1).
   - $s$: estimated query selectivity (p. 6, Table 1).
   - $p_{pre}, p_{in}$: precision of pre-filtering / in-filtering; false-positive rate is explicitly defined as $1 - p$ (p. 6, Table 1; p. 7, §4.3.1).
   - $X_{pre}, X_{in}$: number of SSD pages read for initial batched attribute index scans (p. 6, Table 1).
   - $R$: out-degree in standard proximity graph (p. 6, Table 1).
   - $R_d$: out-degree in densified graph storing 2-hop neighbors (p. 6, Table 1).
   - $S_r$: record size in standard graph (p. 6, Table 1).
   - $S_d$: record size in densified graph with 2-hop neighbors (p. 6, Table 1).
   - $\gamma$: relative compute cost of `is_member_approx` compared to one vector distance computation (default $\gamma = 0.05$) (p. 6, Table 1).
   - $L$: search candidate pool size parameter / target top-$L$ candidates (p. 6, §4.2).
   - $\alpha, \beta$: linear cost model weights balancing SSD I/O page reads vs compute distance comparisons (default $\alpha = 10, \beta = 1$) (p. 7, §4.2).
   - *Filter size / bits per entry representation*: In memory, each vector maintains a lightweight Bloom filter allocated at a fixed 4 bytes (32 bits) per vector (p. 11, §5.4). Mathematical Bloom false-positive rate directly parameterizes precision $p_{in}$ via $1 - p_{in}$ (p. 6, Table 1; p. 7, §4.3.1).

2. **Structure tested by the Bloom filter & behavior on a false positive**:
   - *Structure tested*: For categorical label constraints, each base vector's in-memory Bloom filter encodes its assigned set of categorical labels. During graph traversal, `is_member_approx` tests whether candidate neighbor vectors contain queried labels for `LabelOrSelector` (after checking pre-merged rare label posting lists) (p. 7, §4.3.1).
   - *What happens on a false positive*:
     - In speculative in-filtering, an invalid neighbor falsely passing the Bloom filter is admitted into the graph traversal candidate pool (p. 6, §4.2).
     - At low selectivity ($s R_d / p_{in} \le R$), false-positive nodes act as "bridge edges" preserving traversal connectivity across otherwise fragmented matching sub-graphs, preventing search premature termination (p. 6, §4.2).
     - At high selectivity ($s R_d / p_{in} > R$), false positives consume slots in the candidate pool, expanding the required pool size to $L / p_{in}$ (p. 6–7, §4.2).
     - Full node records (including raw label attributes) are read from SSD, and all candidates undergo exact verification against the query predicate before final top-$k$ results are returned; non-matching vectors are pruned during exact verification (p. 6, §4.1; p. 7, §4.3.1).

## Useful references to snowball (bibkeys or titles from its reference list)
- [4] Burton H. Bloom. Space/time trade-offs in hash coding with allowable errors. CACM 1970.
- [11] Bin Fan, Dave G. Andersen, Michael Kaminsky, Michael D. Mitzenmacher. Cuckoo Filter: Practically Better Than Bloom. CoNEXT 2014.
- [15] Siddharth Gollapudi et al. Filtered-DiskANN: Graph Algorithms for Approximate Nearest Neighbor Search with Filters. WWW 2023.
- [29] Liana Patel, Peter Kraft, Carlos Guestrin, Matei Zaharia. ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data. SIGMOD 2024.
- [49] Huanchen Zhang et al. SuRF: Practical Range Query Filtering with Fast Succinct Tries. SIGMOD 2018.
- [50] Chaoji Zuo, Miao Qiao, Wenchao Zhou, Feifei Li, Dong Deng. SeRF: Segment Graph for Range-Filtering Approximate Nearest Neighbor Search. SIGMOD 2024.
