#!/usr/bin/env python3
import io, json, re, time
from pathlib import Path
from urllib.parse import urljoin, unquote

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "data/models-latest.json"
OUT = ROOT / "images/vehicles"
STAT = ROOT / "data/model-image-status.json"

PAGE_CACHE = {}
S = requests.Session()
S.headers.update({
    "User-Agent": "Mozilla/5.0 Chrome/128 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ko;q=0.8"
})

GOOD = ("34front","front34","3-4","front","exterior","trim","thumbnail","model-list","build","config","360")
REAR = ("rear","back","34rear","rear34")
BAD = ("interior","wheel","logo","icon","banner","detail","headlamp","seat","dashboard","feature","accessory")
NEUTRAL = ("silver","gray","grey","white","uyuni","atlas","snow","ivory","steel","shimmering","ecotronic","cyber")

def norm(base, u):
    if not u:
        return None
    u = str(u).strip().strip("'\"")
    if u.startswith(("data:", "javascript:", "#")):
        return None
    if u.startswith("//"):
        u = "https:" + u
    elif not u.startswith(("http://", "https://")):
        u = urljoin(base, u)
    return u.replace("&amp;", "&")

def toks(name):
    return [x.lower() for x in re.findall(r"[A-Za-z0-9]+", name or "")
            if len(x) > 1 and x.lower() not in {"the","all","new","ev","gt","line"}]

def page_images(page):
    if page in PAGE_CACHE:
        return PAGE_CACHE[page]
    r = S.get(page, timeout=12)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    out = set()
    for tag in soup.find_all(["img", "source"]):
        for a in ("src","data-src","data-original","data-lazy","srcset","data-srcset"):
            v = tag.get(a)
            if not v:
                continue
            for p in str(v).split(","):
                u = norm(r.url, p.strip().split(" ")[0])
                if u:
                    out.add(u)
    for m in re.findall(r'https?://[^"\'<>\s]+?(?:png|jpe?g|webp|avif)(?:\?[^"\'<>\s]*)?', r.text, re.I):
        u = norm(r.url, m)
        if u:
            out.add(u)
    for m in re.findall(r'/(?:content/dam|is/image/)[^"\'<>\s]+?(?:png|jpe?g|webp|avif|\?[^"\'<>\s]*)', r.text, re.I):
        u = norm(r.url, m)
        if u:
            out.add(u)
    PAGE_CACHE[page] = list(out)
    return PAGE_CACHE[page]

def uscore(u, name, want):
    s = 0
    l = unquote(u).lower()
    for t in toks(name):
        if t in l:
            s += 6
    for k in GOOD:
        if k in l:
            s += 2
    for k in BAD:
        if k in l:
            s -= 5
    for k in NEUTRAL:
        if k in l:
            s += 2
    if want == "rear":
        if any(k in l for k in REAR):
            s += 12
        if "front" in l:
            s -= 6
    else:
        if "front" in l:
            s += 5
        if any(k in l for k in REAR):
            s -= 7
    if any(x in l for x in ("1920","1280","1080","960","880","640")):
        s += 2
    return s

def getimg(url):
    if url in IMG_CACHE:
        im, final = IMG_CACHE[url]
        return im.copy(), final
    r = S.get(url, timeout=12)
    r.raise_for_status()
    im = Image.open(io.BytesIO(r.content))
    im.load()
    if im.width < 420 or im.height < 180:
        raise ValueError("too small")
    if im.mode == "RGBA":
        bg = Image.new("RGBA", im.size, (255,255,255,255))
        bg.alpha_composite(im)
        im = bg.convert("RGB")
    else:
        im = im.convert("RGB")
    IMG_CACHE[url] = (im.copy(), r.url)
    return im, r.url

