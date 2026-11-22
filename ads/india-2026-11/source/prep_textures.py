# Build phone-screen textures (status bar + live page capture) and rounded card textures with alpha.
from PIL import Image, ImageDraw, ImageFont
import os, sys
UI = 'E:/render/india-ads/ui'; OUT = 'E:/render/india-ads/tex'; os.makedirs(OUT, exist_ok=True)
S = 3; FONT = 'C:/Users/PC/Videos/WanderBuddy/website/public/fonts/Inter-Bold.ttf'
def status_bar(w, bg):
    bar = Image.new('RGB', (w, 47 * S), bg); d = ImageDraw.Draw(bar)
    ink = (11, 18, 32)
    f = ImageFont.truetype(FONT, 17 * S)
    d.text((52 * S, 25 * S), '9:41', font=f, fill=ink, anchor='mm')
    # signal bars
    x0 = 292 * S
    for i in range(4):
        h = (4 + i * 2.5) * S
        d.rounded_rectangle((x0 + i * 5.5 * S, 30 * S - h, x0 + i * 5.5 * S + 3.5 * S, 30 * S), radius=1 * S, fill=ink)
    # wifi: three arcs
    cx, cy = 327 * S, 31 * S
    for r in (4, 8, 12):
        d.arc((cx - r * S, cy - r * S, cx + r * S, cy + r * S), 225, 315, fill=ink, width=int(2.4 * S))
    d.ellipse((cx - 1.6 * S, cy - 3.6 * S, cx + 1.6 * S, cy - 0.4 * S), fill=ink)
    # battery
    bx, by = 344 * S, 20 * S
    d.rounded_rectangle((bx, by, bx + 25 * S, by + 12 * S), radius=3.5 * S, outline=ink, width=int(1.2 * S))
    d.rounded_rectangle((bx + 2 * S, by + 2 * S, bx + 20 * S, by + 10 * S), radius=2 * S, fill=ink)
    d.rounded_rectangle((bx + 26.5 * S, by + 4 * S, bx + 28 * S, by + 8 * S), radius=1 * S, fill=ink)
    return bar
for name in ['trip-root-bridge', 'trip-dawki', 'trip-mizoram', 'home-typed', 'trip-umngot', 'home-taj', 'trip-taj']:
    page = Image.open(f'{UI}/{name}.png').convert('RGB')
    bg = page.getpixel((page.width // 2, 4))
    scr = Image.new('RGB', (390 * S, 852 * S), bg)
    scr.paste(status_bar(390 * S, bg), (0, 0)); scr.paste(page, (0, 47 * S))
    scr.save(f'{OUT}/screen-{name}.png')
    print('screen', name, scr.size, bg)
def rounded_alpha(img, r):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=r, fill=255)
    out = img.convert('RGBA'); out.putalpha(m); return out
def cards_from(name, limit, tag):
    im = Image.open(f'{UI}/{name}.png').convert('RGB')
    bg = im.getpixel((5, im.height // 2)); x = 20 * S
    runs, start = [], None
    for y in range(0, im.height):
        p = im.getpixel((x, y)); inside = sum(abs(a - b) for a, b in zip(p, bg)) > 12
        if inside and start is None: start = y
        if not inside and start is not None:
            if y - start > 300 * S: runs.append((start, y))
            start = None
    got = []
    for k, (a, b) in enumerate(runs[:limit]):
        # extend a little: the run starts just below the rounded corner at x=20css
        # the run starts/ends where the rounded corner meets x=20css: about 5.4css inside the true edge
        a = max(0, a - 6 * S); b = min(im.height, b + 6 * S)
        c = im.crop((16 * S, a, (16 + 358) * S, b))
        rounded_alpha(c, 16 * S).save(f'{OUT}/card-{tag}{k}.png'); got.append(c.size)
    print('cards', name, got)
cards_from('trips-q-tall', 5, 'h')
cards_from('trips-q-cms', 2, 'c')
