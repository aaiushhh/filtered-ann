import json

with open("tools/snowball_ranked.json", "r", encoding="utf-8") as f:
    ranked = json.load(f)

report_lines = [
    "# Gate 4 Report: Literature Snowballing & Candidate Expansion",
    "",
    "## 1. Executive Summary & Gate Status",
    "- **Gate**: Gate 4 (Phase 4 — Snowball under `AGENTS.md`).",
    "- **Phase 5 Status**: Strictly closed (no text from newly discovered papers read; synthesis not begun).",
    "- **Manifest Expansion**: Expanded `manifest.csv` from 37 to **53 papers** (added 16 verified open-access candidates across Groups A, B, C, D).",
    "- **Paywalled Inventory**: Added 5 paywalled candidate papers to `manual_download.md` (total manual download list: 7 papers).",
    "- **Target Milestone**: Surpasses the `AGENTS.md` threshold of **40+ tracked papers**.",
    "",
    "---",
    "",
    "## 2. Part A: Selectivity Cost Model Re-Checks",
    "Detailed inspection of the full texts of three candidate papers for formal mathematical search complexity / cost formulas parameterized by selectivity $\\sigma$:",
    "",
    "| Bibkey | Selectivity Cost Model? | Locator | Verification Findings & Notes |",
    "|---|---|---|---|",
    "| `filtered2026system` | **none found** | §1 (p. 1), §3 (p. 5), §5.1 (p. 12) | Discusses query optimizer selection heuristics in vector DBs (e.g. pgvector) and defines Global Label Similarity (GLS) correlation metric (§3), but formulates no formal closed-form mathematical cost or complexity model as a function of filter selectivity $\\sigma$. Discussion is purely architectural and empirical. `matrix.csv` retains `no`. |",
    "| `routing2026query` | **none found** | §1 (p. 2), §4.1–4.2 (p. 4–5) | Utilizes query selectivity $\\sigma$ as an input feature into an empirical 3-feature Multi-Layer Perceptron (MLP) neural regression router (`QueryAwareRouter`). Introduces no analytical or closed-form mathematical cost equation for search complexity. `matrix.csv` retains `no`. |",
    "| `curator2026` | **none found** | §1 (p. 2), §2.1 (p. 2), §4.1 (p. 5) | Defines selectivity $\\sigma = |P_\\sigma|/|S|$ and observes that production systems switch between pre- and post-filtering based on selectivity, but proposes an empirical dual-graph architecture (`Curator`) rather than deriving a mathematical cost formula or complexity bound. `matrix.csv` retains `no`. |",
    "",
    "> [!NOTE]",
    "> `matrix.csv` already correctly holds `no` for all three papers. Zero modifications were required for these rows.",
    "",
    "---",
    "",
    "## 3. Part B: Verified Note Addenda",
    "Grounded factual addenda (without interpretation) were incorporated directly into `notes/pipeannfilter2026.md` and `notes/rangefilters2026.md`:",
    "",
    "### 1. `pipeannfilter2026` Addendum Summary",
    "- **Cost Model Parameters (§4.2, Table 1, p. 6)**: $N$ (dataset size), $s$ (estimated selectivity), $p_{pre}, p_{in}$ (precision of pre/in-filtering; false positive rate $= 1 - p$), $X_{pre}, X_{in}$ (SSD pages read for attribute scans), $R$ (standard proximity graph out-degree), $R_d$ (densified graph out-degree with 2-hop neighbors), $S_r$ (standard record size), $S_d$ (densified record size), $\\gamma$ (relative compute cost of `is_member_approx` vs vector distance comparison; default $\\gamma=0.05$), $L$ (search pool size parameter), $\\alpha, \\beta$ (linear weights balancing SSD page I/O vs compute comparisons; default $\\alpha=10, \\beta=1$).",
    "- **Filter Size & Representation**: Fixed 4 bytes (32 bits) allocated per vector in DRAM (§5.4, p. 11). Bloom false-positive rate directly parameterizes traversal precision $p_{in} = 1 - \\text{FPR}$.",
    "- **Structure Tested**: Vector categorical labels for `LabelOrSelector` during graph traversal (§4.3.1, p. 7).",
    "- **False Positive Behavior**: False positives admit non-matching neighbors into the traversal pool. At low selectivity ($s R_d / p_{in} \\le R$), they act as vital 'bridge edges' preserving connectivity across fragmented sub-graphs. At high selectivity ($s R_d / p_{in} > R$), they expand the candidate pool ($L / p_{in}$). Exact verification against raw SSD attributes prunes false positives during final top-$k$ reranking (§4.1–4.2, p. 5–7).",
    "",
    "### 2. `rangefilters2026` Addendum Summary",
    "- **Cost Model Parameters (§2.4, §3.3, Lemma 1, p. 4, 6)**: $T$ (maximum range span $|[v_{min}, v_{max}]|$), $t$ (number of independent hash functions), $m$ (Bloom filter length in bits), $\\alpha$ (target false-positive probability $\\alpha = (1/2)^{(m/r)\\ln 2}$), $r$ (range query length $v_r - v_l + 1$), $\\mathcal{D}_<$ (set of left-bounded canonical dyadic intervals), $d_v^<, c_v^>$ (number of canonical dyadic intervals assigned to node $v$), $n_c$ (reachability set size), $b$ (bits per hash entry), $M$ (HNSW degree parameter).",
    "- **Filter Size & Representation**: Bloom filter bit length $m$ is explicitly parameterized to guarantee false positive rate $\\alpha$ for dyadic interval sets (Lemma 1, p. 4).",
    "- **Structure Tested**: Reachability labeling sets $\\mathcal{L}(u)$ encoding whether graph nodes can reach query range intervals without violating graph paths (§3.1–3.3, p. 4–6).",
    "- **False Positive Behavior**: A false positive erroneously treats a non-matching or unreachable node as reachable, admitting out-of-range vectors into the candidate/result heap. Empirically, the author demonstrates that setting $\\alpha = 0.01$ maintains $>98\\%$ empirical Recall@$k$ without requiring exact graph verification (§4.3, p. 8).",
    "",
    "---",
    "",
    "## 4. Part C: Snowball Candidates Ranked by Citation Frequency",
    "All candidates discovered from reference lists of the 35 notes and survey papers, categorized across the 5 required research topics and ranked by the number of existing notes citing them:",
    "",
    "| Rank | Bibkey | Citations | Topic | Title | Venue / Year | DOI / arXiv | OA Status |",
    "|---|---|---|---|---|---|---|---|",
]

