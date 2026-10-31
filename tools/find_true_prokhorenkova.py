import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

q = "Graph-based nearest neighbor search: From practice to theory Prokhorenkova"
url = f"https://export.arxiv.org/api/query?search_query=ti:{urllib.parse.quote('Graph-based nearest neighbor search: From practice to theory')}&max_results=3"
with urllib.request.urlopen(url, context=ctx) as r:
    root = ET.fromstring(r.read().decode('utf-8'))
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for e in root.findall("atom:entry", ns):
        title = " ".join(e.find("atom:title", ns).text.split())
        aid = e.find("atom:id", ns).text.split("/abs/")[-1]
        print(f"arXiv: {title} | ID: {aid}")

# Also check Crossref for ICML 2020
url_cr = f"https://api.crossref.org/works?query.title={urllib.parse.quote('Graph-based nearest neighbor search: From practice to theory')}&query.author=Prokhorenkova&rows=3"
req = urllib.request.Request(url_cr, headers={"User-Agent": "FilteredANNBot/1.0"})
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))
    for it in data['message']['items']:
        print("CR:", it.get("title", [""])[0], "| DOI:", it.get("DOI"), "| Container:", it.get("container-title", [""])[0], "| URL:", it.get("URL"))
