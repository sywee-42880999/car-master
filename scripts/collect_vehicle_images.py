#!/usr/bin/env python3
import io, json, re, time
from pathlib import Path
from urllib.parse import urljoin, unquote

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "data/models-latest.json"
AUDIT = ROOT / "data/model-image-audit.json"
OUT = ROOT / "images/vehicles"
STAT = ROOT / "data/model-image-status.json"

S = requests.Session()
S.headers.update({
    "User-Agent": "Mozilla/5.0 Chrome/128 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
})
PAGE_CACHE={}
IMG_CACHE={}
GOOD=("34front","front34","3-4","three-quarter","three quarter","front","exterior","vehicle","car","360","thumbnail","jelly","trim","model")
BAD=("interior","seat","wheel","lamp","headlamp","grille","spoiler","sunroof","sensor","safety","adas","detail","close","feature","accessory","profile-eui-sun","governance","suspension","protection","airbag","radar","parking","speaker","storage")
NEUTRAL=("silver","gray","grey","white","uyuni","atlas","snow","steel","pearl","creamy","cyber","ecotronic","shimmering")

def clean(s): return re.sub(r"[^a-z0-9]+","",(s or "").lower())

def aliases(name):
    parts=[p.strip() for p in re.split(r"[/]",name)]
    out=[]
    for p in parts:
        q=clean(p.replace("The ",""))
        if q: out.append(q)
    return out or [clean(name)]

def required_variant(name):
    n=name.lower()
    req=[]
    if "n line" in n: req.append(("nline","n-line"))
    if re.search(r"\bgt\b",n): req.append(("gt",))
    if "electric" in n or re.search(r"\bev\b",n): req.append(("electric","ev","electrified"))
    if "hatchback" in n: req.append(("hatch","hatchback","5door","5-door"))
    if "sportswagon" in n or "wagon" in n: req.append(("wagon","sportswagon","sw"))
    if "coupe" in n: req.append(("coupe",))
    if "single cab" in n: req.append(("singlecab","single-cab","single cab"))
    if "dual cab" in n: req.append(("dualcab","dual-cab","dual cab"))
    return req

def derivative_conflict(name,text):
    n=name.lower(); t=text.lower()
    if "n line" not in n and ("n line" in t or "n-line" in t or "nline" in t): return True
    if not re.search(r"\bgt\b",n) and re.search(r"(^|[^a-z])gt([^a-z]|$)",t): return True
    if "coupe" not in n and "coupe" in t: return True
    if "electric" not in n and not re.search(r"\bev\b",n) and ("electrified" in t or re.search(r"(^|[^a-z])ev([^a-z]|$)",t)): return True
    if "hatchback" not in n and "sportswagon" not in n and "wagon" not in n and "hatchback" in t: return True
    return False

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
    items={}
    for tag in soup.find_all(["img","source"]):
        meta=" ".join(filter(None,[
            tag.get("alt"),tag.get("title"),tag.get("class") and " ".join(tag.get("class")),
            tag.get("aria-label"),tag.get("data-alt")
        ]))
        for a in ("src","data-src","data-original","data-lazy","srcset","data-srcset"):
            v=tag.get(a)
            if not v:continue
            for p in str(v).split(","):
                u=norm(r.url,p.strip().split(" ")[0])
                if u:
                    items[u]=(items.get(u,"")+" "+meta).strip()
    for m in re.findall(r'https?://[^"\'<>\s]+?(?:png|jpe?g|webp|avif)(?:\?[^"\'<>\s]*)?',r.text,re.I):
        u=norm(r.url,m)
        if u and u not in items:items[u]=""
    for m in re.findall(r'/(?:content/dam|is/image/|cstatic/images|ccontents/)[^"\'<>\s]+?(?:png|jpe?g|webp|avif|\?[^"\'<>\s]*)',r.text,re.I):
        u=norm(r.url,m)
        if u and u not in items:items[u]=""
    PAGE_CACHE[page]=[(u,m) for u,m in items.items()]
    return PAGE_CACHE[page]

def candidate_score(u,meta,name,page):
    text=unquote(u+" "+meta).lower()
    ctext=clean(text)
    score=0
    als=aliases(name)
    exact=max((len(a) for a in als if a and a in ctext),default=0)
    score += 18 if exact>=5 else 8 if exact>=2 else -12
    toks=[x for x in re.findall(r"[a-z0-9]+",name.lower()) if len(x)>=2 and x not in {"the","new","line"}]
    score += sum(3 for t in toks if clean(t) in ctext)
    for group in required_variant(name):
        if any(clean(x) in ctext for x in group):score+=10
        else:score-=16
    if derivative_conflict(name,text):score-=30
    for k in GOOD:
        if k in text:score+=2
    for k in BAD:
        if k in text:score-=7
    for k in NEUTRAL:
        if k in text:score+=1.5
    if any(x in text for x in ("1920","1280","1080","960","880","640","520x260")):score+=2
    return score

