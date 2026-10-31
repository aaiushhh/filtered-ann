# mitzenmacher2017adaptive — Adaptive Cuckoo Filters
Authors / Year / Venue / DOI: Michael Mitzenmacher, Salvatore Pontarelli, Pedro Reviriego / 2017 / ACM Journal of Experimental Algorithmics (JEA) 2020 / ALENEX 2018 / 10.1145/3339504
Status: PUB
PDF: papers/mitzenmacher2017adaptive.pdf   Read fully: yes

## Problem addressed (p.)
In repetitive query workloads (such as network flow tracking), non-member elements that trigger false positives continue to generate repeated false positives on subsequent queries, degrading the empirical false-positive rate (FPR) well beyond the nominal false-positive probability (p. 1–2). Existing approximate membership filters cannot adaptively eliminate false positives without introducing false negatives (e.g., retouched Bloom filters) or requiring complex offline profiling (p. 2).

## Method (core idea in ≤5 sentences) (p.)
The paper introduces the Adaptive Cuckoo Filter (ACF), which dynamically eliminates false positives upon detection by altering stored fingerprints without creating false negatives (p. 1–3, §1). Unlike standard cuckoo filters that use partial-key hashing, ACF pairs an in-memory fingerprint cuckoo filter with a secondary cuckoo hash table storing the original keys (p. 3, §1; p. 6, §3). In Variant 1 ($d=4$ tables, $c=1$ cell/bucket), each cell maintains $s$ hash selector bits $\alpha$; when a false positive is detected, $\alpha$ is incremented modulo $2^s$ to select an alternative fingerprint hash function $f_\alpha(y)$ (p. 7, §3.1). In Variant 2 ($d=2$ tables, $c=4$ cells/bucket), each cell slot $j \in \{1..4\}$ within a bucket uses a distinct hash function $f_j$; upon a false positive in cell $j$, element $y$ is swapped with another element $z$ in cell $k \neq j$ within the same bucket, changing both fingerprints to $f_j(z)$ and $f_k(y)$ with zero selector bit overhead (p. 10–11, §3.2).

## Complexity / theoretical claims
- Analytical workload cost model: Total query cost $p_1((q_1 + (1-q_1)q_2)c_P + (1-q_1)(1-q_2)c_F) + p_2 c_I + p_3 c_D$, where $q_2$ is the false-positive rate, $c_P$ is the positive verification cost in secondary memory, and $c_F$ is the filter rejection cost (p. 6–7, §3).
- Markov model for Variant 1: For a bucket storing an item with $\zeta$ non-member items mapping to it, the stopping probability after $k$ false positives is $P_{\text{stop}}(k) = (1 - e^{-\mu})^k e^{-\mu}$ where $\mu = \zeta 2^{-a}$ (p. 8–9, §3.1).
- Asymptotic bucket false-positive rate $F(\zeta, n)$: Closed form given by:
  $F(\zeta, n) = \sum_{i=1}^{2^s-1} (1-e^{-\mu})^i e^{-\mu} \frac{i}{n} + \sum_{Z_0..Z_{2^s-1} > 0} (\prod_{i=0}^{2^s-1} \frac{e^{-\mu}\mu^{Z_i}}{Z_i!}) \frac{2^s}{\sum_{i=0}^{2^s-1} \frac{\zeta}{Z_i}}$ (p. 9).
- Total table expected false-positive rate $F$: Derived via Poisson mixture over bucket loads $\zeta$ and query counts $j$ (p. 9).
- Markov chain for Variant 2: Formulated across 24 permutation states of 4 cells, solved via probability sampling over 16-dimensional vector $\hat{Z}$ (p. 11–12, §3.2).
- Statement, assumptions, theorem number, page: none stated as formal numbered theorems; derived via Markov chain equilibrium models and validated empirically within $<5\%$ error (p. 8–10, 15, §3, §4.1).

## Filter type and selectivity regime handled (p.)
- Filter type: Adaptive Cuckoo Filter (Variant 1: $d=4, c=1$ with $s \in \{1,2,3\}$ selector bits; Variant 2: $d=2, c=4$ with intra-bucket cell swaps) (p. 7, 10, §3).
- Selectivity regime handled: Designed for repeated query workloads where non-member items are repeatedly queried ($n_e \in [10, 1000]$ queries per item); evaluated across non-member to member ratios $A/S \in [1, 100]$ and fingerprint budgets $a \in \{8, 12, 16\}$ bits per cell (p. 13–14, §4.1).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
- Index structure used: other (multi-table cuckoo hash table paired with fingerprint cuckoo filter; no proximity graph or vector index) (p. 4–6, §2, §3).

