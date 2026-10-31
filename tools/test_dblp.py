import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://dblp.org/search/publ/api?q=Multi-probe+LSH+efficient+indexing&format=json&h=3"
req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        hits = data.get("result", {}).get("hits", {}).get("hit", [])
        for h in hits:
            info = h.get("info", {})
            print("DBLP Title:", info.get("title"))
            print("  Venue:", info.get("venue"), "Year:", info.get("year"))
            print("  DOI:", info.get("doi"))
            print("  URL:", info.get("ee"))
except Exception as e:
    print(e)
