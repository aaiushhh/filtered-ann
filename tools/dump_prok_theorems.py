import sys
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def get_text(path, p):
    return (PdfReader(path).pages[p-1].extract_text() or '').replace('\ufb01', 'fi').replace('\ufb02', 'fl')

p_prok = 'papers/prokhorenkova2020graph.pdf'
print("=== PROKHORENKOVA 2020 THEOREMS ===")

for p, label in [
    (4, 'Theorem 1.'),
    (5, 'Theorem 2.'),
    (5, 'Corollary 1.'),
    (5, 'Theorem 3.'),
    (6, 'Corollary 2.'),
    (6, 'Lemma 1.'),
    (6, 'Theorem 4.'),
    (7, 'Corollary 3.')
]:
    t = get_text(p_prok, p)
    idx = t.find(label)
    print(f"\n--- {label} (p. {p}) ---")
    if idx != -1:
        print(t[idx:idx+350].strip())
    else:
        print(f"NOT FOUND on p. {p}!")
