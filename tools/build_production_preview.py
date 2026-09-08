from pathlib import Path
from PIL import Image
import urllib.request
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; OUT.mkdir(exist_ok=True)
url="https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_CenterInsideVehicleOverview.jpg.png"
p=OUT/"0051-0060-overview.png"
urllib.request.urlretrieve(url,p)
im=Image.open(p).convert("RGB")
im.save(OUT/"0051-0060-overview.jpg",quality=94)
print(im.size)
