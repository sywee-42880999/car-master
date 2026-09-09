from PIL import Image, ImageDraw
from pathlib import Path
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"images"/"parts"; OUT.mkdir(parents=True,exist_ok=True)
W,H=800,600
BG=(248,248,246); INK=(35,38,42); MID=(135,140,145); LIGHT=(210,214,218); RED=(205,45,45); WHITE=(255,255,255)

def canvas():
    im=Image.new("RGB",(W,H),BG); return im,ImageDraw.Draw(im)

def line(d,pts,fill=INK,w=8):
    d.line(pts,fill=fill,width=w,joint="curve")

def ellipse(d,box,fill=None,outline=INK,w=6):
    d.ellipse(box,fill=fill,outline=outline,width=w)

def rr(d,box,r=20,fill=None,outline=INK,w=6):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)

def save(id_, im):
    p=OUT/f"{id_}.jpg"; im.save(p,quality=95,subsampling=0)

def underbody_base():
    im,d=canvas()
    d.rounded_rectangle((80,120,720,475),radius=110,outline=LIGHT,width=8)
    d.rectangle((180,165,620,430),outline=LIGHT,width=5)
    for x in (150,650):
        ellipse(d,(x-55,385,x+55,495),fill=None,outline=MID,w=8)
    return im,d

def engine_oil_filter():
    im,d=canvas()
    # detailed spin-on filter
    d.rounded_rectangle((250,120,550,470),radius=55,fill=(215,218,220),outline=INK,width=8)
    d.rectangle((280,165,520,410),fill=(232,234,235),outline=INK,width=6)
    for y in range(190,390,28): line(d,[(300,y),(500,y)],fill=MID,w=4)
    d.ellipse((290,80,510,190),fill=(180,184,188),outline=INK,width=7)
    for a in range(0,360,45):
        cx=400+int(60*math.cos(math.radians(a))); cy=135+int(35*math.sin(math.radians(a)))
        ellipse(d,(cx-9,cy-9,cx+9,cy+9),fill=INK,outline=INK,w=1)
    ellipse(d,(365,105,435,165),fill=BG,outline=INK,w=5)
    return im

