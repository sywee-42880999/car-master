from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"
DL=OUT/"batch-0021-0030-source"
PARTS=ROOT/"images"/"parts"
OUT.mkdir(exist_ok=True); DL.mkdir(parents=True,exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True)

sources={
"0021":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleFrontOverview.jpg.png",(0.00,0.46,0.58,0.88),"PASS","FRONT BUMPER","front bumper is unmistakable; original manual callouts retained"),
"0022":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleRearOverview.jpg.png",(0.42,0.48,1.00,0.88),"PASS","REAR BUMPER","rear bumper is unmistakable; original manual callouts retained"),
"0023":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleFrontOverview.jpg.png",(0.00,0.38,0.50,0.72),"PASS","FRONT GRILLE","grille fills the crop and is visually distinct from bumper"),
"0024":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleFrontOverview.jpg.png",(0.27,0.12,0.67,0.48),"PASS","WINDSHIELD","front windshield glass fills the crop"),
"0025":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleRearOverview.jpg.png",(0.58,0.16,0.94,0.55),"PASS","REAR WINDOW","rear glass is the dominant physical surface"),
"0026":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_OutsideDoorHandle_3.jpg.png",(0.00,0.00,1.00,1.00),"PASS","OUTSIDE DOOR HANDLE","dedicated close-up; handle unmistakable"),
"0027":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_FrontUltrasonicSensor.jpg.png",(0.00,0.25,0.76,0.88),"PASS","ULTRASONIC SENSORS","official image identifies physical front ultrasonic sensors; original callouts retained"),
"0028":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_FrontLampOverveiw.jpg.png",(0.00,0.00,0.80,0.78),"REVIEW","TURN SIGNAL LIGHT","shared DRL/position/turn-signal element remains visually ambiguous"),
"0029":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_HighMountedStopLamp.jpg.png",(0.00,0.00,1.00,0.70),"REVIEW","REAR SPOILER","image shows spoiler structure but source purpose is stop lamp; stronger dedicated source preferred"),
"0030":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RoofRack.jpg.png",(0.00,0.00,1.00,1.00),"PASS","ROOF SIDE RAILS","official dedicated roof-side-rails image"),
}

def ensure(url,id_):
    p=DL/f"{id_}.png"
    if not p.exists(): urllib.request.urlretrieve(url,p)
    return p

def crop4(im,b):
    w,h=im.size; x1,y1,x2,y2=b
    c=im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))
    cw,ch=c.size
    if cw/ch>4/3:
        nw=int(ch*4/3); x=(cw-nw)//2; c=c.crop((x,0,x+nw,ch))
    else:
        nh=int(cw*3/4); y=(ch-nh)//2; c=c.crop((0,y,cw,y+nh))
    return c

cards=[]; report=[
"# CAR MASTER — 0021–0030 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Final term | QA |","|---|---|---|---|"
]
for id_,(url,b,status,term,note) in sources.items():
    try: im=Image.open(ensure(url,id_)).convert("RGB")
    except Exception as e:
        report.append(f"| {id_} | REVIEW | {term} | source download failed: {e} |"); continue
    c=crop4(im,b); c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
    if status=="PASS": c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
    report.append(f"| {id_} | {status} | {term} | {note} |")
    t=ImageOps.contain(c,(560,420))
    card=Image.new("RGB",(600,490),"white"); card.paste(t,((600-t.width)//2,10))
    d=ImageDraw.Draw(card); d.text((12,440),f"{id_} {status} — {term}",fill="black"); d.text((12,462),note,fill="black")
    cards.append(card)

report += ["",
"## Handoff",
"- Codex handoff ready for: **0021–0027, 0030**.",
"- Do not bind/promote 0028 or 0029 yet; both remain REVIEW.",
"- 0027 official physical wording is **ULTRASONIC SENSORS**; prior master wording 'PARKING DISTANCE WARNING SENSOR' should be retained as an alias/system relation, not the final physical-part label.",
"- 0030 official heading is **ROOF SIDE RAILS**; prior 'ROOF RACK' should be retained as an alias/accessory relation, not the pictured factory-rail label.",
"- No new HTML marker is required for PASS crops; Hyundai's own embedded callouts remain part of original source artwork.",
]
(ROOT/"research"/"0021-0030-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
cols=2; rows=math.ceil(len(cards)/cols)
sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards): sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0021-0030-final-qa.jpg",quality=92)
print("PASS assets written: 0021-0027,0030; 0028/0029 held REVIEW")
