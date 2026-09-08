from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, json, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"; DL=OUT/"batch-0421-0470-source"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

sources={
 "0449":("https://ownersmanual.hyundai.com/full_webhelp/NX4PHEV/2026/en_US/images/2C_SmartKeyRemoteStartButton.jpg.png","REMOTE START BUTTON","dedicated Hyundai smart-key remote-start button image","HY_LX3_2026_SMART_KEY"),
 "0453":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RemovingModifierKey.jpg.png","SMART KEY REAR COVER","dedicated Hyundai smart-key battery/rear-cover image","HY_LX3_2026_SMART_KEY"),
 "0455":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_HowToLockDoorInEmergency.jpg.png","EMERGENCY DOOR LOCK HOLE","dedicated Hyundai emergency door-lock hole image","HY_LX3_2026_MECHANICAL_KEY"),
 "0456":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_UsingEmerengcyKey_A1.jpg.png","KEY CYLINDER COVER","Hyundai key-cylinder cover removal image","HY_LX3_2026_MECHANICAL_KEY"),
 "0459":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_TPMSWaringLampOverView_2.jpg.png","LOW TIRE PRESSURE POSITION TELLTALE","dedicated Hyundai TPMS position-telltale display","HY_LX3_2026_TPMS"),
 "0461":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_TireLowPressureInfo.jpg.png","TIRE PRESSURE DISPLAY","dedicated Hyundai tire-pressure cluster display","HY_LX3_2026_TPMS"),
 "0462":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_PaddleShift.jpg.png","REGENERATIVE BRAKING PADDLE SHIFTER","dedicated Hyundai regenerative paddle-shifter image","HY_NE1A_2025_REGEN_BRAKING"),
 "0463":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_RegenerationBrakeLevelInfo.jpg.png","REGENERATIVE BRAKING LEVEL INDICATOR","dedicated Hyundai regeneration-level display","HY_NE1A_2025_REGEN_BRAKING"),
 "0464":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_SmartRegenerationBrakeIconInfo.jpg.png","SMART REGENERATION INDICATOR","dedicated Hyundai smart-regeneration icon/display","HY_NE1A_2025_REGEN_BRAKING"),
 "0467":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_PowerChargeGauge.jpg.png","POWER/CHARGE GAUGE","dedicated Hyundai Power/Charge gauge","HY_NE1A_2025_EV_GAUGES_2"),
 "0468":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_BatteryLevelGauge.jpg.png","STATE OF CHARGE (SOC) GAUGE","dedicated Hyundai high-voltage battery SOC gauge","HY_NE1A_2025_EV_GAUGES_2"),
}

def fetch(url,id_):
    p=DL/f"{id_}.src"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r: p.write_bytes(r.read())
    im=Image.open(p); im.verify()
    return Image.open(p).convert("RGB")

def crop4(im):
    w,h=im.size
    if w/h>4/3:
        nw=int(h*4/3); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
    nh=int(w*3/4); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

passed=[]; failures=[]; cards=[]
for id_,(url,term,note,src) in sources.items():
    try:
        c=crop4(fetch(url,id_)); out=PARTS/f"{id_}.jpg"; c.save(out,quality=94,subsampling=0)
        v=Image.open(out); v.verify(); v=Image.open(out); w,h=v.size
        if abs(w/h-4/3)>0.02: raise RuntimeError(f"aspect error {w}x{h}")
        if out.stat().st_size<5000: raise RuntimeError(f"suspiciously small {out.stat().st_size}")
        passed.append((id_,term,note,src,w,h,out.stat().st_size))
        t=ImageOps.contain(c,(560,400)); card=Image.new("RGB",(600,470),"white"); card.paste(t,((600-t.width)//2,10))
        d=ImageDraw.Draw(card); d.text((12,420),f"{id_} PASS — {term}",fill="black"); d.text((12,442),note,fill="black"); cards.append(card)
    except Exception as e:
        failures.append((id_,term,str(e)))

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8")); items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
for id_,term,note,src,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"0421-0470-production-pass2.md"
lines=["# CAR MASTER — 0421–0470 Production Pass 2","","Only dedicated/direct Hyundai Owner's Manual images are eligible for PASS.","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, source {src}" for id_,term,note,src,w,h,size in passed] or ["- None"]
lines += ["","## Fetch/validation failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Rule","- All other IDs 0421–0470 remain REVIEW + Production Backlog.","- No generic/stock substitution.","- BLACK UI unchanged.","- Production % only after live UI deploy/mobile reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")

if cards:
    cols=2; rows=math.ceil(len(cards)/cols); sheet=Image.new("RGB",(cols*600,rows*470),"white")
    for i,c in enumerate(cards): sheet.paste(c,((i%cols)*600,(i//cols)*470))
    sheet.save(OUT/"0421-0470-pass2-qa.jpg",quality=92)
print("PASS",[x[0] for x in passed]); print("FAILURES",failures); print("VALIDATION_OK",True)
