import urllib.request
import re
import html
import csv
import datetime
import os

os.makedirs('logs', exist_ok=True)

# Initialize logs/fetch_log.csv if not exists
if not os.path.exists('logs/fetch_log.csv'):
    with open('logs/fetch_log.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'bibkey', 'url', 'status'])

papers = ['filtered2026system', 'filteraware2025', 'cftrag2025', 'bridgerag2026']
arxiv_map = {}
with open('manifest.csv', mode='r', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['bibkey'] in papers:
            arxiv_map[row['bibkey']] = row['arxiv_id']

headers = {'User-Agent': 'Mozilla/5.0'}
fetch_log = []

for bibkey in papers:
    aid = arxiv_map.get(bibkey)
    if not aid:
        print(f"No arXiv ID for {bibkey}")
        continue
    url = f'https://arxiv.org/abs/{aid}'
    req = urllib.request.Request(url, headers=headers)
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='replace')
            status = resp.status
            fetch_log.append([ts, bibkey, url, status])
            
            m_title = re.search(r'<meta name="citation_title" content="(.*?)"', content)
            title = html.unescape(m_title.group(1)) if m_title else 'UNVERIFIED'
            
            authors = re.findall(r'<meta name="citation_author" content="(.*?)"', content)
            authors_str = '; '.join([html.unescape(a) for a in authors])
            
            m_abs = re.search(r'<blockquote class="abstract mathjax"><span class="descriptor">Abstract:</span>(.*?)</blockquote>', content, re.DOTALL)
            if not m_abs:
                m_abs = re.search(r'<meta name="citation_abstract" content="(.*?)"', content, re.DOTALL)
            abstract = html.unescape(m_abs.group(1)).strip() if m_abs else 'UNVERIFIED'
            abstract = re.sub(r'\s+', ' ', abstract)
            
            print(f'=== {bibkey} ({aid}) ===')
            print(f'Title: {title}')
            print(f'Authors: {authors_str}')
            print(f'Abstract: {abstract}')
            print('-'*50)
    except Exception as e:
        fetch_log.append([ts, bibkey, url, f'ERR: {e}'])
        print(f'=== {bibkey} ({aid}) ERROR: {e} ===')

with open('logs/fetch_log.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for r in fetch_log:
        writer.writerow(r)
