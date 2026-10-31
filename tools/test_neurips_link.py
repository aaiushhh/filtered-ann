import urllib.request
import re

url = 'https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html_text = resp.read().decode('utf-8')
    for m in re.finditer(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html_text, re.DOTALL):
        print(f"HREF: {m.group(1)} | TEXT: {m.group(2).strip()}")
