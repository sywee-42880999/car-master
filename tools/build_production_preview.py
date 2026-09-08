from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0291-0320-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

def get(url,name):
 p=DL/name
 if not p.exists(): urllib.request.urlretrieve(url,p)
 return Image.open(p).convert("RGB")

usb_data=get("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_USBPort.jpg.png","usb_data.png")
usb_charge=get("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_USBChargeOutlet.jpg.png","usb_charge.png")
power12=get("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_PowerOutlet_1.jpg.png","power12.png")
wireless=get("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_WirelessSmartPhoneChargingSystem.jpg.png","wireless.png")
seat=get("https://ownersmanual.hyundai.com/full_webhelp/NE1N/2026/en_UK/images/1C_FrontSeatOverview.jpg.png","seat.png")

specs={
"0291":(usb_data,(0,0,1,1),"USB DATA PORT","dedicated Hyundai USB data-port image"),
"0292":(usb_charge,(0,0,1,1),"USB CHARGING PORT","dedicated Hyundai USB charging-outlet image"),
"0293":(power12,(0,0,1,1),"12 V POWER OUTLET","dedicated Hyundai 12 V power-outlet image"),
"0295":(wireless,(0,0,1,1),"WIRELESS CHARGING PAD","dedicated wireless smartphone charging-pad image"),
"0311":(seat,(0.00,0.48,0.28,0.98),"SEAT FORWARD/BACKWARD ADJUSTMENT LEVER","manual seat slide lever identified in Hyundai seat overview"),
"0312":(seat,(0.18,0.45,0.42,0.96),"SEATBACK ANGLE ADJUSTMENT LEVER","manual seatback-angle lever identified in Hyundai seat overview"),
"0313":(seat,(0.28,0.45,0.50,0.96),"SEAT HEIGHT ADJUSTMENT LEVER","manual seat-height lever identified in Hyundai seat overview"),
"0314":(seat,(0.48,0.42,0.78,0.94),"POWER SEAT CONTROL SWITCH","power-seat control switch group identified in Hyundai seat overview"),
"0316":(seat,(0.66,0.42,0.94,0.92),"LUMBAR SUPPORT SWITCH","lumbar-support switch identified in Hyundai seat overview"),
}

def crop4(im,b):
 w,h=im.size;x1,y1,x2,y2=b
 c=im.crop((int(w*x1),int(h*y1),int(w*x2),int(h*y2)))
 cw,ch=c.size
 if cw/ch>4/3:
  nw=int(ch*4/3);x=(cw-nw)//2;c=c.crop((x,0,x+nw,ch))
 else:
  nh=int(cw*3/4);y=max(0,(ch-nh)//2);c=c.crop((0,y,cw,y+nh))
 return c

passed=[];cards=[]
for id_,(im,box,term,note) in specs.items():
 c=crop4(im,box)
 c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
 c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
 passed.append(id_)
 t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
 d=ImageDraw.Draw(card);d.text((12,440),f"{id_} PASS — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)

def write(path,title,passrows,reviewrows):
 lines=[f"# CAR MASTER — {title} Chat Production Result","",
 "30-ID batch 0291–0320. Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
 "| ID | Status | Term | QA |","|---|---|---|---|"]
 for id_,term,note in passrows: lines.append(f"| {id_} | PASS | {term} | {note} |")
 for id_,term,note in reviewrows: lines.append(f"| {id_} | REVIEW | {term} | {note} |")
 lines += ["","## Handoff","- REVIEW items move to Production Backlog and do not block forward production.","- Do not increment Production progress from this handoff alone."]
 (ROOT/"research"/path).write_text("\n".join(lines)+"\n",encoding="utf-8")

write("0291-0300-production-result.md","0291–0300",
[("0291","USB DATA PORT","dedicated Hyundai USB data-port image"),
("0292","USB CHARGING PORT","dedicated Hyundai USB charging-outlet image"),
("0293","12 V POWER OUTLET","dedicated Hyundai 12 V power-outlet image"),
("0295","WIRELESS CHARGING PAD","dedicated Hyundai wireless charging-pad image")],
[("0294","AC POWER OUTLET","equipment/location-specific; direct outlet image not secured"),
("0296","CUP HOLDER INSERT","removable insert terminology unresolved"),
("0297","CENTER CONSOLE ARMREST","direct isolated armrest source not secured"),
("0298","CONSOLE STORAGE LID","overlap with armrest/storage lid"),
("0299","PARKING BRAKE PEDAL","model-specific foot-brake hardware"),
("0300","BRAKE PEDAL","direct isolated Hyundai pedal image not secured")])

write("0301-0310-production-result.md","0301–0310",[],
[("0301","REAR CENTER ARMREST","direct model-specific source not secured"),
("0302","REAR CUP HOLDER","location-specific duplicate risk with 0043"),
("0303","SEATBACK POCKET","direct close-up not secured"),
("0304","REAR USB CHARGER","location-specific duplicate risk"),
("0305","REAR POWER OUTLET","location-specific duplicate risk"),
("0306","CARGO FLOOR","direct labeled cargo-floor source not secured"),
("0307","CARGO FLOOR BOARD","overlap with cargo floor"),
("0308","CARGO SIDE TRIM","direct labeled trim source not secured"),
("0309","CARGO HOOK","direct dedicated Hyundai hook source not secured"),
("0310","CARGO POWER OUTLET","location-specific outlet source not secured")])

write("0311-0320-production-result.md","0311–0320",
[("0311","SEAT FORWARD/BACKWARD ADJUSTMENT LEVER","Hyundai seat overview"),
("0312","SEATBACK ANGLE ADJUSTMENT LEVER","Hyundai seat overview"),
("0313","SEAT HEIGHT ADJUSTMENT LEVER","Hyundai seat overview"),
("0314","POWER SEAT CONTROL SWITCH","Hyundai seat overview"),
("0316","LUMBAR SUPPORT SWITCH","Hyundai seat overview")],
[("0315","SEATBACK ANGLE CONTROL SWITCH","subfunction of power-seat switch; separate-card value unresolved"),
("0317","LEG SUPPORT SWITCH","premium/model-specific"),
("0318","WALK-IN SWITCH","model-specific convenience control"),
("0319","RELAXATION COMFORT SEAT SWITCH","feature/model-specific"),
("0320","HEAD RESTRAINT RELEASE BUTTON","direct dedicated release-button source not secured")])

if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0291-0320-final-qa.jpg",quality=92)

for id_ in passed:
 p=PARTS/f"{id_}.jpg"; im=Image.open(p); im.verify()
 im=Image.open(p); w,h=im.size
 if abs((w/h)-(4/3))>0.02: raise RuntimeError(f"{id_} aspect error {w}x{h}")
 if p.stat().st_size<5000: raise RuntimeError(f"{id_} suspiciously small")
print("PASS",passed)
print("VALIDATION_OK",True)
