"""Airport poster for wanderbuddyapp.com, 24 x 36 in (2:3).

The one picture is a real photograph of Earth: NASA DSCOVR/EPIC, 2026-09-15
04:07 UTC, looking down on 6.7N 118.0E (public domain, epic.gsfc.nasa.gov).
Every city is projected onto that photo from its real coordinates, so it sits
where it really is: everyone flies in to Bali at once.

Print set-up: every photographic layer (space, atmosphere, globe, shading, the
fade, arc glow, grain) is baked into one 160 dpi JPEG that runs 0.125 in past
the trim on every side (the bleed); arcs, type and the QR codes stay vector on
top of it, so the PDF is small and the QR edges are sharp.

  python -I build.py [24x36|8x10]   writes background.jpg + poster.html into out/ (or out/8x10/)
  bash render.sh [24x36|8x10]       prints out/poster-print.pdf (24.25 x 36.25 in with trim
                          and bleed boxes, for the printer), out/poster.pdf (trimmed)
                          and out/poster.png (3840 x 5760, trimmed)

QR codes: App Store, Google Play, wanderbuddyapp.com/partners. Edit URLS below.
"""
import math
import os
import sys

import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src', 'epic_1b_20260915041237.png')
FONTS = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'metrics', 'fonts')).replace('\\', '/')

URLS = {
    'ios': 'https://apps.apple.com/app/id6795848498',
    'android': 'https://play.google.com/store/apps/details?id=com.wanderbuddy.wanderbuddy',
    'partners': 'https://wanderbuddyapp.com/partners',
}

# Each print size: poster space is 1200 CSS px across; `inch` says how many make an
# inch, `dpi` the raster resolution. Positions below are in that CSS space.
#   gy, gr       globe centre (x is always 600) and radius
#   fade         where the globe starts sinking into the ink, and over how far
#   horizon      rows where the Earth rises in front of "Everyone's"
#   css          layout overrides on top of poster.tpl.html (which is laid out for 24x36)
FORMATS = {
    '24x36': dict(h=1800, inch=50, dpi=160, out='out', gy=848, gr=620, fade=(1030, 360),
                  horizon=(100, 330), jet=1.3, css=''),
    # 4:5, so the globe is a whole disc between the two words and the lists tighten.
    '8x10': dict(h=1500, inch=150, dpi=320, out='out/8x10', gy=700, gr=480, fade=(880, 300),
                 horizon=(90, 300), jet=1.1, css='''
  .top { top: 30px; }
  .w1 { top: 92px; }
  .w2 { top: 880px; }
  .cols { top: 1068px; }
  .col h2 { font-size: 28px; margin-bottom: 6px; }
  .col li { font-size: 21px; padding: 9px 0; }
  .qrs { margin-top: 16px; }
  .tile { width: 172px; }
  .tile svg { width: 152px; height: 152px; }
  .tile b { font-size: 18px; }
  .url { font-size: 23px; }'''),
}
FMT_NAME = sys.argv[1] if len(sys.argv) > 1 else '24x36'
FMT = FORMATS[FMT_NAME]
OUT = os.path.join(HERE, FMT['out'])
W, H = 1200, FMT['h']
S = FMT['dpi'] / FMT['inch']        # print px per CSS px
BLEED = FMT['inch'] / 8             # 0.125 in
SW, SH = round((W + 2 * BLEED) * S), round((H + 2 * BLEED) * S)   # the sheet, with bleed
GX, GY, GR = 600, FMT['gy'], FMT['gr']
FADE_T, FADE_H = FMT['fade']
HORIZON_T, HORIZON_B = FMT['horizon']

INK = (11, 20, 31)
AZURE = (63, 167, 230)
TEAL = (53, 201, 188)

# The photo's sub-satellite point (EPIC metadata for this frame).
LAT0, LON0 = math.radians(6.7), math.radians(118.0)

DEST = ('DPS', -8.75, 115.17)
ORIGINS = [
    ('HND', 35.55, 139.78),
    ('ICN', 37.46, 126.44),
    ('HKG', 22.31, 113.91),
    ('BKK', 13.69, 100.75),
    ('SIN', 1.36, 103.99),
    ('MNL', 14.51, 121.02),
]
SWEEP = 0.28                        # how far each route bows, as a share of its length
JET_AT = {'MNL': 0.4, 'SIN': 0.5}  # where along the route its jet is; default 0.45


