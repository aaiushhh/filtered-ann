import csv
import json
import os
from datetime import datetime

# Load snowball ranked results
with open("tools/snowball_ranked.json", "r", encoding="utf-8") as f:
    ranked = json.load(f)

# Read current manifest
with open("manifest.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

if "cited_by" not in fieldnames:
    fieldnames.append("cited_by")

print(f"Existing rows in manifest: {len(rows)}")

existing_keys = set(r["bibkey"] for r in rows)

# Define group mapping for candidates
group_map = {
    "breslow2018morton": "A",
    "dillinger2021ribbon": "A",
    "wang2019vacuum": "A",
    "mitzenmacher2018model": "A",
    "gupta2023caps": "D",
    "zuo2023arkgraph": "D",
    "li2025sieve": "D",
    "zhang2023vbase": "D",
    "xu2024multifilterann": "D",
    "johnson2019billion": "C",
    "ren2020hmann": "C",
    "fu2019nsg": "C",
    "prokhorenkova2020graph": "C",
    "indyk2023worst": "B",
    "diwan2024navigable": "B",
    "lv2007multiprobe": "B"
}

added_rows = []
for c in ranked:
    if c["oa_status"] == "OK" and c["bibkey"] not in existing_keys:
        new_row = {
            "bibkey": c["bibkey"],
            "group": group_map.get(c["bibkey"], "D"),
            "seed_status": "",
            "verified_status": "PUB" if c["doi"] or "proceedings" in c["venue"].lower() or "usenix" in c["venue"].lower() or "vldb" in c["venue"].lower() else "PRE",
            "title": c["title"],
            "link": c["link"],
            "doi": c["doi"],
            "arxiv_id": c["arxiv_id"],
            "verified_venue": c["venue"],
            "verified_year": c["year"],
            "origin": "snowball",
            "verification_result": "OK",
            "notes": f"Snowball candidate for Topic {c['topic']}",
            "relevance": "KEEP",
            "relevance_reason": f"Topic {c['topic']}: {c['topic_name']}",
            "added_in_gate": "4",
            "review_status": "SNOWBALL-CANDIDATE",
            "full_text_status": "PENDING-DOWNLOAD",
            "pdf_source": c["pdf_source"],
            "text_version": "open-access" if c["pdf_source"] != "arxiv" else "arXiv",
            "source_url": c["source_url"],
            "file_size_bytes": "",
            "cited_by": "; ".join(c["cited_by"]) if c["cited_by"] else "none"
        }
        # Fill missing fields for old rows
        for k in fieldnames:
            if k not in new_row:
                new_row[k] = ""
        rows.append(new_row)
        added_rows.append(new_row)

# Ensure all old rows have cited_by populated if missing
for r in rows:
    if "cited_by" not in r or not r["cited_by"]:
        r["cited_by"] = "-"

# Write back to manifest.csv
with open("manifest.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated manifest.csv: {len(rows)} total rows (added {len(added_rows)} open-access snowball candidates).")

# Update manual_download.md with paywalled papers
paywalled = [c for c in ranked if c["oa_status"] == "PAYWALLED"]
print(f"Paywalled candidates to record in manual_download.md: {len(paywalled)}")

manual_download_path = "manual_download.md"
with open(manual_download_path, "r", encoding="utf-8") as f:
    md_content = f.read()

new_md_lines = []
for p in paywalled:
    if p["bibkey"] not in md_content:
        new_line = f"| NORMAL | `{p['bibkey']}` | {p['title']} | {p['doi']} | {p['link']} | paywalled ({p['venue']}) |"
        new_md_lines.append(new_line)

if new_md_lines:
    with open(manual_download_path, "a", encoding="utf-8") as f:
        for l in new_md_lines:
            f.write(l + "\n")
    print(f"Added {len(new_md_lines)} paywalled rows to manual_download.md")
else:
    print("No new paywalled rows needed.")
