import re
import sys
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def get_page_text(pdf_path, page_num):
    reader = PdfReader(pdf_path)
    return reader.pages[page_num - 1].extract_text() or ''

print("================================================================================")
print("1. indyk2023worst: Raw PDF text vs Note text")
print("================================================================================")
# Check Lemma 2.1, Definition 3.1, Lemma 3.2, Lemma 3.3, Theorem 3.4, Theorem 3.5, Theorem 3.6, Lemma 3.7
p_indyk = 'papers/indyk2023worst.pdf'
for p in [3, 4, 5, 6]:
    text = get_page_text(p_indyk, p)
    print(f"\n--- PDF Page {p} ---")
    for line in text.split('\n'):
        if any(line.strip().startswith(x) for x in ['Lemma 2.1', 'Definition 3.1', 'Lemma 3.2', 'Lemma 3.3', 'Theorem 3.4', 'Theorem 3.5', 'Theorem 3.6', 'Lemma 3.7']):
            print(f"RAW PDF: {line.strip()[:140]}")

print("\n================================================================================")
print("2. diwan2024navigable: Raw PDF text vs Note text")
print("================================================================================")
p_diwan = 'papers/diwan2024navigable.pdf'
for p in [2, 3, 4, 5, 6, 7, 8, 10]:
    text = get_page_text(p_diwan, p)
    print(f"\n--- PDF Page {p} ---")
    for line in text.split('\n'):
        line_clean = line.replace('\ufb01', 'fi').replace('\ufb02', 'fl').strip()
        if any(line_clean.startswith(x) for x in ['Theorem 1', 'Theorem 2', 'Definition 3', 'Theorem 4', 'Claim 5', 'Definition 6', 'Claim 7', 'Claim 8', 'Claim 9', 'Claim 11', 'Claim 12', 'Theorem 13']):
            print(f"RAW PDF: {line_clean[:140]}")

print("\n================================================================================")
print("3. prokhorenkova2020graph: Raw PDF text vs Note text")
print("================================================================================")
p_prok = 'papers/prokhorenkova2020graph.pdf'
for p in [4, 5, 6, 7]:
    text = get_page_text(p_prok, p)
    print(f"\n--- PDF Page {p} ---")
    for line in text.split('\n'):
        line_clean = line.replace('\ufb01', 'fi').replace('\ufb02', 'fl').strip()
        if any(line_clean.startswith(x) for x in ['Theorem 1', 'Theorem 2', 'Corollary 1', 'Theorem 3', 'Corollary 2', 'Lemma 1', 'Theorem 4', 'Corollary 3']):
            print(f"RAW PDF: {line_clean[:140]}")
