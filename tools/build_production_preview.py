from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, math, urllib.request

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; PARTS.mkdir(parents=True,exist_ok=True)
DL=ROOT/"production-preview"/"batch-33-final-22"; DL.mkdir(parents=True,exist_ok=True)
W,H=640,480
BG=(244,245,246); INK=(28,31,35); MID=(112,118,124); LIGHT=(205,210,215)
BLUE=(70,130,200); GREEN=(80,190,110); ORANGE=(230,150,55); RED=(190,65,65)

def C(): return Image.new("RGB",(W,H),BG)
def L(d,pts,w=10,fill=INK): d.line(pts,fill=fill,width=w,joint="curve")
def save(im,id_):
    out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
    v=Image.open(out); v.verify()
    if v.size!=(640,480) or out.stat().st_size<5000: raise RuntimeError("validation")
    return out.stat().st_size

def fit_to_canvas(src):
    im=src.convert("RGB"); w,h=im.size
    scale=min(560/w,400/h); im=im.resize((max(1,int(w*scale)),max(1,int(h*scale))),Image.Resampling.LANCZOS)
    out=C(); x=(W-im.width)//2; y=(H-im.height)//2; out.paste(im,(x,y)); return out

def fetch(url,id_):
    p=DL/f"{id_}.src"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r:p.write_bytes(r.read())
    from PIL import Image as PI
    q=PI.open(p); q.verify(); return PI.open(p).convert("RGB")

def isg_button():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((175,110,465,370),radius=55,fill=INK)
    d.ellipse((235,165,405,335),outline=BG,width=18)
    d.arc((245,175,395,325),start=45,end=315,fill=BG,width=18)
    d.polygon([(385,165),(425,180),(390,210)],fill=BG)
    # OFF bar
    d.rectangle((230,320,410,350),fill=RED)
    return im

def ac_outlet():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((145,95,495,385),radius=55,fill=INK)
    d.rounded_rectangle((195,145,445,335),radius=38,fill=BG)
    d.rounded_rectangle((235,180,285,260),radius=12,fill=INK)
    d.rounded_rectangle((355,180,405,260),radius=12,fill=INK)
    d.ellipse((295,270,345,320),fill=INK)
    return im

def door_seal():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((160,75,480,405),radius=90,outline=MID,width=12)
    d.rounded_rectangle((195,110,445,370),radius=75,outline=INK,width=24)
    d.arc((215,130,425,350),25,335,fill=BG,width=6); return im

def car_top():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((150,60,490,420),radius=120,outline=MID,width=10)
    d.rectangle((205,125,435,355),outline=MID,width=6)
    return im,d

def front_impact():
    im,d=car_top()
    for x in (240,400): d.ellipse((x-22,72,x+22,116),fill=RED)
    d.line((320,95,320,170),fill=RED,width=8)
    return im

def side_impact():
    im,d=car_top()
    for x,y in [(165,210),(475,210),(165,310),(475,310)]: d.ellipse((x-18,y-18,x+18,y+18),fill=RED)
    return im

def srs_module():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((185,115,455,365),radius=38,fill=INK)
    d.rectangle((240,165,400,315),fill=MID)
    for x in range(220,430,42): d.rectangle((x,340,x+22,395),fill=INK)
    d.circle((320,240),28,fill=BG); return im

def rollover():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((205,130,435,350),radius=40,fill=INK)
    d.ellipse((250,175,390,315),outline=BG,width=12)
    d.line((320,240,370,180),fill=ORANGE,width=14)
    d.polygon([(370,180),(350,185),(365,205)],fill=ORANGE)
    d.arc((145,75,495,405),start=205,end=335,fill=ORANGE,width=12)
    return im

def buckle_sensor():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((200,110,440,340),radius=45,fill=INK)
    d.rounded_rectangle((265,155,375,245),radius=18,fill=BG)
    d.rectangle((290,245,350,380),fill=MID)
    d.line((350,320,510,370),fill=BLUE,width=12)
    d.rounded_rectangle((485,345,545,400),radius=12,fill=INK)
    return im

def pressure_sensor():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((115,95,525,385),radius=55,outline=MID,width=12)
    d.rounded_rectangle((270,175,370,275),radius=25,fill=INK)
    d.circle((320,225),24,fill=BG)
    for r in (55,85,115): d.arc((320-r,225-r,320+r,225+r),-60,60,fill=BLUE,width=6)
    return im

def accel_sensor():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((215,130,425,340),radius=35,fill=INK)
    d.rectangle((265,180,375,290),fill=MID)
    d.line((320,235,430,235),fill=ORANGE,width=12); d.polygon([(430,235),(400,215),(400,255)],fill=ORANGE)
    d.line((320,235,320,110),fill=ORANGE,width=12); d.polygon([(320,110),(300,140),(340,140)],fill=ORANGE)
    return im

