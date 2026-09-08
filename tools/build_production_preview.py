from pathlib import Path
from PIL import Image
import urllib.request, json

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"backlog-recovery-10"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

FRONT="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleFrontOverview.jpg.png"
REAR="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleRearOverview.jpg.png"
jobs={
 "0028":(FRONT,"TURN SIGNAL LIGHT","HY_LX3_2026_EXTERIOR_OVERVIEWS",(0.00,0.44,0.48,0.82)),
 "0029":(REAR,"REAR SPOILER","HY_LX3_2026_REAR_OVERVIEW",(0.18,0.00,0.82,0.30)),
 "0211":(FRONT,"FRONT DOOR GLASS","HY_LX3_2026_EXTERIOR_OVERVIEWS",(0.55,0.12,0.79,0.53)),
 "0212":(FRONT,"REAR DOOR GLASS","HY_LX3_2026_EXTERIOR_OVERVIEWS",(0.70,0.12,0.93,0.54)),
 "0213":(FRONT,"QUARTER GLASS","HY_LX3_2026_EXTERIOR_OVERVIEWS",(0.82,0.12,0.99,0.50)),
 "0235":(REAR,"TAILGATE GLASS","HY_LX3_2026_REAR_OVERVIEW",(0.29,0.10,0.80,0.52)),
 "0237":(FRONT,"FRONT SKID PLATE","HY_LX3_2026_EXTERIOR_OVERVIEWS",(0.07,0.68,0.56,0.98)),
 "0238":(REAR,"REAR SKID PLATE","HY_LX3_2026_REAR_OVERVIEW",(0.18,0.70,0.82,0.99)),
}

_cache={}
def fetch(url):
    if url in _cache: return _cache[url].copy()
    p=DL/("front.src" if "FrontOverview" in url else "rear.src")
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r: p.write_bytes(r.read())
    im=Image.open(p); im.verify()
    im=Image.open(p).convert("RGB"); _cache[url]=im
    return im.copy()

def relcrop(im,b):
    w,h=im.size; x1,y1,x2,y2=b
    return im.crop((int(x1*w),int(y1*h),int(x2*w),int(y2*h)))

def fit4(im):
    w,h=im.size
    if w/h>4/3:
        nw=int(h*4/3); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
    nh=int(w*3/4); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

passed=[]; failures=[]
for id_,(url,term,src,box) in jobs.items():
    try:
        im=fit4(relcrop(fetch(url),box))
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

rf=ROOT/"research"/"backlog-recovery-10.md"
lines=["# CAR MASTER — Backlog Recovery 10","","Hyundai official front/rear exterior overviews, converted into card-specific crops.","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, {src}" for id_,term,src,w,h,size in passed] or ["- None"]
lines += ["","## Failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Reverse-QA","- Each card must read as the requested exterior part, not the whole vehicle.","- 0211/0212/0213 must remain visually distinct as front door glass / rear door glass / quarter glass.","- 0237/0238 must clearly read as lower skid-plate areas.","- Count live Production only after Codex bind + mobile + reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",[x[0] for x in passed]); print("FAILURES",failures)
