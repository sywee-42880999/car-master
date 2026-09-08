from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,re,html,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; DL=OUT/"batch-0061-0070-source"
OUT.mkdir(exist_ok=True); DL.mkdir(parents=True,exist_ok=True)
pages=[
("NE1a_seats","https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/ideb1b81596dd.html"),
("NE1a_headrest","https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/idb9f0cd5cf76.html"),
("NE1a_safety","https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/safety.html"),
("LX3_child","https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/idb1e7bfb1b98.html"),
]
imgs=[]
for tag,url in pages:
    try:
        txt=urllib.request.urlopen(url).read().decode("utf-8","ignore")
    except Exception as e:
        print("PAGE FAIL",tag,e); continue
    # capture image sources from official page
    found=re.findall(r'(?:src|data-src)=["\']([^"\']+\.(?:png|jpg|jpeg))(?:\?[^"\']*)?["\']',txt,re.I)
    seen=set()
    for rel in found:
        rel=html.unescape(rel)
        if rel in seen: continue
        seen.add(rel)
        full=urllib.parse.urljoin(url,rel)
        name=Path(rel).name
        dest=DL/f"{tag}__{name}"
        try:
            urllib.request.urlretrieve(full,dest)
            im=Image.open(dest).convert("RGB")
        except Exception:
            continue
        imgs.append((tag,name,full,im))
print("found",len(imgs),"images")
cards=[]
for tag,name,full,im in imgs:
    t=ImageOps.contain(im,(620,420))
    card=Image.new("RGB",(660,500),"white"); card.paste(t,((660-t.width)//2,10))
    d=ImageDraw.Draw(card); d.text((10,440),f"{tag} — {name}",fill="black"); d.text((10,462),f"{im.width}x{im.height}",fill="black")
    cards.append(card)
if cards:
    cols=2;rows=math.ceil(len(cards)/cols)
    sheet=Image.new("RGB",(cols*660,rows*500),"white")
    for i,c in enumerate(cards):sheet.paste(c,((i%cols)*660,(i//cols)*500))
    sheet.save(OUT/"0061-0070-source-contact.jpg",quality=92)
