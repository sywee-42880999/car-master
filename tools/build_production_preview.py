from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"; DL=OUT/"batch-0071-0080-source"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

specs={
"0071":("https://ownersmanual.hyundai.com/full_webhelp/NX4a/2026/en_US/images/1C_AirbagOverview.jpg.png",(0.00,0.42,0.35,0.98),"PASS","DRIVER'S FRONT AIRBAG","driver steering-wheel airbag deployment zone"),
"0072":("https://ownersmanual.hyundai.com/full_webhelp/NX4a/2026/en_US/images/1C_AirbagOverview.jpg.png",(0.15,0.34,0.53,0.95),"PASS","PASSENGER'S FRONT AIRBAG","front passenger dashboard airbag deployment zone"),
"0073":("https://ownersmanual.hyundai.com/full_webhelp/NX4a/2026/en_US/images/1C_AirbagOverview.jpg.png",(0.16,0.20,0.54,0.76),"PASS","FRONT SIDE AIRBAG","front seat side-airbag deployment zone"),
"0074":("https://ownersmanual.hyundai.com/full_webhelp/NX4a/2026/en_US/images/1C_AirbagOverview.jpg.png",(0.50,0.30,0.90,0.92),"PASS","REAR SIDE AIRBAG","rear seat side-airbag deployment zone"),
"0075":("https://ownersmanual.hyundai.com/full_webhelp/NX4a/2026/en_US/images/1C_AirbagOverview.jpg.png",(0.06,0.00,0.96,0.40),"PASS","CURTAIN AIRBAG","roof-side curtain airbag deployment zones"),
"0076":("https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_UK/images/1C_AirbagOverviewRHD.jpg.png",(0.00,0.62,0.30,1.00),"PASS","FRONT PASSENGER AIRBAG ON/OFF SWITCH","dedicated switch inset in official RHD airbag overview"),
"0077":("https://ownersmanual.hyundai.com/full_webhelp/DN8/2025/en_AU/images/2C_FrontSeatWarmerSwitchTypea.jpg.png",(0.00,0.00,1.00,1.00),"PASS","SEAT WARMER SWITCH","dedicated seat-warmer switch illustration"),
"0078":("https://ownersmanual.hyundai.com/full_webhelp/DN8/2025/en_AU/images/2C_RearSeatVentilationSwitchTypeb.jpg.png",(0.00,0.00,1.00,1.00),"PASS","AIR VENTILATION SEAT SWITCH","dedicated ventilation-seat control switch illustration"),
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

report=["# CAR MASTER — 0071–0080 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[]
for id_,(url,b,status,term,note) in specs.items():
 try:c=crop4(fetch(url,id_),b)
 except Exception as e:
  report.append(f"| {id_} | REVIEW | {term} | source failed: {e} |");continue
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
 report.append(f"| {id_} | {status} | {term} | {note} |")
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} {status} — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

report += ["",
"| 0079 | REVIEW | SEATBACK FOLDING LEVER | current seat overview does not make the physical lever unmistakable enough for a learning crop |",
"| 0080 | REVIEW | REMOTE FOLDING BUTTON | current seat overview does not isolate the cargo-area remote-folding button clearly enough |","",
"## Handoff",
"- Codex handoff ready for: **0071–0078**.",
"- **0078 terminology corrected to AIR VENTILATION SEAT SWITCH** because the learning image teaches the visible physical control, not the seat feature/system.",
"- **0079 and 0080 remain REVIEW** until stronger dedicated Hyundai control images are verified.",
"- Airbag crops intentionally preserve Hyundai's original numbered deployment-zone callouts; no new marker is baked into JPG.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0071-0080-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0071-0080-final-qa.jpg",quality=92)
print("PASS 0071-0078; 0079-0080 REVIEW")
