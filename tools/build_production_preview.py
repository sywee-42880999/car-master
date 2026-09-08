from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import math, urllib.request

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "images" / "source"
OUT = ROOT / "production-preview"
OUT.mkdir(exist_ok=True)

# Optional stronger official Hyundai source for 0017.
alt_dir = OUT / "downloaded"
alt_dir.mkdir(exist_ok=True)
alt_0017 = alt_dir / "2C_WideRearCamera.jpg.png"
if not alt_0017.exists():
    url = "https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_US/images/2C_WideRearViewCamera.jpg.png"
    try:
        urllib.request.urlretrieve(url, alt_0017)
    except Exception as e:
        print("0017 alternate unavailable:", e)

specs = {
    "0011": (SRC/"HY_LX3_2026_REAR_OVERVIEW/1C_OutsideVehicleRearOverview.jpg.png", (0.12,0.27,0.55,0.72), "door panel + seams + handle"),
    "0012": (SRC/"HY_LX3_2026_FUEL_DOOR/2C_FuelInletDoor.jpg.png", (0.20,0.06,0.92,0.94), "fuel filler door"),
    "0013": (SRC/"HY_IONIQ5_IN_OFFICIAL_PDF/2C_HowToUseChargingDoor.jpg.png", (0.00,0.02,0.66,0.88), "charging door/flap"),
    "0014": (SRC/"HY_NX4A_2026_REAR_LAMP/2C_RearLampOverview.jpg.png", (0.12,0.00,0.88,0.72), "complete rear lamp housing"),
    "0015": (SRC/"HY_MX5A_2024_REVERSE/2C_BackupLampChange2.jpg.png", (0.08,0.05,0.90,0.92), "backup lamp unit + connector"),
    "0016": (SRC/"HY_LX3_2026_REAR_OVERVIEW/1C_OutsideVehicleRearOverview.jpg.png", (0.43,0.22,0.94,0.80), "liftgate perimeter + rear glass + lower edge"),
    "0017": ((alt_0017 if alt_0017.exists() else SRC/"HY_AXEV_2025_WIDE_REAR_CAMERA/2C_WideRearViewCamera.jpg.png"), (0.30,0.00,0.70,0.52), "rear camera lens/module"),
    "0018": (SRC/"HY_LX3_2026_ANTENNA/2C_Antenna.jpg.png", (0.66,0.24,0.94,0.62), "roof shark-fin antenna"),
    "0019": (SRC/"HY_LX2_2025_REAR_WIPER/B0452KO05.eps.png", (0.00,0.02,0.72,0.92), "rear wiper blade + arm"),
    "0020": (SRC/"HY_NX4_2025_HIGH_STOP/2C_HighMountedStopLamp.jpg.png", (0.12,0.00,0.88,0.74), "high mounted stop lamp + spoiler context"),
}

def crop_norm(im, b):
    w,h=im.size
    x1,y1,x2,y2 = [max(0,min(1,v)) for v in b]
    box=(int(w*x1),int(h*y1),int(w*x2),int(h*y2))
    c=im.crop(box)
    # Center-trim to exact 4:3 without padding.
    cw,ch=c.size
    if cw/ch > 4/3:
        nw=int(ch*4/3); x=(cw-nw)//2; c=c.crop((x,0,x+nw,ch))
    else:
        nh=int(cw*3/4); y=(ch-nh)//2; c=c.crop((0,y,cw,y+nh))
    return c

cards=[]
for id_, (p,b,note) in specs.items():
    if not p.exists():
        print("missing", id_, p); continue
    im=Image.open(p).convert("RGB")
    c=crop_norm(im,b)
    dst=OUT/f"{id_}.jpg"
    c.save(dst,quality=94,subsampling=0)

    thumb=ImageOps.contain(c,(520,390))
    card=Image.new("RGB",(560,460),"white")
    card.paste(thumb,((560-thumb.width)//2,10))
    d=ImageDraw.Draw(card)
    d.text((12,410),f"{id_} — {note}",fill="black")
    d.text((12,432),f"source: {p.name} | crop: {c.size[0]}x{c.size[1]}",fill="black")
    cards.append(card)

cols=2
rows=math.ceil(len(cards)/cols)
sheet=Image.new("RGB",(cols*560,rows*460),"white")
for i,c in enumerate(cards):
    sheet.paste(c,((i%cols)*560,(i//cols)*460))
sheet.save(OUT/"0011-0020-candidates.jpg",quality=91)
print("generated",len(cards),"production candidates")


report = ROOT / "research" / "0011-0020-production-result.md"
lines = [
    "# CAR MASTER — 0011–0020 Re-crop Production Result",
    "",
    "This is the Chat-owned re-crop handoff. Production percentage is **not** changed here.",
    "",
    "PASS means the new 4:3 crop was promoted to `images/parts/<ID>.jpg`. REVIEW means the previous deployed asset must not be trusted and no new crop is promoted yet.",
    "",
    "| ID | Result | Source key | Crop decision |",
    "|---|---|---|---|",
]
for id_ in sorted(specs):
    decision = specs[id_][2]
    lines.append(f"| {id_} | {status[id_]} | {source_keys[id_]} | {decision} |")
lines += [
    "",
    "## REVIEW blockers",
    "- **0017 WIDE-REAR VIEW CAMERA** — current official candidate identifies location, but the physical camera lens/module is still too small/ambiguous for the user's 'unmistakable part' rule. Keep REVIEW; Codex must not mark PASS merely because the page has a callout.",
    "- **0018 ANTENNA** — current 2C_Antenna crop still reads mainly as a roof overview/callout. Find a stronger official Hyundai antenna close-up before replacing the deployed image.",
    "",
    "## Codex handoff",
    "Pull latest main. Verify permanent-ID binding for PASS crops, add HTML overlay only if genuinely needed, keep 0017/0018 in correction state, then perform BLACK UI swipe/mobile QA and Pages deploy. Do not increment Production percentage from this crop commit alone.",
]
report.write_text("\n".join(lines)+"\n", encoding="utf-8")
print("wrote", report)