def whiteness(im):
    q = im.copy()
    q.thumbnail((500,500))
    w,h = q.size
    sw = max(3, min(w,h)//30)
    cs = [
        q.crop((0,0,w,sw)), q.crop((0,h-sw,w,h)),
        q.crop((0,0,sw,h)), q.crop((w-sw,0,w,h))
    ]
    mean = sum(sum(ImageStat.Stat(c).mean)/3 for c in cs)/4
    std = sum(sum(ImageStat.Stat(c).stddev)/3 for c in cs)/4
    return max(0,min(1,(mean-145)/110))*max(0,min(1,(60-std)/60))

def qscore(im, u, want):
    s = whiteness(im)*18
    ar = im.width/im.height
    if 1.15 <= ar <= 2.6:
        s += 4
    l = unquote(u).lower()
    if want == "rear" and any(k in l for k in REAR):
        s += 10
    if want == "front" and "front" in l:
        s += 6
    s += min(4, (im.width*im.height)/(1600*900)*2.5)
    return s

def bbox(im):
    q = im.copy()
    q.thumbnail((900,600))
    w,h = q.size
    r = max(8, min(w,h)//25)
    cs = [
        q.crop((0,0,r,r)), q.crop((w-r,0,w,r)),
        q.crop((0,h-r,r,h)), q.crop((w-r,h-r,w,h))
    ]
    bg = tuple(int(sum(ImageStat.Stat(c).mean[i] for c in cs)/4) for i in range(3))
    d = ImageChops.difference(q, Image.new("RGB", q.size, bg)).convert("L")
    d = d.point(lambda p: 255 if p > 24 else 0)
    b = d.getbbox()
    if not b:
        return None
    sx,sy = im.width/w, im.height/h
    return (int(b[0]*sx), int(b[1]*sy), int(b[2]*sx), int(b[3]*sy))

def normalize(im, vt):
    b = bbox(im)
    if b:
        l,t,r,bb = b
        bw,bh = r-l, bb-t
        if bw > im.width*.25 and bh > im.height*.18:
            mx,my = int(bw*.06), int(bh*.08)
            im = im.crop((max(0,l-mx), max(0,t-my), min(im.width,r+mx), min(im.height,bb+my)))
    cw,ch = 1194,732
    tw = .80 if vt in ("bus","commercial") else .85 if vt in ("suv","mpv","pickup") else .87
    th = .82 if vt in ("bus","commercial","suv","mpv","pickup") else .78
    sc = min(cw*tw/im.width, ch*th/im.height)
    nw,nh = max(1,int(im.width*sc)), max(1,int(im.height*sc))
    im = im.resize((nw,nh), Image.Resampling.LANCZOS)
    c = Image.new("RGB", (cw,ch), "white")
    y = max(24, min(ch-nh-24, int((ch-nh)*.46)))
    c.paste(im, ((cw-nw)//2, y))
    return c

def choose(name, vt, pages, over, want):
    if over.get(want):
        try:
            im, final = getimg(over[want])
            return im, final, 999
        except Exception as e:
            print(" override failed:", e, flush=True)
    pool = {}
    for p in pages:
        try:
            for u in page_images(p):
                pool[u] = max(pool.get(u,-999), uscore(u,name,want))
        except Exception as e:
            print(" page failed:", p, e, flush=True)
    ranked = sorted(pool.items(), key=lambda x:x[1], reverse=True)
    if want == "rear":
        explicit = [(u,s) for u,s in ranked if any(k in unquote(u).lower() for k in REAR)]
        ranked = explicit
    best = None
    for u, us in ranked[:7]:
        try:
            im, final = getimg(u)
            sc = us + qscore(im, final, want)
            if best is None or sc > best[0]:
                best = (sc, im, final)
        except Exception:
            pass
    if best:
        return best[1], best[2], best[0]
    return None, None, None

def main():
    data = json.loads(REG.read_text())
    status = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "models": {}
    }
    for n,row in enumerate(data["m"],1):
        mid,brand,name,vt,pages,over = row
        rec = {"model":name,"brand":brand}
        print(f"[{n}/{len(data['m'])}] {mid} {name}", flush=True)
        for want in ("front","rear"):
            im,url,score = choose(name,vt,pages,over,want)
            if im:
                out = OUT/brand/f"{mid.lower()}_{want}.webp"
                out.parent.mkdir(parents=True,exist_ok=True)
                normalize(im,vt).save(out,"WEBP",quality=86,method=6)
                rec[want] = {
                    "file": str(out.relative_to(ROOT)),
                    "source": url,
                    "score": round(score,2)
                }
                print(" ",want,"OK",flush=True)
            else:
                rec[want] = {"file":None,"source":None}
                print(" ",want,"MISS",flush=True)
        status["models"][mid] = rec
        STAT.write_text(json.dumps(status,ensure_ascii=False,indent=2))
    print("complete", flush=True)

if __name__ == "__main__":
    main()
