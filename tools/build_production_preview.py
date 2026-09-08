from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,re,html,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";DL=OUT/"batch-0111-0120-source"
OUT.mkdir(exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

pages=[
("LX3_storage","https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/id70d45014823.html"),
("LX3_rear_sunshade","https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/id0ffd950ffb8.html"),
("LX3_cargo_net","https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/id235HA0AH02L.html"),
("LX3_cargo_screen","https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/topic_vsw_rdw_nvb.html"),
("LX2_floor_mat","https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/idc7a3a49fead.html"),
("LX3_sunshade","https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/idcaab9d43c10.html"),
]
cards=[]; total=0
for tag,url in pages:
    try: txt=urllib.request.urlopen(url).read().decode("utf-8","ignore")
    except Exception as e:
        print("PAGE FAIL",tag,e);continue
    found=re.findall(r'(?:src|data-src)=["\']([^"\']+\.(?:png|jpg|jpeg))(?:\?[^"\']*)?["\']',txt,re.I)
    seen=set()
    for rel in found:
        rel=html.unescape(rel)
        if rel in seen:continue
        seen.add(rel)
        full=urllib.parse.urljoin(url,rel); name=Path(rel).name; dest=DL/f"{tag}__{name}"
        try:
            urllib.request.urlretrieve(full,dest); im=Image.open(dest).convert("RGB")
        except Exception:continue
        total+=1
        t=ImageOps.contain(im,(620,420)); card=Image.new("RGB",(660,500),"white");card.paste(t,((660-t.width)//2,10))
        d=ImageDraw.Draw(card);d.text((10,440),f"{tag} — {name}",fill="black");d.text((10,462),f"{im.width}x{im.height}",fill="black")
        cards.append(card)
print("found",total,"images")
if cards:
    cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*660,rows*500),"white")
    for i,c in enumerate(cards):sheet.paste(c,((i%cols)*660,(i//cols)*500))
    sheet.save(OUT/"0111-0120-source-contact.jpg",quality=92)
