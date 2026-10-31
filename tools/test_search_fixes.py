import urllib.request
import urllib.parse
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def cr_search(query):
    url = f"https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(query)}&rows=3"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0 (mailto:research@example.org)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get("message", {}).get("items", [])
            for i in items:
                print("CR:", i.get("title", [""])[0], "| DOI:", i.get("DOI"), "| Container:", i.get("container-title", [""])[0])
    except Exception as e:
        print("CR Err:", e)

def arxiv_search(query):
    url = f"https://export.arxiv.org/api/query?search_query=ti:{urllib.parse.quote(query)}&max_results=3"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNBot/1.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.read().decode('utf-8'))
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for e in root.findall("atom:entry", ns):
                title = e.find("atom:title", ns).text.strip().replace("\n", " ")
                id_url = e.find("atom:id", ns).text.strip()
                print("arXiv:", title, "| ID:", id_url)
    except Exception as e:
        print("arXiv Err:", e)

print("--- Mitzenmacher learned bloom filters ---")
arxiv_search("A Model for Learned Bloom Filters")
cr_search("A Model for Learned Bloom Filters and Optimizing by Sandwiching Mitzenmacher")

print("--- Morton Filters ---")
cr_search("Morton Filters: Faster, Space-Efficient Cuckoo Filters Breslow")

print("--- Vacuum Filters ---")
cr_search("Vacuum Filters: More Space-Efficient and Faster Replacement for Bloom and Cuckoo Filters")

print("--- Multi-probe LSH ---")
cr_search("Multi-probe LSH: efficient indexing for high-dimensional similarity search")
