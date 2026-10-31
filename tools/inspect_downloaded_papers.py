import os
from pypdf import PdfReader

for fname in os.listdir('downloaded_paper'):
    if not fname.endswith('.pdf'):
        continue
    fpath = os.path.join('downloaded_paper', fname)
    print('='*50)
    print(f"File: {fname} ({os.path.getsize(fpath)} bytes)")
    try:
        reader = PdfReader(fpath)
        print(f"Pages: {len(reader.pages)}")
        first_page = reader.pages[0].extract_text()
        print("First page excerpt (first 500 chars):")
        clean_text = first_page[:500].replace('\n', ' ').encode('ascii', errors='replace').decode('ascii')
        print(clean_text)
    except Exception as e:
        print(f"Error reading {fname}: {e}")
