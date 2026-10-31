import os
import re

notes = sorted([f for f in os.listdir('notes') if f.endswith('.md')])

prefix = "Novelty check: does this paper apply a membership filter (Bloom, Cuckoo, Xor) or a metadata predicate check during graph traversal itself, rather than before or after the search? "

for f in notes:
    p = os.path.join('notes', f)
    with open(p, 'r', encoding='utf-8') as fp:
        content = fp.read()

    # Find the Novelty check section
    m = re.search(r'Novelty check:[ \t]*([^\n]+(?:\n[^\n#]+)?)', content, re.IGNORECASE)
    if not m:
        continue
    full_match = m.group(0)

    # Extract answer part
    # Look for 'Answer:' or 'No.' or 'Yes.'
    after_q = full_match
    if 'rather than before or after the search?' in after_q:
        after_q = after_q.split('rather than before or after the search?')[-1]
    
    clean_after = after_q.strip()
    if clean_after.lower().startswith('answer:'):
        clean_after = clean_after[7:].strip()
    elif clean_after.lower().startswith('answer'):
        clean_after = clean_after[6:].strip()

    # Determine yes / no / unclear
    verdict = 'unclear'
    lower = clean_after.lower()
    if lower.startswith(('yes', '**yes**')):
        verdict = 'yes'
    elif lower.startswith(('no', '**no**')):
        verdict = 'no'
    elif lower.startswith(('unclear', '**unclear**')):
        verdict = 'unclear'

    # Now standardize the line:
    new_line = f"Novelty check: {verdict}. {clean_after}"
    # Replace full_match with new_line
    # If clean_after already starts with yes/no/unclear, don't duplicate
    if clean_after.lower().startswith(('yes', 'no', 'unclear')):
        new_line = f"Novelty check: {clean_after}"

    new_content = content.replace(full_match, new_line)
    with open(p, 'w', encoding='utf-8') as fp:
        fp.write(new_content)

print("Standardized all notes!")
