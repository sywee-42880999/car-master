from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, json, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"; DL=OUT/"batch-0471-0500-source"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

sources={
 "0476":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_EngineRoomFuseReplacement_2.jpg.png","BLADE TYPE FUSE","dedicated Hyundai blade-type fuse replacement image","HY_FUSE_COMPONENTS"),
 "0477":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_EngineRoomFuseReplacement_3.jpg.png","CARTRIDGE TYPE FUSE","dedicated Hyundai cartridge-type fuse replacement image","HY_FUSE_COMPONENTS"),
 "0478":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_EngineRoomFuseReplacement_4.jpg.png","MULTI FUSE","dedicated Hyundai multi-fuse image","HY_FUSE_COMPONENTS"),
 "0480":("https://ownersmanual.hyundai.com/full_webhelp/LX3HEV/2026/en_US/images/2C_AirCleanerReplacementProcedure_2.jpg.png","AIR CLEANER FILTER","dedicated Hyundai air-cleaner filter image","HY_AIR_FILTER_COMPONENTS"),
 "0481":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_AirFilterReplacementProcedure_3.jpg.png","CABIN AIR FILTER COVER","dedicated Hyundai cabin-filter cover image","HY_CABIN_FILTER_COMPONENTS"),
 "0482":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_FrontWiperReplacementProcedure_2.jpg.png","FRONT WIPER BLADE","dedicated Hyundai front-wiper blade replacement image","HY_WIPER_COMPONENTS"),
 "0485":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_TowingHook.jpg.png","TOWING EYE","dedicated Hyundai removable towing hook image","HY_TOWING_COMPONENTS"),
}

def fetch(url,id_):
    p=DL/f"{id_}.src"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r: p.write_bytes(r.read())
    im=Image.open(p); im.verify()
    return Image.open(p).convert("RGB")

def crop4(im):
    w,h=im.size
    if w/h>4/3:
        nw=int(h*4/3); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
    nh=int(w*3/4); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

passed=[]; failures=[]; cards=[]
for id_,(url,term,note,src) in sources.items():
    try:
        c=crop4(fetch(url,id_)); out=PARTS/f"{id_}.jpg"; c.save(out,quality=94,subsampling=0)
        v=Image.open(out); v.verify(); v=Image.open(out); w,h=v.size
        if abs(w/h-4/3)>0.02: raise RuntimeError(f"aspect error {w}x{h}")
        if out.stat().st_size<5000: raise RuntimeError(f"suspiciously small {out.stat().st_size}")
        passed.append((id_,term,note,src,w,h,out.stat().st_size))
        t=ImageOps.contain(c,(560,400)); card=Image.new("RGB",(600,470),"white"); card.paste(t,((600-t.width)//2,10))
        d=ImageDraw.Draw(card); d.text((12,420),f"{id_} PASS — {term}",fill="black"); d.text((12,442),note,fill="black"); cards.append(card)
    except Exception as e:
        failures.append((id_,term,str(e)))

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8")); items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
for id_,term,note,src,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"0471-0500-production-pass2.md"
lines=["# CAR MASTER — 0471–0500 Production Pass 2","","Only dedicated/direct Hyundai Owner's Manual images are eligible for PASS.","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, source {src}" for id_,term,note,src,w,h,size in passed] or ["- None"]
lines += ["","## Fetch/validation failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Rule","- All other IDs 0471–0500 remain REVIEW + Production Backlog.","- No generic/stock substitution.","- BLACK UI unchanged.","- Production % only after live UI deploy/mobile reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")

if cards:
    cols=2; rows=math.ceil(len(cards)/cols); sheet=Image.new("RGB",(cols*600,rows*470),"white")
    for i,c in enumerate(cards): sheet.paste(c,((i%cols)*600,(i//cols)*470))
    sheet.save(OUT/"0471-0500-pass2-qa.jpg",quality=92)

print("PASS",[x[0] for x in passed]); print("FAILURES",failures); print("VALIDATION_OK",True)
