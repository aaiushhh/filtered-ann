import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.usenix.org/conference/osdi23/presentation/zhang-qianxi"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx) as r:
    html = r.read().decode('utf-8')
    m = re.findall(r'href="([^"]+\.pdf)"', html)
    print("Found PDF links:", m)
