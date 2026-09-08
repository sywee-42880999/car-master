from pathlib import Path
from PIL import Image
import urllib.request, json

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"backlog-recovery-08"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

jobs={
 "0330":("https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/images/B0053KO11.jpg.png","SEAT BELT GUIDE","HY_LX2_2025_REAR_SEATBELT_GUIDE",(0.00,0.15,0.58,0.98)),
 "0364":("https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/images/B0053EU07.jpg.png","SEAT BELT GUIDE","HY_LX2_2025_REAR_SEATBELT_GUIDE",(0.00,0.08,0.62,0.98)),
}

def fetch(url,id_):
    p=DL/f"{id_}.src"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r: p.write_bytes(r.read())
    im=Image.open(p); im.verify()
    return Image.open(p).convert("RGB")

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
        im=fit4(relcrop(fetch(url,id_),box))
        if im.width<480:
            sc=480/im.width; im=im.resize((int(im.width*sc),int(im.height*sc)),Image.Resampling.LANCZOS); im=fit4(im)
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

rf=ROOT/"research"/"backlog-recovery-08.md"
lines=["# CAR MASTER — Backlog Recovery 08","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, {src}" for id_,term,src,w,h,size in passed] or ["- None"]
lines += ["","## Failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Reverse-QA","- 0330/0364 must visibly show the physical rear-seat seat-belt guide/routing point.","- No generic seat image.","- Count live Production only after Codex reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",[x[0] for x in passed]); print("FAILURES",failures)
