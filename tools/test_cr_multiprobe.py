import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://api.crossref.org/works?query=" + urllib.parse.quote("Multi-probe LSH Lv Josephson") + "&rows=5"
req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for item in data.get("message", {}).get("items", []):
            print("Title:", item.get("title", [""])[0], "| DOI:", item.get("DOI"), "| Container:", item.get("container-title", [""])[0])
except Exception as e:
    print(e)
