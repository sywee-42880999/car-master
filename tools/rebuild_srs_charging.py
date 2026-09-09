from PIL import Image, ImageDraw
from pathlib import Path
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"images"/"parts"; OUT.mkdir(parents=True,exist_ok=True)
W,H=800,600
BG=(248,248,246); INK=(34,37,41); MID=(135,140,146); LIGHT=(213,216,220); RED=(205,45,45); WHITE=(255,255,255)

def C():
    im=Image.new("RGB",(W,H),BG); return im,ImageDraw.Draw(im)
def line(d,pts,fill=INK,w=8): d.line(pts,fill=fill,width=w,joint="curve")
def rr(d,box,r=24,fill=None,outline=INK,w=6): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
def el(d,box,fill=None,outline=INK,w=6): d.ellipse(box,fill=fill,outline=outline,width=w)
def save(id_,im):
    p=OUT/f"{id_}.jpg"; im.save(p,quality=95,subsampling=0)

def car_top():
    im,d=C()
    d.rounded_rectangle((135,60,665,540),radius=150,outline=LIGHT,width=8)
    d.rectangle((235,135,565,465),outline=LIGHT,width=5)
    d.line((235,260,565,260),fill=LIGHT,width=4)
    d.line((400,135,400,465),fill=LIGHT,width=4)
    return im,d

def front_impact_sensor():
    im,d=car_top()
    # two real sensor modules near front crash beam
    d.rectangle((245,100,555,140),fill=(198,201,204),outline=INK,width=5)
    for x in (300,500):
        rr(d,(x-34,145,x+34,205),12,fill=RED,outline=INK,w=5)
        d.rectangle((x-12,205,x+12,230),fill=MID,outline=INK,width=3)
    return im

def side_impact_sensor():
    im,d=car_top()
    # B-pillar / side body sensor position
    for x in (205,595):
        rr(d,(x-25,260,x+25,330),10,fill=RED,outline=INK,w=5)
    return im

def srs_control_module():
    im,d=C()
    # tunnel / center-floor mounting context
    d.rectangle((180,170,620,430),outline=LIGHT,width=6)
    d.polygon([(330,160),(470,160),(520,450),(280,450)],fill=(232,233,234),outline=LIGHT)
    rr(d,(305,225,495,360),24,fill=RED,outline=INK,w=7)
    # ECU-like connector blocks
    d.rectangle((330,345,385,390),fill=MID,outline=INK,width=4)
    d.rectangle((415,345,470,390),fill=MID,outline=INK,width=4)
    for x in range(325,485,24): line(d,[(x,245),(x,330)],fill=(235,120,120),w=3)
    return im

def rollover_sensor():
    im,d=C()
    rr(d,(275,170,525,410),35,fill=(210,213,216),outline=INK,w=7)
    el(d,(335,230,465,360),fill=BG,outline=INK,w=6)
    line(d,[(400,295),(455,220)],fill=RED,w=16)
    d.polygon([(455,220),(423,232),(446,255)],fill=RED)
    # mounting tabs
    for x in (305,495): el(d,(x-22,370,x+22,414),fill=MID,outline=INK,w=4)
    return im

def buckle_sensor():
    im,d=C()
    # seat base + buckle with electrical pigtail
    d.rectangle((110,350,690,430),fill=(225,227,229),outline=LIGHT,width=5)
    rr(d,(300,150,500,360),30,fill=(175,178,181),outline=INK,w=7)
    rr(d,(345,190,455,270),18,fill=BG,outline=INK,w=5)
    # sensor housing on buckle side
    rr(d,(470,260,540,335),15,fill=RED,outline=INK,w=5)
    line(d,[(530,330),(640,390)],fill=RED,w=10)
    return im

def pressure_sensor():
    im,d=C()
    # door cavity context
    d.rounded_rectangle((130,100,670,500),radius=45,outline=LIGHT,width=7)
    d.rectangle((170,145,630,455),outline=LIGHT,width=4)
    # pressure sensor on inner door panel
    rr(d,(210,245,315,350),18,fill=RED,outline=INK,w=6)
    el(d,(245,280,280,315),fill=BG,outline=INK,w=4)
    # pressure tube/port
    line(d,[(315,300),(390,300)],fill=RED,w=10)
    return im

def accel_sensor():
    im,d=C()
    # pillar/body mounting location
    d.rectangle((260,100,540,500),outline=LIGHT,width=7)
    rr(d,(330,230,470,360),22,fill=RED,outline=INK,w=6)
    d.rectangle((360,265,440,325),fill=(235,170,170),outline=INK,width=4)
    # directional axes etched on module, not leader lines
    line(d,[(400,295),(495,295)],fill=INK,w=7)
    d.polygon([(495,295),(470,278),(470,312)],fill=INK)
    line(d,[(400,295),(400,195)],fill=INK,w=7)
    d.polygon([(400,195),(383,220),(417,220)],fill=INK)
    return im

def inlet_base():
    im,d=C()
    # actual charging recess + CCS geometry
    rr(d,(140,90,660,510),55,fill=(225,227,229),outline=INK,w=7)
    rr(d,(205,135,595,465),42,fill=(245,245,243),outline=MID,w=5)
    # AC upper section
    el(d,(250,155,550,395),fill=WHITE,outline=INK,w=7)
    holes=[(325,215),(475,215),(285,285),(400,285),(515,285),(350,350),(450,350)]
    for x,y in holes: el(d,(x-18,y-18,x+18,y+18),fill=INK,outline=INK,w=1)
    # DC lower section
    el(d,(290,385,360,455),fill=WHITE,outline=INK,w=6)
    el(d,(440,385,510,455),fill=WHITE,outline=INK,w=6)
    el(d,(312,407,338,433),fill=INK,outline=INK,w=1)
    el(d,(462,407,488,433),fill=INK,outline=INK,w=1)
    return im,d

def charging_inlet():
    im,d=inlet_base()
    rr(d,(205,135,595,465),42,fill=None,outline=RED,w=12)
    return im

def charging_port_cap():
    im,d=inlet_base()
    # cap shown open beside recess
    d.rounded_rectangle((65,150,195,450),radius=50,fill=RED,outline=INK,width=7)
    line(d,[(195,300),(225,300)],fill=INK,w=8)
    return im

def dc_inlet():
    im,d=inlet_base()
    rr(d,(255,370,545,475),26,fill=None,outline=RED,w=14)
    return im

def ac_inlet():
    im,d=inlet_base()
    el(d,(235,145,565,400),fill=None,outline=RED,w=14)
    return im

def connector_lock():
    im,d=inlet_base()
    # locking pin / actuator area above-right of inlet
    rr(d,(545,185,615,270),16,fill=RED,outline=INK,w=6)
    d.arc((555,145,605,205),180,360,fill=INK,width=8)
    return im

jobs={
"0369":front_impact_sensor,
"0370":side_impact_sensor,
"0371":srs_control_module,
"0372":rollover_sensor,
"0373":buckle_sensor,
"0374":pressure_sensor,
"0375":accel_sensor,
"0397":charging_inlet,
"0493":charging_port_cap,
"0494":dc_inlet,
"0495":ac_inlet,
"0496":connector_lock,
}
for id_,fn in jobs.items(): save(id_,fn())
print("rebuilt",len(jobs),sorted(jobs))
