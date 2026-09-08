from pathlib import Path
from PIL import Image
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"production-preview";DL=OUT/"batch-0321-0370-probe"
OUT.mkdir(exist_ok=True);DL.mkdir(parents=True,exist_ok=True)

candidates={
"0323":"https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SeatBeltOverview.jpg.png",
"0332":"https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_ChildSafetyLock.jpg.png",
"0346":"https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_InsideRearViewMirrorECM.jpg.png",
"0347":"https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_RainSensor.jpg.png",
"0359":"https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_SunglassHolder.jpg.png",
"0360":"https://ownersmanual.hyundai.com/full_webhelp/LX3/2026/en_US/images/2C_MultiConsole.jpg.png",
}
ok=[];bad=[]
for id_,url in candidates.items():
 p=DL/f"{id_}.png"
 try:
  urllib.request.urlretrieve(url,p)
  im=Image.open(p); im.verify()
  ok.append((id_,url,p.stat().st_size))
 except Exception as e:
  bad.append((id_,str(e)))
print("OK",ok)
print("BAD",bad)
