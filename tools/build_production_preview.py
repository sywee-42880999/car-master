from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; DL=OUT/"batch-0101-0110-source"
OUT.mkdir(exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

sources={
"NE1N":("https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_US/images/1C_SteeringWheelControlOverview.jpg.png","NE1N steering controls"),
"NE1A":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/1C_SteeringWheelControlOverview.jpg.png","NE1a steering controls"),
"SUNVISOR":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_Sunvisor.jpg.png","LX3 sunvisor"),
"SUNROOF":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SunroofButtonOverview.jpg.png","LX3 sunroof switch"),
}
cards=[]
for key,(url,note) in sources.items():
 p=DL/f"{key}.png"
 try:
  urllib.request.urlretrieve(url,p); im=Image.open(p).convert("RGB")
 except Exception as e:
  print("FAIL",key,e);continue
 t=ImageOps.contain(im,(760,520))
 card=Image.new("RGB",(800,600),"white");card.paste(t,((800-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,545),f"{key} — {note}",fill="black");d.text((12,568),f"{im.width}x{im.height}",fill="black")
 cards.append(card)
cols=1;rows=len(cards)
sheet=Image.new("RGB",(800,rows*600),"white")
for i,c in enumerate(cards): sheet.paste(c,(0,i*600))
sheet.save(OUT/"0101-0110-source-contact.jpg",quality=92)
print("downloaded",len(cards))
