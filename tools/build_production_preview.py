from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";DL=OUT/"batch-0081-0090-source"
OUT.mkdir(exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

sources={
"0081":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_InsideRearViewMirrorDayNight.jpg.png","INSIDE REARVIEW MIRROR"),
"0082":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_DCMInsidemirrorOverview.jpg.png","DIGITAL CENTER MIRROR"),
"0083":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_MapLampLED.jpg.png","MAP LAMP"),
"0084":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RoomLamp.jpg.png","ROOM LAMP"),
"0085":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_PersonalLamp.jpg.png","REAR PERSONAL LAMP"),
"0086":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_MultiConsole.jpg.png","CENTER CONSOLE LAMP"),
"0087":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_MoodLampLED.jpg.png","MOOD LAMP"),
"0088":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SunvisorLampLED.jpg.png","VANITY MIRROR LAMP"),
"0089":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_GloveBoxLamp.jpg.png","GLOVE BOX LAMP"),
"0090":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_LuggageRoomLamp.jpg.png","CARGO AREA LAMP"),
}
cards=[]
for id_,(url,term) in sources.items():
 p=DL/f"{id_}.png"
 try:
  urllib.request.urlretrieve(url,p);im=Image.open(p).convert("RGB")
 except Exception as e:
  print("FAIL",id_,e);continue
 t=ImageOps.contain(im,(720,500))
 card=Image.new("RGB",(760,570),"white");card.paste(t,((760-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,520),f"{id_} — {term}",fill="black");d.text((12,542),f"{im.width}x{im.height}",fill="black")
 cards.append(card)
cols=2;rows=math.ceil(len(cards)/cols)
sheet=Image.new("RGB",(cols*760,rows*570),"white")
for i,c in enumerate(cards):sheet.paste(c,((i%cols)*760,(i//cols)*570))
sheet.save(OUT/"0081-0090-source-contact.jpg",quality=92)
print("downloaded",len(cards))
