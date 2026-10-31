import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

q = "Multifilterann Approximate nearest neighbor search with multiple filters"
url = f"https://export.arxiv.org/api/query?search_query=ti:{urllib.parse.quote(q)}&max_results=3"
with urllib.request.urlopen(url, context=ctx) as r:
    root = ET.fromstring(r.read().decode('utf-8'))
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)
    print("Found entries:", len(entries))
    for e in entries:
        print("Title:", e.find("atom:title", ns).text.strip())
        print("ID:", e.find("atom:id", ns).text.strip())
