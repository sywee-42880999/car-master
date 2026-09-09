from pathlib import Path
import urllib.request,re
ROOT=Path(__file__).resolve().parents[1]
base="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/"
url=base+"style/webhelp-simbol.css"
req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req,timeout=30) as r: css=r.read().decode("utf-8","ignore")
fonts=re.findall(r'url\(([^)]+)\)',css,re.I)
rf=ROOT/"research"/"warning-font-discovery.md"
rf.write_text("# Warning Font Discovery\n\nCSS: "+url+"\n\n## CSS\n"+css+"\n\n## URLs\n"+"\n".join("- "+x for x in fonts),encoding="utf-8")
print(css)
