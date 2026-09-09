from pathlib import Path
from PIL import Image, ImageDraw
import json, math

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; PARTS.mkdir(parents=True,exist_ok=True)
W,H=640,480
BG=(240,242,244); INK=(27,30,34); MID=(110,116,122); LIGHT=(205,209,214)

def C(): return Image.new("RGB",(W,H),BG)
def L(d,pts,w=10,fill=INK): d.line(pts,fill=fill,width=w,joint="curve")
def fit_save(im,id_):
    out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
    v=Image.open(out); v.verify()
    if out.stat().st_size<5000: raise RuntimeError("small")
    return out.stat().st_size

def oil_filter():
    im=C(); d=ImageDraw.Draw(im); d.rounded_rectangle((210,80,430,400),radius=55,fill=INK)
    d.rectangle((225,95,415,145),fill=MID)
    for x in range(245,405,28): d.line((x,100,x,140),fill=BG,width=8)
    d.ellipse((245,340,395,400),fill=MID); return im

def drive_belt():
    im=C(); d=ImageDraw.Draw(im)
    for box in [(105,95,255,245),(385,95,535,245),(245,270,395,420)]:
        d.ellipse(box,outline=INK,width=20)
    L(d,[(180,105),(460,105),(320,395),(180,105)],18,MID); return im

def spark_plug():
    im=C(); d=ImageDraw.Draw(im)
    d.rectangle((292,70,348,170),fill=INK); d.rectangle((270,155,370,225),fill=MID)
    d.rectangle((286,220,354,330),fill=INK); d.rectangle((300,325,340,410),fill=MID)
    for y in range(235,325,18): d.line((280,y,360,y),fill=BG,width=7)
    d.line((320,410,320,450),fill=INK,width=10); d.line((320,450,365,450),fill=INK,width=10); return im

def fuel_tank():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((110,110,530,370),radius=85,fill=INK)
    d.rectangle((440,70,490,135),fill=INK); d.ellipse((170,155,270,255),fill=MID); return im

def fuel_filter():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((220,95,420,385),radius=65,fill=INK)
    L(d,[(160,170),(220,170)],22); L(d,[(420,310),(500,310)],22)
    d.rectangle((245,125,395,170),fill=MID); return im

def steering_rack():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((160,185,480,295),radius=42,fill=INK)
    L(d,[(55,240),(160,240)],18); L(d,[(480,240),(585,240)],18)
    d.polygon([(110,190),(160,205),(160,275),(110,290),(80,240)],fill=MID)
    d.polygon([(530,190),(480,205),(480,275),(530,290),(560,240)],fill=MID); return im

def steering_boot():
    im=C(); d=ImageDraw.Draw(im)
    L(d,[(90,240),(195,240)],22); L(d,[(445,240),(550,240)],22)
    pts=[]
    for i in range(13):
        x=190+i*22; y1=185+(i%2)*22; y2=295-(i%2)*22
        pts.append((x,y1))
    for i in range(12,-1,-1):
        x=190+i*22; y1=185+(i%2)*22; y2=295-(i%2)*22
        pts.append((x,y2))
    d.polygon(pts,fill=INK); return im

def ball_joint():
    im=C(); d=ImageDraw.Draw(im)
    d.ellipse((240,120,400,280),fill=INK); d.ellipse((285,165,355,235),fill=BG)
    d.rectangle((300,260,340,395),fill=INK); d.polygon([(255,390),(385,390),(355,445),(285,445)],fill=MID); return im

def prop_shaft():
    im=C(); d=ImageDraw.Draw(im)
    L(d,[(110,240),(530,240)],34)
    for x in (130,510):
        d.ellipse((x-55,185,x+55,295),outline=INK,width=20)
        d.line((x-40,200,x+40,280),fill=INK,width=14); d.line((x+40,200,x-40,280),fill=INK,width=14)
    d.ellipse((285,205,355,275),fill=MID); return im

def differential(front=False):
    im=C(); d=ImageDraw.Draw(im)
    d.ellipse((195,105,445,355),fill=INK); d.ellipse((255,165,385,295),fill=BG)
    L(d,[(70,230),(195,230)],24); L(d,[(445,230),(570,230)],24)
    if front: d.rectangle((285,55,355,125),fill=MID)
    else: d.rectangle((285,335,355,425),fill=MID)
    return im

def transfer_case():
    im=C(); d=ImageDraw.Draw(im)
    d.polygon([(165,120),(390,95),(500,190),(455,365),(210,390),(120,270)],fill=INK)
    d.ellipse((315,165,420,270),fill=BG); d.rectangle((80,215,150,285),fill=MID); d.rectangle((470,205,550,275),fill=MID); return im

def stabilizer_bar():
    im=C(); d=ImageDraw.Draw(im)
    pts=[(90,140),(130,140),(165,320),(240,360),(400,360),(475,320),(510,140),(550,140)]
    L(d,pts,22); return im

