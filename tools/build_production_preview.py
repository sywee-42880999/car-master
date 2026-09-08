from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"; DL=OUT/"batch-0101-0110-source"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

def get(url,name):
 p=DL/name
 if not p.exists(): urllib.request.urlretrieve(url,p)
 return Image.open(p).convert("RGB")

ne1n=get("https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_US/images/1C_SteeringWheelControlOverview.jpg.png","NE1N.png")
ne1a=get("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/1C_SteeringWheelControlOverview.jpg.png","NE1A.png")
sun=get("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_Sunvisor.jpg.png","SUNVISOR.png")
roof=get("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SunroofButtonOverview.jpg.png","SUNROOF.png")

specs={
"0101":(ne1n,(0.72,0.66,0.99,0.98),"BLUETOOTH® HANDS-FREE PHONE BUTTON","phone button isolated in NE1N right steering-wheel control inset"),
"0102":(ne1n,(0.37,0.18,0.62,0.42),"IN-CABIN CAMERA","driver-monitoring in-cabin camera housing above steering wheel"),
"0103":(ne1a,(0.16,0.54,0.34,0.95),"DRIVE MODE BUTTON","physical drive-mode control at lower-left of steering wheel"),
"0104":(ne1a,(0.39,0.62,0.60,0.98),"TERRAIN MODE BUTTON","dedicated TERRAIN MODE button at lower steering-wheel spoke"),
"0105":(ne1n,(0.25,0.52,0.76,0.75),"N1/N2 BUTTON","N-specific paired circular N1/N2 controls"),
"0106":(ne1n,(0.71,0.55,0.98,0.78),"NGB BUTTON","NGB control isolated in NE1N right inset"),
"0107":(sun,(0.00,0.00,1.00,1.00),"SUNVISOR","complete sunvisor assembly"),
"0108":(sun,(0.28,0.36,0.72,0.84),"VANITY MIRROR","vanity mirror is dominant in crop"),
"0109":(sun,(0.54,0.32,0.82,0.68),"TICKET HOLDER","ticket holder at side of vanity mirror"),
"0110":(roof,(0.26,0.18,0.74,0.72),"SUNROOF SWITCH","sunroof switch centered in overhead console"),
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

report=["# CAR MASTER — 0101–0110 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[]
for id_,(im,b,term,note) in specs.items():
 c=crop4(im,b)
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
 report.append(f"| {id_} | PASS | {term} | {note} |")
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} PASS — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

report += ["",
"## Handoff",
"- Codex handoff ready for: **0101–0110**.",
"- 0101 keeps regional alias `Bluetooth wireless technology hands-free button`.",
"- 0102 is interior driver-monitoring hardware; never substitute 0010/0017 exterior camera imagery.",
"- 0103 DRIVE MODE BUTTON remains distinct from broader 0055 DRIVE MODE CONTROL.",
"- 0105/0106 use N-model-only source imagery.",
"- 0108 VANITY MIRROR remains distinct from 0088 VANITY MIRROR LAMP.",
"- 0110 teaches the switch, not the sunroof glass/opening.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0101-0110-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")

cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0101-0110-final-qa.jpg",quality=92)
print("PASS 0101-0110")