## Datasets, baselines, metrics (Table N)
- Datasets: Synthetic workloads with uniform query frequencies ($n_e \in \{10, 100, 1000\}$, $A/S \in [1, 100]$, 131,072 total cells) (p. 13–14, §4.1); Real packet traces from CAIDA 2014 (three 60-second 5-tuple traces: equinix-chicago.dirA [18.5M packets, 691K flows], equinix-chicago.dirB [14.6M packets, 632K flows], equinix-sanjose.dirA [37.4M packets, 2.31M flows]) (p. 16, §4.2).
- Baselines: Standard Cuckoo Filter ($d=4, c=1$) at 95% occupancy (p. 13, §4.1).
- Metrics: False-positive rate (%) across $A/S$ ratio (Figs. 1–6, p. 14–17); deviation between theoretical Markov model estimates and simulation results (%) (p. 15, §4.1).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Theoretical model precision: Theoretical Markov estimates match simulation results with error in most cases "well below 5%" (p. 15, §4.1).
- Synthetic evaluation:
  - Variant 2 ($d=2, c=4$) outperforms Variant 1 ($d=4, c=1$) in almost all cases because it avoids dedicating bits to hash selectors (p. 14, §4.1; Figs. 1–3).
  - For 12 and 16 bits per cell, ACFs outperform standard cuckoo filters across all tested $A/S$ ratios from 1 to 100 (p. 14, §4.1; Figs. 2, 3).
  - For small $A/S$ ratios and large $n_e$, false-positive rate reductions reach several orders of magnitude (p. 15, §4.1).
- Real CAIDA packet traces (Figs. 4, 5, 6, p. 16–17):
  - ACF consistently reduces false-positive rates compared to standard cuckoo filters across all three CAIDA traces for 8, 12, and 16 bits per cell (p. 16–17, §4.2).
  - Even at 8 bits per cell, ACF reduces FPR across all $A/S$ ratios on real traces due to heavy-tailed traffic skewness, eliminating repeat errors on large flows (p. 17, §4.2; Fig. 4).
  - No numerical tables reported in the paper (all experimental results presented in Figures 1–6).

## Limitations (author-stated vs. observed)
- Author-stated: ACF requires access to complete original data stored in a secondary/slower table to verify false positives and retrieve keys for re-fingerprinting (p. 3, 6, §1, §3); at 8 bits/cell with very large $A/S$ ratios and uniform traffic, ACF can cycle through hash selectors without suppressing false positives (p. 15, §4.1); does not support inter-bucket element relocation during adaptation (p. 12–13, §3.3).
- Observed: Tailored strictly to 1D network flow classification; does not address multi-dimensional vector search, distance calculations, or graph traversal.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Formulates an explicit two-stage query cost model balancing filter check latency against primary verification costs ($p_1((q_1 + (1-q_1)q_2)c_P + \dots)$), directly applicable to HNSW graph search. Demonstrates how multi-slot cuckoo buckets can eliminate false positives via zero-space permutation swaps, providing a mechanism for adaptive predicate filtering. Informs our analytical cost model regarding the trade-off between filter false-positive rate and expensive downstream vector distance computations.
Novelty check: Novelty check: no (investigates standalone packet classification and pre-filtering to prevent accesses to slow secondary storage in network routers; §1, p. 1–3).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- Page 17 refers to the first variant as "(d = 2, c = 1)", whereas throughout earlier sections the first variant is defined as $d = 4, c = 1$ (p. 7, 13).
- The baseline cuckoo filter comparison in Section 4 evaluates only $d=4, c=1$ and omits the standard $d=2, c=4$ cuckoo filter of Fan et al., arguing that $d=4, c=1$ achieves a superior false-positive rate (p. 13, §4.1).

## Useful references to snowball (bibkeys or titles from its reference list)
- Donnet, B., Baynat, B., and Friedman, T. (2006). Retouched bloom filters: allowing networked applications to trade off selected false positives against false negatives. CoNEXT 2006.
- Erlingsson, U., Manasse, M., and Mcsherry, F. (2006). A cool and practical alternative to traditional hash tables. WDAS 2006.
- Kirsch, A., Mitzenmacher, M., and Wieder, U. (2009). More robust hashing: Cuckoo hashing with a stash. SICOMP 39(4), 1543–1561.
- Pontarelli, S., Reviriego, P., and Maestro, J. A. (2016). Parallel d-Pipeline: a Cuckoo Hashing Implementation for Increased Throughput. IEEE Trans. Computers 65(1), 326–331.
