"""
Audit Task 2: For the 7 Gate 5 notes, report PDF page count and reading coverage.
Audit Task 3: For notes with exact theorem/lemma/cost formulas, verify statements
              character-for-character in PDF text.
Audit Task 4: For EVERY note with Theorem/Lemma/Corollary/Definition/Claim/Eq./Table/Algorithm
              labels, confirm label exists in PDF text with that number and page.
"""
import os
import re

GATE5_NOTES = [
    'prokhorenkova2020graph',
    'diwan2024navigable',
    'indyk2023worst',
    'li2025sieve',
    'gupta2023caps',
    'zhang2023vbase',
    'mitzenmacher2018model',
]

# Priority order for Task 4
PRIORITY_NOTES = [
    'patel2024acorn', 'pipeannfilter2026', 'li2025sieve', 'rangefilters2026'
]

def get_page_count_and_pages(txt_path):
    """Count pages from PAGE markers in extracted text."""
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    pages = re.findall(r'--- PAGE (\d+) ---', text)
    if pages:
        return int(pages[-1]), [int(p) for p in pages]
    return 0, []

def get_page_text(txt_path, page_num):
    """Extract text for a specific page."""
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    pattern = f'--- PAGE {page_num} ---\n(.*?)(?=--- PAGE \\d+ ---|$)'
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1) if m else ''

def find_label_in_text(txt_path, label_type, label_num):
    """Search for a formal label (e.g. 'Theorem 3.4') in the full text.
    Returns (found: bool, page: int or None)."""
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    
    # Normalize ligatures for matching
    norm_text = text.replace('\ufb01', 'fi').replace('\ufb02', 'fl').replace('\ufb00', 'ff')
    
    escaped_num = re.escape(str(label_num))
    patterns = [
        rf'{label_type}\s+{escaped_num}[\.\s\(,:]',
        rf'{label_type}\s+{escaped_num}\b',
    ]
    if label_type.lower() in ['eq.', 'eq', 'equation']:
        patterns.extend([
            rf'Eq\.\s*\({escaped_num}\)',
            rf'Equation\s*\({escaped_num}\)',
            rf'Equation\s+{escaped_num}\b',
            rf'\({escaped_num}\)',
        ])
    
    for pat in patterns:
        for m in re.finditer(pat, norm_text, re.IGNORECASE):
            pos = m.start()
            page_markers = list(re.finditer(r'--- PAGE (\d+) ---', text[:pos+1]))
            page = int(page_markers[-1].group(1)) if page_markers else 0
            return True, page
    
    return False, None

def extract_labels_from_note(note_path):
    """Extract all formal labels from a note file."""
    with open(note_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Pattern: Theorem X.Y, Lemma X.Y, Corollary X, Definition X.Y, Claim X, 
    # Eq. X, Table X, Algorithm X
    pattern = r'(Theorem|Lemma|Corollary|Definition|Claim|Eq\.|Table|Algorithm)\s+([0-9]+(?:\.[0-9]+)*)'
    matches = re.findall(pattern, content)
    
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for label_type, label_num in matches:
        key = (label_type, label_num)
        if key not in seen:
            seen.add(key)
            unique.append(key)
    
    return unique

# Also extract page references from note to check what was claimed
def extract_page_refs_from_note(note_path):
    """Extract page references like (p. 5) or (p. 3-7) from note."""
    with open(note_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    pages = set()
    for m in re.finditer(r'p\.\s*(\d+)(?:\s*[-–]\s*(\d+))?', content):
        start = int(m.group(1))
        end = int(m.group(2)) if m.group(2) else start
        for p in range(start, end+1):
            pages.add(p)
    return sorted(pages)

# ---- TASK 2 ----
out2 = []
out2.append('# Audit Task 2: PDF Page Count and Reading Coverage (Gate 5 Notes)\n\n')
out2.append('| bibkey | PDF pages | Pages referenced in note | Read fully claim | Assessment |\n')
out2.append('|---|---|---|---|---|\n')

for bk in GATE5_NOTES:
    txt_path = f'papers/{bk}.txt'
    note_path = f'notes/{bk}.md'
    
    if not os.path.exists(txt_path):
        out2.append(f'| {bk} | NO TXT | - | - | Cannot verify |\n')
        continue
    
    page_count, all_pages = get_page_count_and_pages(txt_path)
    ref_pages = extract_page_refs_from_note(note_path)
    
    with open(note_path, 'r', encoding='utf-8', errors='replace') as f:
        note_content = f.read()
    
    read_claim = 'yes' if 'Read fully: yes' in note_content else 'no / not stated'
    
    # Check: does the note reference pages that cover most of the paper?
    if page_count > 0:
        coverage = len(ref_pages) / page_count * 100
        if coverage >= 60:
            assessment = f'{len(ref_pages)}/{page_count} pages referenced ({coverage:.0f}%)'
        else:
            assessment = f'Only {len(ref_pages)}/{page_count} pages referenced ({coverage:.0f}%) — may be partial'
    else:
        assessment = 'Cannot determine page count'
    
    out2.append(f'| {bk} | {page_count} | {ref_pages} | {read_claim} | {assessment} |\n')

# ---- TASK 4 ----
out4 = []
out4.append('\n\n# Audit Task 4: Formal Label Verification in PDF Text\n\n')

# Get all note files
all_notes = sorted([f.replace('.md', '') for f in os.listdir('notes') if f.endswith('.md') and not f.startswith('_')])

# Order: priority first, then remaining
ordered_notes = []
for p in PRIORITY_NOTES:
    if p in all_notes:
        ordered_notes.append(p)
for n in all_notes:
    if n not in ordered_notes:
        ordered_notes.append(n)

out4.append('| bibkey | label in note | found in PDF | page in PDF |\n')
out4.append('|---|---|---|---|\n')

total_labels = 0
found_labels = 0
missing_labels = []

for bk in ordered_notes:
    note_path = f'notes/{bk}.md'
    txt_path = f'papers/{bk}.txt'
    
    labels = extract_labels_from_note(note_path)
    if not labels:
        continue
    
    if not os.path.exists(txt_path):
        for lt, ln in labels:
            out4.append(f'| {bk} | {lt} {ln} | NO TXT FILE | - |\n')
            total_labels += 1
            missing_labels.append((bk, f'{lt} {ln}', 'no txt file'))
        continue
    
    for lt, ln in labels:
        total_labels += 1
        found, page = find_label_in_text(txt_path, lt, ln)
        if found:
            found_labels += 1
            out4.append(f'| {bk} | {lt} {ln} | yes | {page} |\n')
        else:
            missing_labels.append((bk, f'{lt} {ln}', 'NOT FOUND'))
            out4.append(f'| {bk} | {lt} {ln} | **NO** | - |\n')

out4.append(f'\n## Summary\n- Total labels checked: {total_labels}\n- Found: {found_labels}\n- Missing: {total_labels - found_labels}\n\n')
if missing_labels:
    out4.append('### Missing labels:\n')
    for bk, label, reason in missing_labels:
        out4.append(f'- **{bk}**: {label} — {reason}\n')

# Write outputs
with open('scratch/audit_task2_coverage.md', 'w', encoding='utf-8') as f:
    f.writelines(out2)

with open('scratch/audit_task4_labels.md', 'w', encoding='utf-8') as f:
    f.writelines(out4)

print(f"Task 2: {len(GATE5_NOTES)} notes checked.")
print(f"Task 4: {total_labels} labels checked, {found_labels} found, {total_labels - found_labels} missing.")
