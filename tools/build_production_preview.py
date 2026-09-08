from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import urllib.request, math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview"
DL=OUT/"batch-0021-0030-source"
OUT.mkdir(exist_ok=True); DL.mkdir(parents=True,exist_ok=True)

sources={
"0021":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleFrontOverview.jpg.png",(0.00,0.46,0.58,0.88),"front bumper"),
"0022":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleRearOverview.jpg.png",(0.42,0.48,1.00,0.88),"rear bumper"),
"0023":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleFrontOverview.jpg.png",(0.00,0.38,0.50,0.72),"front grille"),
"0024":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleFrontOverview.jpg.png",(0.27,0.12,0.67,0.48),"windshield"),
"0025":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleRearOverview.jpg.png",(0.58,0.10,0.94,0.46),"rear window"),
"0026":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_OutsideDoorHandle_3.jpg.png",(0.00,0.00,1.00,1.00),"outside door handle"),
"0027":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_FrontUltrasonicSensor.jpg.png",(0.00,0.25,0.76,0.88),"front ultrasonic / parking sensors"),
"0028":("https://ownersmanual.hyundai.com/full_webhelp/NX4/2025/en_GN/images/2C_FrontLampOverveiw.jpg.png",(0.00,0.00,0.80,0.78),"turn signal light region"),
"0029":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/1C_OutsideVehicleRearOverview.jpg.png",(0.60,0.02,1.00,0.30),"rear spoiler"),
"0030":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RoofRack.jpg.png",(0.00,0.00,1.00,1.00),"roof side rails"),
}

def ensure(url,id_):
    p=DL/f"{id_}.png"
    if not p.exists():
        urllib.request.urlretrieve(url,p)
    return p

def crop4(im,b):
    w,h=im.size
    x1,y1,x2,y2=b
    c=im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))
    cw,ch=c.size
    if cw/ch>4/3:
        nw=int(ch*4/3); x=(cw-nw)//2; c=c.crop((x,0,x+nw,ch))
    else:
        nh=int(cw*3/4); y=(ch-nh)//2; c=c.crop((0,y,cw,y+nh))
    return c

cards=[]
for id_,(url,b,note) in sources.items():
    try:
        im=Image.open(ensure(url,id_)).convert("RGB")
    except Exception as e:
        print("FAIL",id_,e); continue
    c=crop4(im,b)
    c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
    t=ImageOps.contain(c,(560,420))
    card=Image.new("RGB",(600,490),"white")
    card.paste(t,((600-t.width)//2,10))
    d=ImageDraw.Draw(card)
    d.text((12,440),f"{id_} — {note}",fill="black")
    d.text((12,462),f"{c.width}x{c.height}",fill="black")
    cards.append(card)

cols=2; rows=math.ceil(len(cards)/cols)
sheet=Image.new("RGB",(cols*600,rows*490),"white")
for i,c in enumerate(cards): sheet.paste(c,((i%cols)*600,(i//cols)*490))
sheet.save(OUT/"0021-0030-crop-candidates.jpg",quality=92)
print("generated",len(cards),"crop candidates")
