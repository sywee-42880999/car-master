from pathlib import Path
from PIL import Image
import urllib.request, json
ROOT=Path(__file__).resolve().parents[1]; PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"backlog-recovery-11"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)
jobs={
"0334":("https://ownersmanual.hyundai.com/full_webhelp/QZ/2026/ko_KR/images/2C_LQZ030152K.jpg.png","DOOR POCKET","HY_QZ_2026_DOOR_POCKET"),
"0335":("https://ownersmanual.hyundai.com/full_webhelp/AXEV/2026/en_UK/images/2C_ShoppingBagHook_2_RHD.jpg.png","DOOR ARMREST","HY_AXEV_2026_DOOR_ARMREST"),
"0336":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_MoodLamp.jpg.png","DOOR TRIM","HY_LX3_2026_DOOR_TRIM"),
}
def fetch(url,id_):
 p=DL/f"{id_}.src"; req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
 with urllib.request.urlopen(req,timeout=30) as r:p.write_bytes(r.read())
 im=Image.open(p); im.verify(); return Image.open(p).convert("RGB")
def fit4(im):
 w,h=im.size
 if w/h>4/3:
  nw=int(h*4/3); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
 nh=int(w*3/4); y=(h-nh)//2; return im.crop((0,y,w,y+nh))
passed=[]; failures=[]
for id_,(url,term,src) in jobs.items():
 try:
  im=fit4(fetch(url,id_))
  if im.width<480:
   sc=480/im.width; im=im.resize((int(im.width*sc),int(im.height*sc)),Image.Resampling.LANCZOS); im=fit4(im)
  out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
  v=Image.open(out); v.verify(); v=Image.open(out); w,h=v.size
  if abs(w/h-4/3)>0.02 or out.stat().st_size<5000: raise RuntimeError("validation")
  passed.append((id_,term,src,w,h,out.stat().st_size))
 except Exception as e: failures.append((id_,term,str(e)))
mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8")); items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
for id_,term,src,w,h,size in passed:
 x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
rf=ROOT/"research"/"backlog-recovery-11.md"; lines=["# CAR MASTER — Backlog Recovery 11","","## PASS"]+[f"- **{a} {b}** — {d}x{e}, {f} bytes, {c}" for a,b,c,d,e,f in passed]+["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failures]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",[x[0] for x in passed]); print("FAILURES",failures)
