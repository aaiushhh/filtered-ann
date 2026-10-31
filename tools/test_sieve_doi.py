import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Check Crossref for li2025sieve (10.14778/3749646.3749725)
url = "https://api.crossref.org/works/10.14778/3749646.3749725"
req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))['message']
    print("SIEVE Title:", data.get("title"))
    print("  URL:", data.get("URL"))
    print("  Resource link:", data.get("resource", {}).get("primary", {}).get("URL"))
    print("  Links:", data.get("link", []))
