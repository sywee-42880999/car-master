from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"; DL=OUT/"batch-0041-0050-source"
OUT.mkdir(exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

sources={
"0041":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_GloveBox.jpg.png","GLOVE BOX"),
"0042":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_CenterConsoleBox.jpg.png","CENTER CONSOLE"),
"0043":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_CupHolder.jpg.png","CUP HOLDER"),
"0044":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_USBPort.jpg.png","USB PORT"),
"0045":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_USBChargeOutlet.jpg.png","USB CHARGER"),
"0046":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_PowerOutlet_1.jpg.png","POWER OUTLET"),
"0047":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_WirelessSmartPhoneChargingSystem.jpg.png","WIRELESS SMARTPHONE CHARGING SYSTEM"),
"0048":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_HazardWarningLamp.jpg.png","HAZARD WARNING FLASHER BUTTON"),
"0049":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_StartButton.jpg.png","ENGINE START/STOP BUTTON"),
"0050":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_ClusterOverview_1.jpg.png","INSTRUMENT CLUSTER"),
}
cards=[]
for id_,(url,term) in sources.items():
    p=DL/f"{id_}.png"
    try:
        urllib.request.urlretrieve(url,p)
        im=Image.open(p).convert("RGB")
    except Exception as e:
        print("FAIL",id_,e); continue
    t=ImageOps.contain(im,(720,500))
    card=Image.new("RGB",(760,570),"white")
    card.paste(t,((760-t.width)//2,10))
    d=ImageDraw.Draw(card)
    d.text((12,520),f"{id_} — {term}",fill="black")
    d.text((12,542),f"{im.width}x{im.height} | {p.name}",fill="black")
    cards.append(card)
cols=2; rows=math.ceil(len(cards)/cols)
sheet=Image.new("RGB",(cols*760,rows*570),"white")
for i,c in enumerate(cards): sheet.paste(c,((i%cols)*760,(i//cols)*570))
sheet.save(OUT/"0041-0050-source-contact.jpg",quality=92)
print("downloaded",len(cards),"sources")
