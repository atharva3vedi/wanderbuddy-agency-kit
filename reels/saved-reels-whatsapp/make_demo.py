#!/usr/bin/env python3
"""Render the WhatsApp -> WanderBuddy mock demo as 1080x1920 frames.
Deterministic phone-screen recording: share a travel reel to the WhatsApp bot,
it reads it and drops the real place into the trip + saved reels.
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "demo", "frames")
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30

FD = "C:/Windows/Fonts/"
def font(name, sz): return ImageFont.truetype(FD+name, sz)
REG   = lambda s: font("arial.ttf", s)
BOLD  = lambda s: font("arialbd.ttf", s)
EMO   = lambda s: font("seguiemj.ttf", s)

# ---------- brand / ui colors ----------
WA_GREEN   = (0,128,105)
WA_BG      = (231,221,213)
WA_SENT    = (214,248,193)
WA_RECV    = (255,255,255)
INK        = (17,27,33)
META       = (120,132,140)
WB_BLUE    = (30,136,214)
WB_AMBER   = (224,151,42)
WB_TEAL    = (31,168,154)
WB_BG      = (243,246,249)
WB_INK     = (12,22,34)
WB_MUTE    = (94,115,134)
WB_BORDER  = (207,220,230)

def ease(t):  # easeOutCubic
    t = max(0.0, min(1.0, t)); return 1-(1-t)**3
def eob(t):   # easeOutBack
    t = max(0.0,min(1.0,t)); c1=1.70158; c3=c1+1
    return 1+c3*(t-1)**3+c1*(t-1)**2

def is_emo(ch):
    o=ord(ch)
    return (o>=0x1F000 or 0x2190<=o<=0x2BFF or 0x2600<=o<=0x27BF
            or o in (0xFE0F,0x2764,0x2705,0x2728,0x2B50,0x270D,0x2714)
            or 0x1F1E6<=o<=0x1F1FF)

def runs(s):
    out=[]; cur=""; ce=None
    for ch in s:
        if ch=='\ufe0f':
            if out and out[-1][1]: out[-1]=(out[-1][0]+ch,True)
            elif cur: cur+=ch
            continue
        e=is_emo(ch)
        if ce is None: cur=ch; ce=e
        elif e==ce: cur+=ch
        else: out.append((cur,ce)); cur=ch; ce=e
    if cur: out.append((cur,ce))
    return out

def measure(s, tf, ef):
    w=0
    for txt,e in runs(s):
        f=ef if e else tf
        w+=f.getbbox(txt)[2]
    return w

def rich(d, xy, s, tf, ef, fill):
    x,y=xy
    for txt,e in runs(s):
        f=ef if e else tf
        if e:
            d.text((x,y),txt,font=f,embedded_color=True)
        else:
            d.text((x,y),txt,font=f,fill=fill)
        x+=f.getbbox(txt)[2]
    return x

def rr(d, box, r, fill, outline=None, w=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=w)

def load_cover(name, size):
    im=Image.open(os.path.join(HERE,"demo",name)).convert("RGB")
    return ImageOps.fit(im, size, Image.LANCZOS)

def circle_icon(size):
    ic=Image.open(os.path.join(HERE,"demo","app_icon.png")).convert("RGBA").resize((size,size),Image.LANCZOS)
    m=Image.new("L",(size,size),0); ImageDraw.Draw(m).ellipse((0,0,size,size),fill=255)
    ic.putalpha(m); return ic

COVERS = {}
def cover(name,size):
    k=(name,size)
    if k not in COVERS: COVERS[k]=load_cover(name,size)
    return COVERS[k]
ICON64 = circle_icon(72)

# ---------- shared chrome ----------
def status_bar(img, d, dark_text=False):
    col=(255,255,255) if not dark_text else INK
    d.text((44,26), "9:41", font=BOLD(30), fill=col)
    # battery / wifi (simple glyphs)
    bx=W-70
    d.rounded_rectangle((bx,28,bx+44,52), radius=5, outline=col, width=3)
    d.rectangle((bx+46,35,bx+50,45), fill=col)
    d.rounded_rectangle((bx+4,32,bx+34,48), radius=3, fill=col)
    # wifi dot cluster
    d.ellipse((W-150,34,W-130,54), fill=col)

def bubble(d, side, top, text_lines, tf, meta_txt, maxw=760, tail=True,
           bubblecol=None, appear=1.0):
    """draw a chat bubble; returns bottom y. appear 0..1 controls slide/fade via caller clipping."""
    pad=26; lh=48
    tw=max(measure(t,tf,EMO(tf.size)) for t in text_lines) if text_lines else 0
    bw=min(maxw, max(tw+pad*2, 180))
    bh=pad*2+lh*len(text_lines)+ (34 if meta_txt else 0)
    if side=="r":
        x1=W-40-bw; x2=W-40; col=bubblecol or WA_SENT
    else:
        x1=40; x2=40+bw; col=bubblecol or WA_RECV
    rr(d,(x1,top,x2,top+bh),28,col)
    ty=top+pad
    for t in text_lines:
        rich(d,(x1+pad,ty),t,tf,EMO(tf.size),INK); ty+=lh
    if meta_txt:
        mf=REG(24); mw=measure(meta_txt,mf,EMO(24))
        rich(d,(x2-pad-mw,top+bh-38),meta_txt,mf,EMO(24),META)
    return top+bh, (x1,top,x2,top+bh)

def reel_card(base, top, appear):
    """sent bubble containing a shared reel link preview. returns bottom y."""
    d=ImageDraw.Draw(base)
    bw=700; x1=W-40-bw; x2=W-40
    cov_h=430
    bh=cov_h+150
    # bubble
    rr(d,(x1,top,x2,top+bh),28,WA_SENT)
    # cover image
    cv=cover("cover_falls.jpg",(bw-24,cov_h))
    cx,cy=x1+12,top+12
    mask=Image.new("L",cv.size,0); ImageDraw.Draw(mask).rounded_rectangle((0,0,cv.size[0],cv.size[1]),radius=18,fill=255)
    base.paste(cv,(cx,cy),mask)
    # play glyph
    pd=ImageDraw.Draw(base)
    pcx,pcy=cx+cv.size[0]//2, cy+cov_h//2
    pd.ellipse((pcx-46,pcy-46,pcx+46,pcy+46),fill=(0,0,0,120))
    pd.polygon([(pcx-16,pcy-24),(pcx-16,pcy+24),(pcx+26,pcy)],fill=(255,255,255))
    # "REEL" tag
    rr(pd,(cx+16,cy+16,cx+150,cy+62),12,(0,0,0))
    rich(pd,(cx+34,cy+22),"REEL",BOLD(30),EMO(30),(255,255,255))
    # caption + url
    ty=cy+cov_h+16
    rich(pd,(x1+24,ty),"Hidden turquoise falls in Laos \U0001F60d",REG(32),EMO(32),INK); ty+=44
    rich(pd,(x1+24,ty),"instagram.com/reel/laos-kuangsi",REG(28),EMO(28),(70,120,180))
    mf=REG(24); mt="12:24  \u2713\u2713"
    rich(pd,(x2-26-measure(mt,mf,EMO(24)),top+bh-36),mt,mf,EMO(24),(90,150,110))
    return top+bh

def typing(d, top):
    bw=150; x1=40
    rr(d,(x1,top,x1+bw,top+80),28,WA_RECV)
    for i in range(3):
        cx=x1+38+i*34
        d.ellipse((cx-9,top+32,cx+9,top+50),fill=(150,160,166))

# ---------- SCENE 1 : WhatsApp ----------
def scene1(t):
    img=Image.new("RGB",(W,H),WA_BG); d=ImageDraw.Draw(img)
    # header
    d.rectangle((0,0,W,180),fill=WA_GREEN)
    status_bar(img,d)
    d.polygon([(60,110),(96,86),(96,134)],fill=(255,255,255))  # back arrow
    img.paste(ICON64,(112,74),ICON64)
    nf=BOLD(42); d.text((200,80),"WanderBuddy",font=nf,fill=(255,255,255))
    d.text((200,132),"online",font=REG(28),fill=(220,240,235))
    # verified tick (after the name)
    nx=200+nf.getbbox("WanderBuddy")[2]+16
    d.ellipse((nx,88,nx+36,124),fill=(255,255,255))
    d.line((nx+8,106,nx+18,116),fill=WA_GREEN,width=4); d.line((nx+18,116,nx+30,96),fill=WA_GREEN,width=4)
    # date chip
    rr(d,(W//2-90,206,W//2+90,250),20,(220,236,228))
    dt="TODAY"; f=BOLD(24); d.text((W//2-measure(dt,f,EMO(24))//2,214),dt,font=f,fill=(90,110,104))

    # b1 (always present)
    bubble(d,"l",280,["Send me any travel reel \U0001f44b","I'll pull out the places for you"],REG(34),"12:24")
    # b2 reel card: appears 0.4-1.0 (slide up)
    y=520
    if t>=0.35:
        a=ease((t-0.35)/0.6); dy=int((1-a)*50)
        card=Image.new("RGB",(W,H),WA_BG)
        reel_card(card,y+dy,a)
        # crop card region and blend for fade
        reg=(0,y-20,W,y+640)
        piece=card.crop(reg)
        if a<1:
            base=img.crop(reg); piece=Image.blend(base,piece,a)
        img.paste(piece,(0,y-20))
    yb=y+590
    # typing 1.4-2.4
    if 1.35<=t<2.3:
        typing(d, yb+30)
    # b4 reading 2.3+
    if t>=2.3:
        a=ease((t-2.3)/0.4); dy=int((1-a)*40)
        _draw_recv(img,["Reading that reel now\u2026 \U0001f4d6"],yb+30-dy+ (0 if a>=1 else 0),"12:24",a)
    # b5 place found 3.2+
    if t>=3.2:
        a=ease((t-3.2)/0.4); dy=int((1-a)*40)
        _draw_recv(img,["\u2705 Found: Kuang Si Falls, Laos"],yb+165-dy,"12:24",a)
    # b6 added 4.0+
    if t>=4.0:
        a=ease((t-4.0)/0.45); dy=int((1-a)*40)
        _draw_recv(img,["Added to your Laos trip","+ 3 more spots saved \u2728"],yb+300-dy,"12:24",a)

    # input bar
    d.rectangle((0,H-150,W,H),fill=WA_BG)
    rr(d,(30,H-135,W-160,H-35),50,(255,255,255))
    d.text((70,H-108),"Message",font=REG(34),fill=(150,158,164))
    d.ellipse((W-140,H-140,W-30,H-30),fill=WA_GREEN)
    # send triangle
    d.polygon([(W-100,H-108),(W-100,H-62),(W-56,H-85)],fill=(255,255,255))
    return img

def _draw_recv(img,lines,top,meta,a):
    if a>=1:
        d=ImageDraw.Draw(img); bubble(d,"l",top,lines,REG(34),meta); return
    tmp=Image.new("RGB",(W,H),WA_BG); dt=ImageDraw.Draw(tmp)
    _,box=bubble(dt,"l",top,lines,REG(34),meta)
    x1,y1,x2,y2=box; pad=16
    reg=(0,y1-pad,W,y2+pad); piece=tmp.crop(reg); base=img.crop(reg)
    img.paste(Image.blend(base,piece,a),(0,y1-pad))

# ---------- SCENE 2 : WanderBuddy app ----------
def scene2(t):
    img=Image.new("RGB",(W,H),WB_BG); d=ImageDraw.Draw(img)
    # header
    d.rectangle((0,0,W,250),fill=WB_BLUE)
    status_bar(img,d)
    d.polygon([(60,150),(96,126),(96,174)],fill=(255,255,255))
    d.text((130,110),"Laos",font=BOLD(50),fill=(255,255,255))
    d.text((132,178),"5 days \u00b7 Itinerary",font=REG(30),fill=(224,238,250))
    img.paste(ICON64,(W-110,120),ICON64)
    # tab strip
    d.text((60,290),"Day 2 \u00b7 Luang Prabang",font=BOLD(38),fill=WB_INK)

    # existing faded card
    rr(d,(50,360,W-50,470),22,(255,255,255),outline=WB_BORDER,w=2)
    d.ellipse((78,392,126,440),outline=WB_MUTE,width=3)
    d.text((150,378),"Morning market walk",font=BOLD(34),fill=WB_INK)
    d.text((150,424),"8:30 AM \u00b7 old town",font=REG(28),fill=WB_MUTE)

    # NEW card pop-in (t>=0.3)
    top=500
    if t>=0.25:
        a=eob((t-0.25)/0.6); s=0.9+0.1*min(1,a); al=ease((t-0.25)/0.4)
        ch=330
        card=Image.new("RGBA",(W-100,ch),(0,0,0,0)); cd=ImageDraw.Draw(card)
        rr(cd,(0,0,W-100,ch),26,(255,255,255)+(255,))
        cd.rounded_rectangle((0,0,W-100,ch),radius=26,outline=WB_AMBER+(255,),width=5)
        cov=cover("cover_falls.jpg",(230,ch-40)).convert("RGBA")
        m=Image.new("L",cov.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,cov.size[0],cov.size[1]),radius=18,fill=255)
        card.paste(cov,(24,20),m)
        tx=290
        # chip
        rr(cd,(tx,26,tx+300,74),16,WB_AMBER+(255,))
        rich(cd,(tx+18,32),"\U0001f4cd From your reel",BOLD(28),EMO(28),(74,46,8))
        cd.text((tx,100),"Kuang Si Falls",font=BOLD(46),fill=WB_INK)
        cd.text((tx,160),"Turquoise waterfalls",font=REG(32),fill=WB_MUTE)
        cd.text((tx,206),"30 km \u00b7 half day",font=REG(32),fill=WB_MUTE)
        rr(cd,(tx,258,tx+220,314),16,WB_TEAL+(255,))
        rich(cd,(tx+24,268),"On the map",BOLD(30),EMO(30),(255,255,255))
        # scale + place
        cw,chh=card.size; ns=(int(cw*s),int(ch*s))
        card=card.resize(ns,Image.LANCZOS)
        if al<1:
            al_img=card.split()[3].point(lambda p:int(p*al)); card.putalpha(al_img)
        px=50-(ns[0]-(W-100))//2; py=top-(ns[1]-ch)//2
        img.paste(card,(px,py),card)
        # sparkle
        if 0.3<=t<0.9:
            sp=EMO(70); rich(ImageDraw.Draw(img),(W-150,top-40),"\u2728",BOLD(70),sp,WB_AMBER)

    # saved-from-reels row (t>=1.1)
    ry=900
    d.text((60,ry-60),"Saved from your reels",font=BOLD(36),fill=WB_INK)
    names=["cover_road.jpg","cover_tea.jpg","cover_pool.jpg"]
    labels=["Mountain pass","Riverside cafe","Jungle pool"]
    if t>=1.0:
        for i,(nm,lb) in enumerate(zip(names,labels)):
            a=ease((t-1.0-i*0.15)/0.5)
            if a<=0: continue
            dx=int((1-a)*60); cw2=300; cx=60+i*(cw2+30)+dx
            cv=cover(nm,(cw2,400))
            reg=Image.new("RGB",(cw2,470),(255,255,255))
            mm=Image.new("L",(cw2,400),0); ImageDraw.Draw(mm).rounded_rectangle((0,0,cw2,400),radius=20,fill=255)
            reg.paste(cv,(0,0),mm)
            rd=ImageDraw.Draw(reg); rd.text((6,412),lb,font=BOLD(26),fill=WB_INK)
            if a<1:
                base=img.crop((cx,ry,cx+cw2,ry+470)); reg=Image.blend(base,reg,a)
            img.paste(reg,(cx,ry))

    # bottom toast pill (t>=1.9)
    if t>=1.9:
        a=ease((t-1.9)/0.4)
        pill=Image.new("RGBA",(W,160),(0,0,0,0)); pd=ImageDraw.Draw(pill)
        msg="Every reel becomes a real plan"
        f=BOLD(38); mw=measure(msg,f,EMO(38))
        rr(pd,((W-mw-80)//2,40,(W+mw+80)//2,130),44,WB_INK+(235,))
        rich(pd,((W-mw)//2,62),msg,f,EMO(38),(255,255,255))
        ao=pill.split()[3].point(lambda p:int(p*a)); pill.putalpha(ao)
        img.paste(pill,(0,H-360),pill)
    return img

# ---------- timeline ----------
S1, TR, S2 = 5.6, 0.45, 5.0
TOTAL = S1+TR+S2

def render(t):
    if t < S1:
        return scene1(t)
    if t < S1+TR:
        a=ease((t-S1)/TR); off=int(a*W)
        s1=scene1(S1-0.001); s2=scene2(0.0)
        canvas=Image.new("RGB",(W,H))
        canvas.paste(s1,(-off,0)); canvas.paste(s2,(W-off,0))
        return canvas
    return scene2(t-S1-TR)

def main():
    n=int(TOTAL*FPS)
    for i in range(n):
        t=i/FPS
        render(t).save(os.path.join(OUT,f"{i:04d}.png"))
        if i%15==0: print("frame",i,"/",n)
    print("done",n,"frames")

if __name__=="__main__":
    main()
