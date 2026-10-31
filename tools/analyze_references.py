import os
import re
import glob

# Collect all extracted references from the notes
all_refs = {}

for p in glob.glob("notes/*.md"):
    bibkey = os.path.basename(p)[:-3]
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    
    m = re.search(r'## Useful references[^\n]*\n(.*)', content, re.DOTALL)
    if m:
        lines = [line.strip() for line in m.group(1).split('\n') if line.strip().startswith('-')]
        for l in lines:
            entry = l.lstrip('-').strip()
            # Clean up entry
            all_refs.setdefault(entry, []).append(bibkey)

print(f"Total distinct reference entries in notes: {len(all_refs)}")

# Also look for references in survey2025filtered.txt
survey_path = "papers/survey2025filtered.txt"
survey_refs = []
if os.path.exists(survey_path):
    with open(survey_path, "r", encoding="utf-8", errors="ignore") as f:
        st = f.read()
    ref_idx = st.find("References")
    if ref_idx != -1:
        ref_text = st[ref_idx:]
        matches = re.findall(r'\[\d+\]\s+([^\[\n]+(?:\n(?!\s*\[\d+\])[^\n]+)*)', ref_text)
        print(f"Total references parsed from survey: {len(matches)}")
        for m in matches[:15]:
            print("SURVEY REF:", " ".join(m.split()[:15]))
