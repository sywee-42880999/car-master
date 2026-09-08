from pathlib import Path
from PIL import Image
import urllib.request, json

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"backlog-recovery-12"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

URL="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleFrontOverview.jpg.png"
SRC="HY_LX3_2026_EXTERIOR_OVERVIEWS"
jobs={
 "0214":("WINDOW BELT MOLDING",(0.53,0.39,0.95,0.58)),
 "0215":("A-PILLAR GARNISH",(0.49,0.10,0.66,0.49)),
 "0216":("B-PILLAR GARNISH",(0.65,0.12,0.79,0.54)),
 "0217":("C-PILLAR GARNISH",(0.79,0.11,0.96,0.53)),
 "0223":("DOOR SILL",(0.48,0.61,0.84,0.83)),
 "0224":("ROCKER PANEL",(0.44,0.74,0.90,0.99)),
 "0225":("SIDE SILL GARNISH",(0.52,0.72,0.94,0.96)),
}

def fetch():
    p=DL/"source.src"
    req=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0"})
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

source=fetch(); passed=[]; failures=[]
for id_,(term,box) in jobs.items():
    try:
        im=fit4(relcrop(source,box))
        if im.width<480:
            sc=480/im.width
            im=im.resize((int(im.width*sc),int(im.height*sc)),Image.Resampling.LANCZOS)
            im=fit4(im)
        out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
        v=Image.open(out); v.verify(); v=Image.open(out); w,h=v.size
        if abs(w/h-4/3)>0.02: raise RuntimeError("bad aspect")
        if out.stat().st_size<5000: raise RuntimeError("small file")
        passed.append((id_,term,w,h,out.stat().st_size))
    except Exception as e:
        failures.append((id_,term,str(e)))

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
for id_,term,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[SRC]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-12.md"
lines=["# CAR MASTER — Backlog Recovery 12","","Hyundai official exterior overview, converted into card-specific trim/pillar crops.","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, {SRC}" for id_,term,w,h,size in passed] or ["- None"]
lines += ["","## Failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Reverse-QA",
"- 0214 must read as the lower window belt molding.",
"- 0215/0216/0217 must remain visually distinct as A/B/C-pillar garnish.",
"- 0223/0224/0225 must remain visually distinct as door sill / rocker panel / side sill garnish.",
"- Do not use the uncropped exterior overview on any learning card.",
"- Count live Production only after Codex bind + mobile + reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",[x[0] for x in passed]); print("FAILURES",failures)
