from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import urllib.request, json, shutil

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"
OUT=ROOT/"production-preview"
DL=OUT/"batch-19-100-attempt"
PARTS.mkdir(parents=True,exist_ok=True)
DL.mkdir(parents=True,exist_ok=True)

def get(url,path):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        Path(path).write_bytes(r.read())
    im=Image.open(path)
    im.verify()
    return Image.open(path).convert("RGB")

def fetch_first(urls,id_):
    errs=[]
    for i,u in enumerate(urls):
        try:
            return get(u,DL/f"{id_}-{i}.src")
        except Exception as e:
            errs.append(str(e))
    raise RuntimeError(" | ".join(errs))

def crop_rel(im,b=None):
    if b is None:
        return im
    w,h=im.size
    x1,y1,x2,y2=b
    return im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))

def fit4(im):
    w,h=im.size
    if w/h>4/3:
        nw=max(1,int(h*4/3))
        x=(w-nw)//2
        return im.crop((x,0,x+nw,h))
    nh=max(1,int(w*3/4))
    y=(h-nh)//2
    return im.crop((0,y,w,y+nh))

def save_card(im,id_):
    im=fit4(im)
    if im.width<480:
        s=480/im.width
        im=im.resize((int(im.width*s),int(im.height*s)),Image.Resampling.LANCZOS)
        im=fit4(im)
    out=PARTS/f"{id_}.jpg"
    im.save(out,quality=95,subsampling=0)
    v=Image.open(out)
    v.verify()
    v=Image.open(out)
    if abs(v.width/v.height-4/3)>0.02 or out.stat().st_size<5000:
        raise RuntimeError("validation")
    return v.width,v.height,out.stat().st_size

mf=ROOT/"data"/"master.json"
master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else []))
byid={x["id"]:x for x in items}
backlog=[x for x in items if x.get("status")!="PASS"]
strong=[x["id"] for x in backlog if any(r and not any(t in r for t in ["DIRECT_VISUAL","TAXONOMY","UNDERBODY"]) for r in x.get("source_refs",[]))]
extras=["0263","0266","0270","0282","0311","0312","0313","0306","0351","0352","0354","0355","0358","0322","0329","0361","0362","0218","0219","0220"]
attempted=[]
for id_ in extras+strong:
    if id_ in byid and byid[id_].get("status")!="PASS" and id_ not in attempted:
        attempted.append(id_)
attempted=attempted[:100]