def getimg(url):
    if url in IMG_CACHE:
        im,final=IMG_CACHE[url];return im.copy(),final
    r=S.get(url,timeout=15);r.raise_for_status()
    im=Image.open(io.BytesIO(r.content));im.load()
    if im.width<250 or im.height<120:raise ValueError("too small")
    if im.mode=="RGBA":
        bg=Image.new("RGBA",im.size,(255,255,255,255));bg.alpha_composite(im);im=bg.convert("RGB")
    else:im=im.convert("RGB")
    IMG_CACHE[url]=(im.copy(),r.url)
    return im,r.url

def whiteness(im):
    q=im.copy();q.thumbnail((500,500));w,h=q.size;sw=max(3,min(w,h)//30)
    cs=[q.crop((0,0,w,sw)),q.crop((0,h-sw,w,h)),q.crop((0,0,sw,h)),q.crop((w-sw,0,w,h))]
    mean=sum(sum(ImageStat.Stat(c).mean)/3 for c in cs)/4
    std=sum(sum(ImageStat.Stat(c).stddev)/3 for c in cs)/4
    return max(0,min(1,(mean-145)/110))*max(0,min(1,(65-std)/65))

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

def choose(name,vt,pages,over,audit_front=None):
    # Manual closeout candidate in data/model-image-audit.json has highest priority.
    # This lets a reviewed generic/base-model asset supersede a stale trim-specific registry override.
    for label,url in (("audit_override",audit_front),("registry_override",over.get("front"))):
        if not url: continue
        try:
            im,final=getimg(url);return im,final,999,label
        except Exception as e: print(f" {label} failed",e,flush=True)
    pool=[]
    for page in pages:
        try:
            for u,meta in page_images(page):
                pool.append((candidate_score(u,meta,name,page),u,meta,page))
        except Exception as e:
            print(" page failed",page,e,flush=True)
    pool.sort(reverse=True,key=lambda x:x[0])
    for base,u,meta,page in pool[:10]:
        if base<12: continue
        try:
            im,final=getimg(u)
            score=base+whiteness(im)*10+min(3,(im.width*im.height)/(1600*900)*2)
            return im,final,score,(meta or "")[:180]
        except Exception:pass
    return None,None,None,None

def main():
    data=json.loads(REG.read_text())
    audit=json.loads(AUDIT.read_text()) if AUDIT.exists() else {}
    target=set(audit.get("target_ids",[]))
    audit_targets=audit.get("targets",{})
    old=json.loads(STAT.read_text()) if STAT.exists() else {"models":{}}
    rows={r[0]:r for r in data["m"]}
    for n,mid in enumerate(target,1):
        row=rows[mid]; _,brand,name,vt,pages,over=row
        audit_front=(audit_targets.get(mid) or {}).get("preferred_candidate")
        print(f"[{n}/{len(target)}] {mid} {name}",flush=True)
        im,url,score,meta=choose(name,vt,pages,over,audit_front)
        rec=old.setdefault("models",{}).setdefault(mid,{"model":name,"brand":brand})
        diag=[]
        for page in pages:
            try:
                for cu,cm in page_images(page):
                    diag.append((candidate_score(cu,cm,name,page),cu,cm,page))
            except Exception:
                pass
        diag.sort(reverse=True,key=lambda x:x[0])
        rec["candidates"]=[{"score":round(x[0],2),"url":x[1],"meta":(x[2] or "")[:180],"page":x[3]} for x in diag[:20]]
        out=OUT/brand/f"{mid.lower()}_front.webp"
        if im:
            out.parent.mkdir(parents=True,exist_ok=True)
            normalize(im,vt).save(out,"WEBP",quality=87,method=6)
            rec["front"]={"file":str(out.relative_to(ROOT)),"source":url,"score":round(score,2),"meta":meta,"audit":"RECHECK"}
            print(" PASS candidate",url,flush=True)
        else:
            if out.exists():out.unlink()
            rec["front"]={"file":None,"source":None,"audit":"MISS"}
            print(" MISS",flush=True)
        STAT.write_text(json.dumps(old,ensure_ascii=False,indent=2))
    old["generated_at"]=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
    STAT.write_text(json.dumps(old,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
