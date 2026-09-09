from pathlib import Path
from PIL import Image
import urllib.request, json, shutil

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"
OUT=ROOT/"production-preview"
DL=OUT/"batch-21-direct-sensors"
PARTS.mkdir(parents=True,exist_ok=True)
DL.mkdir(parents=True,exist_ok=True)

def fetch(url,id_):
    p=DL/f"{id_}.src"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        p.write_bytes(r.read())
    im=Image.open(p); im.verify()
    return Image.open(p).convert("RGB")

def relcrop(im,b=None):
    if b is None:return im
    w,h=im.size; x1,y1,x2,y2=b
    return im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))

def fit4(im):
    w,h=im.size
    if w/h>4/3:
        nw=max(1,int(h*4/3)); x=(w-nw)//2
        return im.crop((x,0,x+nw,h))
    nh=max(1,int(w*3/4)); y=(h-nh)//2
    return im.crop((0,y,w,y+nh))

def save(im,id_):
    im=fit4(im)
    if im.width<480:
        s=480/im.width
        im=im.resize((int(im.width*s),int(im.height*s)),Image.Resampling.LANCZOS)
        im=fit4(im)
    out=PARTS/f"{id_}.jpg"
    im.save(out,quality=95,subsampling=0)
    v=Image.open(out); v.verify(); v=Image.open(out)
    if abs(v.width/v.height-4/3)>0.02 or out.stat().st_size<5000:
        raise RuntimeError("validation")
    return v.width,v.height,out.stat().st_size

jobs={
"0009":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_US/images/2C_FrontRadar.jpg.png",None,"HY_NX4_2025_RADARS"),
"0010":("https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_US/images/2C_FrontCameraRadar.jpg.png",(0.00,0.00,0.48,0.55),"HY_NE1N_2026_FCA_SENSORS"),
"0218":("https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_US/images/2C_FrontCameraRadar.jpg.png",(0.00,0.00,0.48,0.55),"HY_NE1N_2026_FCA_SENSORS"),
"0378":("https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_US/images/2C_FrontCameraRadar.jpg.png",(0.45,0.35,1.00,1.00),"HY_NE1N_2026_FCA_SENSORS"),
"0379":("https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_US/images/2C_RearRadar_2.jpg.png",None,"HY_NE1N_2026_FCA_SENSORS"),
"0219":("https://ownersmanual.hyundai.com/full_webhelp/ne1n/2025/ko_kr/images/2C_WideFrontSideViewCamera.jpg.png",(0.38,0.18,1.00,1.00),"HY_NE1N_2025_WIDE_CAMERAS"),
"0220":("https://ownersmanual.hyundai.com/full_webhelp/ne1n/2025/ko_kr/images/2C_WideRearCamera.jpg.png",None,"HY_NE1N_2025_WIDE_CAMERAS"),
"0380":("https://ownersmanual.hyundai.com/full_webhelp/ne1n/2025/ko_kr/images/2C_WideFrontSideViewCamera.jpg.png",(0.00,0.00,0.58,0.72),"HY_NE1N_2025_WIDE_CAMERAS"),
"0381":("https://ownersmanual.hyundai.com/full_webhelp/ne1n/2025/ko_kr/images/2C_WideFrontSideViewCamera.jpg.png",(0.38,0.18,1.00,1.00),"HY_NE1N_2025_WIDE_CAMERAS"),
"0475":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_EngineRoomFuseReplacement.jpg.png",(0.48,0.28,1.00,1.00),"HY_NX4_2025_FUSE_PULLER"),
}

mf=ROOT/"data"/"master.json"
master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else []))
byid={x["id"]:x for x in items}
passed=[]; failed=[]
for id_,(url,box,src) in jobs.items():
    if byid[id_].get("status")=="PASS": continue
    try:
        im=relcrop(fetch(url,id_),box)
        w,h,size=save(im,id_)
        passed.append((id_,byid[id_]["en"],src,w,h,size))
    except Exception as e:
        failed.append((id_,byid[id_]["en"],str(e)))

for id_,term,src,w,h,size in passed:
    x=byid[id_]
    x["status"]="PASS"; x["production_backlog"]=False
    x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-21-direct-sensors.md"
lines=["# CAR MASTER — Backlog Recovery 21 — Direct Sensors & Fuse Puller","",
"## PASS"]
lines += [f"- **{a} {b}** — {d}x{e}, {f} bytes — {c}" for a,b,c,d,e,f in passed] or ["- None"]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Reverse-QA",
"- 0009 must show the physical front radar unit/location, not a generic bumper.",
"- 0010/0218 must show front view camera area.",
"- 0378/0379 must distinguish front/rear corner radar.",
"- 0219/0381 must show side/wide-side camera; 0220 rear camera; 0380 wide-front camera.",
"- 0475 must visibly show the fuse puller tool in use.",
"- Count live Production only after Codex bind + mobile + reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",passed)
print("FAIL",failed)
