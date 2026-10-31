"""
Audit Task 5: Quote verification across all 42 notes.
- Count quotes per note (text inside double-quotes in the note body, excluding headers)
- Flag quotes over 15 words
- Flag notes with more than 1 quote
"""
import os
import re

notes_dir = 'notes'
results = []
total_notes = 0
notes_over_15 = []
notes_multi_quote = []

for fname in sorted(os.listdir(notes_dir)):
    if not fname.endswith('.md') or fname.startswith('_'):
        continue
    
    bk = fname.replace('.md', '')
    total_notes += 1
    
    with open(os.path.join(notes_dir, fname), 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Skip the first line (title header) for quote detection
    lines = content.split('\n')
    body = '\n'.join(lines[1:])
    
    # Find all quoted strings (double quotes only, not backtick-code)
    # Match "..." but not empty quotes
    quotes = re.findall(r'"([^"\n]{3,})"', body)
    
    word_counts = []
    over_15 = []
    for q in quotes:
        wc = len(q.split())
        word_counts.append((q, wc))
        if wc > 15:
            over_15.append((q, wc))
    
    results.append({
        'bibkey': bk,
        'num_quotes': len(quotes),
        'over_15': over_15,
    })
    
    if over_15:
        notes_over_15.append((bk, over_15))
    if len(quotes) > 1:
        notes_multi_quote.append((bk, len(quotes), quotes))

with open('scratch/audit_task5_quotes.md', 'w', encoding='utf-8') as f:
    f.write('# Audit Task 5: Quote Verification Across All Notes\n\n')
    f.write(f'Total notes checked: {total_notes}\n\n')
    
    f.write('## Per-note summary\n\n')
    f.write('| bibkey | quotes found | any over 15 words? |\n')
    f.write('|---|---|---|\n')
    for r in results:
        over = 'YES' if r['over_15'] else 'no'
        f.write(f"| {r['bibkey']} | {r['num_quotes']} | {over} |\n")
    
    f.write(f'\n## Notes with quotes over 15 words ({len(notes_over_15)} notes)\n\n')
    for bk, overs in notes_over_15:
        for q, wc in overs:
            f.write(f'- **{bk}**: {wc} words — "{q[:80]}..."\n')
    
    f.write(f'\n## Notes with more than 1 quote ({len(notes_multi_quote)} notes)\n\n')
    for bk, count, qs in notes_multi_quote:
        f.write(f'- **{bk}**: {count} quotes\n')
        for q in qs:
            f.write(f'  - "{q[:60]}..." ({len(q.split())} words)\n')
    
    f.write(f'\n## Summary\n')
    f.write(f'- Total notes: {total_notes}\n')
    f.write(f'- Notes with >15-word quotes: {len(notes_over_15)}\n')
    f.write(f'- Notes with >1 quote: {len(notes_multi_quote)}\n')

print(f"Task 5: {total_notes} notes, {len(notes_over_15)} with >15-word quotes, {len(notes_multi_quote)} with >1 quote.")
