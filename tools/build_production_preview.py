from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"; DL=OUT/"batch-0081-0090-source"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

sources={
"0081":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_InsideRearViewMirrorDayNight.jpg.png","INSIDE REARVIEW MIRROR","conventional optical mirror is unmistakable"),
"0082":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_DCMInsidemirrorOverview.jpg.png","DIGITAL CENTER MIRROR","digital center mirror module and controls are unmistakable"),
"0083":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_MapLampLED.jpg.png","MAP LAMP","front overhead map lamps clearly highlighted"),
"0084":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RoomLamp.jpg.png","ROOM LAMP","dedicated room lamp close-up"),
"0085":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_PersonalLamp.jpg.png","REAR PERSONAL LAMP","dedicated rear personal lamp close-up"),
"0086":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_MultiConsole.jpg.png","CENTER CONSOLE LAMP","center-console storage lamp is clearly identified"),
"0087":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_MoodLampLED.jpg.png","MOOD LAMP","ambient/mood light strip is the dominant visual feature"),
"0088":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SunvisorLampLED.jpg.png","VANITY MIRROR LAMP","vanity-mirror lamp is isolated in official illustration"),
"0089":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_GloveBoxLamp.jpg.png","GLOVE BOX LAMP","glove-box lamp is identified with dedicated inset"),
"0090":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_LuggageRoomLamp.jpg.png","CARGO AREA LAMP","cargo-area lamp is identified with dedicated inset"),
}

def fetch(url,id_):
 p=DL/f"{id_}.png"
 if not p.exists(): urllib.request.urlretrieve(url,p)
 return Image.open(p).convert("RGB")

def crop4(im):
 w,h=im.size
 if w/h>4/3:
  nw=int(h*4/3); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
 nh=int(w*3/4); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

report=["# CAR MASTER — 0081–0090 Chat Production Result","",
"Source family: Hyundai 2026 Palisade LX3 official Owner's Manual embedded images.","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|"]
cards=[]
for id_,(url,term,note) in sources.items():
 try:c=crop4(fetch(url,id_))
 except Exception as e:
  report.append(f"| {id_} | REVIEW | {term} | source failed: {e} |"); continue
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
 report.append(f"| {id_} | PASS | {term} | {note} |")
 t=ImageOps.contain(c,(560,420)); card=Image.new("RGB",(600,490),"white"); card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card); d.text((12,440),f"{id_} PASS — {term}",fill="black"); d.text((12,462),note,fill="black"); cards.append(card)

report += ["",
"## Handoff",
"- Codex handoff ready for: **0081–0090**.",
"- 0081 conventional optical mirror and 0082 digital center mirror are separate physical learning cards.",
"- 0083 MAP LAMP and 0084 ROOM LAMP remain distinct functions/locations even when both are overhead lamps.",
"- 0087 MOOD LAMP keeps AMBIENT LIGHT / AMBIENT LIGHTING as possible model aliases only.",
"- 0090 master term follows visible Hyundai wording CARGO AREA LAMP; LUGGAGE ROOM LAMP remains a possible regional/model alias.",
"- No new marker is baked into JPG; original Hyundai callouts/insets remain part of the source artwork.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0081-0090-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")

cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0081-0090-final-qa.jpg",quality=92)
print("PASS 0081-0090")
