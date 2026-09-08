from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";DL=OUT/"batch-0141-0150-source"
OUT.mkdir(exist_ok=True);DL.mkdir(parents=True,exist_ok=True)
sources={
"LX3_ENGINE":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_EngineRoom.jpg.png","LX3 2026 Engine Room"),
"LX2_ENGINE":("https://ownersmanual.hyundai.com/full_webhelp/LX2/2025/en_US/images/A0419KO02.jpg.png","LX2 2025 Engine Room"),
"NE1N_MOTOR":("https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_US/images/1C_MotorRoomOverview.jpg.png","NE1N 2026 Motor Room"),
}
cards=[]
for key,(url,note) in sources.items():
 p=DL/f"{key}.png"
 try:
  urllib.request.urlretrieve(url,p);im=Image.open(p).convert("RGB")
 except Exception as e:
  print("FAIL",key,e);continue
 t=ImageOps.contain(im,(900,620))
 card=Image.new("RGB",(940,700),"white");card.paste(t,((940-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,645),f"{key} — {note}",fill="black");d.text((12,668),f"{im.width}x{im.height}",fill="black")
 cards.append(card)
sheet=Image.new("RGB",(940,len(cards)*700),"white")
for i,c in enumerate(cards):sheet.paste(c,(0,i*700))
sheet.save(OUT/"0141-0150-source-contact.jpg",quality=92)
print("downloaded",len(cards))