def unit(lat, lon):
    """Lat/lon to a unit vector in view space: x east, y north, z at the camera."""
    la, lo = math.radians(lat), math.radians(lon)
    x = math.cos(la) * math.sin(lo - LON0)
    y = math.cos(LAT0) * math.sin(la) - math.sin(LAT0) * math.cos(la) * math.cos(lo - LON0)
    z = math.sin(LAT0) * math.sin(la) + math.cos(LAT0) * math.cos(la) * math.cos(lo - LON0)
    return np.array([x, y, z])


def screen(v):
    return GX + v[0] * GR, GY - v[1] * GR


def flights():
    """Every arc as poster points, plus where its jet and its code go.

    Cities sit exactly where the photo has them. Seen from straight above,
    true great circles into Bali read as straight spokes, so each route is drawn
    with the same clockwise sweep instead: the flights swirl in to land.
    """
    d = unit(DEST[1], DEST[2])
    dx, dy = screen(d)
    out = []
    for code, lat, lon in ORIGINS:
        ox, oy = screen(unit(lat, lon))
        vx, vy = dx - ox, dy - oy
        ln = math.hypot(vx, vy)
        # Control point: the midpoint pushed to the left of the direction of travel.
        cx, cy = ox + vx / 2 + vy / ln * SWEEP * ln, oy + vy / 2 - vx / ln * SWEEP * ln
        pts = []
        for i in range(201):
            t = i / 200
            pts.append(((1 - t) ** 2 * ox + 2 * (1 - t) * t * cx + t * t * dx,
                        (1 - t) ** 2 * oy + 2 * (1 - t) * t * cy + t * t * dy))
        k = round(JET_AT.get(code, 0.45) * 200)
        (x1, y1), (x2, y2) = pts[k - 3], pts[k + 3]
        ux, uy = ox - dx, oy - dy
        n = math.hypot(ux, uy) or 1
        out.append({
            'code': code, 'pts': pts, 'jet': pts[k],
            'rot': math.degrees(math.atan2(y2 - y1, x2 - x1)),
            # The code sits on the far side of the city from Bali.
            'label': (ox + ux / n * 30, oy + uy / n * 30 + 7),
            'anchor': 'start' if ux > 20 else 'end' if ux < -20 else 'middle',
        })
    return out, (dx, dy)


def stops(v, table):
    """Piecewise-linear lookup: table is [(position, value), ...] sorted."""
    xs, ys = zip(*table)
    return np.interp(v, xs, ys)


def globe_rgba():
    """Cut the disc out of the photo, grade it, size it for print."""
    a = np.asarray(Image.open(SRC).convert('RGB')).astype(np.float32) / 255.0
    ys, xs = np.nonzero(a.mean(axis=2) > 10 / 255)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    r = ((xs.max() - xs.min()) + (ys.max() - ys.min())) / 4
    # Lift the haze, then contrast and a little more colour.
    g = np.clip((a - 0.03) / 0.94, 0, 1) ** 1.18
    grey = g.mean(axis=2, keepdims=True)
    g = np.clip(grey + (g - grey) * 1.35, 0, 1)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    alpha = np.clip((r + 0.5 - np.hypot(xx - cx, yy - cy)) / 1.5, 0, 1)
    img = Image.fromarray((np.concatenate([g, alpha[..., None]], axis=2) * 255).round().astype(np.uint8), 'RGBA')
    pad = 2
    img = img.crop((int(cx - r - pad), int(cy - r - pad), int(cx + r + pad), int(cy + r + pad)))
    disp = 2 * GR + 2 * pad * GR / r                 # CSS px, disc diameter plus the pad
    size = round(disp * S)
    img = img.resize((size, size), Image.LANCZOS)
    al = img.getchannel('A')
    rgb = img.convert('RGB').filter(ImageFilter.UnsharpMask(radius=2.4, percent=80, threshold=2))
    left, top = round((GX - disp / 2 + BLEED) * S), round((GY - disp / 2 + BLEED) * S)
    return np.asarray(rgb).astype(np.float32) / 255.0, np.asarray(al).astype(np.float32) / 255.0, left, top


