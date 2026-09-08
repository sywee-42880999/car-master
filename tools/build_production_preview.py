from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0261-0290-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

def get(url,name):
 p=DL/name
 if not p.exists(): urllib.request.urlretrieve(url,p)
 return Image.open(p).convert("RGB")

cluster=get("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_ClusterOverview_1.jpg.png","cluster.png")
interior=get("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_CenterInsideVehicleOverview.jpg.png","interior.png")

specs={
"0271":(cluster,(0.02,0.12,0.38,0.88),"SPEEDOMETER","speed readout/gauge region in official cluster overview"),
"0272":(cluster,(0.62,0.12,0.98,0.88),"TACHOMETER","engine RPM gauge region in ICE cluster overview"),
"0273":(cluster,(0.58,0.62,0.92,0.98),"FUEL GAUGE","fuel-level area in official cluster overview"),
"0274":(cluster,(0.30,0.62,0.70,0.98),"ODOMETER","odometer/mileage display area in cluster overview"),
"0277":(cluster,(0.20,0.02,0.80,0.35),"TURN SIGNAL INDICATOR","cluster turn-signal indicator area"),
"0278":(cluster,(0.35,0.30,0.70,0.72),"GEAR POSITION INDICATOR","selected gear position shown in cluster display"),
"0280":(interior,(0.00,0.00,1.00,0.70),"DASHBOARD","broad physical dashboard/instrument-panel overview"),
"0281":(interior,(0.35,0.02,0.78,0.62),"INFOTAINMENT DISPLAY","center infotainment display is dominant in crop"),
}

def crop4(im,b):
 w,h=im.size;x1,y1,x2,y2=b
 c=im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))
 cw,ch=c.size
 if cw/ch>4/3:
  nw=int(ch*4/3);x=(cw-nw)//2;c=c.crop((x,0,x+nw,ch))
 else:
  nh=int(cw*3/4);y=max(0,(ch-nh)//2);c=c.crop((0,y,cw,y+nh))
 return c

passed=[];cards=[]
for id_,(im,box,term,note) in specs.items():
 c=crop4(im,box)
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
 passed.append(id_)
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} PASS — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

def write(path,title,passrows,reviewrows):
 lines=[f"# CAR MASTER — {title} Chat Production Result","",
 "30-ID batch 0261–0290. Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
 "| ID | Status | Term | QA |","|---|---|---|---|"]
 for id_,term,note in passrows:
  lines.append(f"| {id_} | PASS | {term} | {note} |")
 for id_,term,note in reviewrows:
  lines.append(f"| {id_} | REVIEW | {term} | {note} |")
 lines += ["","## Handoff","- REVIEW items move to Production Backlog and do not block forward production.","- Do not increment Production progress from this handoff alone."]
 (ROOT/"research"/path).write_text("\n".join(lines)+"\n",encoding="utf-8")

write("0261-0270-production-result.md","0261–0270",[],
[("0261","STEERING WHEEL TILT/TELESCOPIC LEVER","direct unmistakable Hyundai control close-up not secured"),
("0262","POWER STEERING WHEEL ADJUSTMENT SWITCH","trim/model-specific control"),
("0263","INSTRUMENT PANEL ILLUMINATION CONTROL","dedicated control crop not secured"),
("0264","ESC OFF BUTTON","dedicated button source not secured"),
("0265","IDLE STOP AND GO OFF BUTTON","ICE/model-specific; exact source needed"),
("0266","LANE SAFETY BUTTON","overlap with 0097 LANE DRIVING ASSIST BUTTON"),
("0267","POWER LIFTGATE BUTTON","multiple physical locations; source must identify one"),
("0268","FUEL FILLER DOOR RELEASE BUTTON","not present on many modern Hyundai models"),
("0269","CHARGING DOOR OPEN/CLOSE BUTTON","EV/model-specific implementation"),
("0270","HEAD-UP DISPLAY","feature/display source not isolated strongly enough")])

write("0271-0280-production-result.md","0271–0280",
[("0271","SPEEDOMETER","official cluster overview crop"),
("0272","TACHOMETER","official ICE cluster overview crop"),
("0273","FUEL GAUGE","official cluster overview crop"),
("0274","ODOMETER","official cluster overview crop"),
("0277","TURN SIGNAL INDICATOR","official cluster indicator crop"),
("0278","GEAR POSITION INDICATOR","official cluster display crop"),
("0280","DASHBOARD","official interior overview crop")],
[("0275","TRIP COMPUTER","information-page concept rather than physical part"),
("0276","WARNING LIGHT","umbrella term too broad"),
("0279","DRIVER INFORMATION DISPLAY","overlap with instrument cluster/display taxonomy")])

write("0281-0290-production-result.md","0281–0290",
[("0281","INFOTAINMENT DISPLAY","official interior overview crop")],
[("0282","AUDIO CONTROL PANEL","model-specific hardware layout"),
("0283","VOLUME KNOB","physical knob not isolated in verified source"),
("0284","TUNE KNOB","physical knob not isolated in verified source"),
("0285","HOME BUTTON","may be physical/capacitive/software"),
("0286","MEDIA BUTTON","model-specific physical shortcut"),
("0287","SETUP BUTTON","model-specific physical shortcut"),
("0288","SEEK/TRACK BUTTON","dedicated hardware source not secured"),
("0289","PASSENGER AIRBAG INDICATOR","dedicated indicator-module source not secured"),
("0290","DIGITAL KEY PAD","physical interface taxonomy unresolved")])

if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0261-0290-final-qa.jpg",quality=92)

# validation
for id_ in passed:
 p=PARTS/f"{id_}.jpg"
 im=Image.open(p); im.verify()
 im=Image.open(p); w,h=im.size
 if abs((w/h)-(4/3))>0.02: raise RuntimeError(f"{id_} aspect error {w}x{h}")
 if p.stat().st_size<5000: raise RuntimeError(f"{id_} suspiciously small")
print("PASS",passed)
print("VALIDATION_OK",True)
