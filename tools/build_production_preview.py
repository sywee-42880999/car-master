from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"
OUT.mkdir(exist_ok=True)
url="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_SideInsideVehicleOverview.jpg.png"
p=OUT/"0031-0040-overview.png"
urllib.request.urlretrieve(url,p)
im=Image.open(p).convert("RGB")
im.save(OUT/"0031-0040-overview.jpg",quality=94)
print(im.size)