topic_descriptions = {
    1: "AMQ filters in graph/vector search & core filter algorithms",
    2: "Selectivity-aware cost models / complexity analysis for filtered ANN",
    3: "Set-membership / access-control predicates in vector search",
    4: "Cache-miss / memory-latency analysis of HNSW traversal",
    5: "Theory of graph-based ANN search (expected hops, search-cost bounds)"
}

for idx, c in enumerate(ranked, 1):
    doi_or_arxiv = f"arXiv:{c['arxiv_id']}" if c['arxiv_id'] else f"DOI:{c['doi']}"
    if not c['arxiv_id'] and not c['doi']:
        doi_or_arxiv = "vldb.org open PDF"
    oa_disp = f"**{c['oa_status']}**" if c['oa_status'] == "OK" else f"*{c['oa_status']}*"
    report_lines.append(
        f"| {idx} | `{c['bibkey']}` | **{c['cite_count']}** | Topic {c['topic']} | {c['title']} | {c['venue']} ({c['year']}) | {doi_or_arxiv} | {oa_disp} |"
    )

report_lines.extend([
    "",
    "---",
    "",
    "## 5. Topic Breakdown of Snowball Candidates",
    ""
])

for topic_id in range(1, 6):
    topic_cands = [c for c in ranked if c['topic'] == topic_id]
    report_lines.append(f"### Topic {topic_id}: {topic_descriptions[topic_id]} ({len(topic_cands)} candidates)")
    for c in topic_cands:
        citing_str = ", ".join([f"`{k}`" for k in c['cited_by']]) if c['cited_by'] else "None"
        report_lines.append(f"- **`{c['bibkey']}`** ([{c['cite_count']} citing notes: {citing_str}]): *{c['title']}* — {c['venue']} ({c['year']}). OA: `{c['oa_status']}`.")
    report_lines.append("")

report_lines.extend([
    "---",
    "",
    "## 6. Manifest & Repository State at Gate 4",
    "- **`manifest.csv` Total Entries**: **53 papers** (37 existing + 16 verified open-access additions).",
    "- **`manual_download.md` Entries**: **7 papers** (2 priority from Gate 0.5: `cai2024navigating`, `shaikh2026annex`; 5 paywalled candidates: `pagh2004cuckoo`, `broder2004network`, `zheng2025digra`, `datar2004locality`, `zhang2018surf`).",
    "- **`refs.bib` Status**: 35 verified entries corresponding to the 35 fully annotated reading notes.",
    "- **`matrix.csv` Status**: 37 rows populated directly from notes (35 annotated + 2 placeholders).",
    "- **Next Steps**: Awaiting human approval at Gate 4 before initiating any downloads or annotations of Phase 4 papers, or opening Phase 5 synthesis."
])

report_content = "\n".join(report_lines)

out_path = r"C:\Users\eyush\.gemini\antigravity\brain\cb861d3b-000d-4753-b217-dd3521a55ef6\GATE4_report.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(report_content)

print(f"GATE4_report.md created successfully ({len(report_lines)} lines).")
