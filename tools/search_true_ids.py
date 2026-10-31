import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

targets_to_find = [
    {
        "bibkey": "diwan2024navigable",
        "title": "Navigable graphs for high-dimensional nearest neighbor search: Constructions and limits",
        "author": "Diwan"
    },
    {
        "bibkey": "indyk2023worst",
        "title": "Worst-case performance of popular approximate nearest neighbor search implementations: Guarantees and limitations",
        "author": "Indyk"
    },
    {
        "bibkey": "li2025sieve",
        "title": "SIEVE: A Framework for Efficient Filtered Vector Search",
        "author": "Li"
    },
    {
        "bibkey": "xu2024multifilterann",
        "title": "Multi-Filter Approximate Nearest Neighbor Search",
        "author": "Xu"
    },
    {
        "bibkey": "zhang2023vbase",
        "title": "VBASE: Unifying Online Vector Similarity Search and Relational Queries via Relaxed Monotonicity",
        "author": "Zhang"
    }
]

for t in targets_to_find:
    print(f"\n=================== SEARCHING: {t['bibkey']} ===================")
    # 1. Search arXiv by title
    q_title = urllib.parse.quote(f'ti:"{t["title"]}"')
    url_arxiv = f"https://export.arxiv.org/api/query?search_query={q_title}&max_results=3"
    try:
        with urllib.request.urlopen(url_arxiv, context=ctx, timeout=10) as r:
            root = ET.fromstring(r.read().decode('utf-8'))
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            entries = root.findall("atom:entry", ns)
            print(f"arXiv exact matches: {len(entries)}")
            for e in entries:
                title = " ".join(e.find("atom:title", ns).text.split())
                aid = e.find("atom:id", ns).text.split("/abs/")[-1]
                auths = [a.find("atom:name", ns).text for a in e.findall("atom:author", ns)]
                print(f"  arXiv ID: {aid} | {title} | Authors: {', '.join(auths)}")
    except Exception as e:
        print(f"  arXiv search error: {e}")

    # If no exact match, search arXiv by all keywords
    if not entries:
        q_all = urllib.parse.quote(f'{t["title"]} {t["author"]}')
        url_arxiv2 = f"https://export.arxiv.org/api/query?search_query=all:{q_all}&max_results=3"
        try:
            with urllib.request.urlopen(url_arxiv2, context=ctx, timeout=10) as r:
                root = ET.fromstring(r.read().decode('utf-8'))
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                for e in root.findall("atom:entry", ns):
                    title = " ".join(e.find("atom:title", ns).text.split())
                    aid = e.find("atom:id", ns).text.split("/abs/")[-1]
                    auths = [a.find("atom:name", ns).text for a in e.findall("atom:author", ns)]
                    print(f"  arXiv (loose): {aid} | {title} | Authors: {', '.join(auths)}")
        except Exception as e:
            print(f"  arXiv loose error: {e}")

    # 2. Search Crossref
    q_cr = urllib.parse.quote(f'{t["title"]} {t["author"]}')
    url_cr = f"https://api.crossref.org/works?query.bibliographic={q_cr}&rows=3"
    req = urllib.request.Request(url_cr, headers={"User-Agent": "FilteredANNBot/1.0 (mailto:researcher@test.edu)"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            for it in data.get('message', {}).get('items', []):
                t_cr = it.get('title', [''])[0]
                doi = it.get('DOI', '')
                venue = it.get('container-title', [''])[0]
                auths = ", ".join([a.get('family', '') for a in it.get('author', [])])
                print(f"  Crossref: DOI:{doi} | {t_cr} | {venue} | Authors: {auths}")
    except Exception as e:
        print(f"  Crossref error: {e}")
