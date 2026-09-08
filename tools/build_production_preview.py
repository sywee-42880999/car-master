from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0201-0210-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

sources={
"0201":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_LicensePlateLampLED.jpg.png","LICENSE PLATE LIGHT","dedicated license-plate light replacement image"),
"0203":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SideRepeaterLamp.jpg.png","SIDE REPEATER LIGHT","dedicated Hyundai side-repeater light image"),
"0204":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_FrontLampOverView.jpg.png","SIDE MARKER LIGHT","front lamp overview explicitly labels side marker light"),
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

report=["# CAR MASTER — 0201–0210 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[];passed=[]
for id_,(url,term,note) in sources.items():
 try:c=crop4(fetch(url,id_))
 except Exception as e:
  report.append(f"| {id_} | REVIEW | {term} | source failed: {e} |");continue
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0);passed.append(id_)
 report.append(f"| {id_} | PASS | {term} | {note} |")
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} PASS — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

report += [
"| 0202 | REVIEW | REFLECTOR | LX3 distinguishes rear retro-reflector and rear side retro-reflector; generic REFLECTOR is too broad |",
"| 0205 | REVIEW | DAYTIME RUNNING LIGHT | LX3 shares DRL with parking/turn-signal elements; crop alone does not isolate function strongly enough |",
"| 0206 | REVIEW | POSITION LIGHT | current LX3 wording is PARKING LIGHT and shares lamp elements with DRL/turn signal; taxonomy/source wording needs resolution |",
"| 0207 | REVIEW | FRONT PARKING SENSOR | overlaps permanent ID 0027 ULTRASONIC SENSORS; defer taxonomy split |",
"| 0208 | REVIEW | REAR PARKING SENSOR | overlaps permanent ID 0027 ULTRASONIC SENSORS; defer taxonomy split |",
"| 0209 | REVIEW | SIDE VIEW MIRROR TURN SIGNAL | overlaps 0203 SIDE REPEATER LIGHT on mirror-mounted applications; do not duplicate blindly |",
"| 0210 | REVIEW | DOOR SCUFF TRIM | exact Hyundai naming/image still unresolved |","",
"## Handoff",
f"- Codex handoff ready for: **{', '.join(passed)}**.",
"- 0203 master refined to **SIDE REPEATER LIGHT** from broader SIDE REPEATER.",
"- 0202, 0205–0210 move to Production Backlog / taxonomy review and do not block forward production.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0201-0210-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0201-0210-final-qa.jpg",quality=92)
print("PASS",passed)
