from pathlib import Path
from PIL import Image, ImageOps
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/"images"/"parts"
PARTS.mkdir(parents=True,exist_ok=True)
tmp=ROOT/"production-preview"/"fix-0122-0124"
tmp.mkdir(parents=True,exist_ok=True)

url="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_TMKOverview.jpg.png"
src=tmp/"tmk-overview.png"
urllib.request.urlretrieve(url,src)
im=Image.open(src).convert("RGB")

def fit(box,path):
    crop=im.crop(box)
    canvas=Image.new("RGB",(800,600),"white")
    thumb=ImageOps.contain(crop,(800,600),method=Image.Resampling.LANCZOS)
    canvas.paste(thumb,((800-thumb.width)//2,(600-thumb.height)//2))
    canvas.save(path,quality=94,subsampling=0)

# Dedicated inset: compressor on left, sealant bottle on right.
fit((385,230,550,420), PARTS/"0122.jpg")
fit((525,220,675,430), PARTS/"0123.jpg")
# Pressure gauge: tight crop of the round dial on the compressor top.
fit((470,275,535,350), PARTS/"0124.jpg")

print("wrote corrected distinct crops for 0122, 0123, 0124")
