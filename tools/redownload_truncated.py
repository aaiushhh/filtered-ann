import os
import subprocess
import pypdf

urls = {
    "diwan2024navigable": "https://arxiv.org/pdf/2406.07770",
    "gupta2023caps": "https://arxiv.org/pdf/2308.15014"
}

for k, url in urls.items():
    pdf_path = f"papers/{k}.pdf"
    txt_path = f"papers/{k}.txt"
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    print(f"Downloading {k}...")
    cmd = ['curl.exe', '--ssl-no-revoke', '-L', '--max-time', '180', '-o', pdf_path, url]
    subprocess.run(cmd)
    size = os.path.getsize(pdf_path)
    print(f"{k} downloaded: {size} bytes")
    reader = pypdf.PdfReader(pdf_path, strict=False)
    print(f"{k} pages: {len(reader.pages)}")
    text_pages = []
    for p_idx, page in enumerate(reader.pages):
        pt = page.extract_text() or ''
        text_pages.append(f"--- PAGE {p_idx+1} ---\n{pt}")
    with open(txt_path, "w", encoding="utf-8") as tf:
        tf.write("\n\n".join(text_pages))
    print(f"{k} text extracted successfully ({len(text_pages)} pages).")