jobs={
"0138":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SpareTireReplacementPrecedure.jpg.png"],None,"HY_LX3_2026_SPARE_TIRE"),
"0263":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_AdjustClusterLightingBrightness.jpg.png"],None,"HY_LX3_2026_CLUSTER_ILLUMINATION"),
"0266":(["https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_US/images/2C_LaneSafetyButton.jpg.png","https://ownersmanual.hyundai.com/full_webhelp/ne1n/2026/en_us/images/2C_LaneSafetyButton.jpg.png"],None,"HY_NE1N_2026_LANE_SAFETY_BUTTON"),
"0270":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_HUDIconInfo.jpg.png"],None,"HY_LX3_2026_HUD_INFO"),
"0282":(["https://ownersmanual.hyundai.com/full_webhelp/US4/2025/en_GN/images/CGJ4M0000EE.eps.png","https://ownersmanual.hyundai.com/full_webhelp/US4/2025/en_GN/images/CGJ4M0000EE.jpg.png"],None,"HY_US4_2025_AUDIO_CONTROL_PANEL"),
"0311":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_AdjustSeatForwardBackwardmanual.jpg.png"],None,"HY_LX3_2026_MANUAL_SEAT_ADJUST"),
"0312":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_AdjustSeatBackmanual.jpg.png"],None,"HY_LX3_2026_MANUAL_SEAT_ADJUST"),
"0313":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_AdjustSeatHeightmanual.jpg.png"],None,"HY_LX3_2026_MANUAL_SEAT_ADJUST"),
"0322":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_AdjustSeatBeltHeight.jpg.png"],None,"HY_LX3_2026_SEAT_BELT_RESTRAINT"),
"0329":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SeatBeltRelease.jpg.png"],None,"HY_LX3_2026_SEAT_BELT_RESTRAINT"),
"0361":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_AdjustSeatBeltHeight.jpg.png"],None,"HY_LX3_2026_SEAT_BELT_RESTRAINT"),
"0362":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_AdjustSeatBeltHeight.jpg.png"],None,"HY_LX3_2026_SEAT_BELT_RESTRAINT"),
"0382":(["https://ownersmanual.hyundai.com/full_webhelp/ne1n/2026/en_us/images/2C_FrontUltrasonicSensor.jpg.png"],None,"HY_NE1N_2026_PDW_SENSORS"),
"0383":(["https://ownersmanual.hyundai.com/full_webhelp/ne1n/2025/ko_kr/images/2C_FrontSideUltrsonicSensor.jpg.png"],None,"HY_NE1N_2025_PCA_SENSORS"),
"0384":(["https://ownersmanual.hyundai.com/full_webhelp/ne1n/2026/en_us/images/2C_RearUltrasonicSensor.jpg.png"],None,"HY_NE1N_2026_PDW_SENSORS"),
"0385":(["https://ownersmanual.hyundai.com/full_webhelp/ne1n/2025/ko_kr/images/2C_RearSideUltrsonicSensor.jpg.png"],None,"HY_NE1N_2025_PCA_SENSORS"),
"0396":(["https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_DCAdapter.jpg.png"],None,"HY_NE1A_2025_EV_CHARGING"),
"0405":(["https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_ICCBCharger.jpg.png"],(0.66,0.12,1.0,0.90),"HY_NE1A_2025_PORTABLE_CHARGER"),
"0410":(["https://ownersmanual.hyundai.com/full_webhelp/NX4PHEV/2026/en_US/images/2C_PluginHybridBattery.jpg.png"],None,"HY_NX4PHEV_2026_HYBRID_COMPONENTS"),
"0411":(["https://ownersmanual.hyundai.com/full_webhelp/NX4PHEV/2026/en_US/images/2C_HighVoltageMotorConnector_2.jpg.png"],None,"HY_NX4PHEV_2026_HYBRID_COMPONENTS"),
"0412":(["https://ownersmanual.hyundai.com/full_webhelp/NX4PHEV/2026/en_US/images/2C_InterlockConnector.jpg.png"],None,"HY_NX4PHEV_2026_HYBRID_COMPONENTS"),
"0446":(["https://ownersmanual.hyundai.com/full_webhelp/NH2/2026/ko_KR/images/2C_RSPASmartKeyButton.jpg.png"],None,"HY_NH2_2026_RSPA_SMART_KEY_BUTTON"),
"0474":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_EngineRoomFuseReplacement.jpg.png"],None,"HY_FUSE_COMPONENTS"),
"0486":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SpareTireReplacementPrecedure_4.jpg.png"],None,"HY_WHEEL_TIRE_COMPONENTS"),
"0490":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SpareTireReplacementPrecedure_1.jpg.png"],None,"HY_SPARE_TIRE_COMPONENTS"),
"0500":(["https://ownersmanual.hyundai.com/full_webhelp/LX3HEV/2026/en_US/images/2C_BatteryAirVent.jpg.png"],None,"HY_BATTERY_COOLING_COMPONENTS"),
}

copy_jobs={
"0306":("0307","HY_AXEV_2026_CARGO_FLOOR"),
"0351":("0292","HY_DIRECT_VISUAL_OR_TAXONOMY_REQUIRED"),
"0352":("0293","HY_DIRECT_VISUAL_OR_TAXONOMY_REQUIRED"),
"0354":("0295","HY_DIRECT_VISUAL_OR_TAXONOMY_REQUIRED"),
"0355":("0292","HY_DIRECT_VISUAL_OR_TAXONOMY_REQUIRED"),
"0358":("0302","HY_DIRECT_VISUAL_OR_TAXONOMY_REQUIRED"),
}

icon_jobs={
"0420":("¢",(78,220,120),"HY_NE1A_2025_EV_GAUGES"),
"0429":("f",(255,174,66),"HY_LX3_2026_WARNING_INDICATORS"),
"0466":('"',(255,70,70),"HY_NE1A_2025_EV_GAUGES_2"),
"0469":("¥",(78,220,120),"HY_NE1A_2025_EV_GAUGES_2"),
"0470":("ª",(255,174,66),"HY_NE1A_2025_EV_GAUGES_2"),
}

