"""
Detailed check of the 18 'missing' labels from Task 4.
Check for ligature issues, alternate formatting, etc.
"""
import os
import re

missing = [
    ('li2025sieve', 'Eq.', '3'),
    ('li2025sieve', 'Eq.', '4'),
    ('li2025sieve', 'Eq.', '1'),
    ('li2025sieve', 'Theorem', '4.6'),
    ('rangefilters2026', 'Eq.', '5'),
    ('bloom1970space', 'Table', '1'),
    ('cuckoogpu2026', 'Eq.', '4'),
    ('curator2026', 'Table', '4'),
    ('curator2026', 'Table', '3'),
    ('diwan2024navigable', 'Definition', '3'),
    ('diwan2024navigable', 'Definition', '6'),
    ('indyk1998approximate', 'Theorem', '3'),
    ('indyk1998approximate', 'Theorem', '1'),
    ('matsui2025lotusfilter', 'Eq.', '2'),
    ('mitzenmacher2018model', 'Definition', '1'),
    ('mitzenmacher2018model', 'Eq.', '2'),
    ('wu2022hqann', 'Eq.', '4'),
    ('zhang2023vbase', 'Theorem', '1'),
]

for bk, ltype, lnum in missing:
    txt_path = f'papers/{bk}.txt'
    if not os.path.exists(txt_path):
        print(f'{bk} | {ltype} {lnum} | NO TXT FILE')
        continue
    
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    
    # Try various patterns including ligature variants
    variants = [
        f'{ltype} {lnum}',
        f'{ltype.replace("i", "ﬁ").replace("fi", "ﬁ")} {lnum}',  # fi ligature
        f'De\ufb01nition {lnum}',   # explicit fi ligature for Definition
        f'De\ufb01nition{lnum}',
        f'Eq.({lnum})',
        f'Eq. ({lnum})',
        f'({lnum})',               # for equations often just "(3)"
        f'Equation {lnum}',
        f'Equation ({lnum})',
    ]
    
    found = False
    for v in variants:
        idx = text.find(v)
        if idx >= 0:
            # find page
            page_markers = list(re.finditer(r'--- PAGE (\d+) ---', text[:idx+1]))
            page = int(page_markers[-1].group(1)) if page_markers else '?'
            context = text[max(0,idx-30):idx+len(v)+50].replace('\n', ' ')
            print(f'{bk} | {ltype} {lnum} | FOUND as "{v}" on page {page} | context: ...{context}...')
            found = True
            break
    
    if not found:
        # Try broader search
        escaped = re.escape(lnum)
        broad = re.search(rf'(?:Eq|Equation|Table|Theorem|Definition|Def)\S*\s*\(?{escaped}\)?', text, re.IGNORECASE)
        if broad:
            pos = broad.start()
            page_markers = list(re.finditer(r'--- PAGE (\d+) ---', text[:pos+1]))
            page = int(page_markers[-1].group(1)) if page_markers else '?'
            ctx = text[max(0,pos-20):pos+60].replace('\n', ' ')
            print(f'{bk} | {ltype} {lnum} | PARTIAL MATCH: "{broad.group()}" on page {page} | context: ...{ctx}...')
        else:
            print(f'{bk} | {ltype} {lnum} | TRULY NOT FOUND')
