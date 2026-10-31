# EXPERIMENTS.md — Experiment Plan for the Filtered-ANN Project

Read this together with AGENTS.md. All AGENTS.md hard rules still apply (no fabrication, log everything, stop at gates, never touch `paper/`). This file adds rules for running experiments.

## 1. Purpose

Produce a complete, reproducible evidence base so the human can write ONE of:
- **Paper A** (method + theory): in-traversal approximate filters (Bloom/Cuckoo/Xor) with a cost model.
- **Paper B** (analysis): cost model and empirical study of pre-/post-/in-traversal filtering, including negative results.
- **Paper C** (survey with empirical appendix): taxonomy plus measured comparison of filtering strategies.

You (the agent) do NOT decide which paper. You run experiments, store raw results, and report numbers. The human decides.

## 2. Hard rules for experiments

1. Every number in any report must trace to a raw file in `experiments/results/`. No number from memory, from notes, or from another paper.
2. Formulas from papers may be used only from the PDF-verified list in `FINAL_FIX_PASS_report.md` and `AUDIT_report.md`. Never use a formula from `notes/` that is not in those reports.
3. No interpretation. Reports contain tables, plots, and a list of anomalies. Do not write "this shows", "we conclude", or "surprisingly".
4. No cherry-picking. Store every run, including failed and null results. Never overwrite or delete raw results; use new run IDs.
5. Fixed parameters per gate. Do not change a grid mid-gate. If a parameter proves infeasible, log it, skip that cell, and say so in the gate report.
6. Time-box every installation or reproduction of third-party code to one attempt-session. If it fails, log the exact error and move on. Never fake a result or substitute another system silently.
7. If a hardware counter or tool is unavailable (for example `perf` on Windows), write `not available` in the results. Do not estimate it.
8. Stop at each gate and post a report artifact. Do not start the next gate without approval.

## 3. Environment and measurement protocol

- Prefer WSL2/Linux (gcc, `-O3 -march=native`, `perf` if the kernel allows). If only Windows/MSVC is available, say so and mark counters `not available`.
- Single-thread measurements, pinned to one core where the OS allows. High-performance power plan, other applications closed.
- Per configuration: 1 warm-up run (discarded) + 5 measured repeats. Report median and IQR. Randomize the order of strategies across repeats to avoid thermal drift.
- If the coefficient of variation of any cell exceeds 5%, rerun that cell once and flag it.
- Fixed seeds, recorded. Same query set across strategies.
- Record in `env.json`: CPU model, cores, L1/L2/L3 sizes, RAM, OS, compiler and flags, library versions and commits (hnswlib, FAISS, Python, numpy), git commit of this repo, dataset checksums.

## 4. Folder layout

```
experiments/
  harness/            C++ source + CMake + Python bindings/driver
  data/               gitignored; data/MANIFEST.json holds URLs + SHA256
  results/<exp_id>/   config.yaml, raw.csv, env.json, log.txt
  analysis/           scripts that read raw.csv only and write figures/tables
  figures/            generated only by analysis/ scripts
  RESULTS_INDEX.csv   run_id, exp_id, date, git_hash, config_hash, raw_path, status
```

Result row schema (one row per configuration per repeat), `raw.csv`:
`run_id, exp_id, dataset, N, d, predicate_type, correlation, sigma_target, sigma_actual, strategy, structure, bits_per_entry, M, efC, efS, k, repeat, recall_at_10, valid_fraction_at_10, qps, lat_p50_us, lat_p95_us, lat_p99_us, dist_comps_mean, nodes_visited_mean, filter_probes_mean, filter_fp_mean, filter_bytes, setup_s, seed, timestamp, notes`

Per-query latency and distance-computation records are stored as parquet only for the operating point (smallest efS reaching recall >= 0.95), gitignored, with checksum in `RESULTS_INDEX.csv`.

## 5. Gates and experiments

### GATE E0 — Environment, data, ground truth, harness correctness

