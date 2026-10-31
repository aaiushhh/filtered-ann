import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

doi = "10.5555/1325851.1325958"
url = f"https://api.crossref.org/works/{doi}"
req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(data.get("message", {}).get("title"))
except Exception as e:
    print(e)
