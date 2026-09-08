from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0131-0140-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

base="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/"
sources={
"0131":(base+"2C_SpareTireReplacementOverview.jpg.png","PASS","JACK HANDLE","official emergency-tools overview"),
"0132":(base+"2C_SpareTireReplacementOverview.jpg.png","PASS","JACK","official emergency-tools overview"),
"0133":(base+"2C_SpareTireReplacementOverview.jpg.png","PASS","TOWING HOOK","official emergency-tools overview"),
"0134":(base+"2C_SpareTireReplacementOverview.jpg.png","PASS","WHEEL LUG NUT WRENCH","official emergency-tools overview"),
"0135":(base+"2C_SpareTireReplacementOverview.jpg.png","PASS","SOCKET","official emergency-tools overview"),
"0136":(base+"2C_SpareTireReplacementPrecedure_1.jpg.png","PASS","SPARE TIRE","dedicated spare-tire procedure image"),
"0137":(base+"2C_SpareTireReplacementPrecedure_3.jpg.png","REVIEW","SPARE TIRE CARRIER","carrier mechanism not unmistakable enough without stronger crop/source"),
"0138":(base+"2C_SpareTireReplacementPrecedure_3.jpg.png","REVIEW","SPARE TIRE RETAINER GUIDE","retainer guide not unmistakable enough without stronger crop/source"),
"0139":(base+"2C_SpareTireReplacementPrecedure_4.jpg.png","REVIEW","WHEEL STUDS","studs are contextually present but not visually isolated enough"),
"0140":(base+"2C_SpareTireReplacementPrecedure_5.jpg.png","PASS","JACKING POSITION","designated jacking point is clearly identified in procedure image"),
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

report=["# CAR MASTER — 0131–0140 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[];passed=[]
for id_,(url,status,term,note) in sources.items():
 try:c=crop4(fetch(url,id_))
 except Exception as e:
  report.append(f"| {id_} | REVIEW | {term} | source failed: {e} |"); continue
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 if status=="PASS":
  c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0);passed.append(id_)
 report.append(f"| {id_} | {status} | {term} | {note} |")
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} {status} — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

report += ["",
"## Handoff",
f"- Codex handoff ready for: **{', '.join(passed)}**.",
"- **0137 SPARE TIRE CARRIER**, **0138 SPARE TIRE RETAINER GUIDE**, **0139 WHEEL STUDS** remain REVIEW.",
"- 0133 removable TOWING HOOK must not be confused with towing-eye cover/hole.",
"- 0136 SPARE TIRE remains separate from normal TIRES 0007.",
"- 0140 is the vehicle jacking point, not the JACK itself.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0131-0140-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0131-0140-final-qa.jpg",quality=92)
print("PASS",passed)
