from pathlib import Path
from PIL import Image
import urllib.request, json

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"backlog-recovery-14"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

jobs={
 "0261":("https://ownersmanual.hyundai.com/full_webhelp/NX4a/2026/en_US/images/2C_AdjustSteeringWheelManual.jpg.png","STEERING WHEEL TILT/TELESCOPIC LEVER","HY_NX4A_2026_STEERING_LEVER"),
 "0264":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_ESCOffButtion.jpg.png","ESC OFF BUTTON","HY_LX3_2026_ESC_OFF"),
 "0267":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_CrashPadTailgateOpenButton.jpg.png","POWER LIFTGATE BUTTON","HY_LX3_2026_POWER_LIFTGATE_BUTTON"),
 "0268":("https://ownersmanual.hyundai.com/full_webhelp/LX3HEV/2026/en_US/images/2C_HEVFuelDoorOpenButton.jpg.png","FUEL FILLER DOOR RELEASE BUTTON","HY_LX3HEV_2026_FUEL_DOOR_BUTTON"),
 "0269":("https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_US/images/2C_ChargingDoorOpenCloseButton.jpg.png","CHARGING DOOR OPEN/CLOSE BUTTON","HY_NE1N_2026_CHARGING_DOOR_BUTTON"),
}

def fetch(url,id_):
    p=DL/f"{id_}.src"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r: p.write_bytes(r.read())
    im=Image.open(p); im.verify()
    return Image.open(p).convert("RGB")

def fit4(im):
    w,h=im.size
    if w/h>4/3:
        nw=max(1,int(h*4/3)); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
    nh=max(1,int(w*3/4)); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

passed=[]; failures=[]
for id_,(url,term,src) in jobs.items():
    try:
        im=fit4(fetch(url,id_))
        if im.width<480:
            sc=480/im.width
            im=im.resize((int(im.width*sc),int(im.height*sc)),Image.Resampling.LANCZOS)
            im=fit4(im)
        out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
        v=Image.open(out); v.verify(); v=Image.open(out); w,h=v.size
        if abs(w/h-4/3)>0.02: raise RuntimeError("bad aspect")
        if out.stat().st_size<5000: raise RuntimeError("small file")
        passed.append((id_,term,src,w,h,out.stat().st_size))
    except Exception as e:
        failures.append((id_,term,str(e)))

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
for id_,term,src,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-14.md"
lines=["# CAR MASTER — Backlog Recovery 14","","Dedicated Hyundai official control images only.","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, {src}" for id_,term,src,w,h,size in passed] or ["- None"]
lines += ["","## Failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Reverse-QA",
"- Each card uses a dedicated button/lever image rather than a shared cabin overview.",
"- 0261 must visibly show the lock-release lever and steering adjustment context.",
"- 0264/0267/0268/0269 must each show the correct button icon/physical switch.",
"- Count live Production only after Codex bind + mobile + reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",[x[0] for x in passed]); print("FAILURES",failures)
