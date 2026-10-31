import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    ("lv2007multiprobe", "http://www.vldb.org/conf/2007/papers/research/p950-lv.pdf"),
    ("breslow2018morton", "https://www.vldb.org/pvldb/vol11/p1041-breslow.pdf"),
    ("wang2019vacuum", "https://www.vldb.org/pvldb/vol13/p197-wang.pdf"),
    ("fu2019nsg", "https://www.vldb.org/pvldb/vol12/p461-fu.pdf"),
    ("zuo2023arkgraph", "https://www.vldb.org/pvldb/vol16/p1431-zuo.pdf"),
    ("mitzenmacher2018model", "https://proceedings.neurips.cc/paper/2018/file/71e0c50d481b28807d95b5ba6646875b-Paper.pdf"),
    ("ren2020hmann", "https://proceedings.neurips.cc/paper/2020/file/a78b05615797300c14457e937d1ec02a-Paper.pdf"),
    ("zhang2023vbase", "https://www.usenix.org/system/files/osdi23-zhang-qianxi.pdf")
]

for name, u in urls:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            print(f"{name:20}: Status {r.status}, Length {r.headers.get('Content-Length')}, URL={u}")
    except Exception as e:
        print(f"{name:20}: FAILED {e}")
