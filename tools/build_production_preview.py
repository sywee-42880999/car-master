from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import urllib.request,re,html as htmlmod,json,shutil

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"backlog-recovery-18"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

PAGE="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/warning_indicator_lights.html"
FONT_URL="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/style/fonts/HYUNDAI_OWNS-Regular.woff"

def get(url,path=None):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r:data=r.read()
    if path: Path(path).write_bytes(data)
    return data

raw=get(PAGE).decode("utf-8","ignore")
pat=re.compile(r'<div class=" title ">\((\d+)\)\s*<userinput(?:\s+outputclass="([^"]*)")?[^>]*>(.*?)</userinput>\s*([^<]+)</div>',re.I|re.S)
entries={}
for num,cls,glyph,label in pat.findall(raw):
    entries[int(num)]={"class":(cls or "").strip(),"glyph":htmlmod.unescape(re.sub(r'<[^>]+>','',glyph)).strip(),"label":' '.join(htmlmod.unescape(label).split())}

woff=DL/"HYUNDAI_OWNS-Regular.woff"; ttf=DL/"HYUNDAI_OWNS-Regular.ttf"
get(FONT_URL,woff); font=TTFont(str(woff)); font.flavor=None; font.save(str(ttf))
iconfont=ImageFont.truetype(str(ttf),220)
colors={"red":(255,70,70),"orange":(255,174,66),"green":(78,220,120),"blue":(90,160,255),"white":(245,245,245),"":(245,245,245)}
bg=(16,18,22)

passed=[]; failures=[]
def render_item(id_,name,itemno,src):
    try:
        e=entries[itemno]; im=Image.new("RGB",(640,480),bg); d=ImageDraw.Draw(im)
        bb=d.textbbox((0,0),e["glyph"],font=iconfont); tw,th=bb[2]-bb[0],bb[3]-bb[1]
        d.text(((640-tw)/2-bb[0],(480-th)/2-bb[1]),e["glyph"],font=iconfont,fill=colors.get(e["class"],(245,245,245)))
        out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
        if out.stat().st_size<5000: raise RuntimeError("small")
        passed.append((id_,name,src,640,480,out.stat().st_size))
    except Exception as ex: failures.append((id_,name,str(ex)))

render_item("0429","AWD WARNING LIGHT",14,"HY_LX3_2026_WARNING_INDICATORS")
render_item("0460","TPMS MALFUNCTION INDICATOR",11,"HY_LX3_2026_TPMS")

# Same physical gauges, alternate master terminology: reuse already validated exact assets.
for id_,srcid,name in [
    ("0418","0467","CHARGE/POWER GAUGE"),
    ("0419","0468","HIGH VOLTAGE BATTERY SOC GAUGE"),
]:
    try:
        src=PARTS/f"{srcid}.jpg"; out=PARTS/f"{id_}.jpg"
        if not src.exists(): raise RuntimeError(f"missing validated source {srcid}")
        shutil.copyfile(src,out); v=Image.open(out); v.verify(); v=Image.open(out)
        passed.append((id_,name,"HY_NE1A_2025_EV_GAUGES_2",v.width,v.height,out.stat().st_size))
    except Exception as ex: failures.append((id_,name,str(ex)))

# Dedicated V2L official images.
for id_,key,name in [
    ("0406","2C_V2LPosition","V2L CONNECTOR"),
    ("0407","2C_V2LInsideIndicator","V2L POWER OUTLET"),
]:
    try:
        url=f"https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/{key}.jpg.png"
        data=get(url,DL/f"{id_}.src"); im=Image.open(DL/f"{id_}.src"); im.verify(); im=Image.open(DL/f"{id_}.src").convert("RGB")
        w,h=im.size
        if w/h>4/3:
            nw=int(h*4/3); x=(w-nw)//2; im=im.crop((x,0,x+nw,h))
        else:
            nh=int(w*3/4); y=(h-nh)//2; im=im.crop((0,y,w,y+nh))
        out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
        v=Image.open(out); v.verify(); v=Image.open(out)
        if out.stat().st_size<5000: raise RuntimeError("small")
        passed.append((id_,name,"HY_NE1A_2025_V2L",v.width,v.height,out.stat().st_size))
    except Exception as ex: failures.append((id_,name,str(ex)))

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
for id_,name,src,w,h,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False; x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[src]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-18.md"
lines=["# CAR MASTER — Backlog Recovery 18","","## PASS"]+[f"- **{a} {b}** — {d}x{e}, {f} bytes, {c}" for a,b,c,d,e,f in passed]
lines += ["","## Failures"]+[f"- **{a} {b}** — {c}" for a,b,c in failures]
lines += ["","## Notes",
"- 0429 uses Hyundai official warning-page item 14 (AWD) via HyundaiOwns font.",
"- 0460 uses Hyundai official low-tire/TPMS symbol; TPMS malfunction uses the same symbol with blinking behavior.",
"- 0418/0419 reuse exact already-validated physical gauge images from 0467/0468 because the master terminology is synonymous.",
"- 0406/0407 use dedicated Hyundai IONIQ 5 V2L official images.",
"- Count live Production only after Codex bind + mobile + reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("PASS",passed); print("FAIL",failures)
