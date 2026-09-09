from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, math

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; PARTS.mkdir(parents=True,exist_ok=True)
W,H=640,480
BG=(244,245,246); INK=(28,31,35); MID=(110,118,125); LIGHT=(205,210,215); BLUE=(65,120,185); RED=(180,65,65)

def C(): return Image.new("RGB",(W,H),BG)
def L(d,pts,w=10,fill=INK): d.line(pts,fill=fill,width=w,joint="curve")
def save(im,id_):
    out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
    v=Image.open(out); v.verify()
    if out.stat().st_size<5000: raise RuntimeError("small")
    return out.stat().st_size

def folding_lever(remote=False):
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((120,90,520,390),radius=55,outline=MID,width=12)
    d.line((320,100,320,380),fill=MID,width=8)
    if remote:
        d.rounded_rectangle((390,175,490,275),radius=22,fill=INK); d.polygon([(420,205),(465,225),(420,245)],fill=BG)
    else:
        d.rounded_rectangle((165,250,285,315),radius=20,fill=INK); d.line((225,250,250,190),fill=INK,width=16)
    return im

def spare_carrier():
    im=C(); d=ImageDraw.Draw(im)
    d.ellipse((150,80,490,420),outline=INK,width=25); d.ellipse((230,160,410,340),outline=MID,width=15)
    d.line((320,40,320,440),fill=INK,width=16); d.rounded_rectangle((285,45,355,115),radius=18,fill=INK); return im

def wheel_studs():
    im=C(); d=ImageDraw.Draw(im)
    d.ellipse((150,70,490,410),fill=INK); d.ellipse((220,140,420,340),fill=BG)
    for a in range(0,360,72):
        cx,cy=320,240; r=120
        x=cx+math.cos(math.radians(a))*r; y=cy+math.sin(math.radians(a))*r
        d.rounded_rectangle((x-15,y-38,x+15,y+38),radius=8,fill=MID)
    return im

def radiator_cap():
    im=C(); d=ImageDraw.Draw(im)
    d.ellipse((175,110,465,400),fill=INK); d.ellipse((225,160,415,350),fill=MID)
    d.rectangle((115,200,220,310),fill=INK); d.rectangle((420,200,525,310),fill=INK)
    d.polygon([(320,175),(275,285),(365,285)],fill=BG); d.line((320,210,320,255),fill=RED,width=10); return im

def tank_air_filter():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((160,110,480,370),radius=45,fill=INK)
    for y in range(150,340,28): d.line((205,y,435,y),fill=BG,width=8)
    L(d,[(95,240),(160,240)],22); L(d,[(480,240),(545,240)],22); return im

def brake_line():
    im=C(); d=ImageDraw.Draw(im)
    pts=[(80,330),(150,260),(220,270),(300,180),(400,205),(560,120)]
    L(d,pts,12,INK)
    for cx,cy in [(80,330),(300,180),(560,120)]: d.ellipse((cx-16,cy-16,cx+16,cy+16),fill=MID)
    return im

def brake_hose():
    im=C(); d=ImageDraw.Draw(im)
    pts=[]
    for i in range(180):
        t=i/179; x=90+t*460; y=240+75*math.sin(t*3*math.pi)
        pts.append((x,y))
    L(d,pts,24,MID)
    d.rectangle((60,205,115,275),fill=INK); d.rectangle((525,205,580,275),fill=INK); return im

def steering_linkage():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((230,190,410,290),radius=30,fill=INK)
    L(d,[(80,240),(230,240)],18); L(d,[(410,240),(560,240)],18)
    d.ellipse((45,205,115,275),fill=MID); d.ellipse((525,205,595,275),fill=MID)
    d.line((320,190,320,90),fill=INK,width=18); return im

def suspension(front=True):
    im=C(); d=ImageDraw.Draw(im)
    # wheel/knuckle
    d.ellipse((410,105,560,385),outline=MID,width=18)
    d.ellipse((450,190,520,260),fill=INK)
    # strut or shock
    if front:
        d.line((460,70,470,210),fill=INK,width=22)
        pts=[]
        for i in range(90):
            t=i/89; y=90+t*110; x=465+40*math.sin(t*4*2*math.pi); pts.append((x,y))
        L(d,pts,10,MID)
    else:
        d.line((405,100,430,270),fill=INK,width=22)
        pts=[]
        for i in range(90):
            t=i/89; y=130+t*150; x=355+38*math.sin(t*4*2*math.pi); pts.append((x,y))
        L(d,pts,10,MID)
    # arms/subframe
    d.polygon([(150,325),(300,225),(465,240),(430,310),(275,350)],fill=INK)
    d.line((110,365,500,365),fill=MID,width=24)
    if front:
        d.line((160,230,340,170),fill=MID,width=16)
    else:
        d.line((170,175,390,305),fill=MID,width=16)
    return im

