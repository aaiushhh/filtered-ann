# AGENTS.md — Literature Pipeline for "Predicate-Constrained ANN Search via Probabilistic Membership Filters"

Read this file fully before doing anything. Follow it exactly. If an instruction here conflicts with a chat prompt, ask before proceeding.

## 1. Mission

Build a verified, annotated literature base for a research project on **filtered (predicate-constrained) approximate nearest neighbor search in HNSW graphs, using probabilistic membership filters (Bloom / Cuckoo / Xor) to prune non-matching nodes during graph traversal**. The human researcher will later derive the complexity theorem (pre-filter vs post-filter vs filter-augmented hybrid, crossover selectivity σ*) and write the paper. Your job ends at a trustworthy notes + references + gap-analysis package.

## 2. Hard rules (never violate)

1. **No fabrication.** Never invent a paper, author, DOI, venue, year, theorem number, dataset, or numeric result. If something is not in the source, write `not stated`.
2. **Every factual claim in notes carries a locator**: `(p. X)`, `(§X.Y)`, `(Thm N)`, or `(Table N)`. No locator → do not write the claim.
3. **Quotes: max 15 words, max one per paper.** Paraphrase everything else.
4. **Bibliographic data comes from APIs, not memory.** Use Crossref (`https://api.crossref.org/works/<DOI>`, header `Accept: application/x-bibtex`) and the arXiv API. Never hand-write a BibTeX entry.
5. **No paywall circumvention.** No Sci-Hub, no mirror/pirate sites, no credential tricks. If a PDF is not openly accessible, log it in `manual_download.md` (see §6) and move on.
6. **Do not write proofs, derive complexity bounds, or draft any paper text.** Out of scope. If you notice a possible gap or error in a paper, flag it in the note under `Flags`, do not resolve it.
7. **Do not modify** anything in `paper/` or any file you did not create.
8. **Log everything** in `LOG.md` (timestamped, one line per action, including failures).
9. **Stop at each gate** in §4 and post a summary artifact. Do not run on to the next phase without human approval.

## 3. Folder layout (create if missing)

```
filtered-ann/
  AGENTS.md
  LOG.md                 # append-only action log
  manifest.csv           # master paper list (see §5), you maintain it
  manual_download.md     # papers the human must download by hand
  papers/<bibkey>.pdf    # downloaded PDFs
  notes/<bibkey>.md      # one note per paper (template §7)
  refs.bib               # generated from DOIs/arXiv IDs only
  matrix.csv             # comparison matrix (columns §8)
  gaps.md                # synthesis (Phase 5)
  paper/                 # human's LaTeX — DO NOT TOUCH
```

Bibkey format: `firstauthorlastname` + `year` + `firstkeyword` in lowercase, e.g. `malkov2020hnsw`. Keep keys stable once assigned.

## 4. Phases and gates

**Phase 0 — Verify the seed manifest (§5).**
For each seed row: open the URL, confirm it resolves, confirm title/authors/year match, and record the real venue + DOI (via Crossref/arXiv API). Mark `status`: `ok`, `mismatch` (explain), or `dead`. Do not silently fix mismatches.
→ **GATE 0:** post a table of results. Wait for approval.

**Phase 1 — Fetch PDFs.**
Download open-access PDFs to `papers/<bibkey>.pdf`. Prefer the publisher's open version, else the arXiv version (record which in `manifest.csv`, column `pdf_source`). Paywalled → `manual_download.md`. Verify each PDF opens and the first page title matches.
→ **GATE 1:** post counts (downloaded / manual / failed).

**Phase 2 — Read and annotate.**
One note per downloaded paper using the template in §7. Read the full paper, not just the abstract. Spawn parallel agents by group (A–E in §5), one agent per group, each writing only to its own `notes/` files.
→ **GATE 2:** post the list of notes, plus every item you put under `Flags` or marked `not stated` more than twice in one note.

**Phase 3 — References and matrix.**
Generate `refs.bib` programmatically from DOIs / arXiv IDs (script allowed, save it as `tools/make_bib.py`). Fill `matrix.csv` from the notes only.
→ **GATE 3:** post bib validation (every key in notes exists in `refs.bib` and vice versa).

