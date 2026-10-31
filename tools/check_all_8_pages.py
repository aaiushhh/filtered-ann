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
    tp = f"papers/{t}.txt"
    with open(tp, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read(1500)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    print(f"=== {t} ===")
    for l in lines[:4]:
        print(" ", l)
