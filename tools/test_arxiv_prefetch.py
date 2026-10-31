import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

q = "prefetching HNSW"
url = f"https://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(q)}&max_results=5"
with urllib.request.urlopen(url, context=ctx) as r:
    root = ET.fromstring(r.read().decode('utf-8'))
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for e in root.findall("atom:entry", ns):
        title = " ".join(e.find("atom:title", ns).text.split())
        aid = e.find("atom:id", ns).text.split("/abs/")[-1]
        print(f"arXiv: {title} | ID: {aid}")
