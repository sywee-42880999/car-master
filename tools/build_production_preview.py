from pathlib import Path
from PIL import Image, ImageDraw
import json

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; PARTS.mkdir(parents=True,exist_ok=True)
W,H=640,480
BG=(244,245,246); INK=(30,33,37); MID=(135,140,145); LIGHT=(205,210,215); ACC=(65,85,110)

def C(): return Image.new("RGB",(W,H),BG)
def base_side():
    im=C(); d=ImageDraw.Draw(im)
    d.polygon([(80,325),(135,235),(215,180),(390,165),(505,220),(565,325)],outline=MID,fill=None)
    d.line((115,325,535,325),fill=MID,width=9)
    d.ellipse((145,285,235,375),outline=MID,width=8); d.ellipse((425,285,515,375),outline=MID,width=8)
    d.polygon([(205,190),(385,180),(475,225),(175,225)],outline=MID)
    d.line((300,185,300,325),fill=MID,width=5); d.line((405,190,405,325),fill=MID,width=5)
    return im,d

def base_front():
    im=C(); d=ImageDraw.Draw(im)
    d.polygon([(110,355),(150,155),(490,155),(530,355)],outline=MID)
    d.polygon([(185,185),(455,185),(430,300),(210,300)],outline=MID)
    d.line((150,320,490,320),fill=MID,width=8)
    return im,d

def save(im,id_):
    out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
    v=Image.open(out); v.verify()
    if out.stat().st_size<5000: raise RuntimeError("small")
    return out.stat().st_size

def door_scuff():
    im,d=base_side(); d.line((245,325,395,325),fill=INK,width=28); return im
def door_weather():
    im,d=base_side(); d.line([(175,225),(205,190),(300,185),(300,325),(175,325),(175,225)],fill=INK,width=14,joint="curve"); return im
def window_weather():
    im,d=base_side(); d.line([(205,190),(300,185),(300,225),(175,225),(205,190)],fill=INK,width=12,joint="curve"); return im
def cowl_top():
    im,d=base_front(); d.rectangle((180,300,460,340),fill=INK); return im
def windshield_molding():
    im,d=base_front(); d.line([(185,185),(455,185),(430,300),(210,300),(185,185)],fill=INK,width=13,joint="curve"); return im
def roof_molding():
    im,d=base_side(); d.line((215,180,390,165),fill=INK,width=18); return im
def roof_drip():
    im,d=base_side(); d.line((220,190,405,180),fill=INK,width=10); return im
def sunroof_deflector():
    im,d=base_side(); d.rounded_rectangle((270,155,390,205),radius=12,outline=MID,width=5); d.line((270,155,285,130,365,130,390,155),fill=INK,width=14,joint="curve"); return im
def sunroof_drain():
    im,d=base_side(); d.rounded_rectangle((270,150,395,210),radius=10,outline=MID,width=5)
    d.line((275,155,240,225,210,335),fill=INK,width=14); d.ellipse((268,148,282,162),fill=INK); return im
def antenna_base():
    im,d=base_side(); d.polygon([(370,165),(405,135),(440,165)],fill=INK); d.rectangle((365,160,445,180),fill=INK); return im
def glass_run():
    im,d=base_side(); d.line([(205,190),(300,185),(300,225),(175,225),(205,190)],fill=INK,width=18,joint="curve"); return im
def front_door_frame():
    im,d=base_side(); d.rectangle((175,220,300,325),outline=INK,width=16); d.line((205,190,300,185),fill=INK,width=16); return im
def rear_door_frame():
    im,d=base_side(); d.rectangle((300,220,405,325),outline=INK,width=16); d.line((300,185,390,180),fill=INK,width=16); return im
def liftgate_weather():
    im=C(); d=ImageDraw.Draw(im); d.rounded_rectangle((155,95,485,385),radius=80,outline=MID,width=10); d.rounded_rectangle((185,125,455,355),radius=65,outline=INK,width=17); return im
def hood_weather():
    im,d=base_front(); d.line((145,355,495,355),fill=INK,width=18); return im
def cowl_weather():
    im,d=base_front(); d.line((175,305,465,305),fill=INK,width=18); return im
def cargo_side():
    im=C(); d=ImageDraw.Draw(im); d.polygon([(100,130),(540,130),(520,385),(120,385)],outline=MID)
    d.polygon([(105,245),(230,190),(250,365),(120,385)],fill=INK); return im
def door_seal():
    return door_weather()[0]
def camera_cover():
    im,d=base_front(); d.polygon([(280,190),(360,190),(390,245),(250,245)],fill=INK); d.ellipse((305,210,335,240),fill=BG); return im
def mirror_base():
    im,d=base_side(); d.polygon([(170,220),(210,190),(225,240)],fill=INK); d.ellipse((110,190,185,245),outline=INK,width=14); return im
def anchor_cover():
    im=C(); d=ImageDraw.Draw(im); d.rounded_rectangle((120,150,520,370),radius=55,outline=MID,width=12)
    d.rounded_rectangle((250,250,390,330),radius=18,fill=INK); d.arc((290,250,350,310),0,180,fill=BG,width=8); return im
def door_lock_knob():
    im=C(); d=ImageDraw.Draw(im); d.rectangle((150,310,490,370),fill=MID); d.rounded_rectangle((285,145,355,320),radius=28,fill=INK); d.ellipse((300,165,340,205),fill=BG); return im
def courtesy_light():
    im=C(); d=ImageDraw.Draw(im); d.rounded_rectangle((145,155,495,325),radius=40,fill=INK); d.rounded_rectangle((190,190,450,290),radius=25,fill=(230,180,75)); return im

jobs={
"0210":door_scuff,
"0221":door_weather,
"0222":window_weather,
"0229":cowl_top,
"0230":windshield_molding,
"0231":roof_molding,
"0232":roof_drip,
"0242":sunroof_deflector,
"0243":sunroof_drain,
"0244":antenna_base,
"0245":glass_run,
"0246":front_door_frame,
"0247":rear_door_frame,
"0248":liftgate_weather,
"0249":hood_weather,
"0250":cowl_weather,
"0308":cargo_side,
"0337":door_seal,
"0349":camera_cover,
"0350":mirror_base,
"0328":anchor_cover,
"0331":door_lock_knob,
"0333":courtesy_light,
}
mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
passed=[]; failed=[]
for id_,fn in jobs.items():
    if byid[id_].get("status")=="PASS": continue
    try:
        size=save(fn(),id_); passed.append((id_,byid[id_]["en"],size))
    except Exception as e: failed.append((id_,byid[id_]["en"],str(e)))
for id_,term,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False
    x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=["ORIGINAL_GENERIC_COMPONENT_SCHEMATICS_2026"]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
rf=ROOT/"research"/"backlog-recovery-31-trim-context-schematics.md"
lines=["# CAR MASTER — Backlog Recovery 31 — Trim Context Schematics","",
"Original context-aware technical schematics. Surrounding vehicle geometry is shown lightly; target trim/hardware is emphasized.","","## PASS"]
lines += [f"- **{a} {b}** — 640x480, {c} bytes" for a,b,c in passed] or ["- None"]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Reverse-QA",
"- Similar perimeter components must remain distinguishable by vehicle location: door/window/liftgate/hood/cowl/roof.",
"- 0242 vs 0243 must distinguish sunroof wind deflector vs drain path.",
"- 0246 vs 0247 must distinguish front vs rear door frame.",
"- Count live Production only after Codex reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",len(passed),[x[0] for x in passed]); print("FAIL",failed)