def glow_layers(fl, dest):
    """Blurred light under the arcs and soft shade under the codes, at print size."""
    def px(x, y):
        return (x + BLEED) * S, (y + BLEED) * S

    light = Image.new('L', (SW, SH), 0)
    dl = ImageDraw.Draw(light)
    for f in fl:
        dl.line([px(x, y) for x, y in f['pts']], fill=150, width=round(7 * S), joint='curve')
    dx, dy = dest
    dl.ellipse([*px(dx - 34, dy - 34), *px(dx + 34, dy + 34)], fill=255)
    light = light.filter(ImageFilter.GaussianBlur(9 * S))
    shade = Image.new('L', (SW, SH), 0)
    ds = ImageDraw.Draw(shade)
    for f in fl:
        lx, ly = f['label']
        w = 64
        x0 = lx if f['anchor'] == 'start' else lx - w if f['anchor'] == 'end' else lx - w / 2
        ds.rounded_rectangle([*px(x0 - 8, ly - 24), *px(x0 + w + 8, ly + 8)], radius=round(14 * S), fill=200)
    ds.rounded_rectangle([*px(dx + 50, dy - 26), *px(dx + 140, dy + 18)], radius=round(18 * S), fill=200)
    shade = shade.filter(ImageFilter.GaussianBlur(10 * S))
    return np.asarray(light), np.asarray(shade)


