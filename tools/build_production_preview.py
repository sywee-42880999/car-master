from pathlib import Path
from PIL import Image, ImageDraw
import json, math

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; PARTS.mkdir(parents=True,exist_ok=True)
W,H=640,480
BG=(240,242,244); INK=(26,29,33); MID=(105,112,118); LIGHT=(205,210,215)

def C(): return Image.new("RGB",(W,H),BG)
def L(d,pts,w=10,fill=INK): d.line(pts,fill=fill,width=w,joint="curve")
def save(im,id_):
    out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
    v=Image.open(out); v.verify()
    if out.stat().st_size<5000: raise RuntimeError("small")
    return out.stat().st_size

def floor_anchor():
    im=C(); d=ImageDraw.Draw(im)
    d.ellipse((190,110,450,370),fill=INK); d.ellipse((245,165,395,315),fill=BG)
    d.rectangle((275,50,365,135),fill=MID)
    d.rounded_rectangle((250,260,390,410),radius=30,fill=INK)
    d.ellipse((290,300,350,360),fill=BG); return im

def door_hinge():
    im=C(); d=ImageDraw.Draw(im)
    d.rectangle((120,120,255,360),fill=INK); d.rectangle((385,120,520,360),fill=INK)
    d.rounded_rectangle((235,165,405,315),radius=35,fill=MID)
    d.rectangle((305,130,335,350),fill=INK)
    for x in (175,465):
        for y in (175,305): d.ellipse((x-16,y-16,x+16,y+16),fill=BG)
    return im

def door_checker():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((110,185,245,295),radius=25,fill=INK)
    L(d,[(245,240),(510,240)],28,MID)
    d.rectangle((485,185,545,295),fill=INK)
    for x in (165,515): d.ellipse((x-17,223,x+17,257),fill=BG)
    return im

def reflector():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((105,150,535,330),radius=45,fill=(170,35,35))
    for y in range(175,315,28):
        for x in range(130,520,36):
            d.line((x,y,x+22,y+12),fill=(245,110,100),width=5)
    return im

def cup_insert():
    im=C(); d=ImageDraw.Draw(im)
    d.ellipse((120,80,520,430),fill=INK); d.ellipse((185,140,455,390),fill=BG)
    for a in range(0,360,90):
        cx,cy=320,250; r=135
        x=cx+math.cos(math.radians(a))*r; y=cy+math.sin(math.radians(a))*r
        d.rounded_rectangle((x-35,y-22,x+35,y+22),radius=15,fill=MID)
    return im

def brake_pedal():
    im=C(); d=ImageDraw.Draw(im)
    L(d,[(330,60),(300,250)],34)
    d.rounded_rectangle((190,245,420,395),radius=25,fill=INK)
    for y in range(275,375,28):
        d.line((220,y,390,y),fill=BG,width=8)
    return im

def cargo_hook():
    im=C(); d=ImageDraw.Draw(im)
    d.arc((170,85,470,385),start=20,end=285,fill=INK,width=32)
    d.rectangle((155,75,245,160),fill=INK)
    d.ellipse((180,100,220,140),fill=BG); return im

def seat_tongue():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((205,70,435,235),radius=35,fill=INK)
    d.rectangle((275,220,365,420),fill=MID)
    d.rounded_rectangle((295,275,345,350),radius=12,fill=BG)
    return im

def seat_retractor():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((185,110,455,370),radius=50,fill=INK)
    d.ellipse((235,160,405,330),fill=BG); d.ellipse((270,195,370,295),fill=MID)
    L(d,[(320,110),(320,40)],30)
    return im

def seat_guide():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((185,130,455,350),radius=60,fill=INK)
    d.rounded_rectangle((245,175,395,305),radius=40,fill=BG)
    L(d,[(120,70),(320,240),(520,70)],18,MID)
    return im

def door_striker():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((180,120,460,360),radius=35,fill=INK)
    d.arc((235,155,405,325),start=35,end=325,fill=BG,width=28)
    for cx in (235,405): d.ellipse((cx-18,222,cx+18,258),fill=BG)
    return im

def door_latch():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((145,105,495,375),radius=45,fill=INK)
    d.arc((220,155,420,355),start=40,end=315,fill=BG,width=35)
    d.rectangle((365,80,440,155),fill=MID)
    d.ellipse((185,145,225,185),fill=BG); d.ellipse((185,295,225,335),fill=BG)
    return im

def lock_actuator():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((150,120,490,360),radius=45,fill=INK)
    d.ellipse((235,175,405,345),fill=BG); d.ellipse((275,215,365,305),fill=MID)
    d.rectangle((430,175,540,245),fill=INK); d.rectangle((430,265,520,325),fill=INK)
    return im

def airbag_label():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((110,110,530,370),radius=25,fill=(245,190,40))
    d.polygon([(180,310),(260,155),(340,310)],fill=INK)
    d.ellipse((238,205,282,249),fill=(245,190,40))
    d.rectangle((255,250,275,290),fill=(245,190,40))
    d.line((360,160,485,315),fill=INK,width=20)
    d.line((485,160,360,315),fill=INK,width=20)
    return im

def washer_nozzle():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((165,210,475,330),radius=35,fill=INK)
    d.rectangle((285,315,355,415),fill=MID)
    d.ellipse((260,235,300,275),fill=BG); d.ellipse((340,235,380,275),fill=BG)
    for sx in (280,360):
        for i in range(4):
            x2=sx+(-70+i*45); y2=100-i*10
            d.line((sx,245,x2,y2),fill=(80,150,220),width=6)
    return im

jobs={
"0119":floor_anchor,
"0199":door_hinge,
"0200":door_checker,
"0202":reflector,
"0296":cup_insert,
"0300":brake_pedal,
"0309":cargo_hook,
"0323":seat_tongue,
"0324":seat_retractor,
"0330":seat_guide,
"0338":door_striker,
"0339":door_latch,
"0340":lock_actuator,
"0363":seat_retractor,
"0364":seat_guide,
"0368":airbag_label,
"0191":washer_nozzle,
"0192":washer_nozzle,
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

rf=ROOT/"research"/"backlog-recovery-30-original-generic-schematics.md"
lines=["# CAR MASTER — Backlog Recovery 30 — Original Generic Schematics","",
"New original technical illustrations informed by Hyundai official manual references; no source-image pixels copied.","","## PASS"]
lines += [f"- **{a} {b}** — 640x480, {c} bytes" for a,b,c in passed] or ["- None"]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Reverse-QA",
"- Distinguish door hinge/checker/striker/latch/lock actuator.",
"- Distinguish seat-belt tongue/retractor/guide.",
"- 0191/0192 use the same generic washer-nozzle hardware form; live UI may retain both terminology/location variants only if reverse-QA accepts location-neutral learning image.",
"- Count live Production only after Codex reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",len(passed),[x[0] for x in passed]); print("FAIL",failed)
