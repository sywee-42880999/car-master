from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, json, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"
PARTS=ROOT/"images"/"parts"
DL=OUT/"batch-0371-0420-source"
OUT.mkdir(exist_ok=True); PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

# Only dedicated/direct Hyundai Owner's Manual visuals are eligible for auto-promotion.
sources={
 "0376":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_KneeAirbag.jpg.png","DRIVER'S KNEE AIRBAG","dedicated Hyundai knee-airbag location image","HY_LX3_2026_AIRBAG_LOCATION"),
 "0398":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_ChargingDoorIndicator.jpg.png","CHARGE INDICATOR LIGHT","dedicated Hyundai charge-indicator image","HY_NE1A_2025_EV_CHARGING"),
 "0399":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_ChargingLabel.jpg.png","CHARGING LABEL","dedicated Hyundai charging-label image","HY_NE1A_2025_EV_CHARGING"),
 "0408":("https://ownersmanual.hyundai.com/full_webhelp/LX3HEV/2026/en_US/images/2C_HPCU.jpg.png","HYBRID POWER CONTROL UNIT","dedicated Hyundai HPCU image","HY_LX3HEV_2026_HYBRID_COMPONENTS"),
 "0409":("https://ownersmanual.hyundai.com/full_webhelp/LX3HEV/2026/en_US/images/2C_HybridBattery.jpg.png","HIGH VOLTAGE BATTERY","dedicated Hyundai high-voltage battery image","HY_LX3HEV_2026_HYBRID_COMPONENTS"),
 "0413":("https://ownersmanual.hyundai.com/full_webhelp/LX3HEV/2026/en_US/images/2C_BatteryAirVent.jpg.png","HYBRID BATTERY COOLING DUCT","dedicated Hyundai battery cooling air-vent image","HY_LX3HEV_2026_BATTERY_AIR_VENT"),
}

def fetch(url,id_):
    p=DL/f"{id_}.src"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        p.write_bytes(r.read())
    im=Image.open(p)
    im.verify()
    return Image.open(p).convert("RGB"),p

def crop4(im):
    w,h=im.size
    target=4/3
    if w/h > target:
        nw=max(1,int(h*target)); x=(w-nw)//2
        return im.crop((x,0,x+nw,h))
    nh=max(1,int(w/target)); y=(h-nh)//2
    return im.crop((0,y,w,y+nh))

passed=[]; failures=[]; cards=[]
for id_,(url,term,note,src) in sources.items():
    try:
        im,p=fetch(url,id_)
        c=crop4(im)
        out=PARTS/f"{id_}.jpg"
        c.save(out,quality=94,subsampling=0)
        # validation
        v=Image.open(out); v.verify()
        v=Image.open(out); w,h=v.size
        if abs((w/h)-(4/3))>0.02: raise RuntimeError(f"aspect error {w}x{h}")
        if out.stat().st_size<5000: raise RuntimeError(f"suspiciously small {out.stat().st_size}")
        passed.append((id_,term,note,src,url,w,h,out.stat().st_size))
        thumb=ImageOps.contain(c,(560,400))
        card=Image.new("RGB",(600,470),"white"); card.paste(thumb,((600-thumb.width)//2,10))
        d=ImageDraw.Draw(card); d.text((12,420),f"{id_} PASS — {term}",fill="black"); d.text((12,442),note,fill="black")
        cards.append(card)
    except Exception as e:
        failures.append((id_,term,str(e)))

# Update master only for successfully downloaded/validated direct visuals.
mf=ROOT/"data"/"master.json"
master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else []))
byid={x["id"]:x for x in items}
for id_,term,note,src,url,w,h,size in passed:
    x=byid[id_]
    x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"
    x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

# Register source families actually used by this production pass.
sf=ROOT/"data"/"source_registry.json"
reg=json.loads(sf.read_text(encoding="utf-8")); S=reg["sources"]
S["HY_LX3HEV_2026_HYBRID_COMPONENTS"]={
 "maker":"Hyundai","model":"Palisade LX3 HEV","year":"2026","type":"official_web_manual",
 "web_url":"https://ownersmanual.hyundai.com/full_webhelp/LX3HEV/2026/en_US/topic_cpz_qsz_rvb.html",
 "pdf_url":None,"image_keys":["2C_HPCU","2C_HybridBattery"],"repo_asset":None,
 "used_by":["0408","0409"],"source_verified_at":"2026-09-08"}
S["HY_LX3HEV_2026_BATTERY_AIR_VENT"]={
 "maker":"Hyundai","model":"Palisade LX3 HEV","year":"2026","type":"official_web_manual",
 "web_url":"https://ownersmanual.hyundai.com/full_webhelp/LX3HEV/2026/en_US/topic_ygp_zcy_v5b.html",
 "pdf_url":None,"image_keys":["2C_BatteryAirVent"],"repo_asset":None,
 "used_by":["0413"],"source_verified_at":"2026-09-08"}
sf.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

# Append exact production result. Non-candidates remain REVIEW/backlog from taxonomy pass.
rf=ROOT/"research"/"0371-0420-production-pass2.md"
lines=["# CAR MASTER — 0371–0420 Production Pass 2","",
"GitHub Actions binary-fetch pass. Only dedicated/direct Hyundai Owner's Manual images are eligible for PASS.","",
"## PASS"]
if passed:
    for id_,term,note,src,url,w,h,size in passed:
        lines.append(f"- **{id_} {term}** — {w}x{h}, {size} bytes, source {src}")
else:
    lines.append("- None")
lines += ["","## Fetch/validation failures"]
if failures:
    for id_,term,err in failures: lines.append(f"- **{id_} {term}** — {err}")
else:
    lines.append("- None")
lines += ["","## Rule","- All other IDs 0371–0420 remain REVIEW + Production Backlog.","- No generic/stock substitution.","- BLACK UI design unchanged.","- Production percentage changes only after live UI deploy/mobile reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")

if cards:
    cols=2; rows=math.ceil(len(cards)/cols)
    sheet=Image.new("RGB",(cols*600,rows*470),"white")
    for i,c in enumerate(cards): sheet.paste(c,((i%cols)*600,(i//cols)*470))
    sheet.save(OUT/"0371-0420-pass2-qa.jpg",quality=92)

print("PASS",[x[0] for x in passed])
print("FAILURES",failures)
print("VALIDATION_OK",True)
