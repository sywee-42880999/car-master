from pathlib import Path
from PIL import Image
import urllib.request, json

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"batch-22-basic-hardware"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

def fetch(url,id_):
    p=DL/f"{id_}.src"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r:p.write_bytes(r.read())
    im=Image.open(p); im.verify()
    return Image.open(p).convert("RGB")

def crop(im,b=None):
    if b is None:return im
    w,h=im.size; x1,y1,x2,y2=b
    return im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))

def fit4(im):
    w,h=im.size
    if w/h>4/3:
        nw=int(h*4/3); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
    nh=int(w*3/4); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

def save(im,id_):
    im=fit4(im)
    if im.width<480:
        s=480/im.width
        im=im.resize((int(im.width*s),int(im.height*s)),Image.Resampling.LANCZOS)
        im=fit4(im)
    out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
    v=Image.open(out); v.verify(); v=Image.open(out)
    if out.stat().st_size<5000: raise RuntimeError("small file")
    return v.width,v.height,out.stat().st_size

jobs={
"0472":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_JumpStartOverview.jpg.png",(0.00,0.00,0.52,1.00),"HY_LX3_2026_JUMP_TERMINALS"),
"0473":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_JumpStartOverview.jpg.png",(0.48,0.00,1.00,1.00),"HY_LX3_2026_JUMP_TERMINALS"),
"0471":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_CheckCoolantCapLocked.jpg.png",None,"HY_NX4_2025_COOLANT_CAP"),
"0400":("https://ownersmanual.hyundai.com/full_webhelp/SX2EV/2025/en_US/images/2C_ACCharger.jpg.png",None,"HY_SX2EV_2025_AC_CHARGER"),
"0401":("https://ownersmanual.hyundai.com/full_webhelp/SX2EV/2025/en_US/images/2C_ACCharger.jpg.png",(0.45,0.18,1.00,0.92),"HY_SX2EV_2025_AC_CHARGER"),
"0497":("https://ownersmanual.hyundai.com/full_webhelp/SX2EV/2025/en_US/images/2C_ACCharger.jpg.png",(0.45,0.18,1.00,0.92),"HY_SX2EV_2025_AC_CHARGER"),
"0483":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_FrontWiperReplacementProcedure.jpg.png",(0.00,0.00,0.50,1.00),"HY_WIPER_COMPONENTS"),
"0484":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RearWiperReplacementProcedure_1.jpg.png",None,"HY_WIPER_COMPONENTS"),
}

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
passed=[]; failed=[]
for id_,(url,b,src) in jobs.items():
    if byid[id_].get("status")=="PASS": continue
    try:
        w,h,size=save(crop(fetch(url,id_),b),id_)
        passed.append((id_,byid[id_]["en"],src,w,h,size))
    except Exception as e:
        failed.append((id_,byid[id_]["en"],str(e)))

for id_,term,src,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-22-basic-hardware.md"
lines=["# CAR MASTER — Backlog Recovery 22 — Basic Hardware","","## PASS"]
lines += [f"- **{a} {b}** — {d}x{e}, {f} bytes — {c}" for a,b,c,d,e,f in passed] or ["- None"]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Reverse-QA",
"- 0472/0473 must distinguish positive vs negative terminal.",
"- 0471 must show coolant cap, not reservoir only.",
"- 0400 must show charging connector; 0401/0497 must show connector release/unlock control area.",
"- 0483/0484 must show the relevant wiper arm cap areas.",
"- Count live Production only after Codex reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",passed); print("FAIL",failed)
