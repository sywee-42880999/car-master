from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0151-0160-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

url="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_FuelInletDoorOpen.jpg.png"
p=DL/"0154.png"
urllib.request.urlretrieve(url,p)
im=Image.open(p).convert("RGB")

def crop4(im):
 w,h=im.size
 if w/h>4/3:
  nw=int(h*4/3);x=(w-nw)//2;return im.crop((x,0,x+nw,h))
 nh=int(w*3/4);y=(h-nh)//2;return im.crop((0,y,w,y+nh))

c=crop4(im)
c.save(OUT/"0154.jpg",quality=94,subsampling=0)
c.save(PARTS/"0154.jpg",quality=94,subsampling=0)

report=["# CAR MASTER — 0151–0160 Chat Production Result","",
"Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
"| ID | Status | Term | QA |","|---|---|---|---|",
"| 0151 | REVIEW | ENGINE OIL FILTER | official maintenance wording verified, but no unmistakable owner-manual image of the physical filter was verified |",
"| 0152 | REVIEW | DRIVE BELT | official maintenance wording verified, but no dedicated belt-path/physical-part image was verified |",
"| 0153 | REVIEW | SPARK PLUG | official maintenance wording verified, but no dedicated owner-manual physical-part illustration was verified |",
"| 0154 | PASS | FUEL FILLER CAP | dedicated Hyundai fuel-filler-door-open image clearly shows the fuel tank cap behind the door |",
"| 0155 | REVIEW | FUEL TANK | maintenance terminology verified; no unmistakable owner-manual physical tank illustration verified |",
"| 0156 | REVIEW | FUEL TANK AIR FILTER | directly named physical visual still required |",
"| 0157 | REVIEW | FUEL FILTER | directly named physical visual still required |",
"| 0158 | REVIEW | BRAKE LINE | Hyundai groups brake lines/hoses in maintenance text; no isolated rigid-line visual verified |",
"| 0159 | REVIEW | BRAKE HOSE | no isolated flexible brake-hose visual verified |",
"| 0160 | REVIEW | BRAKE PAD | Hyundai maintenance text confirms the term, but no dedicated owner-manual pad illustration was verified |","",
"## Handoff",
"- Codex handoff ready for: **0154 FUEL FILLER CAP**.",
"- **0151–0153, 0155–0160 remain REVIEW**; do not substitute generic web/stock/component imagery.",
"- 0154 remains distinct from 0012 FUEL FILLER DOOR: cap vs exterior flap.",
"- Do not increment Production progress from this handoff alone."
]
(ROOT/"research"/"0151-0160-production-result.md").write_text("\n".join(report)+"\n",encoding="utf-8")
print("PASS 0154; others REVIEW")
