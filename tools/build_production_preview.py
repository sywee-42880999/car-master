from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0061-0070-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

base_ne="https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/"
base_lx="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/"
specs={
"0061":(base_ne+"1C_FrontSeatOverview.jpg.png",(0.00,0.00,0.50,1.00),"PASS","FRONT SEAT","complete front seat and adjustment context"),
"0062":(base_ne+"1C_FrontSeatOverview.jpg.png",(0.48,0.00,1.00,1.00),"PASS","REAR SEAT","rear seating area from official seat overview"),
"0063":(base_ne+"2C_HeadrestOverview.jpg.png",(0.00,0.00,1.00,1.00),"PASS","HEAD RESTRAINT","dedicated head-restraint illustration"),
"0064":(base_ne+"1C_FrontSeatOverview.jpg.png",(0.02,0.10,0.42,0.68),"PASS","SEATBACK","front seatback is the dominant component"),
"0065":(base_ne+"1C_FrontSeatOverview.jpg.png",(0.02,0.45,0.46,0.96),"PASS","SEAT CUSHION","front seat cushion is the dominant component"),
"0066":(base_lx+"2C_ALRSeatBelt.jpg.png",(0.00,0.00,1.00,1.00),"PASS","SEAT BELT","belt webbing and route are clearly shown"),
"0067":(base_lx+"2C_ALRSeatBeltInstall_4.jpg.png",(0.00,0.00,1.00,1.00),"PASS","SEAT BELT BUCKLE","buckle/latch area is clearly visible in installation close-up"),
"0068":(base_lx+"2C_ALRSeatBeltTetherAnchor.jpg.png",(0.00,0.00,1.00,1.00),"PASS","TETHER ANCHOR","dedicated top-tether anchor illustration"),
"0069":(base_lx+"2C_ALRSeatBeltLowerAnchor.jpg.png",(0.00,0.00,1.00,1.00),"PASS","LATCH LOWER ANCHOR","dedicated lower-anchor illustration"),
}

def fetch(url,id_):
 p=DL/f"{id_}.png"
 if not p.exists(): urllib.request.urlretrieve(url,p)
 return Image.open(p).convert("RGB")
def crop4(im,b):
 w,h=im.size;x1,y1,x2,y2=b
 c=im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))
 cw,ch=c.size
 if cw/ch>4/3:
  nw=int(ch*4/3);x=(cw-nw)//2;c=c.crop((x,0,x+nw,ch))
 else:
  nh=int(cw*3/4);y=(ch-nh)//2;c=c.crop((0,y,cw,y+nh))
 return c

report=["# CAR MASTER — 0061–0070 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[]
for id_,(url,b,status,term,note) in specs.items():
 try: c=crop4(fetch(url,id_),b)
 except Exception as e:
  report.append(f"| {id_} | REVIEW | {term} | source failed: {e} |");continue
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
 report.append(f"| {id_} | {status} | {term} | {note} |")
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} {status} — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

report += ["",
"| 0070 | REVIEW | SEAT BELT PRETENSIONER | no dedicated unmistakable official illustration verified in this pass |","",
"## Handoff",
"- Codex handoff ready for: **0061–0069**.",
"- **0070 SEAT BELT PRETENSIONER remains REVIEW** until a dedicated Hyundai pretensioner illustration is verified.",
"- HEAD RESTRAINT is canonical; HEADREST may remain alias.",
"- 0069 LATCH LOWER ANCHOR is US terminology; ISOFIX LOWER ANCHOR should remain regional alias metadata.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0061-0070-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0061-0070-final-qa.jpg",quality=92)
print("PASS 0061-0069; 0070 REVIEW")
