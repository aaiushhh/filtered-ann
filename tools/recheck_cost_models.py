import re

def search_text(path, keywords):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    print('=== File:', path, f'({len(text)} chars) ===')
    for kw in keywords:
        matches = [m.start() for m in re.finditer(re.escape(kw), text, re.IGNORECASE)]
        print(f'Keyword "{kw}": {len(matches)} matches')
        for idx in matches[:4]:
            start = max(0, idx - 100)
            end = min(len(text), idx + 250)
            snippet = ' '.join(text[start:end].replace('\n', ' ').split())
            print(f'   ...{snippet}...')

print("--- filtered2026system ---")
search_text('papers/filtered2026system.txt', ['cost model', 'complexity', 'formula', 'analytical', 'crossover'])

print("\n--- routing2026query ---")
search_text('papers/routing2026query.txt', ['cost model', 'complexity', 'formula', 'analytical', 'crossover'])

print("\n--- curator2026 ---")
search_text('papers/curator2026.txt', ['cost model', 'complexity', 'formula', 'analytical', 'crossover'])
