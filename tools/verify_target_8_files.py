import os

targets = [
    "prokhorenkova2020graph",
    "diwan2024navigable",
    "indyk2023worst",
    "li2025sieve",
    "gupta2023caps",
    "xu2024multifilterann",
    "zhang2023vbase",
    "mitzenmacher2018model"
]

for t in targets:
    p_pdf = f"papers/{t}.pdf"
    p_txt = f"papers/{t}.txt"
    has_pdf = os.path.exists(p_pdf) and os.path.getsize(p_pdf) > 1000
    has_txt = os.path.exists(p_txt) and os.path.getsize(p_txt) > 1000
    pdf_sz = os.path.getsize(p_pdf) if has_pdf else 0
    txt_sz = os.path.getsize(p_txt) if has_txt else 0
    print(f"{t:25}: PDF={has_pdf} ({pdf_sz}B), TXT={has_txt} ({txt_sz}B)")
