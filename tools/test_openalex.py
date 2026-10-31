import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# OpenAlex is free and open
url = "https://api.openalex.org/works?filter=title.search:Multi-probe%20LSH:%20efficient%20indexing"
req = urllib.request.Request(url, headers={"User-Agent": "mailto:researcher@test.edu"})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for r in data.get("results", [])[:3]:
            print("Title:", r.get("title"))
            print("DOI:", r.get("doi"))
            print("Host venue:", r.get("primary_location", {}).get("source", {}).get("display_name"))
            print("Landing page:", r.get("primary_location", {}).get("landing_page_url"))
            print("PDF:", r.get("primary_location", {}).get("pdf_url"))
            print("Authors:", [a.get("author", {}).get("display_name") for a in r.get("authorships", [])])
except Exception as e:
    print(e)
