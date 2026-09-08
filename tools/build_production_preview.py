from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import urllib.request,math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";PARTS=ROOT/"images"/"parts";DL=OUT/"batch-0231-0260-source"
OUT.mkdir(exist_ok=True);PARTS.mkdir(parents=True,exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

sources={
"0239":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_TowingHook.jpg.png","TOWING EYE COVER","Hyundai removable-towing-hook procedure shows the bumper hole cover and installed hook"),
"0241":("https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SunroofSlideOpen.jpg.png","SUNROOF GLASS","dedicated sunroof slide-open image clearly shows the glass panel"),
"0255":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/1C_AutoAircon.jpg.png","CLIMATE CONTROL PANEL","official automatic climate control system overview"),
"0258":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/1C_AutoAircon.jpg.png","AIR INTAKE CONTROL BUTTON","official climate-control overview labels the air-intake control"),
"0259":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/1C_AutoAircon.jpg.png","FRONT WINDSHIELD DEFROSTER BUTTON","official climate-control overview labels the front windshield defroster"),
"0260":("https://ownersmanual.hyundai.com/full_webhelp/NE1a/2025/en_US/images/1C_AutoAircon.jpg.png","REAR WINDOW DEFROSTER BUTTON","official climate-control overview labels the rear windshield/window defroster"),
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

passed=[]; failures=[]; cards=[]
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

def write_result(path, ids, passmap, reviewmap):
 lines=[f"# CAR MASTER — {ids} Chat Production Result","",
 "30-ID trial batch 0231–0260. Production progress remains unchanged until BLACK UI bind/deploy/mobile reverse-QA is confirmed.","",
 "| ID | Status | Term | QA |","|---|---|---|---|"]
 for id_,term,note in passmap:
  status="PASS" if id_ in passed else "REVIEW"
  qa=note if status=="PASS" else "source download/validation failed"
  lines.append(f"| {id_} | {status} | {term} | {qa} |")
 for id_,term,note in reviewmap:
  lines.append(f"| {id_} | REVIEW | {term} | {note} |")
 lines += ["","## Handoff","- REVIEW items move to Production Backlog and do not block forward production.","- Do not increment Production progress from this handoff alone."]
 (ROOT/"research"/path).write_text("\n".join(lines)+"\n",encoding="utf-8")

write_result("0231-0240-production-result.md","0231–0240",
 [("0239","TOWING EYE COVER","Hyundai towing-hook procedure shows bumper access cover")],
 [("0231","ROOF MOLDING","exact Hyundai labeled source not secured"),
 ("0232","ROOF DRIP MOLDING","overlaps roof molding; source distinction required"),
 ("0233","ROOF SPOILER GARNISH","potential overlap with rear spoiler"),
 ("0234","LIFTGATE GARNISH","direct labeled component image not secured"),
 ("0235","TAILGATE GLASS","likely overlaps 0025 REAR WINDOW"),
 ("0236","LICENSE PLATE GARNISH","model-specific trim naming unresolved"),
 ("0237","FRONT SKID PLATE","protective vs styling taxonomy unresolved"),
 ("0238","REAR SKID PLATE","protective vs styling taxonomy unresolved"),
 ("0240","BUMPER MOLDING","generic model-specific trim term")])

write_result("0241-0250-production-result.md","0241–0250",
 [("0241","SUNROOF GLASS","dedicated Hyundai slide-open image")],
 [("0242","SUNROOF WIND DEFLECTOR","direct labeled Hyundai image not secured"),
 ("0243","SUNROOF DRAIN","technical/service source required"),
 ("0244","ROOF ANTENNA BASE","overlaps 0018 ANTENNA unless separately labeled"),
 ("0245","DOOR GLASS RUN","overlaps window weatherstrip"),
 ("0246","FRONT DOOR FRAME","broad structural term"),
 ("0247","REAR DOOR FRAME","broad structural term"),
 ("0248","LIFTGATE WEATHERSTRIP","direct close-up not secured"),
 ("0249","HOOD WEATHERSTRIP","direct close-up not secured"),
 ("0250","COWL WEATHERSTRIP","overlap with hood seal/cowl unresolved")])

write_result("0251-0260-production-result.md","0251–0260",
 [("0255","CLIMATE CONTROL PANEL","official automatic climate-control overview"),
 ("0258","AIR INTAKE CONTROL BUTTON","official control overview"),
 ("0259","FRONT WINDSHIELD DEFROSTER BUTTON","official control overview"),
 ("0260","REAR WINDOW DEFROSTER BUTTON","official control overview")],
 [("0251","FRONT AIR VENT","dedicated vent close-up not secured in this pass"),
 ("0252","REAR AIR VENT","model-specific vent placement; direct source not secured"),
 ("0253","DEFROSTER VENT","actual outlet not isolated"),
 ("0254","SIDE AIR VENT","overlaps FRONT AIR VENT hierarchy"),
 ("0256","TEMPERATURE CONTROL KNOB","hardware varies by model; knob-specific source required"),
 ("0257","FAN SPEED CONTROL","abstract control wording; hardware-specific taxonomy preferred")])

# QA contact
if cards:
 cols=2;rows=math.ceil(len(cards)/cols);sheet=Image.new("RGB",(cols*600,rows*490),"white")
 for i,c in enumerate(cards):sheet.paste(c,((i%cols)*600,(i//cols)*490))
 sheet.save(OUT/"0231-0260-final-qa.jpg",quality=92)

# machine validation: every PASS file is readable 4:3-ish and non-empty
for id_ in passed:
 p=PARTS/f"{id_}.jpg"; im=Image.open(p); im.verify()
 im=Image.open(p); w,h=im.size
 if abs((w/h)-(4/3))>0.02: raise RuntimeError(f"{id_} not 4:3: {w}x{h}")
 if p.stat().st_size < 5000: raise RuntimeError(f"{id_} suspiciously small")
print("PASS",passed)
print("FAILURES",failures)
print("VALIDATION_OK", len(failures)==0)
