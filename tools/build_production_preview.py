from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0141-0150-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

url="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_EngineRoom.jpg.png"
src=DL/"LX3_ENGINE.png"
if not src.exists(): urllib.request.urlretrieve(url,src)
im=Image.open(src).convert("RGB")

specs={
"0141":((0.08,0.10,0.34,0.48),"PASS","ENGINE COOLANT RESERVOIR","engine coolant reservoir and Hyundai callout remain visible"),
"0142":((0.20,0.16,0.47,0.56),"PASS","ENGINE OIL FILLER CAP","engine oil filler-cap location is identified by official Hyundai callout"),
"0143":((0.54,0.08,0.74,0.43),"PASS","BRAKE FLUID RESERVOIR","brake-fluid reservoir is clearly visible at rear of engine bay"),
"0146":((0.02,0.32,0.24,0.70),"PASS","WINDSHIELD WASHER FLUID RESERVOIR","blue washer-fluid filler neck/cap is unmistakable"),
"0148":((0.58,0.31,0.84,0.72),"PASS","AIR CLEANER","engine intake air-cleaner housing is clearly visible"),
}

def crop4(im,b):
 w,h=im.size;x1,y1,x2,y2=b
 c=im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))
 cw,ch=c.size
 if cw/ch>4/3:
  nw=int(ch*4/3);x=(cw-nw)//2;c=c.crop((x,0,x+nw,ch))
 else:
  nh=int(cw*3/4);y=(ch-nh)//2;c=c.crop((0,y,cw,y+nh))
 return c

report=["# CAR MASTER — 0141–0150 Chat Production Result","",
"Primary source: Hyundai 2026 Palisade LX3 Engine Compartment, image key `1C_EngineRoom`.","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[];passed=[]
for id_,(box,status,term,note) in specs.items():
 c=crop4(im,box)
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0);passed.append(id_)
 report.append(f"| {id_} | {status} | {term} | {note} |")
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} {status} — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

report += ["",
"| 0144 | REVIEW | BATTERY | physical low-voltage battery is visible, but master naming must resolve BATTERY vs 12V BATTERY before PASS |",
"| 0145 | REVIEW | FUSE BOX | conflicts with 0040 generic FUSE BOX; location-qualified taxonomy is required |",
"| 0147 | REVIEW | ENGINE OIL DIPSTICK | overview callout is too small/ambiguous for a strong learning crop; dedicated service close-up preferred |",
"| 0149 | REVIEW | RADIATOR CAP | LX2 official terminology verified, but a dedicated unmistakable source asset was not secured in this pass |",
"| 0150 | REVIEW | CABIN AIR FILTER | NE1N motor-room overview identifies location/cover, not the filter element itself; stronger dedicated filter image required |","",
"## Handoff",
f"- Codex handoff ready for: **{', '.join(passed)}**.",
"- **0144, 0145, 0147, 0149, 0150 remain REVIEW**.",
"- 0145 must not become a second generic FUSE BOX card without location-qualified naming.",
"- 0148 AIR CLEANER is engine intake hardware and must remain distinct from 0150 CABIN AIR FILTER.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0141-0150-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")

cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0141-0150-final-qa.jpg",quality=92)
print("PASS",passed)
