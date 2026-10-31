# Action Log

[2026-10-27 18:06:00 +05:30] INIT: Created LOG.md and initializing project directory structure for literature pipeline.
[2026-10-27 18:06:47 +05:30] MKDIR: Created directories papers/, notes/, paper/.
[2026-10-27 18:07:17 +05:30] MKDIR: Created tools/ directory.
[2026-10-27 18:07:57 +05:30] PHASE0: Created tools/verify_seed.py — initial verification script.
[2026-10-27 18:25:55 +05:30] PHASE0: Rewrote tools/verify_seed.py with SSL workaround. First run timed out on arXiv API.
[2026-10-27 20:29:32 +05:30] PHASE0: Created tools/verify_all.py — comprehensive verification using curl subprocess (bypasses SSL/timeout issues).
[2026-10-27 20:29:37 +05:30] PHASE0: Started verify_all.py. Used Crossref DOI content-negotiation and arXiv HTML page scraping.
[2026-10-27 20:34:24 +05:30] PHASE0: verify_all.py completed. All 27 papers checked. Results saved to tools/verification_complete.json.
[2026-10-27 20:34:39 +05:30] PHASE0: Noted mitzenmacher2017adaptive arXiv metadata extraction issue (script bug); confirmed manually via separate curl that arXiv page loads with title "Adaptive Cuckoo Filters".
[2026-10-27 20:57:39 +05:30] PHASE0: Queried Crossref for candidate published DOIs: lshlowerbounds2005 -> 10.1137/050646858 (SIAM J. Discrete Math), beam2025distance -> 10.52202/085713-3346 (NeurIPS 38), curator2026 -> 10.1145/3786635 (PACMMOD), cuckoogpu2026 -> 10.1145/3832810.3832822 (ICPP 2026). routing2026query false positive rejected (Encyclopedia of GIS, wrong paper).
[2026-10-27 22:07:50 +05:30] PHASE0: Crossref search for SPANN: no matching DOI found (NeurIPS 2021 not indexed there). arXiv comment confirms "Accepted to NeurIPS 2021".
[2026-10-27 22:08:06 +05:30] PHASE0: Crossref confirmed mitzenmacher2017adaptive published: DOI 10.1145/3339504 (ACM JEA 2020) and DOI 10.1137/1.9781611975055.4 (ALENEX 2018).
[2026-10-29 16:48:43 +05:30] PHASE0: Ran tools/analyze_verification.py to produce full human-readable summary of all 27 records.
[2026-10-29 16:52:07 +05:30] PHASE0: Created manifest.csv with all 27 seed papers, verified statuses, DOIs, venues, and notes.
[2026-10-29 16:52:30 +05:30] PHASE0: Created manual_download.md (empty — no paywalled downloads needed yet in Phase 0).
[2026-10-29 16:53:00 +05:30] GATE0: Posted GATE 0 artifact with verification results table. Awaiting human approval before Phase 1.
[2026-10-29 17:15:00 +05:30] GATE0.5: Started Gate 0.5. Verified directories logs/, papers/, notes/, paper/.
[2026-10-29 17:18:20 +05:30] GATE0.5: Resolved 4 title mismatches (filtered2026system, filteraware2025 -> KEEP; cftrag2025, bridgerag2026 -> PROPOSED-DROP). Updated manifest.csv and logs/fetch_log.csv.
[2026-10-29 17:22:15 +05:30] GATE0.5: Added 10 verified Group D systems to manifest.csv (added_in_gate=0.5, review_status=ADDED-PENDING-USER-REVIEW). Evaluated candidates recorded in gaps.md.
[2026-10-29 17:28:40 +05:30] GATE0.5: Full-text fetch: 20 open-access PDFs downloaded and text extracted to papers/*.txt; 15 paywalled logged in papers/MISSING.md; 2 skipped (PROPOSED-DROP).
[2026-10-29 17:31:00 +05:30] GATE0.5: Generated paper/refs.bib (37 verified entries), paper/outline.md (section headings only), and gate0_5_report.md.
[2026-10-29 17:35:00 +05:30] GATE1: Initiated Batch 1 reading (Group D: curator2026, filteraware2025, filtered2026system, rangefilters2026, routing2026query).
[2026-10-29 17:36:30 +05:30] GATE1: Completed notes/curator2026.md and notes/filteraware2025.md. Quote checks passed.
[2026-10-29 17:37:35 +05:30] GATE1: Completed notes/filtered2026system.md. Quote checks passed.
[2026-10-29 17:39:18 +05:30] GATE1: Completed notes/rangefilters2026.md. Quote checks passed.
[2026-10-29 17:40:45 +05:30] GATE1: Completed notes/routing2026query.md. Quote checks passed.
[2026-10-29 17:41:10 +05:30] GATE1: Created observations.md with one-line summaries and references for all 5 batch papers.
[2026-10-29 17:41:30 +05:30] GATE1: Updated gaps.md with newly discovered missing literature cited in Batch 1.
[2026-10-29 21:46:25 +05:30] MANUAL_DROPIN: Processed 4 manually downloaded papers from downloaded_paper/: bloom1970space, subramanya2019diskann, gollapudi2023filtereddiskann, luo2025tagfiltered. Copied PDFs to papers/*.pdf and extracted text to papers/*.txt. Updated manifest.csv, papers/MISSING.md, and manual_download.md.
[2026-10-29 21:52:45 +05:30] MANUAL_DROPIN_2: Processed 7 additional downloaded papers: wang2021milvus, wu2022hqann, zuo2024serf, patel2024acorn, fan2014cuckoo, indyk1998approximate, zhang2025dynamic. Extracted text to papers/*.txt, updated manifest.csv, papers/MISSING.md, and manual_download.md. Total OK papers now 31/37 (only 4 missing).
[2026-10-29 22:44:30 +05:30] PHASE1_FETCH: Downloaded kraska2018learned from arXiv (1712.01208). Extracted 30 pages to papers/kraska2018learned.txt. First-page title verified.
[2026-10-29 22:45:20 +05:30] PHASE1_FETCH: Downloaded zou2026rnsg from open PVLDB repository (vldb.org/pvldb/vol19/p2839-zou.pdf). Extracted 14 pages to papers/zou2026rnsg.txt. First-page title verified.
[2026-10-29 22:45:45 +05:30] PHASE1_MANUAL: Logged cai2024navigating and shaikh2026annex as PRIORITY in manual_download.md and papers/MISSING.md.
[2026-10-29 22:46:00 +05:30] GATE1: Reached GATE 1 under AGENTS.md. Completed Phase 1 (PDF fetches and pre-reading inventory).
[2026-10-30 00:08:00 +05:30] PHASE2: Annotated Group C papers (malkov2020hnsw, subramanya2019diskann, chen2021spann, beam2025distance, manohar2025range) in notes/<bibkey>.md strictly following AGENTS.md template.
[2026-10-30 00:09:00 +05:30] PHASE2: Annotated Group B papers (kraska2018learned, indyk1998approximate, pla2025learned, superseding2019learning, lshlowerbounds2005) in notes/<bibkey>.md strictly following Section 7 template in AGENTS.md.
[2026-10-30 00:10:00 +05:30] PHASE2: Annotated Group E papers (matsui2025lotusfilter, pipeannfilter2026, cftrag2025, bridgerag2026, cuckoogpu2026) in notes/<bibkey>.md strictly following AGENTS.md template and user instructions.
[2026-10-30 00:11:00 +05:30] PHASE2: Annotated Group A papers (bloom1970space, fan2014cuckoo, eppstein2016cuckoo, graf2020xor, mitzenmacher2017adaptive, maplets2025) in notes/<bibkey>.md strictly following Section 7 template in AGENTS.md.


[2026-10-30 00:20:00 +05:30] PHASE2: Annotated Group D papers (14 papers: survey2025filtered, filtered2026system, routing2026query, curator2026, filteraware2025, rangefilters2026, gollapudi2023filtereddiskann, patel2024acorn, luo2025tagfiltered, wu2022hqann, zuo2024serf, zhang2025dynamic, zou2026rnsg, wang2021milvus; skipped cai2024navigating and shaikh2026annex without PDFs) in notes/<bibkey>.md strictly following Section 7 template in AGENTS.md.
[2026-10-30 00:20:00 +05:30] PHASE2_COMPLETE: Completed Phase 2 annotation of 35 papers (33 full notes + 2 short notes for cftrag2025 and bridgerag2026) across parallel subagents for Groups A, B, C, D, E. All quotes <= 15 words. Added placeholders in matrix.csv for cai2024navigating and shaikh2026annex.
[2026-10-30 00:24:00 +05:30] GATE2: Reached GATE 2 under AGENTS.md. Posted list of notes written, items with flags or >=2 'not stated' fields, and novelty check table.
[2026-10-30 11:58:30 +05:30] PHASE3_BIB: Generated refs.bib programmatically via tools/make_bib.py from Crossref and arXiv APIs (DataCite for eppstein2016cuckoo; NeurIPS proceedings for subramanya2019diskann). 35 entries match 35 notes with 0 duplicates and 0 missing IDs. Flagged 4 title mismatches (subtitles omitted by publisher Crossref records).
[2026-10-30 11:58:45 +05:30] PHASE3_MATRIX: Filled matrix.csv directly from notes (37 rows: 35 annotated notes + 2 placeholders for cai2024navigating and shaikh2026annex). Reconciled Novelty check counts to 11 YES, 23 NO, 1 UNCLEAR. Evaluated selectivity_cost_model column (patel2024acorn and pipeannfilter2026 = YES).
[2026-10-30 11:59:00 +05:30] GATE3: Reached GATE 3 under AGENTS.md. Posted bib validation, title mismatches, reconciled novelty table, and selectivity cost model list.
[2026-10-30 12:13:30 +05:30] ADDENDUM: Appended cost-model parameters & Bloom filter mechanics to notes/pipeannfilter2026.md (parameters N, s, p_pre, p_in, X_pre, X_in, R, R_d, S_r, S_d, gamma, L, alpha, beta, 4 bytes/vector Bloom filter; tested on vector label sets; false positives act as bridge edges at low selectivity or expand pool at high selectivity before SSD exact re-verification).
[2026-10-30 12:13:55 +05:30] ADDENDUM: Appended cost-model parameters & Bloom filter mechanics to notes/rangefilters2026.md (parameters T, t, m, alpha, r, D_<, d_v^<, c_v^>, n_c, b, M; tested on distance-aware labeling sets; false positives admit out-of-range vectors into candidate/result heap, maintaining >98% recall at alpha=0.01 without exact graph verification).
[2026-10-30 12:15:00 +05:30] PHASE4_RECHECK: Re-checked filtered2026system, routing2026query, curator2026 for selectivity_cost_model. All three confirmed 'none found' (no analytical cost equation parameterized by selectivity; empirical/architectural only). matrix.csv already correctly records 'no' for all three (0 rows modified).
[2026-10-30 12:24:45 +05:30] PHASE4_SNOWBALL: Extracted reference links from all 35 annotated notes and survey2025filtered. Resolved 21 candidate papers across 5 required research topics using Crossref, arXiv API, and publisher open-access portals.
[2026-10-30 12:24:50 +05:30] PHASE4_MANIFEST: Added 16 verified open-access snowball candidates to manifest.csv with origin='snowball', added_in_gate='4', review_status='SNOWBALL-CANDIDATE', and citing notes listed in 'cited_by'. Total manifest rows increased from 37 to 53.
[2026-10-30 12:24:55 +05:30] PHASE4_MANUAL: Identified 5 paywalled candidate papers (pagh2004cuckoo, broder2004network, zheng2025digra, datar2004locality, zhang2018surf) and appended them to manual_download.md.
[2026-10-30 12:25:00 +05:30] GATE4: Reached GATE 4 under AGENTS.md. Compiled candidate rankings by citation frequency across notes and topic mapping (Topics 1-5). Phase 5 remains closed; no new papers read.
[2026-10-30 12:39:20 +05:30] ADDENDUM: Appended Lemma 1 & Lemma 2 formal analysis (Addendum 2) to notes/rangefilters2026.md. Statements, assumptions, bounds, and variable listings documented without quotes. Confirmed neither Lemma 1 nor Lemma 2 bounds cost, space, or recall as a function of alpha (alpha does not appear in either lemma statement or proof). selectivity_cost_model in matrix.csv remains 'no' (0 rows changed).
[2026-10-30 12:41:35 +05:30] TOPIC4_SEARCH: Searched and resolved 6 candidates on memory-access, cache-miss, and prefetching in graph ANN (wang2025anncache, liu2025tieredcache, zhang2026io, huang2025dhnsw, liu2025shine, wu2025inmemory). Added all 6 to manifest.csv with origin='snowball', added_in_gate='5', review_status='SNOWBALL-CANDIDATE'. Manifest rows increased to 59. None read.

2026-10-30T13:06:18.502719 — Manifest updated for Gate 5 notes: 24 field corrections
  - indyk2023worst.arxiv_id: "2310.17030" -> "2310.19126"
  - indyk2023worst.link: "https://arxiv.org/abs/2310.17030" -> "https://arxiv.org/abs/2310.19126"
  - indyk2023worst.text_version: "arXiv-2310.17030" -> "arXiv-2310.19126"
  - indyk2023worst.source_url: "https://arxiv.org/pdf/2310.17030" -> "https://arxiv.org/pdf/2310.19126"
  - li2025sieve.doi: "" -> "10.14778/3749646.3749725"
  - li2025sieve.arxiv_id: "2411.08271" -> ""
  - li2025sieve.verified_status: "PRE" -> "PUB"
  - li2025sieve.link: "https://arxiv.org/abs/2411.08271" -> "https://doi.org/10.14778/3749646.3749725"
  - li2025sieve.verified_venue: "arXiv preprint" -> "Proceedings of the VLDB Endowment (PVLDB)"
  - li2025sieve.verified_year: "2024" -> "2025"
  - li2025sieve.text_version: "arXiv-2411.08271" -> "PVLDB-vol18-p4723"
  - li2025sieve.source_url: "https://arxiv.org/pdf/2411.08271" -> "https://www.vldb.org/pvldb/vol18/p4723-li.pdf"
  - zhang2023vbase.arxiv_id: "2307.03986" -> ""
  - zhang2023vbase.link: "https://arxiv.org/abs/2307.03986" -> "https://www.usenix.org/conference/osdi23/presentation/zhang-qianxi"
  - zhang2023vbase.text_version: "arXiv-2307.03986" -> "OSDI2023-zhang-qianxi"
  - zhang2023vbase.source_url: "https://arxiv.org/pdf/2307.03986" -> "https://www.usenix.org/system/files/osdi23-zhang-qianxi_1.pdf"
  - prokhorenkova2020graph.arxiv_id: "2006.05942" -> "1907.00845"
  - prokhorenkova2020graph.link: "https://arxiv.org/abs/2006.05942" -> "https://arxiv.org/abs/1907.00845"
  - prokhorenkova2020graph.text_version: "arXiv-2006.05942" -> "arXiv-1907.00845"
  - prokhorenkova2020graph.source_url: "https://arxiv.org/pdf/2006.05942" -> "https://arxiv.org/pdf/1907.00845"
  - diwan2024navigable.arxiv_id: "2406.07770" -> "2405.18680"
  - diwan2024navigable.link: "https://arxiv.org/abs/2406.07770" -> "https://arxiv.org/abs/2405.18680"
  - diwan2024navigable.text_version: "arXiv-2406.07770" -> "arXiv-2405.18680"
  - diwan2024navigable.source_url: "https://arxiv.org/pdf/2406.07770" -> "https://arxiv.org/pdf/2405.18680"

2026-10-30T13:08:06.359247 — matrix.csv updated: li2025sieve selectivity_cost_model formatted with locator and definition (§4.2, p. 5–7)

2026-10-30T14:33:08.146662 — Thorough Full-Text Theorem Audit for Theory Papers:
  - Re-read source texts for indyk2023worst, diwan2024navigable, and prokhorenkova2020graph.
  - indyk2023worst: Corrected theoretical claims with exact statements and locators for Lemma 2.1 (p. 3), Definition 3.1 (p. 4), Lemma 3.2 (p. 4), Lemma 3.3 (p. 4), Theorem 3.4 (p. 5), Theorem 3.5 (p. 5), Theorem 3.6 (p. 6), Lemma 3.7 (p. 6), and Section 4 empirical hardness constructions.
  - diwan2024navigable: Corrected theoretical claims with exact statements and locators for Definition 3 (p. 4), Theorem 1 (p. 2, 5), Theorem 2 (p. 3), Theorem 4 (p. 6), Claim 5 (p. 6), Claim 7 (p. 6), Claim 8 (p. 6), Claim 9 (p. 6), and Theorem 13 (p. 25).
  - prokhorenkova2020graph: Corrected theoretical claims with exact statements and locators for Dense Regime Theorem 1 (p. 4), Sparse Regime Theorem 2 (p. 5), Corollary 1 (p. 5), Long-Range Shortcuts Theorem 3 (p. 5), Corollary 2 (p. 6), Lemma 1 (p. 6), Beam Search Theorem 4 (p. 6), and Corollary 3 (p. 6).
  - Marked all remaining unread snowball rows in manifest.csv as UNVERIFIED pending future verification, with strict embargo against citing them.

2026-10-30T14:50:03.844594 — Task 1 (Final fix pass): manifest.csv updated (5 changes):
  - li2025sieve.title: "SIEVE: A Framework for Efficient Filtered Vector Search" -> "SIEVE: Effective Filtered Vector Search with Collection of Indexes"
  - gupta2023caps.title: "CAPS: A Partition-based Index for Filtered Similarity Search" -> "CAPS: A Practical Partition Index for Filtered Similarity Search"
  - zuo2023arkgraph.doi: "10.14778/3587136.3587143" -> "UNVERIFIED - DO NOT USE"
  - ren2020hmann.arxiv_id: "2006.12028" -> "UNVERIFIED - DO NOT USE"
  - xu2024multifilterann.arxiv_id: "2408.08502" -> "UNVERIFIED - DO NOT USE"

2026-10-30T15:02:00.311710 — Task 4 Final Fix Pass: Corrected Label and Page Locator Mismatches Across 7 Notes:
  - notes/li2025sieve.md:
    * BEFORE: Eq. 3, p. 6 (Brute force)
      AFTER:  Table 3, PDF p. 6 / printed p. 4728; defined in Table 2, PDF p. 5 / printed p. 4727
    * BEFORE: Eq. 4, p. 6 (Indexed search cost formula c_search * S_down * M_down / cor)
      AFTER:  Definition 4.7, PDF p. 5 / printed p. 4727; Table 3, PDF p. 6 / printed p. 4728: C(I_h, sef, w, f) := log(card(h)) * sef * (card(h)/card(f))^cor(w, f, h) if h subsumes f else inf
    * BEFORE: Eq. 1, p. 6 (In-memory footprint with sizeof float/uint32)
      AFTER:  Table 3, PDF p. 6 / printed p. 4728; §4.2, PDF p. 5 / printed p. 4727: S(I_h) = M * card(h) = (M_inf * log(card(h)) / log(N)) * card(h)
    * BEFORE: Theorem 4.6, p. 7, §4.3 (Submodular optimization guarantee)
      AFTER:  §4.3, PDF p. 7 / printed p. 4729 citing Nemhauser et al. [49, 70] (noting Definition 4.6 on PDF p. 5 / printed p. 4727 is the M_down downscaling function)
    * BEFORE: Flag claiming empirical p and q exponents
      AFTER:  Flag citing M scaling strictly as M_inf * log(card(h))/log(N) and historical cor(w, f, h) estimation
  - notes/bloom1970space.md:
    * BEFORE: Table 1, p. 426
      AFTER:  un-numbered table ("TABLE OF EXPECTED PERFORMANCE..."), p. 426
  - notes/curator2026.md:
    * BEFORE: Table 4, p. 12 (vector insertion throughput)
      AFTER:  §6.4, p. 12, Figure 13
    * BEFORE: Table 3, p. 10 (Curator construction time and memory overhead)
      AFTER:  §6.4, p. 12, Figure 12
  - notes/indyk1998approximate.md:
    * BEFORE: Proposition 2 (§1, p. 2 / p. 604; Theorem 3, §4.1, p. 6 / p. 609)
      AFTER:  Proposition 2 (§1, p. 2 / p. 605; §4.1, p. 6 / p. 609)
    * BEFORE: Ring-Cover Tree Bounds (Theorem 1, 2, Lemma 1–4, Corollary 2, §3, p. 4–5 / pp. 607–608)
      AFTER:  Ring-Cover Tree Bounds (Lemma 1–4, Corollary 1–2, §3, p. 4–5 / pp. 607–608)
  - notes/mitzenmacher2018model.md:
    * BEFORE: Eq. 2, p. 8 (F_sand formula)
      AFTER:  §5.1, p. 7–8, equation 1–2
  - notes/zhang2023vbase.md:
    * BEFORE: Theorem 1, p. 7-8, §3.3 (Semantic Equivalence Proof)
      AFTER:  §3.3, p. 7–8 / pp. 382–383 (formal property defined in Definition 1 on p. 5 / p. 380)
  - notes/diwan2024navigable.md:
    * BEFORE: Theorem 13 (Maximum Degree Bound, p. 25, Appendix C)
      AFTER:  Theorem 13 (Maximum Degree Lower Bound, §4.3, PDF p. 10 / printed p. 10)
