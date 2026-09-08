from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True)

url="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_CenterInsideVehicleOverview.jpg.png"
src=OUT/"0051-0060-overview.png"
if not src.exists(): urllib.request.urlretrieve(url,src)
im=Image.open(src).convert("RGB")

specs={
"0051":((220,120,520,470),"PASS","HORN","steering-wheel horn pad is unmistakable"),
"0052":((520,110,780,320),"PASS","INFOTAINMENT SYSTEM","center display/head-unit area"),
"0053":((575,300,845,430),"PASS","CLIMATE CONTROL SYSTEM","climate-control panel and knobs"),
"0054":((35,500,235,620),"PASS","AUTO HOLD BUTTON","AUTO HOLD button in dedicated inset"),
"0055":((45,570,240,695),"REVIEW","DRIVE MODE CONTROL","overview shows DRIVE/TERRAIN integrated control area; canonical physical-part wording still unresolved"),
"0056":((270,500,470,620),"PASS","DOWNHILL BRAKE CONTROL BUTTON","DBC/downhill button in inset"),
"0057":((280,565,475,680),"PASS","PARKING SAFETY BUTTON","P button with sensor waves is isolated"),
"0058":((280,625,475,740),"PASS","PARKING/VIEW BUTTON","P/view camera button is isolated"),
"0059":((345,785,470,970),"PASS","UV-C STERILIZER SYSTEM","dedicated UV-C control/sterilizer area"),
"0060":((875,785,1320,1045),"PASS","AC INVERTER","AC 115V inverter outlet is unmistakable"),
}

def crop4(im,box):
    c=im.crop(box); w,h=c.size
    if w/h>4/3:
        nw=int(h*4/3); x=(w-nw)//2; return c.crop((x,0,x+nw,h))
    nh=int(w*3/4); y=(h-nh)//2; return c.crop((0,y,w,y+nh))

report=["# CAR MASTER — 0051–0060 Chat Production Result","",
"Source: Hyundai 2026 Palisade LX3 Center Console Overview, image key `1C_CenterInsideVehicleOverview`.","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[]
for id_,(box,status,term,note) in specs.items():
    c=crop4(im,box)
    c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
    if status=="PASS": c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
    report.append(f"| {id_} | {status} | {term} | {note} |")
    t=ImageOps.contain(c,(560,420))
    card=Image.new("RGB",(600,490),"white"); card.paste(t,((600-t.width)//2,10))
    d=ImageDraw.Draw(card); d.text((12,440),f"{id_} {status} — {term}",fill="black"); d.text((12,462),note,fill="black")
    cards.append(card)

report += ["",
"## Handoff",
"- Codex handoff ready for: **0051–0054, 0056–0060**.",
"- **0055 DRIVE MODE CONTROL remains REVIEW**. The Hyundai overview labels an integrated DRIVE/TERRAIN control system, but the permanent physical-part naming is still not stable enough for PASS.",
"- 0057 is an interior button and must not be confused with 0027 ULTRASONIC SENSORS.",
"- 0058 is a view-control button and must not be confused with rear camera hardware.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0051-0060-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")

cols=2; rows=math.ceil(len(cards)/cols)
sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards): sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0051-0060-final-qa.jpg",quality=92)
print("PASS assets: 0051-0054,0056-0060; 0055 REVIEW")
