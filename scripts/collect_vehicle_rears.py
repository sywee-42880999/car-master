#!/usr/bin/env python3
import io, json, re, time
from pathlib import Path
from urllib.parse import urljoin, unquote

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from PIL import Image, ImageChops, ImageStat

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"data/models-latest.json"
REJECTS_FILE=ROOT/"data/rear-source-rejects.json"
STAT=ROOT/"data/model-image-status.json"
OUT=ROOT/"images/vehicles"
S=requests.Session()
S.headers.update({"User-Agent":"Mozilla/5.0 Chrome/128 Safari/537.36","Accept-Language":"en-US,en;q=0.9,ko;q=0.8"})
PAGE_CACHE={}
IMG_CACHE={}
REJECTS={}
if REJECTS_FILE.exists():
    _rj=json.loads(REJECTS_FILE.read_text()).get("rejects",{})
    for k,v in _rj.items():
        vals=v if isinstance(v,list) else [v]
        REJECTS[k]={x.get("url") for x in vals if isinstance(x,dict) and x.get("url")}
REAR=("rear","back","34rear","rear34","rear-three-quarter","three-quarter-rear","rear_3-4","rear-3-4","back34","back-34","후면","후측면","후측")
BAD=("interior","seat","wheel","lamp","headlamp","grille","spoiler","sunroof","sensor","safety","adas","detail","close","feature","accessory","profile-eui-sun","governance","suspension","protection")
NEUTRAL=("silver","gray","grey","white","uyuni","atlas","snow","steel","pearl","creamy","cyber","ecotronic","shimmering")

def clean(s): return re.sub(r"[^a-z0-9]+","",(s or "").lower())

def aliases(name):
    out=[]
    for p in re.split(r"[/]",name):
        q=clean(p)
        if q: out.append(q)
    return out or [clean(name)]

def variant_groups(name):
    n=name.lower(); req=[]
    if "n line" in n:req.append(("nline","n-line"))
    if re.search(r"\bgt\b",n):req.append(("gt",))
    if "electric" in n or "electrified" in n or re.search(r"\bev\b",n):req.append(("electric","electrified","ev"))
    if "hatchback" in n:req.append(("hatch","hatchback","5door","5-door"))
    if "sportswagon" in n or "wagon" in n:req.append(("wagon","sportswagon","sw"))
    if "coupe" in n:req.append(("coupe",))
    if "single cab" in n:req.append(("singlecab","single-cab","single cab"))
    if "dual cab" in n:req.append(("dualcab","dual-cab","dual cab"))
    return req

def norm(base,u):
    if not u:return None
    u=str(u).strip().strip("'\"")
    if u.startswith(("data:","javascript:","#")):return None
    if u.startswith("//"):u="https:"+u
    elif not u.startswith(("http://","https://")):u=urljoin(base,u)
    return u.replace("&amp;","&")

def page_images(page):
    if page in PAGE_CACHE:return PAGE_CACHE[page]
    r=S.get(page,timeout=15);r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser")
    out={}
    for tag in soup.find_all(["img","source"]):
        meta=" ".join(filter(None,[tag.get("alt"),tag.get("title"),tag.get("aria-label"),tag.get("data-alt")]))
        for a in ("src","data-src","data-original","data-lazy","srcset","data-srcset"):
            v=tag.get(a)
            if not v:continue
            for p in str(v).split(","):
                u=norm(r.url,p.strip().split(" ")[0])
                if u:out[u]=(out.get(u,"")+" "+meta).strip()
    for m in re.findall(r'https?://[^"\'<>\s]+?(?:png|jpe?g|webp|avif)(?:\?[^"\'<>\s]*)?',r.text,re.I):
        u=norm(r.url,m)
        if u and u not in out:out[u]=""
    PAGE_CACHE[page]=list(out.items())
    return PAGE_CACHE[page]

def score(u,meta,name):
    text=unquote(u+" "+meta).lower(); ct=clean(text)
    if not any(k in text for k in REAR):return -999
    exact=max((len(a) for a in aliases(name) if a and a in ct),default=0)
    s=30 if exact>=5 else 12 if exact>=2 else -30
    for g in variant_groups(name):
        s += 12 if any(clean(x) in ct for x in g) else -18
    for k in BAD:
        if k in text:s-=8
    for k in NEUTRAL:
        if k in text:s+=1.5
    if any(x in text for x in ("1920","1280","1080","960","880","640","520x260")):s+=2
    return s