**Phase 4 — Snowball.**
Using reference lists of the notes — especially the survey `survey2025filtered` and the 2026 filtered-ANN papers — find additional relevant papers on: filtered ANN search, AMQ filters, learned Bloom filters, graph-ANN theory. Add candidates to `manifest.csv` with `origin = snowball`, `cited_by = <bibkey>`. Also locate links/DOIs for the §5 "targets without links" list. Target total: **40+ papers**. Do not read the new ones yet.
→ **GATE 4:** post new candidates ranked by how many existing notes cite them.

**Phase 5 — Synthesis (only after the human approves Gate 4 and the new papers are annotated).**
Write `gaps.md`: (a) what each existing filtered-ANN method assumes about selectivity, filter type, and index structure; (b) which papers give formal complexity guarantees vs empirical only; (c) where nobody has analyzed a filter embedded inside HNSW traversal with a false-positive-rate-aware cost model. Every statement cites bibkeys with locators. End with a numbered list of open questions, labelled as *hypotheses for the human to test*.

## 5. Seed manifest (verify in Phase 0)

Descriptions are unverified hypotheses from abstracts. Confirm or correct them in the notes.
Publication status: `PUB` = published in a conference/journal that is typically Scopus-indexed (human verifies in Scopus later; do not claim indexing yourself). `PRE` = arXiv preprint as far as known (check whether a published version now exists and record its DOI).

| bibkey | group | status | title | link |
|---|---|---|---|---|
| bloom1970space | A | PUB | Space/Time Trade-offs in Hash Coding with Allowable Errors | https://dl.acm.org/doi/10.1145/362686.362692 |
| fan2014cuckoo | A | PUB | Cuckoo Filter: Practically Better Than Bloom | https://dl.acm.org/doi/10.1145/2674005.2674994 |
| eppstein2016cuckoo | A | PUB | Cuckoo Filter: Simplification and Analysis | https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SWAT.2016.8 |
| graf2020xor | A | PUB (journal: ACM JEA, DOI 10.1145/3376122) / PRE copy | Xor Filters: Faster and Smaller Than Bloom and Cuckoo Filters | https://arxiv.org/abs/1912.08258 |
| mitzenmacher2017adaptive | A | PRE? | Adaptive Cuckoo Filters | https://arxiv.org/abs/1704.06818 |
| maplets2025 | A | PRE | Time To Replace Your Filter: How Maplets Simplify System Design | https://arxiv.org/abs/2510.05518 |
| kraska2018learned | B | PUB | The Case for Learned Index Structures | https://dl.acm.org/doi/10.1145/3183713.3196909 |
| indyk1998approximate | B | PUB | Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality | https://dl.acm.org/doi/10.1145/276698.276876 |
| pla2025learned | B | PRE | Piecewise Linear Approximation in Learned Index Structures: Theoretical and Empirical Analysis | https://arxiv.org/abs/2506.20139 |
| superseding2019learning | B | PRE? | Superseding Traditional Indexes by Orchestrating Learning and Geometry | https://arxiv.org/abs/1903.00507 |
| lshlowerbounds2005 | B | PRE? | Lower Bounds on Locality Sensitive Hashing | https://arxiv.org/abs/cs/0510088 |
| malkov2020hnsw | C | PUB | Efficient and Robust ANN Search Using Hierarchical Navigable Small World Graphs | https://dl.acm.org/doi/10.1109/TPAMI.2018.2889473 (preprint: https://arxiv.org/abs/1603.09320) |
| subramanya2019diskann | C | PUB | DiskANN: Fast Accurate Billion-point Nearest Neighbor Search on a Single Node | https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html |
| chen2021spann | C | PUB? | SPANN: Highly-efficient Billion-scale Approximate Nearest Neighbor Search | https://arxiv.org/abs/2111.08566 |
| beam2025distance | C | PRE | Distance Adaptive Beam Search for Provably Accurate Graph-Based Nearest Neighbor Search | https://arxiv.org/abs/2505.15636 |
| manohar2025range | C | PRE | Range Retrieval with Graph-Based Indices | https://arxiv.org/abs/2502.13245 |
| survey2025filtered | D | PRE | Survey of Filtered Approximate Nearest Neighbor Search over the Vector-Scalar Hybrid Data | https://arxiv.org/abs/2505.06501 |
| filtered2026system | D | PRE | Filtered ANN Search in Vector Databases: System Design and Performance Analysis | https://arxiv.org/abs/2602.11443 |
| routing2026query | D | PRE | Query-aware Routing for Filtered Approximate Nearest Neighbors Search | https://arxiv.org/abs/2606.19898 |
| curator2026 | D | PRE | Curator: Efficient Vector Search with Low-Selectivity Filters | https://arxiv.org/abs/2601.01291 |
| filteraware2025 | D | PRE | Learning Filter-Aware Distance Metrics for NN Search with Multiple Filters | https://arxiv.org/abs/2511.04073 |
| rangefilters2026 | D | PRE | Approximate Nearest Neighbor Search with Graph Range Filters | https://arxiv.org/abs/2607.00727 |
| matsui2025lotusfilter | E | PUB | LotusFilter: Fast Diverse Nearest Neighbor Search via a Learned Cutoff Table | https://openaccess.thecvf.com/content/CVPR2025/papers/Matsui_LotusFilter_Fast_Diverse_Nearest_Neighbor_Search_via_a_Learned_Cutoff_CVPR_2025_paper.pdf |
| pipeannfilter2026 | E | PRE | PipeANN-Filter: An Efficient Filtered Vector Search System on SSD | https://arxiv.org/abs/2605.17992 |
| cftrag2025 | E | PRE | CFT-RAG: An Entity Tree Based RAG Algorithm With Cuckoo Filter | https://arxiv.org/abs/2501.15098 |
| bridgerag2026 | E | PRE | Bridge-RAG: An Abstract Bridge Tree Based RAG Algorithm | https://arxiv.org/abs/2603.26668 |
| cuckoogpu2026 | E | PRE | Cuckoo-GPU: Accelerating Cuckoo Filters on Modern GPUs | https://arxiv.org/abs/2603.15486 |

