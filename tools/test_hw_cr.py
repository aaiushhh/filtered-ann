import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

q = "graph approximate nearest neighbor hardware acceleration prefetch cache"
url = f"https://api.crossref.org/works?query={urllib.parse.quote(q)}&rows=5"
req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
with urllib.request.urlopen(req, context=ctx) as r:
    items = json.loads(r.read().decode('utf-8'))['message']['items']
    for it in items:
        print("CR:", it.get("title", [""])[0], "| DOI:", it.get("DOI"), "| Venue:", it.get("container-title", [""])[0])
