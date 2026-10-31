import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Search vldb.org for "SIEVE: Effective Filtered Vector Search"
for vol in [18, 17, 19]:
    url = f"https://www.vldb.org/pvldb/vol{vol}.html"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            m = re.findall(r'href="([^"]+\.pdf)"[^>]*>.*?SIEVE', html, re.IGNORECASE | re.DOTALL)
            print(f"Vol {vol} matches: {len(m)}")
            for link in m:
                print(f"  {link}")
    except Exception as e:
        print(f"Vol {vol} err: {e}")