1. Write `env.json`; run a timer-noise test (empty-loop benchmark x30, report CV).
2. Download SIFT1M and GIST1M from the official source or the ann-benchmarks HDF5 mirror. Record exact URL and SHA256. (Optional, if time allows: GloVe-100 angular.)
3. Metadata generation (seeded, stored as .npy with checksum):
   - **Independent labels:** K categories, uniformly random per vector.
   - **Cluster-correlated labels:** k-means (K clusters) on the vectors; label = cluster id.
   - K = 1/sigma for sigma in {0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 0.5}.
   - Query predicate modes: `random` (random label), `near` (label of the cluster containing the query's unfiltered nearest neighbor), `far` (label of a cluster far from the query). Record sigma_actual.
4. Exact filtered ground truth (top-10 per query and predicate) by brute force; verify on 100 queries with a second implementation (FAISS flat + mask).
5. Harness correctness tests (all must pass before E1; report pass/fail):
   - post-filter with efS = N gives recall 1.0;
   - an AMQ variant configured as an exact set returns identical results to the exact variant;
   - measured false-positive rate within tolerance of the PDF-verified theoretical formula;
   - fixed seed reproduces identical results.

### GATE E1 — Filter-structure microbenchmarks (no index)

Purpose: measure the cost of the filter check alone, across structure sizes (cache hierarchy).

- Structures: inline attribute array (uint32), N-bit bitmap, hash set of IDs (open addressing), standard Bloom, blocked Bloom (512-bit blocks), Cuckoo filter (8/12/16-bit fingerprints), Xor filter (8/16-bit). Use existing reference implementations where available; record their versions.
- N in {1e6, 1e7, 1e8, 1e9}. Skip any cell whose memory exceeds 50% of RAM, and say so.
- sigma in {0.001, 0.01, 0.1, 0.5}; Bloom bits per entry in {6, 8, 10, 12, 16}.
- Probe patterns: uniform random IDs; batches of 32 IDs (neighbor-list-like).
- Per cell: ns per probe (10^7 probes), measured false-positive rate (10^7 non-member probes), memory bytes, build time.

Report: tables plus the plot data for ns/probe vs structure bytes. Also report these boolean checks (do not interpret): does any AMQ structure have ns/probe at least 20% lower than the best exact structure at measured FPR <= 2%? In which (N, sigma) cells?

### GATE E2 — Baseline filtered-search strategies on HNSW

Index: hnswlib, M=16, efConstruction=200; efSearch in {16, 32, 64, 128, 256, 512, 1024, 2048}; k=10; the dataset's standard query set. Datasets: SIFT1M, GIST1M.

Predicate types:
- **P1** categorical equality (labels from E0).
- **P3** set membership: allowed ID set of size sigma*N, both random and cluster-clustered; two modes: `static` (set built once, shared) and `per_query` (set built per query; report build time separately and combined).

Strategies:
- **S1** pre-filter: exact SIMD scan over the matching subset.
- **S2** post-filter: standard search, efS doubled until k valid results or cap 16384.
- **S3** hnswlib filter functor (admission-only; traversal continues through non-matching nodes).
- **S4** exact in-traversal pruning: forked hnswlib header, filter checked before distance computation, non-matching neighbors not added to the candidate set. Log the diff against upstream.
- **S5** ACORN official code (time-boxed; skip and log if it cannot be built).
- **S6** Bloom (blocked) as in S4, bits per entry in {8, 10, 12}.
- **S7** Cuckoo (12-bit) as in S4.
- **S8** Xor (8 and 16-bit) as in S4.
- For S6-S8 run two result modes: `verified` (final exact check drops false positives; may return fewer than k) and `unverified` (report valid_fraction_at_10).

Instrument: distance computations, nodes visited, filter probes, filter false positives encountered.

Operating-point table (script-generated): for each cell and strategy, the smallest efS reaching recall >= {0.90, 0.95, 0.99}, with QPS and distance computations at that point, or `not reached`. No interpolation.

Report at the gate: operating-point table, QPS-vs-recall data per cell, list of anomalies, and these boolean checks (do not interpret): in how many cells does S6-S8 reach recall >= 0.95 with QPS at least 10% above the best of S3/S4, with non-overlapping IQR across 5 repeats? Which predicate types and sigma ranges?

**STOP after E2. The human decides whether E3-E5 are worth running.**

### GATE E3 — Approximate-filter parameter study (run only if approved)

- Measured FPR vs bits per entry for Bloom, blocked Bloom, Cuckoo, Xor, next to the theoretical curve (formulas copied from the PDF-verified papers).
- For S6-S8: wasted distance computations per query vs measured FPR; recall and valid_fraction vs bits per entry, at sigma in {0.001, 0.01, 0.1} and both correlation modes.
- Filter memory bytes vs sigma, bitmap vs AMQ.

### GATE E4 — Cost-model validation data (run only if approved)

- **M1 hops vs N:** subsample N in {1e4, 3e4, 1e5, 3e5, 1e6}; unfiltered HNSW; record mean nodes visited and distance computations at efS=64 and at recall >= 0.95. Store fits of log N, power law N^a and linear; report parameters, R^2 and residuals only.
- **M2 efS vs 1/sigma (post-filter):** smallest efS reaching recall >= 0.95 against 1/sigma, for each correlation mode; fit efS ~ a*(1/sigma)^b with bootstrap CI over queries.
- **M3 crossover:** sigma at which S1 QPS equals the best non-S1 strategy at recall >= 0.95, per dataset and correlation mode, with bootstrap CI. Tabulate next to the crossover predicted by the PDF-verified ACORN and SIEVE formulas; do not tune the formulas.
- **M4:** slope of wasted distance computations vs FPR from E3, with CI.

### GATE E5 — Optional extensions (time-boxed; skip and log on failure)

- FAISS HNSW with IDSelector filtering on the same workload.
- Official Filtered-DiskANN or other open-source filtered systems if installable on this machine.
- N = 1e7 run of E2 (S1-S4, S6) if RAM >= 32 GB, using an official dataset subset.
- Reproduction-status table: system | installed yes/no | ran yes/no | error text | version.

### Survey-support outputs (no experiments, no prose)

From `matrix.csv` and E2/E5 results: CSV tables of method | predicate types supported | strategy | formal complexity yes/no | open code url | datasets used | reproduced yes/no.

## 6. Deliverables map (for the human)

| Item | Source | Raw file |
|---|---|---|
| F1 ns/probe vs structure size, per structure | E1 | `E1/raw.csv` |
| F2 recall-QPS curves per sigma, strategy, dataset | E2 | `E2/raw.csv` |
| F3 QPS at recall 0.95 vs sigma, all strategies | E2 | `E2/raw.csv` |
| F4 distance computations vs sigma | E2 | `E2/raw.csv` |
| F5 FPR vs bits per entry, measured vs theory | E3 | `E3/raw.csv` |
| F6 wasted distance computations vs FPR | E3/E4-M4 | `E3/raw.csv` |
| F7 hops vs N with fits | E4-M1 | `E4/raw.csv` |
| F8 efS vs 1/sigma with fit | E4-M2 | `E4/raw.csv` |
| F9 crossover sigma: measured vs predicted | E4-M3 | `E4/raw.csv` |
| T1 datasets, hardware, parameters | E0 | `env.json` |
| T2 operating-point table | E2 | `E2/raw.csv` |
| T3 reproduction status | E5 | `E5/raw.csv` |
| T4 survey taxonomy | matrix.csv | `survey_support/` |

## 7. Pre-registered checks (the agent reports booleans, the human decides)

- **Paper A indicators:** E1 check true in at least one cell; E2 check true in at least 3 cells of the same predicate type; E4-M4 slope stable across datasets.
- **Paper B indicators:** M2 fit R^2 >= 0.9 on both datasets for at least one correlation mode; M3 crossover CIs narrower than a factor of 3 in sigma.
- **Paper C indicators:** neither of the above holds; E5 reproduction table is non-trivial.

These thresholds were set before running anything. Report them against the results exactly as defined; do not adjust them after seeing data.

## 8. Report format at every gate

Short artifact: what was run (config hashes), counts of cells run/skipped/failed with reasons, tables, anomalies list, list of files written. No conclusions. Commit results (not data/ or large parquet) to git and report the commit hash.