def background(fl, dest):
    """Bake the photographic layers at print size.

    Rows between HORIZON_T and HORIZON_B are split in two: the space behind
    (in background.jpg) and the planet's horizon with its atmosphere (in
    horizon.png, with alpha), so the top word can sit between them, behind the
    Earth. Everywhere else background.jpg holds the finished picture.
    """
    Wp, Hp = SW, SH
    grgb, galpha, gl, gt = globe_rgba()
    light, shade = glow_layers(fl, dest)
    ink = np.array(INK, np.float32) / 255
    azure = np.array(AZURE, np.float32) / 255
    teal = np.array(TEAL, np.float32) / 255
    space = np.array((18, 48, 77), np.float32) / 255
    night = np.array((4, 10, 18), np.float32) / 255
    rim = np.array((155, 211, 245), np.float32) / 255
    rng = np.random.default_rng(7)
    out = np.empty((Hp, Wp, 3), np.uint8)
    hz0, hz1 = round((HORIZON_T + BLEED) * S), round((HORIZON_B + BLEED) * S)
    horizon = np.zeros((hz1 - hz0, Wp, 4), np.uint8)
    xs = (np.arange(Wp, dtype=np.float32) + 0.5) / S - BLEED
    cuts = sorted(set([0, hz0, hz1, Hp] + list(range(hz1, Hp, 600))))
    for y0, y1 in zip(cuts, cuts[1:]):
        rows = y1 - y0
        ys = (np.arange(y0, y1, dtype=np.float32) + 0.5) / S - BLEED
        X, Y = np.meshgrid(xs, ys)
        d = np.hypot(X - GX, Y - GY) / GR
        base = np.broadcast_to(ink, (rows, Wp, 3)).copy()
        cp = np.zeros((rows, Wp, 3), np.float32)      # the planet layer, premultiplied
        A = np.zeros((rows, Wp, 1), np.float32)

        def lay(col, a):
            nonlocal cp, A
            a = a[..., None] if a.ndim == 2 else a
            cp = col * a + cp * (1 - a)
            A = a + A * (1 - a)

        # Deep blue light in space around the planet.
        a = (0.9 * np.clip(1 - d / 1.45, 0, 1))[..., None]
        base = base * (1 - a) + space * a
        # Atmosphere, the photo, night on the far limb, a thin rim of light.
        mix = np.clip((d - 1.0) / 0.045, 0, 1)[..., None]
        lay(azure * (1 - mix) + teal * mix, stops(d, [(0.93, 0), (1.0, 0.6), (1.045, 0.18), (1.17, 0)]))
        ga = np.zeros((rows, Wp, 1), np.float32)
        gc = np.zeros((rows, Wp, 3), np.float32)
        gy0, gy1 = max(y0, gt), min(y1, gt + grgb.shape[0])
        if gy0 < gy1:
            gx0, gx1 = max(0, gl), min(Wp, gl + grgb.shape[1])
            ga[gy0 - y0:gy1 - y0, gx0:gx1, 0] = galpha[gy0 - gt:gy1 - gt, gx0 - gl:gx1 - gl]
            gc[gy0 - y0:gy1 - y0, gx0:gx1] = grgb[gy0 - gt:gy1 - gt, gx0 - gl:gx1 - gl]
        lay(gc, ga)
        inside = np.clip((1 - d) * GR * S / 1.5 + 0.5, 0, 1)
        dl = np.hypot(X - (GX - 0.4 * GR), Y - (GY - 0.55 * GR)) / (1.8 * GR)
        lay(night, 0.62 * np.clip((dl - 0.4) / 0.6, 0, 1) ** 1.4 * inside)
        lay(rim, 0.5 * np.exp(-(((d - 1) * GR) / 1.6) ** 2))
        # The globe sinks into the ink under the headline.
        f = stops((Y - FADE_T) / FADE_H, [(0, 0), (0.45, 0.55), (0.92, 1.0)])[..., None]
        base = base * (1 - f) + ink * f
        cp = cp * (1 - f) + ink * f * A
        img = cp + base * (1 - A)
        # Arc glow (screen) and the shade under the codes (multiply).
        li = light[y0:y1].astype(np.float32)[..., None] / 255
        img = 1 - (1 - img) * (1 - azure * 0.55 * li)
        img = img * (1 - 0.55 * shade[y0:y1].astype(np.float32)[..., None] / 255)
        # Film grain, strongest in the mid tones; one field for both layers.
        lum = img.mean(axis=2, keepdims=True)
        n = rng.normal(0, 1, (rows, Wp, 1)).astype(np.float32) * 0.03 * (0.35 + 2.6 * lum * (1 - lum))
        if y0 >= hz0 and y1 <= hz1:
            out[y0:y1] = (np.clip(base + n, 0, 1) * 255 + 0.5).astype(np.uint8)
            col = cp / np.maximum(A, 1e-4) + n
            horizon[y0 - hz0:y1 - hz0] = (np.clip(np.concatenate([col, A], axis=2), 0, 1) * 255 + 0.5).astype(np.uint8)
        else:
            out[y0:y1] = (np.clip(img + n, 0, 1) * 255 + 0.5).astype(np.uint8)
    Image.fromarray(out, 'RGB').save(os.path.join(OUT, 'background.jpg'), quality=93, subsampling=0, dpi=(160, 160))
    Image.fromarray(horizon, 'RGBA').save(os.path.join(OUT, 'horizon.png'), optimize=True)


PLANE = ('M14,0C14,-1.3 12.6,-1.8 11,-1.8L3.2,-1.8L-3,-12.5L-6.2,-12.5L-1.8,-1.8L-9,-1.8'
         'L-11.6,-5.8L-13.8,-5.8L-12.2,-1.4L-12.2,1.4L-13.8,5.8L-11.6,5.8L-9,1.8L-1.8,1.8'
         'L-6.2,12.5L-3,12.5L3.2,1.8L11,1.8C12.6,1.8 14,1.3 14,0Z')


