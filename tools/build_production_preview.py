from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"
DL=OUT/"batch-0021-0030-source"
OUT.mkdir(exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

sources={
"0024":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleFrontOverview.jpg.png","LX3 front overview / windshield context"),
"0025":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleRearOverview.jpg.png","LX3 rear overview / rear window context"),
"0026":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_OutsideDoorHandle_3.jpg.png","LX3 outside door handle"),
"0027":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_FrontUltrasonicSensor.jpg.png","NX4 front ultrasonic sensors"),
"0028":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_FrontLampOverveiw.jpg.png","NX4 turn signal lamp overview"),
"0030":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RoofRack.jpg.png","LX3 roof side rails"),
}

cards=[]
for id_,(url,note) in sources.items():
    p=DL/f"{id_}.png"
    try:
        urllib.request.urlretrieve(url,p)
        im=Image.open(p).convert("RGB")
    except Exception as e:
        print("FAILED",id_,e); continue
    t=ImageOps.contain(im,(720,500))
    card=Image.new("RGB",(760,570),"white")
    card.paste(t,((760-t.width)//2,10))
    d=ImageDraw.Draw(card)
    d.text((12,520),f"{id_} — {note}",fill="black")
    d.text((12,542),f"{im.width}x{im.height} | {url.split('/')[-1]}",fill="black")
    cards.append(card)

cols=2; rows=math.ceil(len(cards)/cols)
sheet=Image.new("RGB",(cols*760,rows*570),"white")
for i,c in enumerate(cards): sheet.paste(c,((i%cols)*760,(i//cols)*570))
sheet.save(OUT/"0021-0030-source-contact.jpg",quality=92)
print("downloaded",len(cards),"strong/usable source candidates")
