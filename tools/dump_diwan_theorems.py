import sys
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def get_text(path, p):
    return (PdfReader(path).pages[p-1].extract_text() or '').replace('\ufb01', 'fi').replace('\ufb02', 'fl')

p_diwan = 'papers/diwan2024navigable.pdf'
print("=== DIWAN 2024 THEOREMS ===")

for p, label in [
    (2, 'Theorem 1.'),
    (3, 'Theorem 2.'),
    (4, 'Definition 3'),
    (7, 'Theorem 4.'),
    (7, 'Claim 5'),
    (7, 'Definition 6'),
    (7, 'Claim 7'),
    (7, 'Claim 8'),
    (7, 'Claim 9'),
    (8, 'Claim 11'),
    (8, 'Claim 12'),
    (10, 'Theorem 13.')
]:
    t = get_text(p_diwan, p)
    idx = t.find(label)
    print(f"\n--- {label} (p. {p}) ---")
    if idx != -1:
        print(t[idx:idx+350].strip())
    else:
        print(f"NOT FOUND on p. {p}!")
