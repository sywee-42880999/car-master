from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0121-0130-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

sources={
"0121":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_TMKOverview.jpg.png","PASS","TIRE MOBILITY KIT","complete emergency tire mobility kit"),
"0122":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_TMKPartsOverview.jpg.png","PASS","COMPRESSOR","official TMK parts overview; compressor identified"),
"0123":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_TMKPartsOverview.jpg.png","PASS","SEALANT BOTTLE","official TMK parts overview; sealant bottle identified"),
"0124":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_TMKPartsOverview.jpg.png","PASS","PRESSURE GAUGE","official TMK parts overview; pressure gauge identified"),
"0126":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_TMKProcedure_3.jpg.png","PASS","TIRE VALVE","procedure close-up shows wheel/tire valve connection"),
"0127":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SmartKeyOverview.jpg.png","PASS","SMART KEY","dedicated smart-key overview"),
"0128":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_UsingEmerengcyKey_A1.jpg.png","PASS","MECHANICAL KEY","mechanical emergency key visible in dedicated procedure"),
"0129":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_UsingEmerengcyKey_A4.jpg.png","PASS","KEY CYLINDER","driver-door key cylinder exposed"),
"0130":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_EmergencyTrunkOpen.jpg.png","PASS","EMERGENCY LIFTGATE SAFETY RELEASE LATCH","dedicated emergency liftgate release illustration"),
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

report=["# CAR MASTER — 0121–0130 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[]; passed=[]
for id_,(url,status,term,note) in sources.items():
 try:c=crop4(fetch(url,id_))
 except Exception as e:
  report.append(f"| {id_} | REVIEW | {term} | source failed: {e} |"); continue
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0);passed.append(id_)
 report.append(f"| {id_} | {status} | {term} | {note} |")
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} {status} — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

report += ["",
"| 0125 | REVIEW | FILLING HOSE | Hyundai source distinguishes two filling-hose roles; do not collapse without visual/source resolution |","",
"## Handoff",
f"- Codex handoff ready for: **{', '.join(passed)}**.",
"- **0125 FILLING HOSE remains REVIEW**.",
"- 0121 complete kit remains distinct from 0122 compressor / 0123 sealant bottle / 0124 pressure gauge.",
"- 0127 SMART KEY, 0128 MECHANICAL KEY, 0129 KEY CYLINDER remain separate physical items.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0121-0130-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0121-0130-final-qa.jpg",quality=92)
print("PASS",passed,"REVIEW 0125")
