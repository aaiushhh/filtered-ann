import re
import sys
from pypdf import PdfReader

# Force utf-8 stdout
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

papers = {
    'indyk2023worst': 'papers/indyk2023worst.pdf',
    'diwan2024navigable': 'papers/diwan2024navigable.pdf',
    'prokhorenkova2020graph': 'papers/prokhorenkova2020graph.pdf'
}

out_lines = []

for bibkey, path in papers.items():
    header = f'=== {bibkey} ({path}) ==='
    print(header)
    out_lines.append(header)
    reader = PdfReader(path)
    total_pages = len(reader.pages)
    info = f'Total pages: {total_pages}'
    print(info)
    out_lines.append(info)
    
    full_text = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ''
        full_text.append((idx + 1, text))
        
    found_count = 0
    for page_num, text in full_text:
        lines = text.split('\n')
        i = 0
        while i < len(lines):
            line_s = lines[i].strip()
            # Check if line starts with formal statement header
            match = re.match(r'^(Theorem|Lemma|Corollary|Definition|Claim|Proposition)\s+([0-9\.]+)', line_s, re.IGNORECASE)
            if match:
                # Capture the full block until next empty line or next section
                block = [line_s]
                j = i + 1
                while j < len(lines) and lines[j].strip() != '' and not re.match(r'^(Theorem|Lemma|Corollary|Definition|Claim|Proposition|\d+\s+[A-Z]|Proof)\b', lines[j].strip()):
                    block.append(lines[j].strip())
                    j += 1
                full_stmt = ' '.join(block)
                res = f'  [p.{page_num}] {full_stmt}'
                print(res[:140] + ('...' if len(res) > 140 else ''))
                out_lines.append(res)
                found_count += 1
                i = j - 1
            i += 1
    summary = f'Total formal statements indexed: {found_count}\n'
    print(summary)
    out_lines.append(summary)

with open('tools/extracted_theorems.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))