def drive_belt():
    im,d=canvas()
    pts=[(260,190),(540,180),(585,330),(475,445),(260,410),(205,300),(260,190)]
    line(d,pts,fill=RED,w=22)
    for x,y,r in [(270,210,70),(525,210,55),(545,340,65),(430,415,65),(270,390,55),(220,300,45)]:
        ellipse(d,(x-r,y-r,x+r,y+r),fill=(226,228,230),outline=INK,w=7)
        ellipse(d,(x-r//2,y-r//2,x+r//2,y+r//2),fill=BG,outline=MID,w=5)
    return im

def spark_plug():
    im,d=canvas()
    rr(d,(330,65,470,180),25,fill=(210,212,214),outline=INK,w=7)
    for y in range(80,170,18): line(d,[(342,y),(458,y)],fill=MID,w=3)
    d.polygon([(315,185),(485,185),(455,285),(345,285)],fill=(190,193,196),outline=INK)
    rr(d,(350,280,450,460),12,fill=(240,240,236),outline=INK,w=6)
    for y in range(305,435,18): line(d,[(360,y),(440,y)],fill=MID,w=3)
    line(d,[(400,460),(400,525)],fill=INK,w=12)
    line(d,[(400,525),(455,525)],fill=INK,w=12)
    d.arc((420,475,505,555),180,290,fill=RED,width=10)
    return im

def fuel_tank():
    im,d=underbody_base()
    d.rounded_rectangle((240,245,560,390),radius=55,fill=RED,outline=INK,width=7)
    d.rectangle((520,220,610,255),fill=MID,outline=INK,width=5)
    line(d,[(610,237),(665,205)],fill=MID,w=8)
    return im

def small_filter(kind="fuel"):
    im,d=canvas()
    if kind=="air":
        rr(d,(280,155,520,390),38,fill=(220,223,225),outline=INK,w=7)
        for x in (320,400,480): ellipse(d,(x-18,190,x+18,226),fill=BG,outline=INK,w=5)
        line(d,[(240,205),(280,205)],fill=MID,w=10); line(d,[(520,205),(580,205)],fill=MID,w=10)
        d.rectangle((330,260,470,335),fill=RED,outline=INK,width=5)
    else:
        rr(d,(315,135,485,430),30,fill=(215,218,220),outline=INK,w=7)
        for y in range(180,390,30): line(d,[(335,y),(465,y)],fill=MID,w=3)
        line(d,[(265,180),(315,180)],fill=INK,w=12); line(d,[(485,350),(545,350)],fill=INK,w=12)
    return im

def brake_line(hose=False):
    im,d=underbody_base()
    if not hose:
        pts=[(145,245),(250,250),(360,320),(505,318),(640,250)]
        line(d,pts,fill=RED,w=13)
        for x,y in pts[1:-1]: ellipse(d,(x-10,y-10,x+10,y+10),fill=RED,outline=RED,w=1)
    else:
        line(d,[(575,265),(620,310)],fill=MID,w=9)
        # flexible ribbed hose
        for i in range(8):
            x=620+i*8; y=310+i*12
            line(d,[(x-10,y),(x+10,y)],fill=RED,w=6)
        line(d,[(680,405),(690,430)],fill=RED,w=10)
    return im

def brake_part(which):
    im,d=canvas()
    # rotor/caliper assembly context
    ellipse(d,(210,90,590,470),fill=(225,227,229),outline=INK,w=8)
    ellipse(d,(290,170,510,390),fill=BG,outline=MID,w=7)
    ellipse(d,(365,245,435,315),fill=(190,193,196),outline=INK,w=6)
    for a in range(0,360,60):
        cx=400+int(80*math.cos(math.radians(a))); cy=280+int(80*math.sin(math.radians(a)))
        ellipse(d,(cx-8,cy-8,cx+8,cy+8),fill=MID,outline=MID,w=1)
    # caliper and pads
    rr(d,(515,175,650,365),28,fill=(180,183,186),outline=INK,w=7)
    rr(d,(485,205,525,335),10,fill=(120,123,126),outline=INK,w=5)
    if which=="disc":
        ellipse(d,(210,90,590,470),fill=None,outline=RED,w=18)
    elif which=="caliper":
        rr(d,(515,175,650,365),28,fill=RED,outline=INK,w=7)
    elif which=="pad":
        rr(d,(485,205,525,335),10,fill=RED,outline=INK,w=5)
    return im

def steering_rack(which="rack"):
    im,d=canvas()
    # rack housing
    rr(d,(185,250,615,350),35,fill=(210,213,215),outline=INK,w=7)
    # tie rods
    line(d,[(115,300),(185,300)],fill=MID,w=12); line(d,[(615,300),(685,300)],fill=MID,w=12)
    # boots
    for base in (175,585):
        for i in range(5):
            x=base+i*8 if base<300 else base-i*8
            d.ellipse((x-24,265,x+24,335),outline=INK,width=4)
    if which=="rack":
        rr(d,(245,270,555,330),18,fill=RED,outline=INK,w=5)
    elif which=="boot":
        for i in range(5):
            x=175+i*8
            d.ellipse((x-24,265,x+24,335),outline=RED,width=7)
    elif which=="linkage":
        line(d,[(115,300),(185,300)],fill=RED,w=16); line(d,[(615,300),(685,300)],fill=RED,w=16)
        ellipse(d,(85,270,125,310),fill=RED,outline=INK,w=4); ellipse(d,(675,270,715,310),fill=RED,outline=INK,w=4)
    return im

def driveshaft(boot=False):
    im,d=canvas()
    line(d,[(170,300),(630,300)],fill=(165,168,171),w=36)
    ellipse(d,(130,250,220,350),fill=(190,193,196),outline=INK,w=7)
    ellipse(d,(580,250,670,350),fill=(190,193,196),outline=INK,w=7)
    for x in range(210,275,12): d.ellipse((x-20,265,x+20,335),outline=INK,width=4)
    for x in range(525,590,12): d.ellipse((x-20,265,x+20,335),outline=INK,width=4)
    if boot:
        for x in range(210,275,12): d.ellipse((x-20,265,x+20,335),outline=RED,width=7)
    else:
        line(d,[(285,300),(515,300)],fill=RED,w=40)
    return im

def ball_joint():
    im,d=canvas()
    d.polygon([(150,390),(360,260),(620,390),(575,440),(350,335),(200,445)],fill=(220,222,224),outline=INK)
    ellipse(d,(320,235,390,305),fill=RED,outline=INK,w=6)
    line(d,[(355,235),(355,170)],fill=RED,w=14)
    return im

def propeller():
    im,d=underbody_base()
    line(d,[(250,300),(575,300)],fill=RED,w=24)
    ellipse(d,(330,265,380,335),fill=(190,193,196),outline=INK,w=5)
    ellipse(d,(520,260,585,340),fill=(190,193,196),outline=INK,w=5)
    return im

def differential(front=True):
    im,d=underbody_base()
    y=260 if front else 390
    x=260 if front else 540
    ellipse(d,(x-70,y-55,x+70,y+55),fill=RED,outline=INK,w=7)
    line(d,[(x-120,y),(x-70,y)],fill=MID,w=12); line(d,[(x+70,y),(x+120,y)],fill=MID,w=12)
    return im

def transfer_case():
    im,d=underbody_base()
    rr(d,(340,260,470,360),28,fill=RED,outline=INK,w=7)
    line(d,[(405,260),(405,190)],fill=MID,w=12); line(d,[(470,310),(570,370)],fill=MID,w=12)
    return im

def suspension(front=True):
    im,d=canvas()
    wheelx=230 if front else 570
    ellipse(d,(wheelx-95,195,wheelx+95,385),fill=None,outline=MID,w=9)
    # strut and spring
    line(d,[(wheelx,120),(wheelx,315)],fill=INK,w=14)
    for i in range(8):
        y=145+i*20
        d.arc((wheelx-55,y,wheelx+55,y+36),0,180,fill=RED,width=8)
    # control arm
    d.polygon([(wheelx-120,365),(wheelx,315),(wheelx+115,375),(wheelx+70,410),(wheelx,350),(wheelx-75,410)],fill=RED,outline=INK)
    return im

def shock_or_strut(strut=False):
    im,d=canvas()
    if strut:
        line(d,[(400,90),(400,475)],fill=INK,w=18)
        rr(d,(340,280,460,455),22,fill=(190,193,196),outline=INK,w=6)
        for i in range(8):
            y=130+i*24
            d.arc((325,y,475,y+55),0,180,fill=RED,width=9)
        ellipse(d,(320,70,480,140),fill=(210,213,215),outline=INK,w=6)
    else:
        line(d,[(400,80),(400,230)],fill=INK,w=16)
        rr(d,(350,220,450,500),28,fill=RED,outline=INK,w=7)
        ellipse(d,(365,485,435,555),fill=BG,outline=INK,w=7)
    return im

def coil():
    im,d=canvas()
    for i in range(11):
        y=90+i*38
        d.arc((260,y,540,y+90),0,180,fill=RED,width=13)
        d.arc((260,y+20,540,y+110),180,360,fill=RED,width=13)
    return im

def stabilizer_bar():
    im,d=canvas()
    pts=[(130,350),(180,300),(270,290),(400,360),(530,290),(620,300),(670,350)]
    line(d,pts,fill=RED,w=22)
    for x in (180,620): rr(d,(x-25,265,x+25,335),15,fill=(190,193,196),outline=INK,w=5)
    return im

def control_arm(upper=False):
    im,d=canvas()
    if upper:
        pts=[(170,260),(400,360),(630,260),(565,205),(400,285),(235,205)]
    else:
        pts=[(150,390),(400,245),(650,390),(590,445),(400,330),(210,445)]
    d.polygon(pts,fill=RED,outline=INK)
    for x,y in [(pts[0][0],pts[0][1]),(pts[2][0],pts[2][1]),(400,300 if upper else 290)]:
        ellipse(d,(x-30,y-30,x+30,y+30),fill=BG,outline=INK,w=6)
    return im

def tie_rod():
    im,d=canvas()
    line(d,[(180,300),(560,300)],fill=(180,183,186),w=24)
    rr(d,(510,250,650,350),35,fill=RED,outline=INK,w=7)
    ellipse(d,(610,220,690,300),fill=RED,outline=INK,w=7)
    line(d,[(650,255),(650,180)],fill=RED,w=14)
    return im

def hub_or_bearing(bearing=False):
    im,d=canvas()
    ellipse(d,(220,120,580,480),fill=(220,222,224),outline=INK,w=8)
    ellipse(d,(285,185,515,415),fill=RED if bearing else (190,193,196),outline=INK,w=7)
    ellipse(d,(345,245,455,355),fill=BG,outline=INK,w=7)
    for a in range(0,360,72):
        cx=400+int(85*math.cos(math.radians(a))); cy=300+int(85*math.sin(math.radians(a)))
        ellipse(d,(cx-12,cy-12,cx+12,cy+12),fill=RED if not bearing else MID,outline=INK,w=3)
    return im

def mount():
    im,d=canvas()
    ellipse(d,(250,140,550,430),fill=RED,outline=INK,w=8)
    ellipse(d,(330,220,470,360),fill=BG,outline=INK,w=7)
    for a in (30,150,270):
        cx=400+int(105*math.cos(math.radians(a))); cy=285+int(105*math.sin(math.radians(a)))
        ellipse(d,(cx-16,cy-16,cx+16,cy+16),fill=INK,outline=INK,w=1)
    return im

def stabilizer_link():
    im,d=canvas()
    line(d,[(330,140),(470,460)],fill=RED,w=22)
    ellipse(d,(285,95,375,185),fill=RED,outline=INK,w=7)
    ellipse(d,(425,415,515,505),fill=RED,outline=INK,w=7)
    return im

def knuckle():
    im,d=canvas()
    d.polygon([(310,110),(480,165),(540,305),(460,480),(290,430),(240,275)],fill=RED,outline=INK)
    ellipse(d,(320,220,460,360),fill=BG,outline=INK,w=8)
    for x,y in [(300,160),(495,220),(455,430)]: ellipse(d,(x-18,y-18,x+18,y+18),fill=INK,outline=INK,w=1)
    return im

def frame_part(kind):
    im,d=underbody_base()
    if kind=="subframe":
        pts=[(200,255),(310,210),(490,210),(600,255),(550,365),(250,365)]
        d.polygon(pts,fill=RED,outline=INK)
    elif kind=="crossmember":
        rr(d,(180,310,620,355),18,fill=RED,outline=INK,w=6)
    elif kind=="undercover":
        d.polygon([(190,205),(610,205),(660,390),(140,390)],fill=RED,outline=INK)
    elif kind=="mudguard":
        d.arc((80,325,280,525),190,350,fill=RED,width=28)
        d.arc((520,325,720,525),190,350,fill=RED,width=28)
    return im

def washer(rear=False):
    im,d=canvas()
    if rear:
        d.polygon([(160,180),(640,180),(690,420),(110,420)],fill=(230,232,233),outline=LIGHT)
        rr(d,(360,190,440,245),18,fill=RED,outline=INK,w=6)
        line(d,[(400,245),(400,330)],fill=MID,w=4)
    else:
        d.polygon([(150,220),(650,220),(610,430),(190,430)],fill=(230,232,233),outline=LIGHT)
        for x in (315,485):
            rr(d,(x-35,230,x+35,275),14,fill=RED,outline=INK,w=5)
            d.arc((x-70,170,x+70,310),210,330,fill=MID,width=3)
    return im

jobs={
"0151":engine_oil_filter,
"0152":drive_belt,
"0153":spark_plug,
"0155":fuel_tank,
"0156":lambda:small_filter("air"),
"0157":lambda:small_filter("fuel"),
"0158":lambda:brake_line(False),
"0159":lambda:brake_line(True),
"0160":lambda:brake_part("pad"),
"0161":lambda:brake_part("disc"),
"0162":lambda:brake_part("caliper"),
"0163":lambda:steering_rack("rack"),
"0164":lambda:steering_rack("linkage"),
"0165":lambda:steering_rack("boot"),
"0166":lambda:driveshaft(False),
"0167":lambda:driveshaft(True),
"0168":ball_joint,
"0169":propeller,
"0170":lambda:differential(False),
"0171":lambda:differential(True),
"0172":transfer_case,
"0173":lambda:suspension(True),
"0174":lambda:suspension(False),
"0175":lambda:shock_or_strut(False),
"0176":coil,
"0177":stabilizer_bar,
"0178":lambda:control_arm(False),
"0179":tie_rod,
"0180":lambda:hub_or_bearing(False),
"0181":lambda:hub_or_bearing(True),
"0182":lambda:shock_or_strut(True),
"0183":mount,
"0184":lambda:control_arm(True),
"0185":stabilizer_link,
"0186":knuckle,
"0187":lambda:frame_part("subframe"),
"0188":lambda:frame_part("crossmember"),
"0189":lambda:frame_part("undercover"),
"0190":lambda:frame_part("mudguard"),
"0191":lambda:washer(False),
"0192":lambda:washer(True),
}

for id_,fn in jobs.items():
    save(id_,fn())
print("replaced",len(jobs),sorted(jobs))