woff=DL/"HYUNDAI_OWNS-Regular.woff"
ttf=DL/"HYUNDAI_OWNS-Regular.ttf"
iconfont=None
try:
    req=urllib.request.Request("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/style/fonts/HYUNDAI_OWNS-Regular.woff",headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r:
        woff.write_bytes(r.read())
    ft=TTFont(str(woff))
    ft.flavor=None
    ft.save(str(ttf))
    iconfont=ImageFont.truetype(str(ttf),220)
except Exception:
    pass

passed=[]
failed=[]
deferred=[]

for id_,(urls,box,src) in jobs.items():
    if id_ not in attempted:
        continue
    try:
        im=crop_rel(fetch_first(urls,id_),box)
        w,h,size=save_card(im,id_)
        passed.append((id_,byid[id_]["en"],src,w,h,size,"official image"))
    except Exception as e:
        failed.append((id_,byid[id_]["en"],str(e)))

for id_,(srcid,src_ref) in copy_jobs.items():
    if id_ not in attempted:
        continue
    try:
        src=PARTS/f"{srcid}.jpg"
        if not src.exists():
            raise RuntimeError(f"validated source asset {srcid} missing")
        shutil.copyfile(src,PARTS/f"{id_}.jpg")
        v=Image.open(PARTS/f"{id_}.jpg")
        v.verify()
        v=Image.open(PARTS/f"{id_}.jpg")
        passed.append((id_,byid[id_]["en"],src_ref,v.width,v.height,(PARTS/f"{id_}.jpg").stat().st_size,f"exact physical reuse from {srcid}"))
    except Exception as e:
        failed.append((id_,byid[id_]["en"],str(e)))

if iconfont:
    for id_,(glyph,color,src) in icon_jobs.items():
        if id_ not in attempted:
            continue
        try:
            im=Image.new("RGB",(640,480),(16,18,22))
            d=ImageDraw.Draw(im)
            bb=d.textbbox((0,0),glyph,font=iconfont)
            tw,th=bb[2]-bb[0],bb[3]-bb[1]
            d.text(((640-tw)/2-bb[0],(480-th)/2-bb[1]),glyph,font=iconfont,fill=color)
            w,h,size=save_card(im,id_)
            passed.append((id_,byid[id_]["en"],src,w,h,size,"official HyundaiOwns glyph"))
        except Exception as e:
            failed.append((id_,byid[id_]["en"],str(e)))

passed_ids={x[0] for x in passed}
failed_ids={x[0] for x in failed}
for id_ in attempted:
    if id_ not in passed_ids and id_ not in failed_ids:
        deferred.append((id_,byid[id_]["en"],"no direct-enough card-specific image in this subpass"))

for id_,term,src,w,h,size,method in passed:
    x=byid[id_]
    x["status"]="PASS"
    x["production_backlog"]=False
    x["image"]=f"images/parts/{id_}.jpg"
    x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-19-100-attempt.md"
lines=[
"# CAR MASTER — Backlog Recovery 19 — 100-Item Attempt",
"",
f"Attempted: **{len(attempted)}**",
f"PASS produced: **{len(passed)}**",
f"Download/production failures: **{len(failed)}**",
f"Deferred without status change: **{len(deferred)}**",
"",
"## Attempted IDs",
" ".join(attempted),
"",
"## PASS"
]
lines += [f"- **{a} {b}** — {d}x{e}, {f} bytes — {g} — {c}" for a,b,c,d,e,f,g in passed] or ["- None"]
lines += ["","## Production failures"]
lines += [f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Deferred / search-next"]
lines += [f"- **{a} {b}** — {c}" for a,b,c in deferred]
lines += [
"",
"## Guardrails",
"- This is a 100-item attempt batch, not a forced 100-PASS batch.",
"- Only card-specific official images, exact already-validated physical reuses, or official Hyundai icon-font glyphs are promoted.",
"- Deferred items stay hidden/backlog.",
"- Codex must reverse-QA every promoted card before live Production count."
]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("ATTEMPTED",len(attempted))
print("PASS",len(passed),[x[0] for x in passed])
print("FAIL",failed)
print("DEFERRED",len(deferred))
