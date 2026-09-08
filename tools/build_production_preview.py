from pathlib import Path
from PIL import Image
import urllib.request, json

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"backlog-recovery-16"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

URL="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SmartKeyOverview.jpg.png"
SRC="HY_LX3_2026_SMART_KEY"
jobs={
 "0447":("DOOR LOCK BUTTON",(0.04,0.08,0.52,0.36)),
 "0448":("DOOR UNLOCK BUTTON",(0.04,0.29,0.52,0.55)),
 "0450":("PANIC BUTTON",(0.48,0.55,0.97,0.88)),
 "0451":("LIFTGATE OPEN/CLOSE BUTTON",(0.47,0.28,0.97,0.58)),
}

def fetch():
    p=DL/"smartkey.src"
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
        nw=max(1,int(h*4/3)); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
    nh=max(1,int(w*3/4)); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

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

rf=ROOT/"research"/"backlog-recovery-16.md"
lines=["# CAR MASTER — Backlog Recovery 16","","Smart-key button cards use distinct crops from Hyundai official Smart Key Overview.","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, {SRC}" for id_,term,w,h,size in passed] or ["- None"]
lines += ["","## Failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Reverse-QA",
"- 0447/0448/0450/0451 must each show the correct smart-key icon/button.",
"- Do not bind the uncropped full smart-key overview to these cards.",
"- If any crop does not clearly isolate the requested button, Codex must hold only that exact ID.",
"- Count live Production only after Codex bind + mobile + reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",[x[0] for x in passed]); print("FAILURES",failures)
