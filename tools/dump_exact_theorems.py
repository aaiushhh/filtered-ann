import sys
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def get_text(path, p):
    return PdfReader(path).pages[p-1].extract_text() or ''

print("=== INDYK 2023 THEOREMS ===")
p3 = get_text('papers/indyk2023worst.pdf', 3)
p4 = get_text('papers/indyk2023worst.pdf', 4)
p5 = get_text('papers/indyk2023worst.pdf', 5)
p6 = get_text('papers/indyk2023worst.pdf', 6)

print("\n--- Lemma 2.1 (p. 3) ---")
idx = p3.find("Lemma 2.1")
print(p3[idx:idx+400])

print("\n--- Definition 3.1 (p. 4) ---")
idx = p4.find("Definition 3.1")
print(p4[idx:idx+400])

print("\n--- Lemma 3.2 (p. 4) ---")
idx = p4.find("Lemma 3.2")
print(p4[idx:idx+300])

print("\n--- Lemma 3.3 (p. 4) ---")
idx = p4.find("Lemma 3.3")
print(p4[idx:idx+300])

print("\n--- Theorem 3.4 (p. 5) ---")
idx = p5.find("Theorem 3.4")
print(p5[idx:idx+400])

print("\n--- Theorem 3.5 (p. 5) ---")
idx = p5.find("Theorem 3.5")
print(p5[idx:idx+400])

print("\n--- Theorem 3.6 (p. 6) ---")
idx = p6.find("Theorem 3.6")
print(p6[idx:idx+400])

print("\n--- Lemma 3.7 (p. 6) ---")
idx = p6.find("Lemma 3.7")
print(p6[idx:idx+400])
