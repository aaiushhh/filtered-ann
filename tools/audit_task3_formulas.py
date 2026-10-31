"""
Audit Task 3: For each Gate 5 note with an exact theorem/lemma/cost formula,
re-open the PDF text and confirm the statement and its locator.
Focus on mathematical formulas character-for-character.
"""
import os
import re

CHECKS = [
    # (bibkey, label, key_formula_fragment, expected_page_range)
    ('indyk2023worst', 'Lemma 2.1', 'O(k^d)', (3, 4)),
    ('indyk2023worst', 'Lemma 3.3', 'O((4alpha)^d log Delta)', (4, 5)),
    ('indyk2023worst', 'Theorem 3.4', 'alpha+1 / alpha-1', (5, 5)),
    ('indyk2023worst', 'Theorem 3.4', 'log_alpha', (5, 5)),
    ('indyk2023worst', 'Theorem 3.5', 'Omega(log Delta)', (5, 5)),
    ('indyk2023worst', 'Theorem 3.6', 'alpha+1 / alpha-1', (5, 6)),
    
    ('diwan2024navigable', 'Theorem 1', 'sqrt(n ln n)', (2, 5)),
    ('diwan2024navigable', 'Theorem 1', 'at most 2 steps', (2, 5)),
    ('diwan2024navigable', 'Theorem 2', 'Omega(n^{1/2-delta})', (3, 3)),
    ('diwan2024navigable', 'Theorem 4', 'Omega(n^{3/2-epsilon})', (6, 7)),
    ('diwan2024navigable', 'Claim 8', 'sqrt(n)/6', (6, 7)),
    
    ('prokhorenkova2020graph', 'Theorem 1', 'n^{1/d}', (4, 4)),
    ('prokhorenkova2020graph', 'Theorem 1', 'M^d', (4, 4)),
    ('prokhorenkova2020graph', 'Theorem 2', 'n^{1-M+o(1)}', (5, 5)),
    ('prokhorenkova2020graph', 'Theorem 3', 'O(log^2 n)', (5, 6)),
    ('prokhorenkova2020graph', 'Theorem 4', 'O(L^d M^d)', (6, 7)),
    ('prokhorenkova2020graph', 'Corollary 3', '(27/16)^{d/2}', (6, 7)),
    
    ('li2025sieve', 'Cost formula', 'C_bf(f) = gamma * card(f)', (5, 7)),
    ('li2025sieve', 'Cost formula', 'selectivity', (4, 7)),
]

