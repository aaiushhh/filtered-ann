import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://api.openalex.org/works?filter=title.search:Multi-probe%20LSH:%20efficient%20indexing"
req = urllib.request.Request(url, headers={"User-Agent": "mailto:researcher@test.edu"})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    r = data.get("results", [])[0]
    print("Title:", r.get("title"))
    print("DOI:", r.get("doi"))
    print("Pub Year:", r.get("publication_year"))
    print("Locations:", [(loc.get("landing_page_url"), loc.get("pdf_url"), loc.get("is_oa")) for loc in r.get("locations", [])])
    print("Authors:", [a.get("author", {}).get("display_name") for a in r.get("authorships", [])])