def defroster_vent():
    im=C(); d=ImageDraw.Draw(im)
    d.polygon([(100,330),(180,170),(460,170),(540,330)],outline=MID)
    d.rounded_rectangle((160,260,480,315),radius=18,fill=INK)
    for x in range(190,470,35): d.line((x,270,x-10,305),fill=BG,width=6)
    for x in range(220,450,55): d.line((x,250,x-20,170),fill=BLUE,width=5)
    return im

def steering_adjust_switch():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((175,120,465,360),radius=50,fill=INK)
    d.ellipse((245,180,395,330),fill=BG)
    d.polygon([(320,145),(290,185),(350,185)],fill=MID)
    d.polygon([(320,335),(290,295),(350,295)],fill=MID)
    d.polygon([(205,240),(245,210),(245,270)],fill=MID)
    d.polygon([(435,240),(395,210),(395,270)],fill=MID); return im

def display_card(kind):
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((95,85,545,395),radius=45,fill=INK)
    d.rounded_rectangle((135,125,505,355),radius=25,fill=(28,40,55))
    if kind=="trip":
        d.line((175,285,470,285),fill=BLUE,width=10); d.arc((170,150,300,280),180,350,fill=BLUE,width=12)
        d.rectangle((335,165,455,205),fill=MID); d.rectangle((335,225,430,255),fill=MID)
    elif kind=="warning":
        d.polygon([(320,145),(205,330),(435,330)],fill=(230,175,45)); d.line((320,205,320,270),fill=INK,width=18); d.ellipse((309,292,331,314),fill=INK)
    else:
        d.rectangle((170,160,470,205),fill=MID); d.rectangle((170,235,390,275),fill=BLUE); d.rectangle((170,305,440,330),fill=MID)
    return im

def washer_system(rear=False):
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((120,175,300,350),radius=45,fill=INK)
    d.rectangle((185,110,235,190),fill=MID)
    L(d,[(300,260),(430,220 if not rear else 300),(520,160 if not rear else 330)],12,BLUE)
    d.ellipse((500,140 if not rear else 310,540,180 if not rear else 350),fill=INK); return im

def heated_mirror():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((140,100,500,380),radius=80,fill=INK); d.rounded_rectangle((175,135,465,345),radius=65,fill=(180,200,215))
    for x in (250,320,390):
        pts=[(x,300),(x-20,270),(x+15,240),(x-15,210),(x+10,180)]
        L(d,pts,8,RED)
    return im

def tpms(sensor=True):
    im=C(); d=ImageDraw.Draw(im)
    d.ellipse((160,80,480,400),outline=INK,width=20)
    d.rectangle((305,125,335,340),fill=MID)
    if sensor:
        d.rounded_rectangle((255,280,385,360),radius=20,fill=INK); d.rectangle((300,220,340,290),fill=INK)
    else:
        d.rounded_rectangle((285,70,355,145),radius=18,fill=INK); d.ellipse((305,88,335,118),fill=BG)
    return im

jobs={
"0079":lambda:folding_lever(False),
"0080":lambda:folding_lever(True),
"0137":spare_carrier,
"0139":wheel_studs,
"0149":radiator_cap,
"0156":tank_air_filter,
"0158":brake_line,
"0159":brake_hose,
"0164":steering_linkage,
"0173":lambda:suspension(True),
"0174":lambda:suspension(False),
"0253":defroster_vent,
"0262":steering_adjust_switch,
"0275":lambda:display_card("trip"),
"0276":lambda:display_card("warning"),
"0279":lambda:display_card("info"),
"0341":lambda:washer_system(False),
"0342":lambda:washer_system(True),
"0345":heated_mirror,
"0457":lambda:tpms(True),
"0458":lambda:tpms(False),
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
rf=ROOT/"research"/"backlog-recovery-32-final-generic-schematics.md"
lines=["# CAR MASTER — Backlog Recovery 32 — Final Generic Schematics","",
"Original technical/context schematics for remaining generic components.","","## PASS"]
lines += [f"- **{a} {b}** — 640x480, {c} bytes" for a,b,c in passed] or ["- None"]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Reverse-QA",
"- Front vs rear suspension must be visibly distinct.",
"- Brake line vs hose must read as rigid routed line vs flexible hose.",
"- 0079 vs 0080 must distinguish manual folding lever vs remote folding button.",
"- TPMS sensor vs valve stem must be visually distinct.",
"- Trip computer / warning light / driver information display are conceptual display schematics and require strict reverse-QA.",
"- Count live Production only after Codex reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",len(passed),[x[0] for x in passed]); print("FAIL",failed)
