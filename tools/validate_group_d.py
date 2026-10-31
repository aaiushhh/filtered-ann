import os, re

required_sections = [
    '## Problem addressed (p.)',
    '## Method (core idea in <=5 sentences) (p.)',
    '## Complexity / theoretical claims',
    '## Filter type and selectivity regime handled (p.)',
    '## Index structure used (HNSW / IVF / Vamana / other) (p.)',
    '## Datasets, baselines, metrics (Table N)',
    '## Key results (numbers exactly as reported, with Table/Fig locator)',
    '## Limitations (author-stated vs. observed)',
    '## Relevance to our project',
    '## Flags',
    '## Useful references to snowball'
]

papers = [
    'survey2025filtered',
    'filtered2026system',
    'routing2026query',
    'curator2026',
    'filteraware2025',
    'rangefilters2026',
    'gollapudi2023filtereddiskann',
    'patel2024acorn',
    'luo2025tagfiltered',
    'wu2022hqann',
    'zuo2024serf',
    'zhang2025dynamic',
    'zou2026rnsg',
    'wang2021milvus'
]

print(f'Checking {len(papers)} papers...')

for bib in papers:
    path = f'notes/{bib}.md'
    if not os.path.exists(path):
        print(f'MISSING: {path}')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check header
    if not content.startswith(f'# {bib}'):
        print(f'{bib}: Header does not start with # {bib}')
    if 'Authors / Year / Venue / DOI:' not in content:
        print(f'{bib}: Missing Authors / Year / Venue / DOI')
    if 'Status:' not in content or 'PDF:' not in content or 'Read fully: yes' not in content:
        print(f'{bib}: Missing Status/PDF header line')
        
    # Check sections
    for sec in required_sections:
        # Check if section header prefix matches
        prefix = sec.split('(')[0].strip()
        found = any(line.strip().startswith(prefix) for line in content.split('\n'))
        if not found:
            print(f'{bib}: Missing section matching "{sec}"')
            
    # Check novelty check
    if 'Novelty check: does this paper apply a membership filter (Bloom, Cuckoo, Xor) or a metadata predicate check during graph traversal itself, rather than before or after the search?' not in content:
        print(f'{bib}: Missing exact Novelty check line')
        
    # Check quotes
    # Quotes are text in quotes "..."
    double_quotes = re.findall(r'"([^"\n]{5,})"', content)
    long_quotes = []
    for q in double_quotes:
        words = q.split()
        if len(words) > 15:
            long_quotes.append((len(words), q[:40]))
    if long_quotes:
        print(f'{bib}: Quotes > 15 words: {long_quotes}')
        
    # Check 'not stated' count
    not_stated_count = len(re.findall(r'not stated', content, re.I))
    
    # Check flags
    flags_match = re.search(r'## Flags[^\n]*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    flags_text = flags_match.group(1).strip() if flags_match else 'none'
    has_flags = flags_text != '- none noted.' and flags_text != 'none noted.'
    
    print(f'{bib}: OK (not stated count: {not_stated_count}, has flags: {has_flags})')
    if has_flags:
        print(f'   Flag: {flags_text}')
    if not_stated_count >= 2:
        print(f'   >= 2 not stated fields ({not_stated_count})')
