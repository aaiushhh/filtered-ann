import os
import re
import csv
import json

notes_keys = sorted([f.replace('.md', '') for f in os.listdir('notes') if f.endswith('.md')])

with open('manifest.csv', 'r', encoding='utf-8') as f:
    manifest = {r['bibkey']: r for r in csv.DictReader(f)}

# Header columns required by AGENTS.md + 2 extra requested:
# bibkey, year, venue, status, index_structure, filter_type, selectivity_regime, strategy (pre/post/in-traversal/partition), formal_complexity (yes/no), complexity_form, uses_probabilistic_filter (yes/no/which), datasets, main_baselines, open_source_code (url or none), gap_note, novelty_check, selectivity_cost_model
header = [
    'bibkey', 'year', 'venue', 'status', 'index_structure', 'filter_type',
    'selectivity_regime', 'strategy', 'formal_complexity', 'complexity_form',
    'uses_probabilistic_filter', 'datasets', 'main_baselines', 'open_source_code',
    'gap_note', 'novelty_check', 'selectivity_cost_model'
]

rows = []

def clean_field(s):
    if not s or s.strip().lower() in ['none', 'none stated', 'not stated']:
        return 'not stated'
    return ' '.join(s.strip().replace('\n', ' ').split())

for k in notes_keys:
    note_path = os.path.join('notes', f"{k}.md")
    with open(note_path, 'r', encoding='utf-8') as fp:
        c = fp.read()

    # Parse header from note
    m_head = re.search(r'Authors / Year / Venue / DOI:[ \t]*([^\n]+)', c)
    head_parts = [p.strip() for p in m_head.group(1).split('/')] if m_head else []
    year = head_parts[1] if len(head_parts) > 1 else manifest[k].get('verified_year', 'not stated')
    venue = head_parts[2] if len(head_parts) > 2 else manifest[k].get('verified_venue', 'not stated')
    
    m_stat = re.search(r'Status:[ \t]*([^\n]+)', c)
    status = m_stat.group(1).split()[0] if m_stat else manifest[k].get('verified_status', 'not stated')

    # Parse sections
    def extract_section(title_pattern):
        m = re.search(rf'## [^\n]*{title_pattern}[^\n]*\n(.*?)(?=\n## |\Z)', c, re.DOTALL | re.IGNORECASE)
        return m.group(1).strip() if m else ''

    prob_sec = extract_section('Problem')
    meth_sec = extract_section('Method')
    comp_sec = extract_section('Complexity')
    filter_sec = extract_section('Filter type')
    index_sec = extract_section('Index structure')
    data_sec = extract_section('Datasets')
    results_sec = extract_section('Key results')
    rel_sec = extract_section('Relevance')
    flags_sec = extract_section('Flags')

    # index_structure
    index_structure = clean_field(index_sec)
    if not index_sec and k in ['cftrag2025', 'bridgerag2026']:
        index_structure = 'Entity Tree / Abstract Bridge Tree + Cuckoo Filter'

    # filter_type
    filter_type = 'not stated'
    selectivity_regime = 'not stated'
    if filter_sec:
        # Split filter type and selectivity regime if mentioned
        lines = [l.strip() for l in filter_sec.split('\n') if l.strip()]
        filter_type = clean_field(lines[0])
        for l in lines:
            if 'selectivity' in l.lower():
                selectivity_regime = clean_field(l.replace('- Selectivity regime handled:', '').replace('Selectivity regime handled:', ''))

    # strategy: pre / post / in-traversal / partition / none
    strategy = 'none'
    lower_c = c.lower()
    if 'in-traversal' in lower_c or 'in-filtering' in lower_c or 'filteredgreedysearch' in lower_c or 'acorn-search-layer' in lower_c:
        strategy = 'in-traversal'
    elif 'post-filter' in lower_c or 'post-processing' in lower_c:
        strategy = 'post'
    elif 'pre-filter' in lower_c:
        strategy = 'pre'
    elif 'partition' in lower_c:
        strategy = 'partition'

    if k in ['curator2026']:
        strategy = 'partition / hybrid'
    elif k in ['rangefilters2026', 'pipeannfilter2026', 'patel2024acorn', 'luo2025tagfiltered', 'gollapudi2023filtereddiskann', 'zuo2024serf', 'zou2026rnsg', 'wu2022hqann', 'filteraware2025']:
        strategy = 'in-traversal'
    elif k in ['wang2021milvus']:
        strategy = 'pre / in-traversal'
    elif k in ['matsui2025lotusfilter']:
        strategy = 'post'
    elif k in ['routing2026query']:
        strategy = 'query-routing'
    elif k in ['bloom1970space', 'fan2014cuckoo', 'eppstein2016cuckoo', 'graf2020xor', 'mitzenmacher2017adaptive', 'maplets2025', 'cuckoogpu2026']:
        strategy = 'standalone-filter'
    elif k in ['kraska2018learned', 'pla2025learned', 'superseding2019learning']:
        strategy = 'learned-index'
    elif k in ['indyk1998approximate', 'lshlowerbounds2005']:
        strategy = 'lsh-theory'
    elif k in ['malkov2020hnsw', 'subramanya2019diskann', 'chen2021spann', 'beam2025distance', 'manohar2025range']:
        strategy = 'unfiltered-graph'

    # formal_complexity
    formal_complexity = 'no'
    complexity_form = 'none stated'
    if comp_sec and 'none stated' not in comp_sec.lower():
        formal_complexity = 'yes'
        complexity_form = clean_field(comp_sec[:150])
    elif comp_sec:
        complexity_form = clean_field(comp_sec)

    # uses_probabilistic_filter (yes/no/which)
    uses_prob = 'no'
    if k in ['bloom1970space']:
        uses_prob = 'yes (Bloom filter)'
    elif k in ['fan2014cuckoo', 'eppstein2016cuckoo', 'cuckoogpu2026']:
        uses_prob = 'yes (Cuckoo filter)'
    elif k in ['graf2020xor']:
        uses_prob = 'yes (Xor filter)'
    elif k in ['mitzenmacher2017adaptive']:
        uses_prob = 'yes (Adaptive Cuckoo filter)'
    elif k in ['maplets2025']:
        uses_prob = 'yes (Maplet / Quotient / Cuckoo)'
    elif k in ['rangefilters2026', 'pipeannfilter2026']:
        uses_prob = 'yes (Bloom filter)'
    elif k in ['cftrag2025', 'bridgerag2026']:
        uses_prob = 'yes (Cuckoo hash table / pointer map)'
    elif k in ['kraska2018learned']:
        uses_prob = 'yes (Learned Bloom filter)'

    # datasets
    datasets = clean_field(data_sec[:120])

    # main_baselines
    m_base = re.search(r'baselines[^\n:]*:[ \t]*([^\n]+)', data_sec, re.IGNORECASE)
    main_baselines = clean_field(m_base.group(1)) if m_base else 'not stated'

    # open_source_code
    m_code = re.search(r'(https?://github\.com/[^\s)]+)', c)
    open_source_code = m_code.group(1) if m_code else 'none'

    # gap_note
    gap_note = 'none noted'
    if flags_sec and flags_sec.lower() not in ['none', 'none.', 'none stated', 'none noted']:
        gap_note = clean_field(flags_sec[:150])

    # novelty_check
    m_nov = re.search(r'Novelty check:[ \t]*([^\n]+(?:\n[^\n#]+)?)', c, re.IGNORECASE)
    nov_raw = ' '.join(m_nov.group(0).split()) if m_nov else 'unclear'
    after_nov = re.sub(r'^(?:Novelty check:\s*)+', '', nov_raw, flags=re.IGNORECASE).strip()
    if after_nov.lower().startswith('yes'):
        novelty_check = 'yes'
    elif after_nov.lower().startswith('no'):
        novelty_check = 'no'
    else:
        novelty_check = 'unclear'

    # selectivity_cost_model
    # Does the paper give a formal cost or complexity model as a function of filter selectivity, with locator
    if k == 'patel2024acorn':
        selectivity_cost_model = 'yes (§3.2, p. 6; expected post-filtering search cost O(log|X| + k/sigma))'
    elif k == 'pipeannfilter2026':
        selectivity_cost_model = 'yes (§4.2, Table 1, p. 6; analytical I/O and compute cost formulas parameterized by selectivity s)'
    else:
        selectivity_cost_model = 'no'

    rows.append([
        k, year, venue, status, index_structure, filter_type, selectivity_regime,
        strategy, formal_complexity, complexity_form, uses_prob,
        datasets, main_baselines, open_source_code, gap_note, novelty_check, selectivity_cost_model
    ])

# Append placeholder rows for cai2024navigating and shaikh2026annex
for k, yr, vn, st, d, lnk in [
    ('cai2024navigating', '2024', 'PACMMOD / SIGMOD 2024', 'PUB', '10.1145/3698822', 'https://dl.acm.org/doi/10.1145/3698822'),
    ('shaikh2026annex', '2026', 'IgMin Research', 'PUB', '10.61927/igmin365', 'https://doi.org/10.61927/igmin365')
]:
    rows.append([
        k, yr, vn, st, 'no note yet', 'no note yet', 'no note yet',
        'no note yet', 'no note yet', 'no note yet', 'no note yet',
        'no note yet', 'no note yet', 'no note yet', 'no note yet (paywalled)',
        'no note yet', 'no note yet'
    ])

with open('matrix.csv', 'w', encoding='utf-8', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Generated matrix.csv with {len(rows)} rows (35 annotated notes + 2 placeholders).")
