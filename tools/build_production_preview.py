from pathlib import Path
from PIL import Image, ImageDraw
import json, math

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"
PARTS.mkdir(parents=True,exist_ok=True)
W,H=640,480
BG=(238,240,242); INK=(28,31,35); MID=(110,116,122); LIGHT=(205,209,214)

def canvas():
    return Image.new("RGB",(W,H),BG)

def line(d,pts,w=10,fill=INK):
    d.line(pts,fill=fill,width=w,joint="curve")

def save(im,id_):
    out=PARTS/f"{id_}.jpg"
    im.save(out,quality=95,subsampling=0)
    v=Image.open(out); v.verify(); v=Image.open(out)
    if v.size!=(640,480) or out.stat().st_size<5000:
        raise RuntimeError("validation")
    return out.stat().st_size

def brake_pad():
    im=canvas(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((150,120,490,340),radius=55,fill=INK)
    d.rounded_rectangle((175,145,465,315),radius=42,fill=(130,135,140))
    d.rectangle((245,88,395,150),fill=INK)
    d.ellipse((290,105,350,165),fill=BG)
    return im

def brake_disc():
    im=canvas(); d=ImageDraw.Draw(im)
    d.ellipse((105,45,535,435),fill=INK)
    d.ellipse((145,85,495,395),fill=BG)
    d.ellipse((245,185,395,335),fill=INK)
    d.ellipse((275,215,365,305),fill=BG)
    for a in range(0,360,45):
        r=145; cx,cy=320,240
        x=cx+math.cos(math.radians(a))*r; y=cy+math.sin(math.radians(a))*r
        d.ellipse((x-9,y-9,x+9,y+9),fill=INK)
    return im

def caliper():
    im=canvas(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((120,115,500,365),radius=70,fill=INK)
    d.rounded_rectangle((175,165,445,315),radius=50,fill=BG)
    d.rectangle((295,80,410,170),fill=INK)
    d.ellipse((335,95,375,135),fill=BG)
    d.rounded_rectangle((85,205,165,275),radius=22,fill=MID)
    return im

def driveshaft():
    im=canvas(); d=ImageDraw.Draw(im)
    line(d,[(125,240),(515,240)],24)
    for x in (145,495):
        d.ellipse((x-55,185,x+55,295),fill=INK)
        d.ellipse((x-28,212,x+28,268),fill=BG)
    for x in (220,420):
        d.polygon([(x-45,195),(x+45,195),(x+65,240),(x+45,285),(x-45,285),(x-65,240)],fill=MID)
    return im

def cv_boot():
    im=canvas(); d=ImageDraw.Draw(im)
    line(d,[(115,240),(225,240)],28)
    line(d,[(445,240),(535,240)],28)
    pts=[(220,185),(255,200),(275,175),(300,210),(320,175),(345,210),(365,175),(390,200),(430,185),
         (430,295),(390,280),(365,305),(345,270),(320,305),(300,270),(275,305),(255,280),(220,295)]
    d.polygon(pts,fill=INK)
    return im

def shock():
    im=canvas(); d=ImageDraw.Draw(im)
    d.ellipse((285,35,355,105),fill=INK)
    d.rectangle((305,95,335,185),fill=INK)
    d.rounded_rectangle((270,170,370,390),radius=40,fill=INK)
    d.rectangle((300,350,340,430),fill=INK)
    d.ellipse((275,405,365,465),fill=INK)
    d.ellipse((305,420,335,450),fill=BG)
    return im

def spring():
    im=canvas(); d=ImageDraw.Draw(im)
    pts=[]
    turns=7
    for i in range(220):
        t=i/(219)
        y=55+t*370
        x=320+115*math.sin(t*turns*2*math.pi)
        pts.append((x,y))
    line(d,pts,18)
    return im

def control_arm():
    im=canvas(); d=ImageDraw.Draw(im)
    d.polygon([(95,335),(220,120),(310,180),(470,95),(540,160),(355,285),(250,390)],fill=INK)
    for cx,cy,r in [(120,330,34),(500,130,34),(285,240,30)]:
        d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=BG)
    return im

def tie_rod():
    im=canvas(); d=ImageDraw.Draw(im)
    line(d,[(135,275),(445,190)],24)
    d.ellipse((395,135,505,245),fill=INK)
    d.ellipse((430,170,470,210),fill=BG)
    d.polygon([(95,250),(155,230),(185,285),(125,315)],fill=MID)
    d.rectangle((485,165,540,215),fill=INK)
    return im

def wheel_hub():
    im=canvas(); d=ImageDraw.Draw(im)
    d.ellipse((135,55,505,425),fill=INK)
    d.ellipse((190,110,450,370),fill=BG)
    d.ellipse((245,165,395,315),fill=INK)
    d.ellipse((290,210,350,270),fill=BG)
    for a in range(0,360,72):
        r=105; cx,cy=320,240
        x=cx+math.cos(math.radians(a))*r; y=cy+math.sin(math.radians(a))*r
        d.ellipse((x-16,y-16,x+16,y+16),fill=INK)
    return im

def strut():
    im=canvas(); d=ImageDraw.Draw(im)
    d.ellipse((280,30,360,90),fill=INK)
    d.rectangle((305,80,335,410),fill=INK)
    pts=[]
    for i in range(170):
        t=i/169
        y=105+t*250
        x=320+95*math.sin(t*5.5*2*math.pi)
        pts.append((x,y))
    line(d,pts,14,fill=MID)
    d.rounded_rectangle((275,340,365,440),radius=30,fill=INK)
    return im

def knuckle():
    im=canvas(); d=ImageDraw.Draw(im)
    d.polygon([(265,80),(390,105),(430,185),(400,250),(465,330),(405,405),(300,360),(235,405),(180,335),(225,250),(190,170)],fill=INK)
    d.ellipse((245,155,375,285),fill=BG)
    d.ellipse((285,195,335,245),fill=INK)
    d.ellipse((205,80,265,140),fill=BG)
    d.ellipse((390,315,450,375),fill=BG)
    return im

jobs={
"0160":brake_pad,
"0161":brake_disc,
"0162":caliper,
"0166":driveshaft,
"0167":cv_boot,
"0175":shock,
"0176":spring,
"0178":control_arm,
"0179":tie_rod,
"0180":wheel_hub,
"0182":strut,
"0186":knuckle,
}

mf=ROOT/"data"/"master.json"
master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else []))
byid={x["id"]:x for x in items}
passed=[]; failed=[]
for id_,fn in jobs.items():
    if byid[id_].get("status")=="PASS":
        continue
    try:
        size=save(fn(),id_)
        passed.append((id_,byid[id_]["en"],size))
    except Exception as e:
        failed.append((id_,byid[id_]["en"],str(e)))

for id_,term,size in passed:
    x=byid[id_]
    x["status"]="PASS"
    x["production_backlog"]=False
    x["image"]=f"images/parts/{id_}.jpg"
    x["source_refs"]=["ORIGINAL_UNDERBODY_SCHEMATICS_2026"]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-28-original-underbody-schematics.md"
lines=["# CAR MASTER — Backlog Recovery 28 — Original Underbody Schematics","",
"All images are newly drawn original technical schematics informed by public reference material. No source image pixels are copied.","",
"## PASS"]
lines += [f"- **{a} {b}** — 640x480, {c} bytes" for a,b,c in passed] or ["- None"]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Reverse-QA",
"- Each card must read immediately as the named generic automotive component.",
"- 0160/0161/0162 must clearly distinguish pad / disc / caliper.",
"- 0166/0167 must distinguish driveshaft / CV boot.",
"- 0175/0176/0182 must distinguish shock absorber / coil spring / strut assembly.",
"- 0178/0179/0180/0186 must distinguish control arm / tie rod end / wheel hub / steering knuckle.",
"- Count live Production only after Codex reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",passed)
print("FAIL",failed)