Groups: A = membership filters, B = learned indexes + LSH theory, C = graph ANN, D = filtered ANN, E = applications.

**Targets without links (find via Crossref/DBLP in Phase 4; do not guess URLs):**
ACORN (predicate-agnostic filtered HNSW); CAPS (partition index for filtered similarity search); Tag-Filtered ANN Search (ICDE 2025); MultiFilterANN; DIGRA (range-filtered graph index, PACMMOD 2025); NSG (VLDB 2019); FAISS "Billion-scale similarity search with GPUs" (IEEE Trans. Big Data); Learned Bloom Filters — Mitzenmacher "A Model for Learned Bloom Filters and Optimizing by Sandwiching" (NeurIPS 2018); Morton Filters (VLDB 2018); Ribbon Filter; Vacuum Filters; Pagh & Rodler "Cuckoo Hashing"; Broder & Mitzenmacher "Network Applications of Bloom Filters: A Survey"; Datar et al. p-stable LSH (SoCG 2004); Multi-Probe LSH (VLDB 2007); Prokhorenkova & Shekhovtsov "Graph-based nearest neighbor search: From practice to theory" (ICML 2020).

## 6. `manual_download.md` format

For every paper you cannot fetch legally: one line each — `bibkey | title | DOI | publisher URL | reason (paywall / 403 / dead link)`. The human will download these through institutional access and drop them into `papers/`. When a PDF appears there, treat it as fetched and continue.

## 7. Note template (`notes/<bibkey>.md`)

```
# <bibkey> — <title>
Authors / Year / Venue / DOI:      (from API, not memory)
Status: PUB | PRE (published version DOI if exists)
PDF: papers/<bibkey>.pdf   Read fully: yes/no

## Problem addressed (p.)
## Method (core idea in ≤5 sentences) (p.)
## Complexity / theoretical claims
- Statement, assumptions, theorem number, page. Write `none stated` if purely empirical.
## Filter type and selectivity regime handled (p.)
## Index structure used (HNSW / IVF / Vamana / other) (p.)
## Datasets, baselines, metrics (Table N)
## Key results (numbers exactly as reported, with Table/Fig locator)
## Limitations (author-stated vs. observed)
## Relevance to our project (≤3 sentences; which part: filter structure / HNSW traversal / cost model / baseline to beat)
## Flags (possible errors, inconsistencies, unclear claims — do NOT resolve them)
## Useful references to snowball (bibkeys or titles from its reference list)
```

## 8. `matrix.csv` columns

`bibkey, year, venue, status, index_structure, filter_type, selectivity_regime, strategy (pre/post/in-traversal/partition), formal_complexity (yes/no), complexity_form, uses_probabilistic_filter (yes/no/which), datasets, main_baselines, open_source_code (url or none), gap_note`

Fill only from notes. Unknown → `not stated`.

## 9. Final report (post at the end of every gate)

Short artifact with: what was done, counts, anything skipped and why, anything uncertain. No marketing language, no padding.
