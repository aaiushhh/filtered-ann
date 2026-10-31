# kraska2018learned — The Case for Learned Index Structures
Authors / Year / Venue / DOI: Tim Kraska, Alex Beutel, Ed H. Chi, Jeffrey Dean, Neoklis Polyzotis / 2018 / SIGMOD 2018 / 10.1145/3183713.3196909
Status: PUB
PDF: papers/kraska2018learned.pdf   Read fully: yes

## Problem addressed (p.)
Replacing general-purpose database index structures (B-Trees, Hash-maps, and Bloom filters) that do not exploit data distributions with machine learned models that approximate the underlying cumulative distribution function (CDF) or classification boundary, reducing memory footprint and lookup latency (p. 1–3).

## Method (core idea in ≤5 sentences) (p.)
The paper posits that indexes are predictive models: a B-Tree predicts record positions in a sorted array, a Hash-map predicts positions in an unsorted array, and a Bloom filter predicts set membership (p. 1–3). For range indexing, it introduces the Recursive Model Index (RMI), a multi-stage hierarchy of lightweight models (e.g., small neural networks or linear models) where each stage predicts which model in the next stage to invoke, narrowing the search window to bounded error intervals corrected by local search (p. 5–7). For existence indexing, it introduces learned Bloom filters that frame membership as a binary classification problem: a machine learning classifier (e.g., RNN) predicts membership above a threshold $\tau$, while an auxiliary backup/overflow Bloom filter stores false negatives to preserve the zero false negative rate guarantee (p. 15–17). An alternative existence index uses classifier outputs to generate learned hash positions within a bitmap (p. 17).

## Complexity / theoretical claims
- Statement, assumptions, theorem number, page: `none stated`. (The paper is primarily empirical; informal arithmetic precision gain comparisons against B-Tree cycle costs are given in §2.1 (p. 4), and the compound false positive rate formula $FPR_O = FPR_\tau + (1 - FPR_\tau)FPR_B$ is given in §5.1.1 (p. 16–17)).

## Filter type and selectivity regime handled (p.)
Learned Bloom filter combining a binary classification model (character-level RNN/GRU) with a standard overflow Bloom filter for false negatives (§5.1.1, p. 16–17), and Bloom filters using discretized model-hashes (§5.1.2, p. 17; Appendix E, p. 30). Selectivity regime handled: `not stated` (evaluates binary point existence filtering on URLs, not range or metadata predicate selectivity queries).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
Recursive Model Index (RMI) hierarchy and learned Bloom filter (§3, p. 5–10; §5, p. 15–17). Proximity graphs (HNSW, IVF, Vamana) are not used (only mentioned in related work §6, p. 19).

## Datasets, baselines, metrics (Table N)
- Datasets:
  - Range Index (§3.7.1, p. 11): Weblogs (200M timestamp entries), Maps (200M OpenStreetMap longitude coordinates), Lognormal (190M unique values, $\mu=0, \sigma=2$), String data (reverse web-paths) (§3.7.2, p. 13).
  - Existence Index (§5.2, p. 17): Google Transparency Report phishing blacklist (1.7M unique URLs) with negative sets of random and whitelisted URLs.
  - Hash-map (§B, p. 23; Table 1, p. 28): 20-byte records on lognormal data.
- Baselines: Cache-line optimized B-Tree (dense pages, 100% fill factor), FAST (SIMD-optimized B-Tree), Fixed-size B-Tree with interpolation search, standard Bloom filter, Commercial Cuckoo hash-map (§3.7, p. 11–12; §5.2, p. 17; Table 1, p. 28).
- Metrics: Lookup time (ns), model execution time (ns), index size / memory footprint (MB), false positive rate (FPR), false negative rate (FNR), number of collisions (§3.7, p. 10–12; §5.2, p. 17–18; Table 1, p. 28; Figure 4, p. 10; Figure 10, p. 18).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Range index lookup speed and size (Figure 4, p. 10): On Weblogs, B-Tree (page size 128) achieves 265 ns lookup at 12.8 MB; 2-stage RMI (100k second-stage models) achieves 193 ns lookup (1.37× speedup) at 1.5 MB (8.5× space reduction). On Maps, B-Tree (page size 128) achieves 248 ns (12.8 MB); RMI (10k models) achieves 148 ns (1.68× speedup) at 0.1 MB (128× smaller).
- Hash map collision reduction (Figure 8, p. 15; Table 1, p. 28): Learned hash functions reduce collisions by up to 77% over MurmurHash3; in Table 1 (p. 28), in-place chained hash-map with learned hash functions achieves 35 ns lookup time at 100% space utilization vs. 90 ns and 95% utilization for Commercial Cuckoo.
- Learned Bloom filter memory reduction (§5.2, p. 17; Figure 10, p. 18): Standard Bloom filter at 1% FPR requires 2.04 MB; learned Bloom filter (16-d GRU, 32-d character embeddings, 0.0259 MB model size, 55% FNR) plus overflow Bloom filter uses 1.31 MB (36% reduction). At 0.1% overall FPR (76% FNR), size is reduced from 3.06 MB to 2.59 MB (15% reduction). Discretized model hash in Appendix E (p. 30) reduces memory by 41% at 1% FPR (1.19 MB) and 27.4% at 0.1% FPR (2.21 MB).

## Limitations (author-stated vs. observed)
- Author-stated: Evaluated primarily on static, read-only in-memory dense sorted arrays; writes require buffering in delta-indexes with periodic retrains (§2, p. 4; §D.1, p. 27); ML accelerator invocation latency (2–3 $\mu$s) requires amortization/batching (§7, p. 20); learned Bloom filters depend on non-key query distributions and may degrade under covariate shift (§5.1, p. 16; §5.2, p. 17).
- Observed: No multi-dimensional vector indexing or similarity search is implemented; learned Bloom filter evaluation does not evaluate traversal overhead or membership check latency in graph-based similarity search.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Foundational paper proposing learned Bloom filters (classifier cascade with backup Bloom filter) to reduce existence filter footprint. Highly relevant to our filter structure design and false positive rate cost modeling ($FPR_O = FPR_\tau + (1 - FPR_\tau)FPR_B$).
Novelty check: No. The paper evaluates standalone scalar key-value lookup and string existence filtering on point queries, without proximity graph traversal or in-traversal predicate checking (p. 1–3, 15–18).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Page numbering note: The source text has 30 pages (arXiv:1712.01208v3 extended version with appendices), whereas the conference proceedings version in SIGMOD 2018 is condensed into 14 pages; page locators in this note cite the extended full-text version.

## Useful references to snowball (bibkeys or titles from its reference list)
- Bloom (1970) [22]: Space/Time Trade-offs in Hash Coding with Allowable Errors
- Mitzenmacher (2018): Personal communication acknowledged regarding learned Bloom filter FPR analysis (p. 17, 20)
- Athanassoulis & Ailamaki (2014) [13]: BF-tree: Approximate Tree Indexing
- Kim et al. (2010) [44]: FAST: Fast Architecture Sensitive Tree Search on Modern CPUs and GPUs
- Rao & Ross (1999) [58]: Cache-conscious indexing for decision-support in main memory (CSB+-Tree)
