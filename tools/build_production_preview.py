from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True)
url="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_SideInsideVehicleOverview.jpg.png"
src=OUT/"0031-0040-overview.png"
if not src.exists(): urllib.request.urlretrieve(url,src)
im=Image.open(src).convert("RGB")

# pixel-space crops selected from visual QA of the official LX3 interior overview.
specs={
"0031":((0,430,360,790),"PASS","INSIDE DOOR HANDLE","inside handle + door-trim context"),
"0032":((130,720,420,1050),"PASS","POWER WINDOW SWITCHES","driver window switch bank"),
"0033":((145,875,390,1080),"PASS","POWER WINDOW LOCK BUTTON","bottom lock button region"),
"0034":((210,750,400,900),"PASS","CENTRAL DOOR LOCK SWITCH","door lock/unlock switch"),
"0035":((220,680,405,825),"PASS","SIDE VIEW MIRROR CONTROL SWITCH","mirror direction/control pad"),
"0036":((180,690,355,825),"PASS","SIDE VIEW MIRROR FOLDING BUTTON","mirror folding control area"),
"0037":((230,165,380,365),"PASS","EPB (ELECTRONIC PARKING BRAKE) SWITCH","dedicated EPB switch in inset"),
"0038":((410,650,550,930),"PASS","HOOD RELEASE LEVER","lower dash hood release lever"),
"0039":((500,90,1190,790),"PASS","STEERING WHEEL","complete steering wheel"),
"0040":((455,600,625,900),"REVIEW","FUSE BOX","overview indicates location but cover/box is not unmistakable enough"),
}

def crop4(im,box):
    c=im.crop(box)
    w,h=c.size
    if w/h>4/3:
        nw=int(h*4/3); x=(w-nw)//2; c=c.crop((x,0,x+nw,h))
    else:
        nh=int(w*3/4); y=(h-nh)//2; c=c.crop((0,y,w,y+nh))
    return c

report=["# CAR MASTER — 0031–0040 Chat Production Result","",
"Source: Hyundai 2026 Palisade LX3 Owner's Manual Interior Overview, image key `1C_SideInsideVehicleOverview`.","",
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
"- Codex handoff ready for: **0031–0039**.",
"- **0040 FUSE BOX remains REVIEW**. The overview is adequate for terminology/location but not for a self-evident fuse-box learning image. Find a dedicated official Hyundai fuse-box/fuse-panel illustration before promotion.",
"- No new HTML marker requested for PASS crops; original Hyundai callouts remain part of the embedded source artwork.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0031-0040-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
cols=2; rows=math.ceil(len(cards)/cols)
sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards): sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0031-0040-final-qa.jpg",quality=92)
print("PASS assets: 0031-0039; 0040 REVIEW")
