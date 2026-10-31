# Gate 0.5 Summary Report

## 1. Overview of Changes
- **Phase 0 (Preflight)**: Confirmed directory layout and verified all required columns in `manifest.csv`. Created `logs/` directory.
- **Phase 1 (Resolve Title Mismatches & Relevance)**: 
  - Fetched official arXiv abstract metadata for the 4 mismatched papers (`filtered2026system`, `filteraware2025`, `cftrag2025`, `bridgerag2026`).
  - Corrected full titles in `manifest.csv`.
  - Assessed relevance to predicate-constrained filtered ANN search in HNSW graphs:
    - `filtered2026system`: **KEEP** (Evaluates hybrid filtering across vector databases including HNSW).
    - `filteraware2025`: **KEEP** (Optimizes distance metric for graph search with attribute filters).
    - `cftrag2025`: **PROPOSED-DROP** (Focuses on entity localization in hierarchical tree structures for RAG, not vector similarity search).
    - `bridgerag2026`: **PROPOSED-DROP** (Focuses on abstract bridge trees for LLM chunk retrieval, not predicate pruning in graph ANN).
- **Phase 2 (Coverage Gap — Group D Additions)**:
  - Identified and verified 10 major systems specifically handling filtered/predicate-constrained graph search via Crossref DOIs.
  - Added to `manifest.csv` with `group = D`, `added_in_gate = "0.5"`, and `review_status = "ADDED-PENDING-USER-REVIEW"`:
    1. `gollapudi2023filtereddiskann` (WWW 2023, DOI: 10.1145/3543507.3583552)
    2. `patel2024acorn` (PACMMOD/SIGMOD 2024, DOI: 10.1145/3654923)
    3. `luo2025tagfiltered` (ICDE 2025, DOI: 10.1109/icde65448.2025.00272)
    4. `wu2022hqann` (CIKM 2022, DOI: 10.1145/3511808.3557610)
    5. `cai2024navigating` (PACMMOD/SIGMOD 2024, DOI: 10.1145/3698822)
    6. `zuo2024serf` (PACMMOD/SIGMOD 2024, DOI: 10.1145/3639324)
    7. `zhang2025dynamic` (PACMMOD/SIGMOD 2025, DOI: 10.1145/3725401)
    8. `zou2026rnsg` (PVLDB 2026, DOI: 10.14778/3828612.3828636)
    9. `wang2021milvus` (SIGMOD 2021, DOI: 10.1145/3448016.3457550)
    10. `shaikh2026annex` (IgMin Research 2026, DOI: 10.61927/igmin365)
  - Documented all accepted and rejected/unverifiable candidates (e.g. CAPS, VBase) in `gaps.md`.
- **Phase 3 (Full Text Downloads & Extraction)**:
  - Downloaded open-access PDFs and extracted text to `papers/<bibkey>.txt`.
  - Generated `papers/MISSING.md` for paywalled conference/journal versions.
- **Phase 4 (Scaffolding)**:
  - Generated `paper/refs.bib` programmatically with 37 verified entries.
  - Created `paper/outline.md` containing only the specified section headings.

## 2. Full-Text Download Counts

| Category | Count | Papers |
|---|---|---|
| **OK** (Downloaded & text extracted) | **20** | `eppstein2016cuckoo`, `graf2020xor`, `mitzenmacher2017adaptive`, `maplets2025`, `pla2025learned`, `superseding2019learning`, `lshlowerbounds2005`, `malkov2020hnsw`, `chen2021spann`, `beam2025distance`, `manohar2025range`, `survey2025filtered`, `filtered2026system`, `routing2026query`, `curator2026`, `filteraware2025`, `rangefilters2026`, `matsui2025lotusfilter`, `pipeannfilter2026`, `cuckoogpu2026` |
| **PAYWALLED** (Listed in `papers/MISSING.md`) | **15** | `bloom1970space`, `fan2014cuckoo`, `kraska2018learned`, `indyk1998approximate`, `subramanya2019diskann`, `gollapudi2023filtereddiskann`, `patel2024acorn`, `luo2025tagfiltered`, `wu2022hqann`, `cai2024navigating`, `zuo2024serf`, `zhang2025dynamic`, `zou2026rnsg`, `wang2021milvus`, `shaikh2026annex` |
| **SKIPPED** (Relevance: PROPOSED-DROP) | **2** | `cftrag2025`, `bridgerag2026` |
| **FAILED** | **0** | None |
| **Total Manifest Rows** | **37** | 27 seed papers + 10 Group D additions |

## 3. Proposed Drops
1. `cftrag2025`: Entity localization in hierarchical tree structures for RAG; not filtered graph vector search.
2. `bridgerag2026`: Abstract bridge trees for LLM document chunk retrieval; not graph ANN pruning.

## 4. Additions Pending Review
Ten papers added to Group D (`ADDED-PENDING-USER-REVIEW`). All have verified Crossref DOIs and directly address filtered/hybrid graph ANN search.

## 5. Uncertainties & Next Steps
- The 15 PAYWALLED papers require manual download via institutional access if their full text is needed for quote-grounded reading.
- For Gate 1 (grounded reading notes), 20 open-access papers are ready with full text extracted in `papers/<bibkey>.txt`.
