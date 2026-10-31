import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

q = "Multi-Filter Approximate Nearest Neighbor"
url = f"https://api.crossref.org/works?query.title={urllib.parse.quote(q)}&rows=5"
req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))['message']
    for it in data['items']:
        print("CR:", it.get("title", [""])[0], "| DOI:", it.get("DOI"), "| Container:", it.get("container-title", [""])[0], "| Authors:", [a.get("family") for a in it.get("author", [])])
