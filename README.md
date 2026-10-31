# Filtered ANN Search via Probabilistic Membership Filters

A verified, annotated literature base and research toolkit for **predicate-constrained (filtered) approximate nearest neighbor (ANN) search on proximity graphs (e.g., HNSW), utilizing probabilistic membership filters (Bloom / Cuckoo / Xor filters) to prune non-matching nodes during graph traversal**.

---

## 1. Project Overview

Vector search with scalar predicate constraints (hybrid search) is critical for modern database systems, retrieval-augmented generation (RAG), and vector databases. Traditional methods typically employ:
1. **Pre-filtering**: Evaluating predicates upfront via inverted indexes or attribute scans, then searching over the filtered subset or brute-forcing. Fails at moderate-to-high selectivity.
2. **Post-filtering**: Traversing an unconstrained vector index and discarding non-matching vectors. Fails catastrophically at low selectivity due to traversal inflation and empty result sets.
3. **In-graph Filtering (Predicate-Agnostic / Traversal-Time)**: Evaluating predicates during graph traversal (e.g., ACORN, PipeANN-Filter). 

This project explores **filter-augmented hybrid graph traversal**, modeling the interaction between probabilistic approximate membership query (AMQ) filters, graph connectivity, false positive rates, and crossover selectivity thresholds $\sigma^*$.

---

## 2. Repository Structure

```
filtered-ann/
├── README.md               # Project documentation and navigation guide
├── AGENTS.md               # Multi-agent literature pipeline specification & protocol
├── LOG.md                  # Append-only chronological action log with diffs
├── manifest.csv            # Master paper catalog with verified DOIs, arXiv IDs, and statuses
├── matrix.csv              # Systematic 44-row comparative feature & complexity matrix
├── refs.bib                # 100% verified BibTeX bibliography matching all notes
├── manual_download.md      # Registry of paywalled papers requiring institutional access
├── gaps.md                 # Gap analysis and open theoretical questions
├── notes/                  # 42 detailed, locator-grounded paper reading notes
│   ├── bloom1970space.md
│   ├── fan2014cuckoo.md
│   ├── graf2020xor.md
│   ├── indyk2023worst.md
│   ├── diwan2024navigable.md
│   ├── li2025sieve.md
│   ├── patel2024acorn.md
│   ├── pipeannfilter2026.md
│   ├── prokhorenkova2020graph.md
│   └── ...
├── tools/                  # Verification, BibTeX generation, and audit scripts
│   ├── make_bib.py         # Programmatic BibTeX generator via Crossref & arXiv APIs
│   ├── verify_quotes.py    # Verbatim quotation length and uniqueness verifier
│   └── ...
├── papers/                 # Local working directory for paper PDFs (git-ignored)
└── paper/                  # Manuscript workspace (human LaTeX & outline)
```

---

## 3. Key Literature Insights

- **Formal Selectivity Cost Models**: Across the 42 analyzed papers, exactly three provide formal mathematical cost models parameterized by query predicate selectivity:
  - **ACORN** (`patel2024acorn`, SIGMOD 2024): Expected post-filtering search cost is $O(\log |X| + k/\sigma)$, explaining search cost explosion as $\sigma \to 0$.
  - **PipeANN-Filter** (`pipeannfilter2026`, 2026): Analytical compute and SSD I/O cost formulas parameterized by selectivity $s$ and false-positive precision $p$.
  - **SIEVE** (`li2025sieve`, PVLDB 2025): Mathematical brute-force cost $C_{bf}(f) = \gamma \cdot card(f)$ and indexed graph latency $C(I_h, sef, w, f)$ parameterized by attribute cardinality.
- **Novelty Finding**: Among all annotated papers, none embed probabilistic membership filters (Bloom/Cuckoo/Xor) directly inside the graph traversal edge-relaxation loop to probabilistically bypass distance computations while preserving graph small-world navigation.

---

## 4. Rigorous Audit & Verification Standards

All notes and bibliographies in this repository follow strict verification rules:
- **No Hallucinations**: Every factual assertion contains an explicit section/page/theorem locator (e.g., `(§3.2, p. 6)`, `(Theorem 3.4, p. 5)`).
- **100% Verified Identifiers**: All BibTeX entries in `refs.bib` are generated programmatically via Crossref, arXiv, and DataCite APIs. Unverified candidate preprints are quarantined.
- **Formal Label Audit**: 147 formal mathematical labels (Theorems, Lemmas, Definitions, Equations) across all 42 notes were audited character-for-character against extracted PDF texts (100% verified, 0 missing).
- **Verbatim Quote Bounds**: All direct quotations are constrained to $\le 15$ words per paper.

---

## 5. License & Copyright Notice

Academic paper PDFs and raw text dumps are excluded from this public repository (`.gitignore`) in compliance with copyright law. Reading notes, metadata matrices, analysis reports, and research scripts are made publicly available for academic and research purposes.
