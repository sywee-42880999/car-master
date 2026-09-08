from pathlib import Path
from PIL import Image
import urllib.request, json

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"backlog-recovery-13"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

REAR="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleRearOverview.jpg.png"
jobs={
 "0233":([REAR],"ROOF SPOILER GARNISH","HY_LX3_2026_REAR_OVERVIEW",(0.18,0.00,0.83,0.25)),
 "0234":([REAR],"LIFTGATE GARNISH","HY_LX3_2026_REAR_OVERVIEW",(0.25,0.34,0.84,0.68)),
 "0236":([REAR],"LICENSE PLATE GARNISH","HY_LX3_2026_REAR_OVERVIEW",(0.27,0.52,0.75,0.76)),
 "0240":([REAR],"BUMPER MOLDING","HY_LX3_2026_REAR_OVERVIEW",(0.12,0.61,0.88,0.94)),
 "0307":(["https://ownersmanual.hyundai.com/full_webhelp/AXEV/2026/en_AU/images/2C_CargoCompartmentStorageOrganizationBox.jpg.png"],"CARGO FLOOR BOARD","HY_AXEV_2026_CARGO_FLOOR",(0.00,0.00,1.00,0.72)),
 "0359":([
   "https://ownersmanual.kia.com/full_webhelp/ON/2024/en_US/images/OON042021.jpg",
   "https://ownersmanual.kia.com/full_webhelp/ON/2024/en_US/images/OON042021.png",
   "https://ownersmanual.kia.com/full_webhelp/ON/2024/en_US/images/OON042021.jpg.png"
 ],"SUNGLASSES HOLDER","KIA_ON_2024_SUNGLASS_HOLDER",(0.00,0.00,1.00,1.00)),
}

_cache={}
def fetch_first(urls,id_):
    errs=[]
    for i,url in enumerate(urls):
        try:
            if url in _cache: return _cache[url].copy()
            p=DL/f"{id_}-{i}.src"
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=30) as r: p.write_bytes(r.read())
            im=Image.open(p); im.verify()
            im=Image.open(p).convert("RGB"); _cache[url]=im
            return im.copy()
        except Exception as e: errs.append(str(e))
    raise RuntimeError(" | ".join(errs))

def relcrop(im,b):
    w,h=im.size; x1,y1,x2,y2=b
    return im.crop((int(x1*w),int(y1*h),int(x2*w),int(y2*h)))

def fit4(im):
    w,h=im.size
    if w/h>4/3:
        nw=max(1,int(h*4/3)); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
    nh=max(1,int(w*3/4)); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

passed=[]; failures=[]
for id_,(urls,term,src,box) in jobs.items():
    try:
        im=fit4(relcrop(fetch_first(urls,id_),box))
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

rf=ROOT/"research"/"backlog-recovery-13.md"
lines=["# CAR MASTER — Backlog Recovery 13","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, {src}" for id_,term,src,w,h,size in passed] or ["- None"]
lines += ["","## Failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Reverse-QA",
"- 0233/0234/0236/0240 are distinct rear-body crops; do not substitute the uncropped rear overview.",
"- 0307 must show the physical cargo floor board/cover being lifted, not only the storage tray beneath.",
"- 0359 uses Kia official Owner’s Manual under the approved manufacturer-manual fallback policy and must visibly show the sunglass holder.",
"- Count live Production only after Codex bind + mobile + reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",[x[0] for x in passed]); print("FAILURES",failures)
