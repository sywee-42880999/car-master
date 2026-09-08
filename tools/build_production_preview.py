from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0191-0200-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

sources={
"0193":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_FrontWiperReplacementProcedure_2.jpg.png","PASS","WIPER ARM","front wiper arm is exposed during blade-removal procedure"),
"0194":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RearWiperReplacementProcedure_1.jpg.png","PASS","REAR WIPER ARM","rear wiper arm is explicitly raised in dedicated procedure"),
"0195":("https://ownersmanual.hyundai.com/full_webhelp/DN8/2026/ko_KR/images/2C_HoodOpen.jpg.png","PASS","HOOD LATCH","hood latch/release hardware is shown under hood edge"),
"0196":("https://ownersmanual.hyundai.com/full_webhelp/DN8/2026/ko_KR/images/2C_HoodOpen.jpg.png","PASS","SECONDARY HOOD RELEASE LEVER","official hood-opening procedure identifies the secondary release lever"),
"0197":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_OutsideTailgateOpenButton.jpg.png","PASS","LIFTGATE HANDLE BUTTON","dedicated exterior liftgate handle/open button image"),
"0198":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_GasLift.jpg.png","PASS","LIFTGATE SUPPORT STRUTS","dedicated Hyundai warning image identifies liftgate support struts"),
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

report=["# CAR MASTER — 0191–0200 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|",
"| 0191 | REVIEW | WINDSHIELD WASHER NOZZLE | washer operation pages do not isolate the physical nozzle |",
"| 0192 | REVIEW | REAR WINDOW WASHER NOZZLE | washer operation pages do not isolate the physical rear nozzle |"]
cards=[];passed=[]
for id_,(url,status,term,note) in sources.items():
 try:c=crop4(fetch(url,id_))
 except Exception as e:
  report.append(f"| {id_} | REVIEW | {term} | source failed: {e} |");continue
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0);passed.append(id_)
 report.append(f"| {id_} | {status} | {term} | {note} |")
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} {status} — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

report += [
"| 0199 | REVIEW | DOOR HINGE | no unmistakable dedicated Hyundai Owner's Manual hinge close-up verified in this pass |",
"| 0200 | REVIEW | DOOR CHECKER | exact Hyundai physical-part wording/image not directly verified |","",
"## Handoff",
f"- Codex handoff ready for: **{', '.join(passed)}**.",
"- 0196 terminology corrected from HOOD SAFETY LATCH to **SECONDARY HOOD RELEASE LEVER**; prior term retained as alias.",
"- 0197 terminology refined to **LIFTGATE HANDLE BUTTON** to match visible physical control.",
"- 0198 terminology refined to Hyundai wording **LIFTGATE SUPPORT STRUTS**; LIFTGATE STRUT retained as alias.",
"- 0191, 0192, 0199, 0200 move to Production Backlog; do not block forward progress.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0191-0200-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0191-0200-final-qa.jpg",quality=92)
print("PASS",passed)
