from pathlib import Path
from PIL import Image
import urllib.request, json

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"batch-23-seat-tire"
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
        s=480/im.width; im=im.resize((int(im.width*s),int(im.height*s)),Image.Resampling.LANCZOS); im=fit4(im)
    out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
    v=Image.open(out); v.verify(); v=Image.open(out)
    if out.stat().st_size<5000: raise RuntimeError("small")
    return v.width,v.height,out.stat().st_size

jobs={
"0079":("https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/images/B0053EU09.jpg.png",None,"HY_LX2_2025_REAR_SEAT_GUIDE"),
"0330":("https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/images/B0053EU07.jpg.png",None,"HY_LX2_2025_REAR_SEAT_GUIDE"),
"0364":("https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/images/B0053EU08.jpg.png",None,"HY_LX2_2025_REAR_SEAT_GUIDE"),
"0488":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_TMKProcedure_3.jpg.png",(0.30,0.20,0.90,0.95),"HY_LX3_2026_TMK_VALVE"),
}
mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
passed=[]; failed=[]
for id_,(url,b,src) in jobs.items():
    if byid[id_].get("status")=="PASS": continue
    try:
        w,h,size=save(crop(fetch(url,id_),b),id_)
        passed.append((id_,byid[id_]["en"],src,w,h,size))
    except Exception as e: failed.append((id_,byid[id_]["en"],str(e)))
for id_,term,src,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
rf=ROOT/"research"/"backlog-recovery-23-seat-tire.md"
lines=["# CAR MASTER — Backlog Recovery 23 — Seat/Tire","","## PASS"]
lines += [f"- **{a} {b}** — {d}x{e}, {f} bytes — {c}" for a,b,c,d,e,f in passed] or ["- None"]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Reverse-QA","- 0079 must show the folding lever/strap, not generic rear seat.","- 0330/0364 must show seat-belt guide routing points.","- 0488 must show the tire valve cap/valve area clearly.","- Count live Production only after Codex reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",passed); print("FAIL",failed)
