import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://openreview.net/pdf?id=a2eBgp4sjH"
req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
})

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        print("Status:", r.status, "Content-Type:", r.headers.get("Content-Type"))
        data = r.read()
        print("Length:", len(data), "Header:", data[:10])
        if data[:4] == b'%PDF':
            with open("papers/xu2024multifilterann.pdf", "wb") as f:
                f.write(data)
            print("Successfully saved PDF!")
except Exception as e:
    print(e)
