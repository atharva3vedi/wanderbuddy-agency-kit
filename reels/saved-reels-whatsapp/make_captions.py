#!/usr/bin/env python3
"""Render meme-style caption PNGs (1080x1920, transparent) for the reel.
White bold text + heavy black stroke + soft shadow; colour emoji drawn inline.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,"captions"); os.makedirs(OUT,exist_ok=True)
W,H=1080,1920
FD="C:/Windows/Fonts/"
BOLD=lambda s: ImageFont.truetype(FD+"arialbd.ttf",s)
EMO =lambda s: ImageFont.truetype(FD+"seguiemj.ttf",s)

def is_emo(ch):
    o=ord(ch)
    return (o>=0x1F000 or 0x2190<=o<=0x2BFF or 0x2600<=o<=0x27BF
            or o in (0xFE0F,0x2764,0x2705,0x2728,0x2B50) or 0x1F1E6<=o<=0x1F1FF)
def runs(s):
    out=[];cur="";ce=None
    for ch in s:
        if ch=='\ufe0f':
            if out and out[-1][1]: out[-1]=(out[-1][0]+ch,True)
            continue
        e=is_emo(ch)
        if ce is None:cur=ch;ce=e
        elif e==ce:cur+=ch
        else:out.append((cur,ce));cur=ch;ce=e
    if cur:out.append((cur,ce))
    return out
def wline(s,tf,ef):
    return sum((ef if e else tf).getbbox(t)[2] for t,e in runs(s))

def caption(name, lines, size=72, y_center=1180, stroke=8, lh_mul=1.18):
    img=Image.new("RGBA",(W,H),(0,0,0,0))
    tf=BOLD(size); ef=EMO(size)
    lh=int(size*lh_mul)
    total=lh*len(lines)
    y=y_center-total//2
    # shadow layer
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
    d=ImageDraw.Draw(img)
    for ln in lines:
        w=wline(ln,tf,ef); x=(W-w)//2
        # shadow (text only)
        sx=x
        for t,e in runs(ln):
            f=ef if e else tf
            if not e: sd.text((sx+4,y+6),t,font=f,fill=(0,0,0,180))
            sx+=f.getbbox(t)[2]
        # main with stroke
        cx=x
        for t,e in runs(ln):
            f=ef if e else tf
            if e:
                d.text((cx,y),t,font=f,embedded_color=True)
            else:
                d.text((cx,y),t,font=f,fill=(255,255,255,255),
                       stroke_width=stroke,stroke_fill=(0,0,0,255))
            cx+=f.getbbox(t)[2]
        y+=lh
    sh=sh.filter(ImageFilter.GaussianBlur(6))
    out=Image.alpha_composite(sh,img)
    out.save(os.path.join(OUT,name+".png"))
    print("wrote",name)

# ---- version A : meme hook ----
caption("A1",["i could never be the","person who saves a reel"],size=70,y_center=1150)
caption("A2",["\u2026and never finds","it again \U0001f480"],size=74,y_center=1150)
# ---- version B : POV hook ----
caption("B1",["POV: your saved folder","IS your dream trip \U0001f60d"],size=66,y_center=1150)
caption("B2",["\u2026and you can't find","a single one of them"],size=66,y_center=1150)
# ---- shared ----
caption("S3",["so here's what i","do instead \U0001f447"],size=76,y_center=1150)
caption("D1",["just text the reel","to WhatsApp \U0001f4f2"],size=64,y_center=1600)
caption("P1",["now i only plan with","places i actually loved"],size=64,y_center=1180)
caption("P2",["wander more.","plan less."],size=88,y_center=1150)
# ---- promo (2nd half) captions ----
caption("PW1",["text WanderBuddy","any travel reel \U0001f4f2"],size=64,y_center=1600)
caption("PW2",["it pulls out the","actual place ✨"],size=64,y_center=1600)
caption("PR0",["really connected","to your WhatsApp ✅"],size=60,y_center=1360)
caption("PR1",["every reel becomes","a saved place \U0001f4cc"],size=62,y_center=1360)
caption("PR2",["find your whole trip","again in one tap \U0001f50e"],size=58,y_center=1360)
