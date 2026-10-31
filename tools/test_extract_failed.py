import os
import pypdf

for k in ["diwan2024navigable", "gupta2023caps"]:
    p = f"papers/{k}.pdf"
    if os.path.exists(p):
        print(f"{k} size: {os.path.getsize(p)}")
        try:
            reader = pypdf.PdfReader(p, strict=False)
            print(f"  Pages: {len(reader.pages)}")
            t = reader.pages[0].extract_text()
            print(f"  Page 1: {t[:100]}...")
            text_pages = []
            for p_idx, page in enumerate(reader.pages):
                try:
                    pt = page.extract_text() or ''
                    text_pages.append(f"--- PAGE {p_idx+1} ---\n{pt}")
                except Exception as ex:
                    print(f"  Page {p_idx+1} failed: {ex}")
            with open(f"papers/{k}.txt", "w", encoding="utf-8") as tf:
                tf.write("\n\n".join(text_pages))
            print(f"  Successfully extracted {len(text_pages)} pages to papers/{k}.txt")
        except Exception as e:
            print(f"  Reader failed: {e}")
