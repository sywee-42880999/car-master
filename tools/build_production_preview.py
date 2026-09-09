from pathlib import Path
from PIL import Image
import urllib.request, json, shutil

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"batch-26-interior-hardware"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

def fetch_first(urls,id_):
    errs=[]
    for i,u in enumerate(urls):
        try:
            p=DL/f"{id_}-{i}.src"
            req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=30) as r:p.write_bytes(r.read())
            im=Image.open(p); im.verify()
            return Image.open(p).convert("RGB")
        except Exception as e: errs.append(str(e))
    raise RuntimeError(" | ".join(errs))

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
    if out.stat().st_size<5000: raise RuntimeError("small")
    return v.width,v.height,out.stat().st_size

jobs={
"0070":([
"https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RetractPretensioner.jpg.png",
"https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_PretensionerComponent.jpg.png"],None,"HY_LX3_2026_PRETENSIONER_DIRECT"),
"0332":([
"https://ownersmanual.hyundai.com/full_webhelp/NH2/2026/ko_KR/images/2C_CheckChildProtectRearDoorLock.jpg.png",
"https://ownersmanual.hyundai.com/full_webhelp/NH2/2026/ko_KR/images/2C_ChildProtectRearDoorLockButton.jpg.png"],None,"HY_NH2_2026_CHILD_LOCK_DIRECT"),
"0299":([
"https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_ReleasingParkingbrake_Foottype.jpg.png",
"https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_ApplyingParkingbrake_Foottype.jpg.png"],None,"HY_NX4_2025_PARKING_BRAKE_PEDAL"),
"0301":([
"https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_CupHolderRearArmrest.jpg.png"],(0.00,0.00,1.00,0.82),"HY_NX4_2025_REAR_ARMREST_CUP"),
}

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
passed=[]; failed=[]
for id_,(urls,b,src) in jobs.items():
    if byid[id_].get("status")=="PASS": continue
    try:
        w,h,size=save(crop(fetch_first(urls,id_),b),id_)
        passed.append((id_,byid[id_]["en"],src,w,h,size))
    except Exception as e: failed.append((id_,byid[id_]["en"],str(e)))

# Same physical rear/cargo power outlet as already validated 0310.
if byid["0305"].get("status")!="PASS":
    try:
        src=PARTS/"0310.jpg"
        if not src.exists(): raise RuntimeError("0310 source missing")
        shutil.copyfile(src,PARTS/"0305.jpg")
        v=Image.open(PARTS/"0305.jpg"); v.verify(); v=Image.open(PARTS/"0305.jpg")
        passed.append(("0305",byid["0305"]["en"],"HY_NX4_2025_CARGO_POWER_OUTLET",v.width,v.height,(PARTS/"0305.jpg").stat().st_size))
    except Exception as e: failed.append(("0305",byid["0305"]["en"],str(e)))

for id_,term,src,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-26-interior-hardware.md"
lines=["# CAR MASTER — Backlog Recovery 26 — Interior Hardware","","## PASS"]
lines += [f"- **{a} {b}** — {d}x{e}, {f} bytes — {c}" for a,b,c,d,e,f in passed] or ["- None"]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Reverse-QA",
"- 0070 must visibly show the pretensioner/retractor component.",
"- 0332 must show the child-protector rear door lock control/location.",
"- 0299 must show the foot-type parking brake pedal.",
"- 0301 must read as rear center armrest; 0305 as rear/cargo power outlet.",
"- Count live Production only after Codex reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",passed); print("FAIL",failed)
