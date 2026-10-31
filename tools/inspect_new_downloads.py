import os
from pypdf import PdfReader

files = [
    '3448016.3457550.pdf',
    '3511808.3557610.pdf',
    '3639324.pdf',
    '3654923.pdf',
    'conext14_cuckoofilter.pdf',
    'IndykM-curse.pdf',
    'V3mod-152-RangePQ.pdf'
]

for fname in files:
    fpath = os.path.join('downloaded_paper', fname)
    if not os.path.exists(fpath):
        continue
    print('='*60)
    print(f"File: {fname} ({os.path.getsize(fpath)} bytes)")
    try:
        reader = PdfReader(fpath)
        print(f"Pages: {len(reader.pages)}")
        first_page = reader.pages[0].extract_text() or ""
        clean_text = first_page[:600].replace('\n', ' ').encode('ascii', errors='replace').decode('ascii')
        print("First page excerpt:")
        print(clean_text)
    except Exception as e:
        print(f"Error reading {fname}: {e}")
