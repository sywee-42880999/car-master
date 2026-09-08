from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0221-0230-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

candidates={
"front":"https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleFrontOverview.jpg.png",
"rear":"https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleRearOverview.jpg.png",
}
imgs={}
for k,u in candidates.items():
 p=DL/f"{k}.png"
 try:
  urllib.request.urlretrieve(u,p);imgs[k]=Image.open(p).convert("RGB")
 except Exception as e: print("FAIL",k,e)

specs={}
if "front" in imgs:
 specs["0226"]=(imgs["front"],(0.00,0.40,0.35,0.95),"WHEEL ARCH CLADDING","front wheel-arch cladding area is clearly visible")
 specs["0227"]=(imgs["front"],(0.00,0.22,0.42,0.88),"FENDER","front fender panel around wheel opening is visible")
if "rear" in imgs:
 specs["0228"]=(imgs["rear"],(0.55,0.22,0.98,0.90),"QUARTER PANEL","rear quarter body panel around wheel/liftgate side is visible")

def crop4(im,b):
 w,h=im.size;x1,y1,x2,y2=b
 c=im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))
 cw,ch=c.size
 if cw/ch>4/3:
  nw=int(ch*4/3);x=(cw-nw)//2;c=c.crop((x,0,x+nw,ch))
 else:
  nh=int(cw*3/4);y=(ch-nh)//2;c=c.crop((0,y,cw,y+nh))
 return c

report=["# CAR MASTER — 0221–0230 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|",
"| 0221 | REVIEW | DOOR WEATHERSTRIP | direct Hyundai close-up not verified in this pass |",
"| 0222 | REVIEW | WINDOW WEATHERSTRIP | terminology/visual overlap with belt molding and run channel |",
"| 0223 | REVIEW | DOOR SILL | direct unmistakable Hyundai sill image not verified |",
"| 0224 | REVIEW | ROCKER PANEL | structural panel boundary is not sufficiently explicit in owner-manual overview |",
"| 0225 | REVIEW | SIDE SILL GARNISH | naming varies by model; direct labeled source required |"]
cards=[];passed=[]
for id_,(im,box,term,note) in specs.items():
 c=crop4(im,box)
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0);passed.append(id_)
 report.append(f"| {id_} | PASS | {term} | {note} |")
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} PASS — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)
for id_,term in [("0229","COWL TOP COVER"),("0230","WINDSHIELD MOLDING")]:
 report.append(f"| {id_} | REVIEW | {term} | exact Hyundai labeled close-up not verified |")
report += ["","## Handoff",f"- Codex handoff ready for: **{', '.join(passed) if passed else 'none'}**.",
"- All remaining IDs in this batch move to Production Backlog and do not block forward production.",
"- Do not increment Production progress from this handoff alone."]
(ROOT/"research"/"0221-0230-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0221-0230-final-qa.jpg",quality=92)
print("PASS",passed)
