from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; DL=OUT/"batch-0041-0050-source"; PARTS=ROOT/"images"/"parts"
OUT.mkdir(exist_ok=True); DL.mkdir(parents=True,exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True)

sources={
"0041":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_GloveBox.jpg.png","PASS","GLOVE BOX","dedicated glove-box illustration"),
"0042":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_CenterConsoleBox.jpg.png","REVIEW","CENTER CONSOLE","dedicated image is center-console STORAGE, not the complete console; avoid taxonomy collision with 0111"),
"0043":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_CupHolder.jpg.png","PASS","CUP HOLDER","official multi-location cup-holder overview"),
"0044":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_USBPort.jpg.png","PASS","USB PORT","data/media USB port is clearly isolated"),
"0045":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_USBChargeOutlet.jpg.png","PASS","USB CHARGER","charge-only terminals are clearly identified"),
"0046":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_PowerOutlet_1.jpg.png","PASS","POWER OUTLET","12V outlets clearly shown"),
"0047":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_WirelessSmartPhoneChargingSystem.jpg.png","PASS","WIRELESS SMARTPHONE CHARGING SYSTEM","charging pad and indicator are clearly identified"),
"0048":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_HazardWarningLamp.jpg.png","PASS","HAZARD WARNING FLASHER BUTTON","dedicated hazard button close-up"),
"0049":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_StartButton.jpg.png","PASS","ENGINE START/STOP BUTTON","dedicated physical start/stop button close-up"),
"0050":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_ClusterOverview_1.jpg.png","PASS","INSTRUMENT CLUSTER","complete cluster display is unmistakable"),
}

def ensure(url,id_):
    p=DL/f"{id_}.png"
    if not p.exists(): urllib.request.urlretrieve(url,p)
    return p

def crop4(im):
    w,h=im.size
    if w/h>4/3:
        nw=int(h*4/3); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
    nh=int(w*3/4); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

report=["# CAR MASTER — 0041–0050 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[]
for id_,(url,status,term,note) in sources.items():
    try: im=Image.open(ensure(url,id_)).convert("RGB")
    except Exception as e:
        report.append(f"| {id_} | REVIEW | {term} | source download failed: {e} |"); continue
    c=crop4(im)
    c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
    if status=="PASS": c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
    report.append(f"| {id_} | {status} | {term} | {note} |")
    t=ImageOps.contain(c,(560,420))
    card=Image.new("RGB",(600,490),"white"); card.paste(t,((600-t.width)//2,10))
    d=ImageDraw.Draw(card); d.text((12,440),f"{id_} {status} — {term}",fill="black"); d.text((12,462),note,fill="black")
    cards.append(card)

report += ["",
"## Handoff",
"- Codex handoff ready for: **0041, 0043–0050**.",
"- **0042 CENTER CONSOLE remains REVIEW** because the dedicated official image is specifically Center Console Storage. Use a full-console overview/stronger dedicated source so 0042 does not collide with permanent ID 0111 CENTER CONSOLE STORAGE.",
"- 0049 uses ICE/HEV wording ENGINE START/STOP BUTTON; retain START/STOP BUTTON as EV alias/model variant.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0041-0050-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
cols=2; rows=math.ceil(len(cards)/cols)
sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards): sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0041-0050-final-qa.jpg",quality=92)
print("PASS assets: 0041,0043-0050; 0042 REVIEW")
