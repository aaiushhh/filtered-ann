import os
import re

notes = sorted([f for f in os.listdir('notes') if f.endswith('.md')])
print(f"Checking quotes across {len(notes)} notes...")

over_15 = []

for f in notes:
    p = os.path.join('notes', f)
    with open(p, 'r', encoding='utf-8') as fp:
        c = fp.read()

    # extract double-quoted strings
    quotes = re.findall(r'"([^"\n]+)"', c)
    for q in quotes:
        words = q.split()
        if len(words) > 15:
            over_15.append((f, len(words), q))

if not over_15:
    print("ALL quotes across all notes are <= 15 words! (Rule 3 passed)")
else:
    print(f"Found {len(over_15)} quotes > 15 words:")
    for f, count, q in over_15:
        print(f"  [{f}] ({count} words): \"{q[:50]}...\"")