results = []
for bk, label, formula_frag, page_range in CHECKS:
    txt_path = f'papers/{bk}.txt'
    if not os.path.exists(txt_path):
        results.append((bk, label, formula_frag, 'NO TXT', '-'))
        continue
    
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    
    # Extract text for specified page range
    start_p, end_p = page_range
    page_text = ''
    for p in range(start_p, end_p + 1):
        pattern = f'--- PAGE {p} ---\n(.*?)(?=--- PAGE \\d+ ---|$)'
        m = re.search(pattern, text, re.DOTALL)
        if m:
            page_text += m.group(1)
    
    # Normalize for search (collapse whitespace)
    clean_page = ' '.join(page_text.split())
    clean_full = ' '.join(text.split())
    
    # Try to find formula fragment
    # Search for recognizable fragments
    search_terms = {
        'O(k^d)': [r'O\s*\(\s*k\s*d\s*\)', r'Opk\s*dq', r'O\(k\^d\)'],
        'O((4alpha)^d log Delta)': [r'O\s*\(\s*\(4', r'Op\(?4', r'4\s*[αa]\s*\)\s*d\s*log'],
        'alpha+1 / alpha-1': [r'α\+1.*α.1', r'α\s*\+\s*1.*α\s*.\s*1', r'α`1.*α´1'],
        'log_alpha': [r'log\s*α', r'logα', r'log_α'],
        'Omega(log Delta)': [r'Ω\s*\(\s*log', r'Ωplog', r'Omega.*log.*Delta'],
        'sqrt(n ln n)': [r'√\s*n\s*ln\s*n', r'n ln n', r'n\s*ln\s*n'],
        'at most 2 steps': [r'at most 2 steps', r'at most 2', r'2\s*steps'],
        'Omega(n^{1/2-delta})': [r'Ω\s*\(\s*n\s*1/2', r'n1/2.*δ', r'n\^?\{?1/2'],
        'Omega(n^{3/2-epsilon})': [r'Ω\s*\(\s*n\s*3/2', r'n3/2', r'n\^?\{?3/2'],
        'sqrt(n)/6': [r'√\s*n\s*/\s*6', r'n/6', r'√n.*6'],
        'n^{1/d}': [r'n1/d', r'n\^?\{?1/d\}?', r'n\s*1/d'],
        'M^d': [r'Md', r'M\s*d\b', r'M\^d'],
        'n^{1-M+o(1)}': [r'n1.M', r'n\^?\{?1.*M'],
        'O(log^2 n)': [r'O\s*\(\s*log\s*2\s*n', r'O\(?log2\s*n', r'log\^?2\s*n'],
        'O(L^d M^d)': [r'O\s*\(\s*Ld.*Md', r'Ld\s*.\s*Md', r'L\s*d.*M\s*d'],
        '(27/16)^{d/2}': [r'27.*16.*d/2', r'27\s*/\s*16', r'\(?27/16\)'],
        'C_bf(f) = gamma * card(f)': [r'C.*bf.*card', r'brute.*force.*cost', r'gamma.*card'],
        'selectivity': [r'selectiv', r'cardinality'],
    }
    
    found_in_range = False
    found_anywhere = False
    match_detail = ''
    
    patterns = search_terms.get(formula_frag, [re.escape(formula_frag)])
    
    for pat in patterns:
        if re.search(pat, clean_page, re.IGNORECASE):
            found_in_range = True
            m = re.search(pat, clean_page, re.IGNORECASE)
            match_detail = m.group()[:40] if m else ''
            break
    
    if not found_in_range:
        for pat in patterns:
            if re.search(pat, clean_full, re.IGNORECASE):
                found_anywhere = True
                m = re.search(pat, clean_full, re.IGNORECASE)
                match_detail = m.group()[:40] if m else ''
                break
    
    if found_in_range:
        status = f'FOUND on p.{start_p}-{end_p}'
    elif found_anywhere:
        status = f'FOUND elsewhere (NOT on p.{start_p}-{end_p})'
    else:
        status = 'NOT FOUND'
    
    safe_detail = match_detail.encode('ascii', 'replace').decode('ascii')
    results.append((bk, label, formula_frag, status, safe_detail))

with open('scratch/audit_task3_formulas.md', 'w', encoding='utf-8') as f:
    f.write('# Audit Task 3: Formula Verification in PDF Text\n\n')
    f.write('| bibkey | label | formula fragment | status | matched text |\n')
    f.write('|---|---|---|---|---|\n')
    for bk, label, frag, status, detail in results:
        f.write(f'| {bk} | {label} | `{frag}` | {status} | `{detail}` |\n')
    
    mismatches = [(bk, label, frag) for bk, label, frag, status, _ in results if 'NOT FOUND' in status]
    f.write(f'\n## Summary\n- Total checks: {len(results)}\n- Found in expected range: {len([r for r in results if "FOUND on" in r[3]])}\n- Found elsewhere: {len([r for r in results if "elsewhere" in r[3]])}\n- Not found: {len(mismatches)}\n')
    if mismatches:
        f.write('\n### Not found:\n')
        for bk, label, frag in mismatches:
            f.write(f'- **{bk}** {label}: `{frag}`\n')

print(f"Task 3 done: {len(results)} checks, {len([r for r in results if 'NOT FOUND' in r[3]])} not found.")
