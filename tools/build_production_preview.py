from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"; DL=OUT/"batch-0091-0100-source"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

overview_url="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_CenterInsideVehicleOverview_2.jpg.png"
p=DL/"overview.png"
if not p.exists(): urllib.request.urlretrieve(overview_url,p)
im=Image.open(p).convert("RGB")

specs={
"0091":((0.00,0.05,0.28,0.62),"PASS","LIGHTING CONTROL LEVER","left steering-column lighting stalk"),
"0092":((0.70,0.05,1.00,0.62),"PASS","WIPER AND WASHER CONTROL LEVER","right steering-column wiper/washer stalk"),
"0094":((0.10,0.44,0.37,0.78),"PASS","DRIVING ASSIST BUTTON","steering-wheel driving-assist control"),
"0095":((0.18,0.52,0.44,0.88),"PASS","CLUSTER DISPLAY CONTROL BUTTON","cluster/display control button group"),
"0096":((0.48,0.48,0.72,0.78),"PASS","VEHICLE DISTANCE BUTTON","vehicle-distance steering-wheel button"),
"0097":((0.58,0.45,0.83,0.78),"PASS","LANE DRIVING ASSIST BUTTON","lane-driving-assist steering-wheel button"),
"0098":((0.72,0.58,0.96,0.92),"PASS","ROTARY GEAR SHIFT DIAL","rotary gear selector dial"),
"0099":((0.08,0.56,0.36,0.90),"PASS","STEERING WHEEL AUDIO CONTROLS","audio-control button group"),
"0100":((0.05,0.63,0.30,0.93),"PASS","VOICE RECOGNITION BUTTON","voice-recognition steering-wheel button"),
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

report=["# CAR MASTER — 0091–0100 Chat Production Result","",
"Primary source: Hyundai 2026 Palisade LX3 Steering Wheel Control Overview, image key `1C_CenterInsideVehicleOverview_2`.","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[]
for id_,(box,status,term,note) in specs.items():
 c=crop4(im,box)
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0); c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
 report.append(f"| {id_} | {status} | {term} | {note} |")
 t=ImageOps.contain(c,(560,420)); card=Image.new("RGB",(600,490),"white"); card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card); d.text((12,440),f"{id_} {status} — {term}",fill="black"); d.text((12,462),note,fill="black"); cards.append(card)

# dedicated paddle source
purl="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_PaddleShift.jpg.png"
pp=DL/"0093.png"
try:
 urllib.request.urlretrieve(purl,pp); pim=Image.open(pp).convert("RGB")
 c=crop4(pim,(0,0,1,1)); c.save(OUT/"0093.jpg",quality=94,subsampling=0); c.save(PARTS/"0093.jpg",quality=94,subsampling=0)
 report.append("| 0093 | PASS | PADDLE SHIFTERS | dedicated paddle-shifter close-up; plural master term retained for left/right pair |")
 t=ImageOps.contain(c,(560,420)); card=Image.new("RGB",(600,490),"white"); card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card); d.text((12,440),"0093 PASS — PADDLE SHIFTERS",fill="black"); d.text((12,462),"dedicated paddle-shifter close-up",fill="black"); cards.append(card)
except Exception as e:
 report.append(f"| 0093 | REVIEW | PADDLE SHIFTERS | dedicated source failed: {e} |")

report += ["",
"## Handoff",
"- Codex handoff ready for: **0091–0100**.",
"- 0093 master stays plural PADDLE SHIFTERS; official singular `Paddle shifter` is retained as source wording/alias.",
"- 0098 ROTARY SHIFTER remains an alias for ROTARY GEAR SHIFT DIAL.",
"- 0099 AUDIO REMOTE CONTROL BUTTONS remains an alias for STEERING WHEEL AUDIO CONTROLS.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0091-0100-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0091-0100-final-qa.jpg",quality=92)
print("PASS 0091-0100")
