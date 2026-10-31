import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://api.crossref.org/works?query.title=" + urllib.parse.quote("Multi-probe LSH: efficient indexing for high-dimensional similarity search") + "&query.author=Lv&rows=3"
req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        items = data.get("message", {}).get("items", [])
        for i in items:
            print("Title:", i.get("title", [""])[0], "| DOI:", i.get("DOI"), "| Container:", i.get("container-title", [""])[0], "| URL:", i.get("URL"))
except Exception as e:
    print(e)
