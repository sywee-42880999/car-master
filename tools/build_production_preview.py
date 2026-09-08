from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import math

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "images" / "source"
OUT = ROOT / "production-preview"
OUT.mkdir(exist_ok=True)

files = sorted([p for p in SRC.rglob("*") if p.is_file() and p.suffix.lower() in {".png",".jpg",".jpeg"}])

thumbs=[]
for p in files:
    try:
        im=Image.open(p).convert("RGB")
    except Exception:
        continue
    # center 4:3 candidate without upscaling
    w,h=im.size
    target=w/h
    if target>4/3:
        nw=int(h*4/3); x=(w-nw)//2; box=(x,0,x+nw,h)
    else:
        nh=int(w*3/4); y=(h-nh)//2; box=(0,y,w,y+nh)
    crop=im.crop(box)
    rel=p.relative_to(ROOT)
    dst=OUT/(str(rel).replace("/","__")+".jpg")
    crop.save(dst,quality=92)

    t=ImageOps.contain(im,(520,360))
    canvas=Image.new("RGB",(560,430),"white")
    canvas.paste(t,((560-t.width)//2,10))
    d=ImageDraw.Draw(canvas)
    label=str(rel)
    d.text((12,380),label,fill="black")
    d.text((12,400),f"{w}x{h}",fill="black")
    thumbs.append(canvas)

if thumbs:
    cols=2
    rows=math.ceil(len(thumbs)/cols)
    sheet=Image.new("RGB",(cols*560,rows*430),"white")
    for i,t in enumerate(thumbs):
        sheet.paste(t,((i%cols)*560,(i//cols)*430))
    sheet.save(OUT/"source-contact-sheet.jpg",quality=90)
print(f"generated {len(thumbs)} previews")
