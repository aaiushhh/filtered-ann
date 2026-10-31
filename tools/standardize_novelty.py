import os
import re

notes = sorted([f for f in os.listdir('notes') if f.endswith('.md')])

for f in notes:
    p = os.path.join('notes', f)
    with open(p, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('Novelty check: does this paper apply'):
            # Check if next line is 'Answer: ...'
            if i + 1 < len(lines) and lines[i+1].strip().lower().startswith(('answer:', 'answer')):
                ans_line = lines[i+1].strip()
                # Clean up into single line: Novelty check: <ans_line>
                clean_ans = re.sub(r'^answer:?\s*', '', ans_line, flags=re.IGNORECASE)
                new_lines.append(f"Novelty check: {clean_ans}\n")
                i += 2
                continue
            elif '?' in line:
                # Prompt question without inline answer; check if answer is on same line or next
                # Let's inspect
                new_lines.append(line)
                i += 1
                continue
        new_lines.append(line)
        i += 1

    with open(p, 'w', encoding='utf-8') as fp:
        fp.writelines(new_lines)

print("Standardized Novelty check lines.")
