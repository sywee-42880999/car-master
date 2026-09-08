from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0321-0370-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

sources={
"0346":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_InsideRearViewMirrorECM.jpg.png","AUTO-DIMMING INSIDE REARVIEW MIRROR","dedicated Hyundai ECM inside-mirror image"),
"0347":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RainSensor.jpg.png","RAIN SENSOR","dedicated Hyundai rain-sensor illustration"),
"0360":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_MultiConsole.jpg.png","OVERHEAD CONSOLE","Hyundai multi/overhead-console module image"),
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
 "First 50-ID validation batch (0321–0370). Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
 "| ID | Status | Term | QA |","|---|---|---|---|"]
 for id_,term,note in passrows:
  st="PASS" if id_ in passed else "REVIEW"
  qa=note if st=="PASS" else "source fetch/validation failed"
  lines.append(f"| {id_} | {st} | {term} | {qa} |")
 for id_,term,note in reviewrows:
  lines.append(f"| {id_} | REVIEW | {term} | {note} |")
 lines += ["","## Handoff","- REVIEW items move to Production Backlog and do not block forward production.","- Do not increment Production progress from this handoff alone."]
 (ROOT/"research"/path).write_text("\n".join(lines)+"\n",encoding="utf-8")

write_result("0321-0330-production-result.md","0321–0330",[],
[("0321","SEAT BELT HEIGHT ADJUSTER","direct labeled close-up not secured"),
("0322","SEAT BELT ANCHOR","anchor hardware not isolated"),
("0323","SEAT BELT TONGUE","direct Hyundai source URL probe failed; defer"),
("0324","SEAT BELT RETRACTOR","hidden mechanism; diagram required"),
("0325","CHILD RESTRAINT ANCHORAGE","umbrella term overlaps existing anchors"),
("0326","TOP TETHER ANCHORAGE","overlap with 0068 TETHER ANCHOR"),
("0327","LOWER ANCHORAGE","overlap with 0069 LATCH LOWER ANCHOR"),
("0328","CHILD RESTRAINT ANCHOR COVER","model-specific trim subcomponent"),
("0329","SEAT BELT BUCKLE RELEASE BUTTON","subcomponent of 0067 buckle"),
("0330","SEAT BELT GUIDE","form/wording varies by seat design")])

write_result("0331-0340-production-result.md","0331–0340",[],
[("0331","DOOR LOCK KNOB","direct labeled close-up not secured"),
("0332","CHILD-PROTECTOR REAR DOOR LOCK","candidate source probe failed; defer"),
("0333","DOOR COURTESY LIGHT","model-specific lamp source required"),
("0334","DOOR POCKET","broad door-trim crop not strong enough"),
("0335","DOOR ARMREST","broad door-trim crop not strong enough"),
("0336","DOOR TRIM","whole trim boundary ambiguous"),
("0337","DOOR SEAL","overlap with 0221 DOOR WEATHERSTRIP"),
("0338","DOOR STRIKER","direct hardware close-up required"),
("0339","DOOR LATCH","direct hardware close-up required"),
("0340","DOOR LOCK ACTUATOR","hidden service component")])

write_result("0341-0350-production-result.md","0341–0350",
[("0346","AUTO-DIMMING INSIDE REARVIEW MIRROR","dedicated Hyundai ECM mirror image"),
("0347","RAIN SENSOR","dedicated Hyundai rain-sensor illustration")],
[("0341","WINDSHIELD WASHER","system/nozzle ambiguity"),
("0342","REAR WINDOW WASHER","system/nozzle ambiguity"),
("0343","WINDSHIELD DEFROSTER","function/system term rather than discrete physical part"),
("0344","REAR WINDOW DEFROSTER","heating element/function source not isolated"),
("0345","HEATED SIDE VIEW MIRROR","heated function not visually separable from mirror"),
("0348","AUTO LIGHT SENSOR","direct verified source not secured"),
("0349","WINDSHIELD CAMERA COVER","camera-cover taxonomy unresolved"),
("0350","MIRROR BASE","subcomponent source not secured")])

write_result("0351-0360-production-result.md","0351–0360",
[("0360","OVERHEAD CONSOLE","Hyundai multi/overhead-console module image")],
[("0351","FRONT USB CHARGER","overlaps existing USB charger entries"),
("0352","12V POWER OUTLET","duplicates 0293/0046 scope"),
("0353","AC POWER OUTLET","equipment-specific"),
("0354","WIRELESS CHARGING PAD","duplicates 0295 physical pad"),
("0355","CENTER CONSOLE USB PORT","location-specific duplicate risk"),
("0356","REAR CONSOLE USB PORT","location-specific duplicate risk"),
("0357","CENTER CONSOLE CUP HOLDER","location-specific duplicate risk"),
("0358","REAR ARMREST CUP HOLDER","location-specific duplicate risk"),
("0359","SUNGLASSES HOLDER","candidate source probe failed; defer")])

write_result("0361-0370-production-result.md","0361–0370",[],
[("0361","SEAT BELT HEIGHT ADJUSTER","duplicate concept with 0321"),
("0362","SEAT BELT ANCHOR","duplicate concept with 0322"),
("0363","SEAT BELT RETRACTOR","hidden mechanism; diagram required"),
("0364","SEAT BELT GUIDE","duplicate concept with 0330"),
("0365","CHILD RESTRAINT TOP TETHER ANCHOR","overlaps 0068/0326"),
("0366","CHILD RESTRAINT LOWER ANCHOR","overlaps 0069/0327"),
("0367","PASSENGER OCCUPANT SENSOR","hidden seat sensor"),
("0368","AIRBAG WARNING LABEL","label taxonomy low priority / source required"),
("0369","FRONT IMPACT SENSOR","hidden crash sensor; technical diagram required"),
("0370","SIDE IMPACT SENSOR","hidden crash sensor; technical diagram required")])

if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0321-0370-final-qa.jpg",quality=92)

for id_ in passed:
 p=PARTS/f"{id_}.jpg"; im=Image.open(p); im.verify()
 im=Image.open(p); w,h=im.size
 if abs((w/h)-(4/3))>0.02: raise RuntimeError(f"{id_} aspect error {w}x{h}")
 if p.stat().st_size<5000: raise RuntimeError(f"{id_} suspiciously small")
if failures: raise RuntimeError("PASS source failures: "+repr(failures))
print("PASS",passed)
print("VALIDATION_OK",True)