def getimg(url):
    if url in IMG_CACHE:
        im,final=IMG_CACHE[url];return im.copy(),final
    r=S.get(url,timeout=15);r.raise_for_status()
    im=Image.open(io.BytesIO(r.content));im.load()
    if im.width<250 or im.height<120:raise ValueError("small")
    if im.mode=="RGBA":
        bg=Image.new("RGBA",im.size,(255,255,255,255));bg.alpha_composite(im);im=bg.convert("RGB")
    else:im=im.convert("RGB")
    IMG_CACHE[url]=(im.copy(),r.url)
    return im,r.url

def bbox(im):
    q=im.copy();q.thumbnail((900,600));w,h=q.size;r=max(8,min(w,h)//25)
    cs=[q.crop((0,0,r,r)),q.crop((w-r,0,w,r)),q.crop((0,h-r,r,h)),q.crop((w-r,h-r,w,h))]
    bg=tuple(int(sum(ImageStat.Stat(c).mean[i] for c in cs)/4) for i in range(3))
    d=ImageChops.difference(q,Image.new("RGB",q.size,bg)).convert("L").point(lambda p:255 if p>24 else 0)
    b=d.getbbox()
    if not b:return None
    sx,sy=im.width/w,im.height/h
    return (int(b[0]*sx),int(b[1]*sy),int(b[2]*sx),int(b[3]*sy))

def normalize(im,vt):
    b=bbox(im)
    if b:
        l,t,r,bb=b;bw,bh=r-l,bb-t
        if bw>im.width*.25 and bh>im.height*.18:
            mx,my=int(bw*.06),int(bh*.08)
            im=im.crop((max(0,l-mx),max(0,t-my),min(im.width,r+mx),min(im.height,bb+my)))
    cw,ch=1194,732
    tw=.80 if vt in ("bus","commercial") else .85 if vt in ("suv","mpv","pickup") else .87
    th=.82 if vt in ("bus","commercial","suv","mpv","pickup") else .78
    sc=min(cw*tw/im.width,ch*th/im.height);nw,nh=max(1,int(im.width*sc)),max(1,int(im.height*sc))
    im=im.resize((nw,nh),Image.Resampling.LANCZOS)
    canvas=Image.new("RGB",(cw,ch),"white")
    y=max(24,min(ch-nh-24,int((ch-nh)*.46)))
    canvas.paste(im,((cw-nw)//2,y))
    return canvas

def choose(mid,name,vt,pages,over):
    if over.get("rear"):
        try:
            im,final=getimg(over["rear"]);return im,final,999,"override"
        except Exception as e: print(" override failed",e,flush=True)
    ranked=[]
    for p in pages:
        try:
            for u,m in page_images(p):
                if u in REJECTS.get(mid,set()):
                    continue
                sc=score(u,m,name)
                if sc>-999:ranked.append((sc,u,m,p))
        except Exception as e: print(" page failed",p,e,flush=True)
    ranked.sort(reverse=True,key=lambda x:x[0])
    for sc,u,m,p in ranked[:8]:
        if sc<12:continue
        try:
            im,final=getimg(u);return im,final,sc,(m or "")[:160]
        except Exception:pass
    return None,None,None,None

def prefetch(pages):
    uniq=list(dict.fromkeys(pages))
    def one(p):
        try:
            return p,page_images(p)
        except Exception:
            return p,[]
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs=[ex.submit(one,p) for p in uniq]
        for fut in as_completed(futs):
            p,items=fut.result()
            PAGE_CACHE[p]=items

def main():
    data=json.loads(REG.read_text())
    prefetch([p for row in data["m"] for p in row[4]])
    status=json.loads(STAT.read_text()) if STAT.exists() else {"models":{}}
    found=0
    for n,row in enumerate(data["m"],1):
        mid,brand,name,vt,pages,over=row
        print(f"[{n}/{len(data['m'])}] {mid} {name}",flush=True)
        rec=status.setdefault("models",{}).setdefault(mid,{"model":name,"brand":brand})
        im,url,sc,meta=choose(mid,name,vt,pages,over)
        out=OUT/brand/f"{mid.lower()}_rear.webp"
        if im:
            out.parent.mkdir(parents=True,exist_ok=True)
            normalize(im,vt).save(out,"WEBP",quality=87,method=6)
            rec["rear"]={"file":str(out.relative_to(ROOT)),"source":url,"score":round(sc,2),"meta":meta,"audit":"RECHECK"}
            found+=1
            print(" rear candidate",url,flush=True)
        else:
            if out.exists():out.unlink()
            rec["rear"]={"file":None,"source":None,"audit":"MISS"}
        STAT.write_text(json.dumps(status,ensure_ascii=False,indent=2))
    status["rear_generated_at"]=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
    status["rear_found"]=found
    STAT.write_text(json.dumps(status,ensure_ascii=False,indent=2))
    print("rear found",found,flush=True)

if __name__=="__main__":
    main()
