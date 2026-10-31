# superseding2019learning — Superseding Traditional Indexes by Orchestrating Learning and Geometry
Authors / Year / Venue / DOI: Vinciguerra, Giorgio, Ferragina, Paolo, Miccinesi, Michele / 2019 / not stated / none
Status: PRE
PDF: papers/superseding2019learning.pdf   Read fully: yes

## Problem addressed (p.)
Resolving the space-time limitations of traditional indexing structures (such as B-trees and CSS-trees, which take $O(n)$ space) and early learned indexes (such as RMI, which rely on heuristic DAG architectures without worst-case guarantees or principled bounds on lookup time and space) (p. 1–4).

## Method (core idea in ≤5 sentences) (p.)
The paper proposes the Piecewise Geometric Model index (PGM-index), which casts dictionary indexing into the geometric problem of covering 2D points $(k_i, i)$ with a minimal number of $\epsilon$-approximate linear segments computed via optimal streaming algorithms in $O(n)$ time (p. 1–2, 6–7). To index the resulting $m$ models, it introduces the Recursive PGM-index, recursively repeating the geometric modeling process on the first keys of each segment until a single root model remains, creating a tree with constant node size and variable, data-dependent fan-out $c \ge 2\epsilon$ (p. 11–14). It additionally designs a Distribution-Aware PGM-index that adapts to query access frequencies to achieve biased-search query bounds, as well as a multicriteria optimization framework that dynamically tunes the error parameter $\epsilon$ to meet target time or space constraints (p. 1–2, 15–18).

## Complexity / theoretical claims
- Theorem 1 (§2.1.1, p. 7): Given a sequence of $n$ 2D points and max error $\epsilon \ge 0$, an optimal streaming algorithm computes the minimal number of $\epsilon$-approximate linear segments in $O(n)$ time and $O(1)$ space.
- Theorem 5 (§2.3, p. 11): The 2-level PGM-index takes $\Theta(m)$ space and answers membership, successor, and predecessor queries in $O(t_{index}(m) + \log \epsilon)$ time, where $m \le n/(2\epsilon)$ is the number of models.
- Theorem 6 (§2.3, p. 13–14): The Recursive PGM-index takes $\Theta(m)$ space and answers queries in $O(\log m)$ time in RAM, and $O(\log_c m \cdot \log(\epsilon/B))$ I/Os in the External Memory (EM) model with fan-out $c \ge 2\epsilon$ and page size $B$ (yielding $O(1)$ best-case I/Os when $c \gg 2\epsilon$; Table 1, p. 15).
- Theorem 7 (§3, p. 15): The Distribution-Aware PGM-index takes $O(m)$ space and answers queries in $O\left(\frac{1}{H}\sum_{k \in D} p_k \log \frac{1}{p_k}\right)$ expected time where $p_k$ is the access probability of key $k$ and $H$ is the entropy.
- Lemma 2–4 (§2.1.2, p. 8–9): Provides bounds on the average strip and segment coverage under geometric and coordinate regularity assumptions.

## Filter type and selectivity regime handled (p.)
`not stated` (the paper addresses scalar 1D dictionary predecessor, successor, and point search; no probabilistic membership filters like Bloom/Cuckoo/Xor or selectivity regimes are considered).

## Index structure used (HNSW / IVF / Vamana / other) (p.)
PGM-index (Recursive PGM-index, Piecewise Geometric Model) (§1, p. 1–2; §2.3, p. 11–14). Proximity graphs (HNSW, IVF, Vamana) are not used.

## Datasets, baselines, metrics (Table N)
- Datasets (§5, p. 20):
  - Web logs: ~715M timestamps of web server requests.
  - Longitude: ~166M point-of-interest coordinates from OpenStreetMap.
  - IoT: ~26M timestamps from building IoT sensors.
- Baselines: B+-tree (stx::btree library, page sizes 256 B to 16 KiB), CSS-tree (Cache-Sensitive Search tree, page sizes 128 B to 16 KiB), RMI (10K to 400K second-stage models) (§5.2, p. 23; Figure 11, p. 23).
- Metrics: Index space (MiB/KiB), query time (ns), number of segments $m$, Mean Absolute Error (MAE), construction time (§5, p. 20–25; Table 1, p. 15; Figure 11, p. 23).

## Key results (numbers exactly as reported, with Table/Fig locator)
- Space reduction over CSS-tree (Figure 11(right), p. 23; §5.2, p. 23): On Web logs, the fastest CSS-tree (128-byte page size) occupied 341 MiB; Recursive PGM-index with $\epsilon=128$ achieved matching query performance while occupying only 4 MiB (an 82.7× space reduction).
- Space reduction over B+-tree (Figure 11(right), p. 23; §5.2, p. 23): The fastest B+-tree (256-byte page size) occupied 874 MiB; Recursive PGM-index with $\epsilon=4096$ achieved matching query latency while occupying only 87 KiB (a 4 orders of magnitude space reduction).
- Model compression (Footnote 5, p. 14; Figure 8, p. 20): On the 715M Web logs dataset, PGM-index achieves $m = 423\text{K}$ segments at $\epsilon=64$, compressing the index by three orders of magnitude.
- Predictability vs. RMI (§5.2, p. 25): At $\sim$32K segments ($\epsilon=512$), PGM-index had MAE $226 \pm 139$, whereas RMI with the same number of leaf models had MAE $892 \pm 3729$ (3.9× higher with high error variance).

## Limitations (author-stated vs. observed)
- Author-stated: Keys are assumed stored uncompressed in a contiguous sorted array $A$ (p. 25, §6); static dictionary setting without concurrent insertions/deletions (p. 2, 25); hybrid models incorporating small neural networks offered only up to 11% segment reduction without improving overall memory footprint (§5.1.2, p. 23).
- Observed: Purely 1D scalar indexing; does not support high-dimensional metric vector spaces, multi-attribute predicate filtering, or graph traversals.

## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
Introduces the PGM-index, establishing provable worst-case $O(\log m)$ query time and $\Theta(m)$ space complexity bounds for learned piecewise linear index structures. Informs the theoretical modeling of learned index hierarchies and cost models, but does not address vector graph traversal.
Novelty check: No. The paper addresses 1D dictionary indexing (successor, predecessor, point queries) over sorted scalar arrays using recursive linear models without proximity graph traversal or membership filtering (p. 1–4, 11–14).

## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
- None. (Preprint version on arXiv; published later in PVLDB 2020 as "The PGM-index: a new approach to the design of a learned index", recorded as PRE with venue `not stated` in tools/bib_meta.json).

## Useful references to snowball (bibkeys or titles from its reference list)
- Kraska et al. (2018) [27]: The Case for Learned Index Structures (SIGMOD 2018)
- Galakatos et al. (2018) [16]: FITing-Tree: A Data-Aware Index to Solve the Read/Write Trade-Off (A-tree / FITing-tree)
- Rao & Ross (1999) [34]: Cache-conscious indexing for decision-support in main memory (CSS-tree)
- O'Rourke (1981) [32]: An on-line algorithm for fitting straight lines between data ranges
- Idreos et al. (2018) [22]: The data calculator: Data structure design and cost synthesis from first principles (SIGMOD 2018)
