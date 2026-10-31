with open("manual_download.md", "r", encoding="utf-8") as f:
    content = f.read()

line = "| NORMAL | `xu2024multifilterann` | Multifilterann: Approximate nearest neighbor search with multiple filters | none | https://openreview.net/forum?id=a2eBgp4sjH | 403 Forbidden (OpenReview PDF download blocked) |\n"

if "xu2024multifilterann" not in content:
    with open("manual_download.md", "a", encoding="utf-8") as f:
        f.write(line)
    print("Added xu2024multifilterann to manual_download.md")
else:
    print("Already in manual_download.md")
