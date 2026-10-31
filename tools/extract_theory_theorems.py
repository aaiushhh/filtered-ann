import re
import os

def extract_theorems(bibkey, txt_path, out_path):
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()

    lines = text.split('\n')
    
    # We want to find all sections, definitions, theorems, lemmas, propositions, corollaries
    # and print their full statements.
    pattern = re.compile(r'^\s*(Theorem|Lemma|Proposition|Corollary|Definition)\s+([0-9]+(\.[0-9]+)*)', re.IGNORECASE)
    
    extracted = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = pattern.match(line)
        if m:
            header = m.group(0).strip()
            # collect statement until next blank line or next header
            stmt_lines = [line]
            j = i + 1
            blank_count = 0
            while j < len(lines):
                next_line = lines[j]
                if pattern.match(next_line) or next_line.strip().startswith('Proof') or next_line.strip().startswith('Section') or next_line.strip().startswith('References'):
                    break
                if next_line.strip() == '':
                    blank_count += 1
                    if blank_count > 2:
                        break
                else:
                    blank_count = 0
                stmt_lines.append(next_line)
                j += 1
            extracted.append({
                'header': header,
                'start_line': i,
                'content': '\n'.join(stmt_lines)
            })
            i = j
        else:
            i += 1

    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(f"# Formal Statements Extracted for {bibkey}\n\n")
        out.write(f"Total entries found: {len(extracted)}\n\n")
        for e in extracted:
            out.write(f"## {e['header']} (around line {e['start_line']})\n")
            out.write(e['content'].strip() + "\n\n")
            out.write("---\n\n")

os.makedirs('scratch', exist_ok=True)
extract_theorems('indyk2023worst', 'papers/indyk2023worst.txt', 'scratch/indyk2023worst_theorems.md')
extract_theorems('diwan2024navigable', 'papers/diwan2024navigable.txt', 'scratch/diwan2024navigable_theorems.md')
extract_theorems('prokhorenkova2020graph', 'papers/prokhorenkova2020graph.txt', 'scratch/prokhorenkova2020graph_theorems.md')
print("Extracted all theorems to scratch/")
