from pathlib import Path
import urllib.request, re, html as htmlmod

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"
OUT.mkdir(exist_ok=True)
url="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/warning_indicator_lights.html"
req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req,timeout=30) as r:
    raw=r.read().decode("utf-8","ignore")

# collect image tags in document order with nearby text
tags=[]
for m in re.finditer(r'<img\b[^>]*>',raw,re.I):
    tag=m.group(0)
    srcm=re.search(r'\bsrc=["\']([^"\']+)["\']',tag,re.I)
    altm=re.search(r'\balt=["\']([^"\']*)["\']',tag,re.I)
    if not srcm: continue
    src=htmlmod.unescape(srcm.group(1))
    alt=htmlmod.unescape(altm.group(1) if altm else "")
    before=re.sub(r'<[^>]+>',' ',raw[max(0,m.start()-300):m.start()])
    after=re.sub(r'<[^>]+>',' ',raw[m.end():m.end()+300])
    ctx=' '.join(htmlmod.unescape(before+" "+after).split())
    tags.append((src,alt,ctx[:450]))

rf=ROOT/"research"/"warning-icon-discovery.md"
lines=["# Warning Icon Discovery","",f"Page: {url}","",f"Image tags found: {len(tags)}",""]
for i,(src,alt,ctx) in enumerate(tags,1):
    lines += [f"## {i}",f"- src: `{src}`",f"- alt: {alt}",f"- context: {ctx}",""]
rf.write_text("\n".join(lines),encoding="utf-8")
print("FOUND",len(tags))
for x in tags[:80]: print(x)
