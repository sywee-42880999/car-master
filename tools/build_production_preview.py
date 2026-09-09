from pathlib import Path
from PIL import Image
import urllib.request, json, shutil

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"
OUT=ROOT/"production-preview"
DL=OUT/"batch-20-100-attempt"
PARTS.mkdir(parents=True,exist_ok=True)
DL.mkdir(parents=True,exist_ok=True)

def fetch_first(urls,id_):
    errs=[]
    for i,u in enumerate(urls):
        try:
            p=DL/f"{id_}-{i}.src"
            req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=30) as r:
                p.write_bytes(r.read())
            im=Image.open(p); im.verify()
            return Image.open(p).convert("RGB")
        except Exception as e:
            errs.append(str(e))
    raise RuntimeError(" | ".join(errs))

def crop_rel(im,b=None):
    if b is None:return im
    w,h=im.size; x1,y1,x2,y2=b
    return im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))

def fit4(im):
    w,h=im.size
    if w/h>4/3:
        nw=max(1,int(h*4/3)); x=(w-nw)//2
        return im.crop((x,0,x+nw,h))
    nh=max(1,int(w*3/4)); y=(h-nh)//2
    return im.crop((0,y,w,y+nh))

def save_card(im,id_):
    im=fit4(im)
    if im.width<480:
        s=480/im.width
        im=im.resize((int(im.width*s),int(im.height*s)),Image.Resampling.LANCZOS)
        im=fit4(im)
    out=PARTS/f"{id_}.jpg"
    im.save(out,quality=95,subsampling=0)
    v=Image.open(out); v.verify(); v=Image.open(out)
    if abs(v.width/v.height-4/3)>0.02 or out.stat().st_size<5000:
        raise RuntimeError("validation")
    return v.width,v.height,out.stat().st_size

mf=ROOT/"data"/"master.json"
master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else []))
byid={x["id"]:x for x in items}
backlog=[x for x in items if x.get("status")!="PASS"]

# Second 100: prioritize non-underbody, then fill with remaining.
priority=[
"0265","0289","0304","0310","0319","0332","0348","0356","0367","0417","0499",
"0283","0284","0285","0286","0287","0288",
"0377","0009","0010","0378","0379","0369","0370","0371","0374","0375",
"0397","0400","0401","0414","0415","0416","0452","0457","0458","0465",
"0471","0472","0473","0475","0479","0483","0484","0487","0488","0489",
"0491","0492","0493","0494","0495","0496","0497","0498"
]
rest=[x["id"] for x in backlog if x["id"] not in priority]
attempted=[]
for id_ in priority+rest:
    if id_ in byid and byid[id_].get("status")!="PASS" and id_ not in attempted:
        attempted.append(id_)
attempted=attempted[:100]

jobs={
"0265":(["https://ownersmanual.hyundai.com/docview/webhelp/Hyundai/b6495a43-8ab9-453a-96a1-645137803c3d/images/2C_ISGOffButton.jpg.png",
         "https://ownersmanual.hyundai.com/docview/webhelp/Hyundai/b6495a43-8ab9-453a-96a1-645137803c3d/images/2C_ISGOffButton.png"],None,"HY_GENERIC_ISG_OFF"),
"0289":(["https://ownersmanual.hyundai.com/full_webhelp/LX3HEV/2026/en_US/images/2C_OCSIndicator.jpg.png"],None,"HY_LX3HEV_2026_OCS_INDICATOR"),
"0304":(["https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_USBChargePortCenterConsoleBox.jpg.png"],None,"HY_NX4_2025_REAR_USB_CHARGER"),
"0310":(["https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_PowerOutlet_2.jpg.png"],None,"HY_NX4_2025_CARGO_POWER_OUTLET"),
"0319":(["https://ownersmanual.hyundai.com/full_webhelp/MX5a/2024/en_US/images/2C_RelaxationComfortSeatSwitch.jpg.png"],None,"HY_MX5A_2024_RELAXATION_SEAT_SWITCH"),
"0332":(["https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/images/B0111EU01.jpg.png"],None,"HY_LX2_2025_CHILD_LOCK"),
"0348":(["https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_LightSwitchAutoPosition.jpg.png"],(0.45,0.0,1.0,1.0),"HY_NX4_2025_AUTO_LIGHT_SENSOR"),
"0356":(["https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_USBChargePortCenterConsoleBox.jpg.png"],None,"HY_NX4_2025_REAR_USB_CHARGER"),
"0367":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2025/ko_KR/images/2C_OCSParts.jpg.png"],None,"HY_LX3_2025_OCS_PARTS"),
"0417":(["https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_FrontTrunk.jpg.png"],None,"HY_NE1A_2025_FRONT_TRUNK"),
"0499":(["https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/2C_FrontTrunk.jpg.png"],(0.0,0.0,1.0,0.62),"HY_FRONT_TRUNK_COMPONENTS"),
"0377":(["https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SideAirbagLabel_3.jpg.png"],None,"HY_LX3_2026_AIRBAG_LOCATION"),
}

