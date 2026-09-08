from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, json, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"; DL=OUT/"backlog-recovery-07"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

jobs={
 "0297":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_CenterConsoleBox.jpg.png","CENTER CONSOLE ARMREST","HY_LX3_2026_CENTER_CONSOLE_STORAGE_DETAIL",(0.05,0.00,0.95,0.55)),
 "0298":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_CenterConsoleBox_2.jpg.png","CONSOLE STORAGE LID","HY_LX3_2026_CENTER_CONSOLE_STORAGE_DETAIL",(0.02,0.00,0.98,0.60)),
 "0320":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_AdjustHeadrestUpDown.jpg.png","HEAD RESTRAINT RELEASE BUTTON","HY_LX3_2026_HEAD_RESTRAINT_DETAIL",(0.20,0.30,0.75,0.98)),
}

def fetch(url,id_):
    p=DL/f"{id_}.src"; req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
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
        if abs(w/h-4/3)>0.02: raise RuntimeError(f"aspect {w}x{h}")
        if out.stat().st_size<5000: raise RuntimeError(f"small {out.stat().st_size}")
        passed.append((id_,term,src,w,h,out.stat().st_size))
    except Exception as e:
        failures.append((id_,term,str(e)))

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
for id_,term,src,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-07.md"
lines=["# CAR MASTER — Backlog Recovery 07","","Card-specific crops only.","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, {src}" for id_,term,src,w,h,size in passed] or ["- None"]
lines += ["","## Failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Reverse-QA","- 0297 must visibly read as the armrest portion of the center console.","- 0298 must visibly read as the storage lid/cover, not merely the console box.","- 0320 must visibly show the head-restraint release button/support area.","- Do not count live Production until Codex reverse-QA passes."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",[x[0] for x in passed]); print("FAILURES",failures)