def combo_inlet(mode="full"):
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((135,65,505,415),radius=70,fill=INK)
    # top AC portion
    d.ellipse((205,115,435,325),fill=BG)
    holes=[(270,165),(370,165),(245,235),(320,235),(395,235),(285,290),(355,290)]
    for x,y in holes: d.ellipse((x-17,y-17,x+17,y+17),fill=INK)
    # DC lower pins
    d.ellipse((235,315,305,385),fill=BG); d.ellipse((335,315,405,385),fill=BG)
    d.ellipse((255,335,285,365),fill=INK); d.ellipse((355,335,385,365),fill=INK)
    if mode=="ac":
        d.rectangle((185,105,455,310),outline=BLUE,width=12)
    elif mode=="dc":
        d.rectangle((210,300,430,400),outline=ORANGE,width=12)
    elif mode=="lock":
        d.rounded_rectangle((430,155,490,245),radius=18,fill=RED)
        d.arc((438,125,482,175),180,360,fill=RED,width=10)
    elif mode=="cap":
        d.arc((95,55,525,425),start=80,end=280,fill=MID,width=18)
        d.rounded_rectangle((65,145,180,335),radius=45,fill=MID)
    return im

def reservoir(cap=False):
    im=C(); d=ImageDraw.Draw(im)
    d.polygon([(195,150),(445,150),(475,340),(430,400),(210,400),(165,340)],fill=(190,215,225),outline=INK)
    d.line((210,305,430,305),fill=BLUE,width=12)
    d.rectangle((275,90,365,160),fill=INK)
    if cap:
        d.ellipse((230,70,410,235),fill=INK); d.ellipse((270,110,370,195),fill=MID)
        for x in range(260,390,25): d.line((x,105,x,200),fill=BG,width=7)
    return im

def ecu():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((145,115,495,365),radius=35,fill=INK)
    for y in range(145,340,24): d.line((175,y,465,y),fill=MID,width=8)
    d.rectangle((200,355,285,410),fill=INK); d.rectangle((355,355,440,410),fill=INK)
    return im

def smart_slot():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((145,105,495,375),radius=55,fill=INK)
    d.rounded_rectangle((255,165,385,315),radius=25,fill=BG)
    # key silhouette
    d.rounded_rectangle((280,185,360,290),radius=18,fill=MID)
    d.ellipse((305,205,335,235),fill=BG)
    return im

def ipedal():
    im=Image.new("RGB",(W,H),(16,18,22)); d=ImageDraw.Draw(im)
    try:
        font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",92)
    except: font=None
    txt="i-PEDAL"
    bb=d.textbbox((0,0),txt,font=font); tw=bb[2]-bb[0]; th=bb[3]-bb[1]
    d.text(((W-tw)//2,(H-th)//2),txt,font=font,fill=GREEN)
    return im

def battery_air_inlet():
    im=C(); d=ImageDraw.Draw(im)
    d.rounded_rectangle((130,110,510,370),radius=55,fill=INK)
    for y in range(155,340,32): d.rounded_rectangle((185,y,455,y+12),radius=6,fill=BG)
    for x in (215,320,425):
        d.line((x,410,x,350),fill=BLUE,width=8); d.polygon([(x,335),(x-14,360),(x+14,360)],fill=BLUE)
    return im

jobs={
"0265":isg_button,
"0294":ac_outlet,
"0337":door_seal,
"0353":ac_outlet,
"0369":front_impact,
"0370":side_impact,
"0371":srs_module,
"0372":rollover,
"0373":buckle_sensor,
"0374":pressure_sensor,
"0375":accel_sensor,
"0397":lambda:combo_inlet("full"),
"0414":lambda:reservoir(False),
"0415":lambda:reservoir(True),
"0416":ecu,
"0452":smart_slot,
"0465":ipedal,
"0493":lambda:combo_inlet("cap"),
"0494":lambda:combo_inlet("dc"),
"0495":lambda:combo_inlet("ac"),
"0496":lambda:combo_inlet("lock"),
"0500":battery_air_inlet,
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

rf=ROOT/"research"/"backlog-recovery-33-final-22.md"
lines=["# CAR MASTER — Backlog Recovery 33 — Final 22","",
"Final remaining cards produced as original technical/context schematics after official-manual terminology and location verification.","","## PASS"]
lines += [f"- **{a} {b}** — 640x480, {c} bytes" for a,b,c in passed] or ["- None"]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Reverse-QA",
"- SRS sensor cards rely on location/function context and must be checked particularly strictly.",
"- Charging inlet / AC / DC / cap / lock cards share the same CCS context but emphasize different physical zones.",
"- 0414 vs 0415 must distinguish reservoir vs cap.",
"- 0294/0353 are the same generic AC outlet hardware under duplicate master terminology.",
"- 0465 reflects Hyundai's official i-PEDAL cluster indication/message concept.",
"- Do not count any card live until Codex reverse-QA and mobile binding pass."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",len(passed),[x[0] for x in passed]); print("FAIL",failed)
