from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, json, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; PARTS=ROOT/"images"/"parts"; DL=OUT/"codex-hold-recovery"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

# Exact Codex-held cards. Each must become card-specific; full overviews are not acceptable.
jobs={
 "0131":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SpareTireReplacementOverview.jpg.png","JACK HANDLE","HY_LX3_2026_SPARE_TIRE",(0.02,0.07,0.18,0.50)),
 "0132":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SpareTireReplacementOverview.jpg.png","JACK","HY_LX3_2026_SPARE_TIRE",(0.17,0.04,0.42,0.52)),
 "0133":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SpareTireReplacementOverview.jpg.png","TOWING HOOK","HY_LX3_2026_SPARE_TIRE",(0.40,0.05,0.58,0.50)),
 "0134":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SpareTireReplacementOverview.jpg.png","WHEEL LUG NUT WRENCH","HY_LX3_2026_SPARE_TIRE",(0.56,0.05,0.75,0.50)),
 "0135":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SpareTireReplacementOverview.jpg.png","SOCKET","HY_LX3_2026_SPARE_TIRE",(0.72,0.05,0.90,0.50)),
 "0144":("https://ownersmanual.hyundai.com/full_webhelp/MX5/2026/ko_KR/images/1C_EngineRoom.jpg.png","BATTERY","HY_MX5_2026_ENGINE_ROOM_RECOVERY",(0.67,0.18,0.93,0.62)),
 "0145":("https://ownersmanual.hyundai.com/full_webhelp/MX5/2026/ko_KR/images/1C_EngineRoom.jpg.png","FUSE BOX","HY_MX5_2026_ENGINE_ROOM_RECOVERY",(0.72,0.26,0.97,0.72)),
 "0147":("https://ownersmanual.hyundai.com/full_webhelp/MX5/2026/ko_KR/images/1C_EngineRoom.jpg.png","ENGINE OIL DIPSTICK","HY_MX5_2026_ENGINE_ROOM_RECOVERY",(0.20,0.28,0.45,0.72)),
 "0360":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_MapLamp.jpg.png","OVERHEAD CONSOLE","HY_NX4_2025_OVERHEAD_CONSOLE_RECOVERY",None),
}

def fetch(url,id_):
    p=DL/f"{id_}.src"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r: p.write_bytes(r.read())
    im=Image.open(p); im.verify()
    return Image.open(p).convert("RGB")

def relcrop(im,box):
    if box is None: return im
    w,h=im.size
    x1,y1,x2,y2=box
    return im.crop((int(x1*w),int(y1*h),int(x2*w),int(y2*h)))

def fit4(im):
    w,h=im.size
    target=4/3
    if w/h>target:
        nw=max(1,int(h*target)); x=(w-nw)//2; return im.crop((x,0,x+nw,h))
    nh=max(1,int(w/target)); y=(h-nh)//2; return im.crop((0,y,w,y+nh))

passed=[]; failures=[]; cards=[]
for id_,(url,term,src,box) in jobs.items():
    try:
        im=fit4(relcrop(fetch(url,id_),box))
        # upscale tiny crops to keep card readability
        if im.width < 480:
            scale=480/im.width
            im=im.resize((int(im.width*scale),int(im.height*scale)),Image.Resampling.LANCZOS)
            im=fit4(im)
        out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
        v=Image.open(out); v.verify(); v=Image.open(out); w,h=v.size
        if abs(w/h-4/3)>0.02: raise RuntimeError(f"aspect {w}x{h}")
        if out.stat().st_size<5000: raise RuntimeError(f"small {out.stat().st_size}")
        passed.append((id_,term,src,w,h,out.stat().st_size))
        t=ImageOps.contain(im,(560,400)); card=Image.new("RGB",(600,470),"white"); card.paste(t,((600-t.width)//2,10))
        d=ImageDraw.Draw(card); d.text((12,420),f"{id_} RECOVERY — {term}",fill="black"); cards.append(card)
    except Exception as e:
        failures.append((id_,term,str(e)))

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
for id_,term,src,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"codex-hold-recovery.md"
lines=["# CAR MASTER — Codex Hold Recovery","","These IDs were held by Codex reverse-QA and are re-produced only as card-specific crops/replacement images.","","## PASS"]
lines += [f"- **{id_} {term}** — {w}x{h}, {size} bytes, {src}" for id_,term,src,w,h,size in passed] or ["- None"]
lines += ["","## Failures"]
lines += [f"- **{id_} {term}** — {err}" for id_,term,err in failures] or ["- None"]
lines += ["","## Reverse-QA requirement","- 0131–0135 must each show only the requested tool, not the five-tool overview.","- 0144/0145/0147 must each show a card-specific engine-bay crop.","- 0360 must depict a ceiling overhead console, not center-console storage.","- Do not count these as live Production until Codex binds and reverse-QA passes."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")

if cards:
    cols=2; rows=math.ceil(len(cards)/cols); sheet=Image.new("RGB",(cols*600,rows*470),"white")
    for i,c in enumerate(cards): sheet.paste(c,((i%cols)*600,(i//cols)*470))
    sheet.save(OUT/"codex-hold-recovery-qa.jpg",quality=92)

print("PASS",[x[0] for x in passed]); print("FAILURES",failures); print("VALIDATION_OK",True)
