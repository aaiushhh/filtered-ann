import re
import sys
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def get_pdf_text_by_pages(pdf_path):
    reader = PdfReader(pdf_path)
    return [p.extract_text() or '' for p in reader.pages]

def audit_paper(bibkey, pdf_path, note_path):
    print(f'======================================================================')
    print(f'AUDIT FOR {bibkey}')
    print(f'PDF: {pdf_path}')
    print(f'NOTE: {note_path}')
    print(f'======================================================================')
    
    pages = get_pdf_text_by_pages(pdf_path)
    print(f'Total PDF Pages: {len(pages)}')
    
    with open(note_path, encoding='utf-8') as f:
        note_content = f.read()
        
    # Extract lines under Complexity / theoretical claims
    claims_match = re.search(r'## Complexity / theoretical claims\n(.*?)\n## Filter type', note_content, re.DOTALL)
    if not claims_match:
        print('Could not find Complexity section in note!')
        return
        
    claims_text = claims_match.group(1).strip()
    claim_items = [line for line in claims_text.split('\n') if line.strip().startswith('-')]
    
    print(f'\nChecking {len(claim_items)} theoretical claim items in note:')
    for item in claim_items:
        print(f'\n--- NOTE ITEM: {item[:100]}...')
        
        # Extract label (e.g., Theorem 3.4, Lemma 2.1, etc.)
        label_match = re.search(r'-\s*(Theorem\s+[\d\.]+|Lemma\s+[\d\.]+|Definition\s+[\d\.]+|Corollary\s+[\d\.]+|Claim\s+[\d\.]+|Proposition\s+[\d\.]+|Section\s+\d+)', item, re.IGNORECASE)
        label = label_match.group(1) if label_match else 'Unknown'
        
        # Extract page locator
        page_match = re.search(r'p\.\s*([\d\–\-]+)', item)
        page_loc = page_match.group(1) if page_match else 'None'
        print(f'    Label: {label} | Stated page: {page_loc}')
        
        # Search for the label in the PDF
        found_pages = []
        for p_idx, p_text in enumerate(pages):
            p_num = p_idx + 1
            # Normalize whitespace and ligatures
            norm = p_text.replace('\ufb01', 'fi').replace('\ufb02', 'fl')
            if re.search(r'\b' + re.escape(label) + r'\b', norm, re.IGNORECASE):
                found_pages.append(p_num)
                
        print(f'    Found in PDF on pages: {found_pages}')
        if page_loc != 'None':
            # Check if claimed page is in found_pages
            claimed_p_nums = []
            for part in re.split(r'[\–\-]', page_loc):
                try:
                    claimed_p_nums.append(int(part))
                except:
                    pass
            match_page = any(cp in found_pages for cp in claimed_p_nums)
            print(f'    Page locator match: {"YES" if match_page else "CHECK (claimed " + page_loc + ", found " + str(found_pages) + ")"}')

audit_paper('indyk2023worst', 'papers/indyk2023worst.pdf', 'notes/indyk2023worst.md')
audit_paper('diwan2024navigable', 'papers/diwan2024navigable.pdf', 'notes/diwan2024navigable.md')
audit_paper('prokhorenkova2020graph', 'papers/prokhorenkova2020graph.pdf', 'notes/prokhorenkova2020graph.md')
