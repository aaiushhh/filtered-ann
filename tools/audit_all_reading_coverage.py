import os
import re
from pypdf import PdfReader

notes_dir = 'notes'
papers_dir = 'papers'

results = []
for f in sorted(os.listdir(notes_dir)):
    if not f.endswith('.md'):
        continue
    bibkey = f[:-3]
    pdf_path = os.path.join(papers_dir, f"{bibkey}.pdf")
    if not os.path.exists(pdf_path):
        continue
    
    try:
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
    except:
        num_pages = 'error'
        
    with open(os.path.join(notes_dir, f), encoding='utf-8') as nf:
        content = nf.read()
        
    # Check "Read fully:" line
    rf_match = re.search(r'Read fully:\s*([^\n]+)', content)
    rf_status = rf_match.group(1).strip() if rf_match else 'not found'
    
    # Check max page cited in note
    cited_pages = [int(p) for p in re.findall(r'p\.\s*(\d+)', content)]
    max_cited = max(cited_pages) if cited_pages else 0
    
    results.append((bibkey, num_pages, max_cited, rf_status))

print(f"{'bibkey':<30} | {'PDF pp':<8} | {'max cited':<10} | {'Read fully status'}")
print('-' * 75)
for b, np, mc, rf in results:
    flag = ''
    if isinstance(np, int) and np > 20 and mc <= np // 2:
        flag = ' [APPENDIX UNREAD?]'
    print(f"{b:<30} | {str(np):<8} | {str(mc):<10} | {rf}{flag}")
