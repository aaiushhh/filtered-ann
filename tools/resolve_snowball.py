import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import time
import ssl
import os
import glob
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Load notes to find who cites what
notes = {}
for p in glob.glob("notes/*.md"):
    k = os.path.basename(p)[:-3]
    with open(p, "r", encoding="utf-8") as f:
        notes[k] = f.read()

def find_citing_notes(bibkey, title_keywords, authors):
    citing = set()
    for k, text in notes.items():
        if bibkey in text.lower():
            citing.add(k)
            continue
        for kw in title_keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE):
                citing.add(k)
                break
        for auth in authors:
            if auth and re.search(r'\b' + re.escape(auth) + r'\b', text, re.IGNORECASE):
                # Only if title also has partial match or in references
                pass
    return sorted(list(citing))

def fetch_crossref_doi(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNSearchBot/1.0 (mailto:research@example.org)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            msg = data.get("message", {})
            title = msg.get("title", [""])[0]
            authors_list = msg.get("author", [])
            auth_str = ", ".join([f"{a.get('family', '')}, {a.get('given', '')}".strip(', ') for a in authors_list])
            venue = msg.get("container-title", [""])[0] or msg.get("publisher", "")
            issued = msg.get("issued", {}).get("date-parts", [[None]])[0][0]
            link = msg.get("URL", f"https://doi.org/{doi}")
            # Check open access
            is_oa = False
            oa_url = ""
            for l in msg.get("link", []):
                if l.get("content-type") == "application/pdf":
                    oa_url = l.get("URL")
                    is_oa = True
                    break
            return {
                "status": "OK",
                "title": title,
                "authors": auth_str,
                "venue": venue,
                "year": str(issued),
                "doi": doi,
                "link": link,
                "is_oa": is_oa,
                "oa_url": oa_url
            }
    except Exception as e:
        return {"status": "ERR", "error": str(e)}

def fetch_arxiv_id(aid):
    url = f"https://export.arxiv.org/api/query?id_list={aid}"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNSearchBot/1.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            root = ET.fromstring(resp.read().decode('utf-8'))
            ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
            entry = root.find("atom:entry", ns)
            if entry is None:
                return {"status": "ERR", "error": "Not found in arXiv"}
            title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
            title = " ".join(title.split())
            auths = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
            published = entry.find("atom:published", ns).text[:4]
            doi_elem = entry.find("arxiv:doi", ns)
            doi = doi_elem.text if doi_elem is not None else ""
            link = f"https://arxiv.org/abs/{aid}"
            pdf_url = f"https://arxiv.org/pdf/{aid}.pdf"
            return {
                "status": "OK",
                "title": title,
                "authors": ", ".join(auths),
                "venue": "arXiv preprint",
                "year": published,
                "doi": doi,
                "arxiv_id": aid,
                "link": link,
                "is_oa": True,
                "oa_url": pdf_url
            }
    except Exception as e:
        return {"status": "ERR", "error": str(e)}

def search_crossref(query):
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&rows=1"
    req = urllib.request.Request(url, headers={"User-Agent": "FilteredANNSearchBot/1.0 (mailto:research@example.org)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get("message", {}).get("items", [])
            if not items:
                return {"status": "ERR", "error": "No items found"}
            item = items[0]
            title = item.get("title", [""])[0]
            doi = item.get("DOI", "")
            authors_list = item.get("author", [])
            auth_str = ", ".join([f"{a.get('family', '')}, {a.get('given', '')}".strip(', ') for a in authors_list])
            venue = item.get("container-title", [""])[0] or item.get("publisher", "")
            issued = item.get("issued", {}).get("date-parts", [[None]])[0][0]
            link = item.get("URL", f"https://doi.org/{doi}")
            return {
                "status": "OK",
                "title": title,
                "authors": auth_str,
                "venue": venue,
                "year": str(issued),
                "doi": doi,
                "link": link
            }
    except Exception as e:
        return {"status": "ERR", "error": str(e)}

print("Script template ready.")
