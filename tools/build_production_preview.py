from pathlib import Path
import urllib.request,re
ROOT=Path(__file__).resolve().parents[1]
url="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/warning_indicator_lights.html"
req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req,timeout=30) as r: raw=r.read().decode("utf-8","ignore")
terms=["Seat belt warning light","Motor Driven Power Steering","Low fuel level warning light","High Beam Assist"]
lines=["# Warning DOM Discovery",""]
for t in terms:
    i=raw.find(t)
    lines += [f"## {t}", raw[max(0,i-1200):i+800], ""]
styles=re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)',raw,re.I)
lines += ["## styles"]+[f"- {x}" for x in styles]
(ROOT/"research"/"warning-dom-discovery.md").write_text("\n".join(lines),encoding="utf-8")
print("styles",styles)
