from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0291-0320-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

sources={
"0291":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_USBPort.jpg.png","USB DATA PORT","dedicated Hyundai USB port image"),
"0292":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_USBChargeOutlet.jpg.png","USB CHARGING PORT","dedicated Hyundai USB charging outlet image"),
"0293":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_PowerOutlet_1.jpg.png","12 V POWER OUTLET","dedicated Hyundai power-outlet image"),
"0295":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_WirelessSmartPhoneChargingSystem.jpg.png","WIRELESS CHARGING PAD","dedicated Hyundai wireless-charging surface image"),
}

def fetch(url,id_):
 p=DL/f"{id_}.png"
 if not p.exists(): urllib.request.urlretrieve(url,p)
 return Image.open(p).convert("RGB")

def crop4(im):
 w,h=im.size
 if w/h>4/3:
  nw=int(h*4/3);x=(w-nw)//2;return im.crop((x,0,x+nw,h))
 nh=int(w*3/4);y=(h-nh)//2;return im.crop((0,y,w,y+nh))

passed=[];cards=[];failures=[]
for id_,(url,term,note) in sources.items():
 try:
  c=crop4(fetch(url,id_))
  c.save(OUT/f"{id_}.jpg",quality=94,subsampling=0)
  c.save(PARTS/f"{id_}.jpg",quality=94,subsampling=0)
  passed.append(id_)
  t=ImageOps.contain(c,(560,420));card=Image.new("RGB",(600,490),"white");card.paste(t,((600-t.width)//2,10))
  d=ImageDraw.Draw(card);d.text((12,440),f"{id_} PASS — {term}",fill="black");d.text((12,462),note,fill="black");cards.append(card)
 except Exception as e:
  failures.append((id_,str(e)))

def write_result(path,title,passrows,reviewrows):
 lines=[f"# CAR MASTER — {title} Chat Production Result","",
 "Third 30-ID validation batch. Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
 "| ID | Status | Term | QA |","|---|---|---|---|"]
 for id_,term,note in passrows:
  st="PASS" if id_ in passed else "REVIEW"
  qa=note if st=="PASS" else "source fetch/validation failed"
  lines.append(f"| {id_} | {st} | {term} | {qa} |")
 for id_,term,note in reviewrows:
  lines.append(f"| {id_} | REVIEW | {term} | {note} |")
 lines += ["","## Handoff","- REVIEW items move to Production Backlog and do not block forward production.","- Do not increment Production progress from this handoff alone."]
 (ROOT/"research"/path).write_text("\n".join(lines)+"\n",encoding="utf-8")

write_result("0291-0300-production-result.md","0291–0300",
[("0291","USB DATA PORT","dedicated Hyundai USB port image"),
 ("0292","USB CHARGING PORT","dedicated Hyundai USB charging outlet image"),
 ("0293","12 V POWER OUTLET","dedicated Hyundai power outlet image"),
 ("0295","WIRELESS CHARGING PAD","dedicated Hyundai wireless charging surface image")],
[("0294","AC POWER OUTLET","equipment-specific; exact outlet image not secured"),
 ("0296","CUP HOLDER INSERT","removable insert terminology unresolved"),
 ("0297","CENTER CONSOLE ARMREST","direct Hyundai armrest/lid close-up not secured"),
 ("0298","CONSOLE STORAGE LID","overlap with center-console armrest/lid"),
 ("0299","PARKING BRAKE PEDAL","legacy/model-specific foot-brake hardware"),
 ("0300","BRAKE PEDAL","direct isolated official pedal image not secured")])

write_result("0301-0310-production-result.md","0301–0310",[],
[("0301","REAR CENTER ARMREST","direct official close-up not secured"),
 ("0302","REAR CUP HOLDER","location-specific duplicate risk vs 0043"),
 ("0303","SEATBACK POCKET","direct official close-up not secured"),
 ("0304","REAR USB CHARGER","location-specific overlap with USB charger taxonomy"),
 ("0305","REAR POWER OUTLET","location-specific overlap with 0046"),
 ("0306","CARGO FLOOR","direct unmistakable official crop not secured"),
 ("0307","CARGO FLOOR BOARD","possible overlap with cargo floor"),
 ("0308","CARGO SIDE TRIM","broad interior trim component"),
 ("0309","CARGO HOOK","direct close-up not secured"),
 ("0310","CARGO POWER OUTLET","location-specific overlap with generic power outlet")])

write_result("0311-0320-production-result.md","0311–0320",[],
[("0311","SEAT FORWARD/BACKWARD ADJUSTMENT LEVER","manual-seat specific source required"),
 ("0312","SEATBACK ANGLE ADJUSTMENT LEVER","manual-seat specific source required"),
 ("0313","SEAT HEIGHT ADJUSTMENT LEVER","manual-seat specific source required"),
 ("0314","POWER SEAT CONTROL SWITCH","direct labeled switch close-up not secured"),
 ("0315","SEATBACK ANGLE CONTROL SWITCH","subfunction overlap with power seat control"),
 ("0316","LUMBAR SUPPORT SWITCH","direct labeled switch image not secured"),
 ("0317","LEG SUPPORT SWITCH","premium/model-specific"),
 ("0318","WALK-IN SWITCH","model-specific convenience feature"),
 ("0319","RELAXATION COMFORT SEAT SWITCH","feature/model-specific"),
 ("0320","HEAD RESTRAINT RELEASE BUTTON","direct close-up not secured")])

if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0291-0320-final-qa.jpg",quality=92)

for id_ in passed:
 p=PARTS/f"{id_}.jpg"; im=Image.open(p); im.verify()
 im=Image.open(p); w,h=im.size
 if abs((w/h)-(4/3))>0.02: raise RuntimeError(f"{id_} aspect error {w}x{h}")
 if p.stat().st_size<5000: raise RuntimeError(f"{id_} suspiciously small")

if failures: raise RuntimeError("PASS source failures: "+repr(failures))
print("PASS",passed)
print("VALIDATION_OK",True)