def flights_svg(fl, dest):
    dx, dy = dest
    defs, paths, dots, jets, codes = [], [], [], [], []
    for i, f in enumerate(fl):
        ox, oy = f['pts'][0]
        defs.append(f'<linearGradient id="g{i}" gradientUnits="userSpaceOnUse" x1="{ox:.1f}" y1="{oy:.1f}" '
                    f'x2="{dx:.1f}" y2="{dy:.1f}"><stop offset="0" stop-color="#fff" stop-opacity=".45"/>'
                    f'<stop offset="1" stop-color="#fff"/></linearGradient>')
        paths.append('<path stroke="url(#g%d)" d="M%s"/>' % (i, ' L'.join(f'{x:.1f},{y:.1f}' for x, y in f['pts'])))
        jx, jy = f['jet']
        jets.append(f'<path d="{PLANE}" transform="translate({jx:.1f} {jy:.1f}) rotate({f["rot"]:.1f}) scale({FMT["jet"]})"/>')
        dots.append(f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="12" class="halo"/><circle cx="{ox:.1f}" cy="{oy:.1f}" r="5.5" class="dot"/>')
        lx, ly = f['label']
        codes.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{f["anchor"]}">{f["code"]}</text>')
    hub = (f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="48" class="ring2"/><circle cx="{dx:.1f}" cy="{dy:.1f}" r="26" class="ring"/>'
           f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="9" class="dot"/><text x="{dx + 60:.1f}" y="{dy + 10:.1f}" class="dest">{DEST[0]}</text>')
    return ('<defs>' + ''.join(defs) + '</defs><g class="arcs">' + ''.join(paths) + '</g><g class="jets">' + ''.join(jets)
            + '</g><g class="dots">' + ''.join(dots) + hub + '</g><g class="codes">' + ''.join(codes) + '</g>')


def qr_svg(url):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0, box_size=1)
    q.add_data(url)
    q.make(fit=True)
    m = q.get_matrix()
    quiet = 4
    cells = ''.join(f'M{x + quiet},{y + quiet}h1v1h-1z' for y, row in enumerate(m) for x, on in enumerate(row) if on)
    v = len(m) + 2 * quiet
    return (f'<svg viewBox="0 0 {v} {v}" shape-rendering="crispEdges" aria-label="{url}">'
            f'<rect width="{v}" height="{v}" fill="#fff"/><path d="{cells}" fill="#0B141F"/></svg>')


MARK = ('<svg viewBox="0 0 1024 1024" class="mark" aria-hidden="true"><defs><linearGradient id="mk" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#2E8AD3"/><stop offset="1" stop-color="#175A97"/></linearGradient></defs>'
        '<rect width="1024" height="1024" rx="220" fill="url(#mk)"/>'
        '<polygon points="224,512 404,296 494,422 602,224 800,512" fill="#fff"/>'
        '<path d="M 217 620 Q 290 584 364 620 T 512 620 T 660 620 T 807 620 L 807 692 L 217 692 Z" fill="#fff"/></svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    fl, dest = flights()
    background(fl, dest)
    tpl = open(os.path.join(HERE, 'poster.tpl.html'), encoding='utf-8').read()
    html = (tpl.replace('%%FONTS%%', 'file:///' + FONTS)
               .replace('%%W%%', str(W)).replace('%%H%%', str(H)).replace('%%FMT_CSS%%', FMT['css'])
               .replace('%%PAGE_W%%', f'{W / FMT["inch"] + 0.25:g}').replace('%%PAGE_H%%', f'{H / FMT["inch"] + 0.25:g}')
               .replace('%%ZOOM%%', f'{96 / FMT["inch"]:g}')
               .replace('%%B%%', str(BLEED)).replace('%%SW%%', str(W + 2 * BLEED)).replace('%%SH%%', str(H + 2 * BLEED))
               .replace('%%HZ_T%%', str(HORIZON_T)).replace('%%HZ_H%%', str(HORIZON_B - HORIZON_T))
               .replace('%%FLIGHTS%%', flights_svg(fl, dest))
               .replace('%%MARK%%', MARK)
               .replace('%%QR_IOS%%', qr_svg(URLS['ios']))
               .replace('%%QR_ANDROID%%', qr_svg(URLS['android']))
               .replace('%%QR_PARTNERS%%', qr_svg(URLS['partners'])))
    open(os.path.join(OUT, 'poster.html'), 'w', encoding='utf-8').write(html)
    # What render.sh needs to print this size.
    env = dict(WIN_W=math.ceil(W + 2 * BLEED), WIN_H=math.ceil(H + 2 * BLEED), DSF=f'{S:.6f}', SHEET_W=SW, SHEET_H=SH,
               BLEED_PX=round(BLEED * S), DPI=FMT['dpi'], PREVIEW_W=800, PREVIEW_H=round(800 * H / W))
    open(os.path.join(OUT, 'render.env'), 'w').write(''.join(f'export {k}={v}\n' for k, v in env.items()))
    print('wrote', os.path.join(OUT, 'poster.html'))


if __name__ == '__main__':
    main()
