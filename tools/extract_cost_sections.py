"""
Task 3: Cost-model formula extraction from PDFs.
For patel2024acorn, pipeannfilter2026, li2025sieve:
extract raw formula text from the PDF around the cost-model sections.
"""
import re
import os

def extract_pages(txt_path, start_page, end_page):
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    result = ''
    for p in range(start_page, end_page + 1):
        pattern = f'--- PAGE {p} ---\n(.*?)(?=--- PAGE \\d+ ---|$)'
        m = re.search(pattern, text, re.DOTALL)
        if m:
            result += f'\n=== PDF PAGE {p} ===\n' + m.group(1)
    return result

os.makedirs('scratch', exist_ok=True)

# patel2024acorn: §3.2, around pages 6-7
text = extract_pages('papers/patel2024acorn.txt', 5, 8)
with open('scratch/cost_patel.txt', 'w', encoding='utf-8') as f:
    f.write(text)

# pipeannfilter2026: Table 1 §4.2, around pages 5-7
text = extract_pages('papers/pipeannfilter2026.txt', 5, 8)
with open('scratch/cost_pipe.txt', 'w', encoding='utf-8') as f:
    f.write(text)

# li2025sieve: §4.2, around pages 4-7
text = extract_pages('papers/li2025sieve.txt', 4, 8)
with open('scratch/cost_sieve.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print("Extracted cost-model sections.")
