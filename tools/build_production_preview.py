from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,re,html,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0111-0120-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

sources={
"0111":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_CenterConsoleBox.jpg.png","CENTER CONSOLE STORAGE","dedicated center-console storage image"),
"0112":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_OpenTray.jpg.png","OPEN TRAY","dedicated open-tray image"),
"0113":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_InteractiveMulticonsoleBottomStorageBox.jpg.png","SLIDING TRAY","dedicated sliding-tray storage image"),
"0114":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_CargoCompartmentStorageOrganizationBox.jpg.png","CARGO TRAY","dedicated under-floor cargo tray image"),
"0115":("https://ownersmanual.hyundai.com/full_webhelp/NX4a/2026/en_US/images/2C_CoatHook.jpg.png","COAT HOOK","dedicated coat-hook illustration"),
"0116":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RearSeatSideCurtain.jpg.png","REAR SIDE SUNSHADE","dedicated rear-side sunshade illustration"),
"0117":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_CargoNet_2.jpg.png","CARGO NET HOLDER","cargo-net holder/anchor points are visible"),
"0118":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_LuggageScreen.jpg.png","CARGO SECURITY SCREEN","dedicated luggage/cargo screen illustration"),
"0119":("https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/images/2C_FloorMatAnchor.jpg.png","FLOOR MAT ANCHORS","floor-mat anchor hardware"),
"0120":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_DualSunroofButton.jpg.png","POWER SUNSHADE SWITCH","overhead power-sunshade control module"),
}

def fetch(url,id_):
 p=DL/f"{id_}.png"
 if not p.exists(): urllib.request.urlretrieve(url,p)
 return Image.open(p).convert("RGB")
def crop4(im):
 w,h=im.size
 if w/h>4/3:
  nw=int(h*4/3);x=(w-nw)//2;return im.crop((x,0,x+nw,h))
 nh=int(w*3/4);y=(h-nh)//2;return im.crop((0,y,w,y+nh))

report=["# CAR MASTER — 0111–0120 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[]; passed=[]
for id_,(url,term,note) in sources.items():
 try:c=crop4(fetch(url,id_))
 except Exception as e:
  report.append(f"| {id_} | REVIEW | {term} | source failed: {e} |");continue
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0);passed.append(id_)
 report.append(f"| {id_} | PASS | {term} | {note} |")
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} PASS — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

report += ["",
"## Handoff",
f"- Codex handoff ready for: **{', '.join(passed)}**.",
"- 0111 CENTER CONSOLE STORAGE remains distinct from 0042 CENTER CONSOLE assembly.",
"- 0117 teaches the holder/anchor area, not merely the cargo net fabric.",
"- 0118 uses LUGGAGE SCREEN as source/asset wording only; master remains CARGO SECURITY SCREEN.",
"- 0119 master remains plural FLOOR MAT ANCHORS; source may use Floor Mat Anchor(s).",
"- 0120 teaches the dedicated power-sunshade control; do not confuse with 0110 SUNROOF SWITCH.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0111-0120-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0111-0120-final-qa.jpg",quality=92)
print("PASS",passed)