def wheel_bearing():
    im=C(); d=ImageDraw.Draw(im)
    d.ellipse((120,40,520,440),fill=INK); d.ellipse((170,90,470,390),fill=BG)
    d.ellipse((235,155,405,325),fill=INK); d.ellipse((275,195,365,285),fill=BG)
    for a in range(0,360,30):
        cx,cy=320,240; r=125
        x=cx+math.cos(math.radians(a))*r; y=cy+math.sin(math.radians(a))*r
        d.ellipse((x-11,y-11,x+11,y+11),fill=MID)
    return im

def strut_mount():
    im=C(); d=ImageDraw.Draw(im)
    d.ellipse((150,80,490,420),fill=INK); d.ellipse((235,165,405,335),fill=BG)
    for a in (30,150,270):
        cx,cy=320,250; r=125
        x=cx+math.cos(math.radians(a))*r; y=cy+math.sin(math.radians(a))*r
        d.ellipse((x-18,y-18,x+18,y+18),fill=BG)
    d.ellipse((285,215,355,285),fill=MID); return im

def upper_arm():
    im=C(); d=ImageDraw.Draw(im)
    d.polygon([(105,330),(205,125),(310,195),(435,115),(535,320),(455,360),(320,265),(190,365)],fill=INK)
    for cx,cy in [(135,325),(505,315),(320,235)]:
        d.ellipse((cx-30,cy-30,cx+30,cy+30),fill=BG)
    return im

def stabilizer_link():
    im=C(); d=ImageDraw.Draw(im)
    L(d,[(220,360),(420,120)],24)
    d.ellipse((170,310,270,410),fill=INK); d.ellipse((370,70,470,170),fill=INK)
    d.ellipse((205,345,235,375),fill=BG); d.ellipse((405,105,435,135),fill=BG); return im

def subframe():
    im=C(); d=ImageDraw.Draw(im)
    d.polygon([(100,130),(215,95),(270,165),(370,165),(425,95),(540,130),(500,365),(390,330),(250,330),(140,365)],fill=INK)
    d.rectangle((260,175,380,315),fill=BG)
    for cx,cy in [(135,150),(505,150),(170,335),(470,335)]:
        d.ellipse((cx-24,cy-24,cx+24,cy+24),fill=BG)
    return im

def crossmember():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((85,190,555,290),radius=35,fill=INK)
    d.polygon([(140,190),(205,100),(250,100),(225,190)],fill=MID)
    d.polygon([(415,190),(390,100),(435,100),(500,190)],fill=MID)
    for cx in (135,505): d.ellipse((cx-22,218,cx+22,262),fill=BG)
    return im

def under_cover():
    im=C(); d=ImageDraw.Draw(im)
    d.polygon([(100,90),(500,90),(550,165),(520,390),(120,390),(90,165)],fill=INK)
    for cx,cy in [(145,135),(455,135),(150,345),(490,345)]:
        d.ellipse((cx-14,cy-14,cx+14,cy+14),fill=BG)
    d.rectangle((235,175,405,310),fill=MID); return im

def mud_guard():
    im=C(); d=ImageDraw.Draw(im)
    d.arc((120,50,520,450),start=195,end=345,fill=INK,width=45)
    d.polygon([(160,260),(235,330),(220,440),(130,390)],fill=INK)
    d.polygon([(480,260),(405,330),(420,440),(510,390)],fill=INK); return im

jobs={
"0151":oil_filter,
"0152":drive_belt,
"0153":spark_plug,
"0155":fuel_tank,
"0157":fuel_filter,
"0163":steering_rack,
"0165":steering_boot,
"0168":ball_joint,
"0169":prop_shaft,
"0170":lambda: differential(False),
"0171":lambda: differential(True),
"0172":transfer_case,
"0177":stabilizer_bar,
"0181":wheel_bearing,
"0183":strut_mount,
"0184":upper_arm,
"0185":stabilizer_link,
"0187":subframe,
"0188":crossmember,
"0189":under_cover,
"0190":mud_guard,
}

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
passed=[]; failed=[]
for id_,fn in jobs.items():
    if byid[id_].get("status")=="PASS": continue
    try:
        size=fit_save(fn(),id_); passed.append((id_,byid[id_]["en"],size))
    except Exception as e: failed.append((id_,byid[id_]["en"],str(e)))
for id_,term,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False
    x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=["ORIGINAL_UNDERBODY_SCHEMATICS_2026"]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-29-original-mechanical-schematics.md"
lines=["# CAR MASTER — Backlog Recovery 29 — Original Mechanical Schematics","",
"New original technical illustrations; no source-image pixels copied.","","## PASS"]
lines += [f"- **{a} {b}** — 640x480, {c} bytes" for a,b,c in passed] or ["- None"]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Reverse-QA",
"- Every card must read immediately as the named generic component.",
"- Distinguish steering rack vs rack boot; rear vs front differential; wheel bearing vs hub; strut mount vs strut; subframe vs crossmember.",
"- Count live Production only after Codex reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",len(passed),[x[0] for x in passed]); print("FAIL",failed)
