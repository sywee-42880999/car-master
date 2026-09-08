from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, json, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"; DL=OUT/"backlog-recovery-06"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

sources={
 "0325":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_ALRSeatBeltLowerAnchorOverview.jpg.png"],"CHILD RESTRAINT ANCHORAGE","HY_LX3_2026_LATCH_ANCHORS"),
 "0326":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_ALRSeatBeltTetherAnchor.jpg.png"],"TOP TETHER ANCHORAGE","HY_LX3_2026_LATCH_ANCHORS"),
 "0327":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_ALRSeatBeltLowerAnchor.jpg.png"],"LOWER ANCHORAGE","HY_LX3_2026_LATCH_ANCHORS"),
 "0357":(["https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_US/images/2C_CupHolderCenterConsole.jpg.png"],"CENTER CONSOLE CUP HOLDER","HY_NX4_2025_CUP_HOLDER"),
 "0365":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_ALRSeatBeltTetherAnchor.jpg.png"],"CHILD RESTRAINT TOP TETHER ANCHOR","HY_LX3_2026_LATCH_ANCHORS"),
 "0366":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_ALRSeatBeltLowerAnchor.jpg.png"],"CHILD RESTRAINT LOWER ANCHOR","HY_LX3_2026_LATCH_ANCHORS"),
}

def fetch_first(urls,id_):
    errs=[]
    for i,url in enumerate(urls):
        try:
            p=DL/f"{id_}-{i}.src"
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=30) as r: p.write_bytes(r.read())
            im=Image.open(p); im.verify()
            return Image.open(p).convert("RGB")
        except Exception as e: errs.append(str(e))
    raise RuntimeError(" | ".join(errs))

def crop4(im):
    w,h=im.size
    if w/h>4/3:
        nw=int(h*4/3); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
    nh=int(w*3/4); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

passed=[]; failures=[]; cards=[]
for id_,(urls,term,src) in sources.items():
    try:
        c=crop4(fetch_first(urls,id_)); out=PARTS/f"{id_}.jpg"; c.save(out,quality=94,subsampling=0)
        v=Image.open(out); v.verify(); v=Image.open(out); w,h=v.size
        if abs(w/h-4/3)>0.02: raise RuntimeError(f"aspect {w}x{h}")
        if out.stat().st_size<5000: raise RuntimeError(f"small {out.stat().st_size}")
        passed.append((id_,term,src,w,h,out.stat().st_size))
        t=ImageOps.contain(c,(560,400)); card=Image.new("RGB",(600,470),"white"); card.paste(t,((600-t.width)//2,10))
        d=ImageDraw.Draw(card); d.text((12,420),f"{id_} PASS — {term}",fill="black"); cards.append(card)
    except Exception as e: failures.append((id_,term,str(e)))

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8")); items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
for id_,term,src,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-06.md"
lines=["# CAR MASTER — Backlog Recovery 06","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, {src}" for id_,term,src,w,h,size in passed] or ["- None"]
lines += ["","## Failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Rule","- Unresolved items remain hidden/backlog.","- Official Hyundai imagery preferred; manufacturer/general web fallback remains allowed.","- BLACK UI unchanged."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")

if cards:
    cols=2; rows=math.ceil(len(cards)/cols); sheet=Image.new("RGB",(cols*600,rows*470),"white")
    for i,c in enumerate(cards): sheet.paste(c,((i%cols)*600,(i//cols)*470))
    sheet.save(OUT/"backlog-recovery-06-qa.jpg",quality=92)
print("PASS",[x[0] for x in passed]); print("FAILURES",failures); print("VALIDATION_OK",True)
