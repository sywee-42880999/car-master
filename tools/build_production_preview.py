from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import urllib.request, re, html as htmlmod, json

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"; OUT=ROOT/"production-preview"; DL=OUT/"warning-icons-batch-17"
PARTS.mkdir(parents=True,exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

PAGE="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/warning_indicator_lights.html"
FONT_URL="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/style/fonts/HYUNDAI_OWNS-Regular.woff"
SRC="HY_LX3_2026_WARNING_INDICATORS"

targets={
"0390":"Airbag warning light",
"0391":"Seat belt warning light",
"0392":"Parking brake & Brake fluid warning light",
"0393":"Anti-lock Brake System (ABS) warning light",
"0394":"Electronic Stability Control (ESC) indicator light",
"0395":"Master warning light",
"0421":"Motor Driven Power Steering (MDPS) warning light",
"0422":"Low fuel level warning light",
"0423":"Engine oil pressure warning light",
"0424":"Malfunction Indicator Lamp (MIL)",
"0425":"12 V Battery Charging system warning light",
"0426":"Low tire pressure warning light",
"0427":"Electronic Parking Brake (EPB) warning light",
"0428":"AUTO HOLD indicator light",
"0429":"AWD warning light",
"0430":"Forward Safety warning light",
"0431":"Emergency steering warning light",
"0432":"Lane Safety indicator light",
"0433":"Lane Following Assist (LFA) indicator light",
"0434":"Speed limiter indicator light",
"0435":"Intelligent Speed Limit Assist (ISLA) indicator light",
"0436":"Inattentive driving warning light",
"0437":"Forward Attention Warning light",
"0438":"LED headlight warning light",
"0439":"Downhill Brake Control (DBC) indicator light",
"0440":"Electronic Stability Control (ESC) indicator light",
"0441":"Electronic Stability Control (ESC) OFF indicator light",
"0442":"Immobilizer indicator light",
"0443":"Low beam indicator light",
"0444":"High beam indicator light",
"0445":"High Beam Assist (HBA) indicator light",
}

def get(url,path=None):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as r: data=r.read()
    if path: Path(path).write_bytes(data)
    return data

raw=get(PAGE).decode("utf-8","ignore")
# Parse official title entries: number + userinput glyph + visible label
entries=[]
pat=re.compile(r'<div class=" title ">\((\d+)\)\s*<userinput(?:\s+outputclass="([^"]*)")?[^>]*>(.*?)</userinput>\s*([^<]+)</div>',re.I|re.S)
for num,cls,glyph,label in pat.findall(raw):
    entries.append({
        "num":int(num),
        "class":(cls or "").strip(),
        "glyph":htmlmod.unescape(re.sub(r'<[^>]+>','',glyph)).strip(),
        "label":' '.join(htmlmod.unescape(label).split())
    })

woff=DL/"HYUNDAI_OWNS-Regular.woff"; ttf=DL/"HYUNDAI_OWNS-Regular.ttf"
get(FONT_URL,woff)
font=TTFont(str(woff)); font.flavor=None; font.save(str(ttf))

def norm(s):
    return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()

colors={
    "red":(255,70,70),
    "orange":(255,174,66),
    "green":(78,220,120),
    "blue":(90,160,255),
    "white":(245,245,245),
    "":(245,245,245),
}
bg=(16,18,22)
iconfont=ImageFont.truetype(str(ttf),220)
passed=[]; failures=[]; mapping=[]
for id_,wanted in targets.items():
    try:
        wn=norm(wanted)
        # exact normalized first, then containment
        cand=[e for e in entries if norm(e["label"])==wn]
        if not cand:
            cand=[e for e in entries if wn in norm(e["label"]) or norm(e["label"]) in wn]
        if not cand:
            raise RuntimeError("label not found")
        e=cand[0]
        if not e["glyph"]:
            raise RuntimeError("empty glyph")
        im=Image.new("RGB",(640,480),bg); d=ImageDraw.Draw(im)
        bbox=d.textbbox((0,0),e["glyph"],font=iconfont)
        tw,th=bbox[2]-bbox[0],bbox[3]-bbox[1]
        col=colors.get(e["class"],(245,245,245))
        d.text(((640-tw)/2-bbox[0],(480-th)/2-bbox[1]),e["glyph"],font=iconfont,fill=col)
        out=PARTS/f"{id_}.jpg"; im.save(out,quality=95,subsampling=0)
        v=Image.open(out); v.verify()
        if out.stat().st_size<5000: raise RuntimeError("small file")
        passed.append((id_,wanted,e["num"],e["glyph"],e["class"],out.stat().st_size))
        mapping.append((id_,wanted,e["label"],e["num"],e["glyph"],e["class"]))
    except Exception as ex:
        failures.append((id_,wanted,str(ex)))

mf=ROOT/"data"/"master.json"; master=json.loads(mf.read_text(encoding="utf-8"))
items=master.get("items",master.get("entries",master if isinstance(master,list) else [])); byid={x["id"]:x for x in items}
for id_,wanted,num,glyph,cls,size in passed:
    x=byid[id_]; x["status"]="PASS"; x["production_backlog"]=False
    x["image"]=f"images/parts/{id_}.jpg"; x["source_refs"]=[SRC]
mf.write_text(json.dumps(master,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

rf=ROOT/"research"/"backlog-recovery-17-warning-icons.md"
lines=["# CAR MASTER — Backlog Recovery 17 / Hyundai Warning Icons","",
"Method: parse Hyundai official warning-light page, map each official label to its HyundaiOwns glyph/color class, convert Hyundai official WOFF to TTF, and render one 4:3 learning card per icon.","",
"## PASS"]
lines += [f"- **{id_} {name}** — official item ({num}), glyph `{glyph}`, class `{cls or 'default'}`, {size} bytes" for id_,name,num,glyph,cls,size in passed] or ["- None"]
lines += ["","## Failures"]
lines += [f"- **{id_} {name}** — {err}" for id_,name,err in failures] or ["- None"]
lines += ["","## Reverse-QA",
"- Each image is generated from Hyundai's official warning-page glyph rendered with Hyundai's official HyundaiOwns font.",
"- The card contains only the target icon on a dark field; no generic cluster screenshot is reused.",
"- 0394 and 0440 intentionally map to the same official ESC symbol because the master contains both warning/indicator terminology variants.",
"- Count live Production only after Codex bind + mobile + reverse-QA."]
rf.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("ENTRIES",len(entries)); print("PASS",len(passed),[x[0] for x in passed]); print("FAIL",failures)