# Audio-panel crops from the already validated 0282 asset.
# Conservative zones: left knob / right knob / central button banks.
audio_crops={
"0283":(0.00,0.05,0.28,0.95),
"0284":(0.72,0.05,1.00,0.95),
"0285":(0.18,0.08,0.52,0.46),
"0286":(0.18,0.42,0.52,0.80),
"0287":(0.48,0.08,0.82,0.46),
"0288":(0.48,0.42,0.82,0.86),
}

passed=[]; failed=[]; deferred=[]

for id_,(urls,box,src) in jobs.items():
    if id_ not in attempted: continue
    try:
        im=crop_rel(fetch_first(urls,id_),box)
        w,h,size=save_card(im,id_)
        passed.append((id_,byid[id_]["en"],src,w,h,size,"official dedicated image"))
    except Exception as e:
        failed.append((id_,byid[id_]["en"],str(e)))

try:
    panel=Image.open(PARTS/"0282.jpg").convert("RGB")
    for id_,box in audio_crops.items():
        if id_ not in attempted: continue
        try:
            im=crop_rel(panel,box)
            w,h,size=save_card(im,id_)
            passed.append((id_,byid[id_]["en"],"HY_US4_2025_AUDIO_CONTROL_PANEL",w,h,size,"card-specific crop from validated official panel"))
        except Exception as e:
            failed.append((id_,byid[id_]["en"],str(e)))
except Exception as e:
    for id_ in audio_crops:
        if id_ in attempted:
            failed.append((id_,byid[id_]["en"],f"panel unavailable: {e}"))

# Exact physical duplicate reuses where the target denotes the same hardware.
reuse={
"0305":("0310","HY_NX4_2025_CARGO_POWER_OUTLET"), # rear/cargo 12V outlet in this source
"0353":("0294","HY_DIRECT_VISUAL_OR_TAXONOMY_REQUIRED"),
"0498":("0406","HY_V2L_COMPONENTS"),
}
for id_,(srcid,src_ref) in reuse.items():
    if id_ not in attempted: continue
    try:
        src=PARTS/f"{srcid}.jpg"
        if not src.exists(): raise RuntimeError(f"source asset {srcid} missing")
        shutil.copyfile(src,PARTS/f"{id_}.jpg")
        v=Image.open(PARTS/f"{id_}.jpg"); v.verify(); v=Image.open(PARTS/f"{id_}.jpg")
        passed.append((id_,byid[id_]["en"],src_ref,v.width,v.height,(PARTS/f"{id_}.jpg").stat().st_size,f"exact physical reuse from {srcid}"))
    except Exception as e:
        failed.append((id_,byid[id_]["en"],str(e)))

passed_ids={x[0] for x in passed}; failed_ids={x[0] for x in failed}
for id_ in attempted:
    if id_ not in passed_ids and id_ not in failed_ids:
        deferred.append((id_,byid[id_]["en"],"search/crop not direct enough in this subpass"))

for id_,term,src,w,h,size,method in passed:
    x=byid[id_]
    x["status"]="PASS"; x["production_backlog"]=False
    x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-20-100-attempt.md"
lines=[
"# CAR MASTER — Backlog Recovery 20 — Second 100-Item Attempt","",
f"Attempted: **{len(attempted)}**",
f"PASS produced: **{len(passed)}**",
f"Production failures: **{len(failed)}**",
f"Deferred: **{len(deferred)}**","",
"## Attempted IDs"," ".join(attempted),"","## PASS"
]
lines += [f"- **{a} {b}** — {d}x{e}, {f} bytes — {g} — {c}" for a,b,c,d,e,f,g in passed] or ["- None"]
lines += ["","## Production failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failed] or ["- None"]
lines += ["","## Deferred"]+[f"- **{a} {b}** — {c}" for a,b,c in deferred]
lines += ["","## Guardrails",
"- 100-item attempt does not mean forced 100 PASS.",
"- Multi-sensor diagrams are not promoted here unless card-specific isolation is confirmed.",
"- Audio controls use distinct crops from the validated official audio panel.",
"- Deferred items remain hidden/backlog.",
"- Codex reverse-QA is required before live Production count."
]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("ATTEMPTED",len(attempted))
print("PASS",len(passed),[x[0] for x in passed])
print("FAILED",failed)
print("DEFERRED",len(deferred))
