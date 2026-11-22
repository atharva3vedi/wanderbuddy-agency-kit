# Writes spec.json for build_ad.py: per ad and size, a photo crop placed so the subject sits clear of the phone.
from PIL import Image
import json, os, sys
R = 'E:/render/india-ads'; P = f'{R}/photos'; T = f'{R}/tex'; C = f'{R}/crops'; os.makedirs(C, exist_ok=True)
SIZES = {'45': (1080, 1350), '916': (1080, 1920)}
VFOV = 36 / 50; D = 0.32

def crop(src, name, size, subject, target, zoom=1.0, trim_bottom=0.0):
    im = Image.open(f'{P}/{src}.jpg').convert('RGB')
    sw, sh = im.size; sh_eff = sh * (1 - trim_bottom)
    W, H = size; a = W / H
    ch = sh_eff / zoom; cw = ch * a
    if cw > sw: cw = sw; ch = cw / a
    left = subject[0] * sw - target[0] * cw; top = subject[1] * sh - target[1] * ch
    left = max(0, min(sw - cw, left)); top = max(0, min(sh_eff - ch, top))
    out = im.crop((int(left), int(top), int(left + cw), int(top + ch))).resize((int(W * 1.1), int(H * 1.1)), Image.LANCZOS)
    path = f'{C}/{name}.jpg'; out.save(path, quality=95); return path

def extend_sky(src, name, size, width_frac):
    # The Taj photo is wide; for portrait frames, continue its plain hazy sky upward (blurred top band, stretched).
    from PIL import ImageFilter
    im = Image.open(f'{P}/{src}.jpg').convert('RGB'); sw, sh = im.size
    cw = int(sw * width_frac); left = (sw - cw) // 2; im = im.crop((left, 0, left + cw, sh))
    W, H = size; th = int(cw * H / W); ext = max(0, th - sh)
    # plain vertical gradient from the photo's top-row haze colour, a touch lighter towards the top
    strip = im.crop((0, 0, cw, 24)).resize((1, 1), Image.BOX).getpixel((0, 0))
    lite = tuple(min(255, int(c * 1.05 + 6)) for c in strip)
    grad = Image.linear_gradient('L').resize((1, ext))  # 0 at top -> 255 at seam
    band = Image.composite(Image.new('RGB', (1, ext), strip), Image.new('RGB', (1, ext), lite), grad).resize((cw, ext))
    canvas = Image.new('RGB', (cw, th)); canvas.paste(band, (0, 0)); canvas.paste(im, (0, ext))
    F = 80; fm = Image.linear_gradient('L').resize((cw, F))  # photo fades in over its top 80 px
    seam = Image.composite(im.crop((0, 0, cw, F)), Image.new('RGB', (cw, F), strip), fm); canvas.paste(seam, (0, ext))
    out = canvas.resize((int(W * 1.1), int(H * 1.1)), Image.LANCZOS); path = f'{C}/{name}.jpg'; out.save(path, quality=95); return path

def phone_at(size, cx, cy, height_frac, **kw):
    W, H = size; fh = VFOV * D; fw = fh * W / H
    scale = height_frac * fh / 0.1486
    return dict(loc=((cx - 0.5) * fw, 0, (0.5 - cy) * fh), scale=scale, **kw)

ADS = [
  dict(name='root-bridge', photo='root-bridge', screen='trip-root-bridge', subject=(0.545, 0.56),
       t={'45': (0.30, 0.62), '916': (0.32, 0.60)}, zoom={'45': 1.0, '916': 1.0}),
  dict(name='umngot', photo='umngot', screen='trip-umngot', subject=(0.845, 0.42), trim=0.07, side='left',
       t={'45': (0.72, 0.55), '916': (0.70, 0.55)}, zoom={'45': 1.0, '916': 1.0}),
  dict(name='mizoram', photo='hmuifang', screen='trip-mizoram', subject=(0.88, 0.75), side='left',
       t={'45': (0.74, 0.74), '916': (0.72, 0.72)}, zoom={'45': 1.0, '916': 1.0}),
  dict(name='taj', photo='taj', screen='trip-taj', subject=(0.5, 0.42),
       t={'45': (0.44, 0.47), '916': (0.33, 0.47)}, zoom={'45': 1.0, '916': 1.0}, p45=(0.74, 0.66, 0.50), extend={'45': 1.0, '916': 0.72}),
]
shots = []
for ad in ADS:
    for k, size in SIZES.items():
        if ad.get('extend'): crop_path = extend_sky(ad['photo'], f"{ad['name']}-{k}", size, ad['extend'][k])
        else: crop_path = crop(ad['photo'], f"{ad['name']}-{k}", size, ad['subject'], ad['t'][k], ad['zoom'][k], ad.get('trim', 0))
        left = ad.get('side') == 'left'; sgn = -1 if left else 1
        cx = (0.31 if left else 0.69) if k == '45' else (0.36 if left else 0.64)
        pcx, pcy, phf = (cx, 0.62, 0.60) if k == '45' else (cx, 0.555, 0.46)
        if k == '45' and ad.get('p45'): pcx, pcy, phf = ad['p45']
        ph = phone_at(size, pcx, pcy, phf, turn=-16 * sgn, lean=4, roll=-4 * sgn)
        shots.append(dict(name=f"{ad['name']}-{k}", res=list(size), mode='photo', photo_crop=crop_path,
                          screen=f"{T}/screen-{ad['screen']}.png", phone=ph, fstop=ad.get('fstop', 26),
                          out=f"{R}/renders/{ad['name']}-{k}.png"))
# finder: studio backdrop, phone with the typed search, real result cards floating around it
for k, size in SIZES.items():
    W, H = size; fh = VFOV * D; fw = fh * W / H
    ph = phone_at(size, 0.50, 0.63 if k == '45' else 0.555, 0.56 if k == '45' else 0.44, turn=-10, lean=3, roll=-2)
    sx = fw / 0.1843
    cards = [
        dict(tex=f'{T}/card-h3.png', loc=(-0.050 * sx, 0.045, 0.012), rz=9, rx=-3, ry=-2, w=0.060, emit=0.22),
        dict(tex=f'{T}/card-c1.png', loc=(0.052 * sx, 0.060, 0.004), rz=-9, rx=-3, ry=3, w=0.060, emit=0.22),
        dict(tex=f'{T}/card-h1.png', loc=(-0.047 * sx, 0.030, -0.066), rz=5, rx=2, ry=-3, w=0.056, emit=0.22),
        dict(tex=f'{T}/card-h4.png', loc=(0.047 * sx, -0.035, -0.062), rz=-11, rx=4, ry=4, w=0.052, emit=0.22),
    ]
    if k == '916':  # keep the bottom-left clear for the logo: drop the lower-left card, lift the front one
        cards = [cards[0], cards[1], dict(cards[3], loc=(0.047 * sx, -0.035, -0.050))]
    shots.append(dict(name=f'finder-{k}', res=list(size), mode='studio', screen=f'{T}/screen-home-typed.png',
                      phone=ph, cards=cards, fstop=5.6, backdrop_dist=0.30, key=4.5, fill=1.2, world=0.25,
                      bg_top=(0.93, 0.96, 0.99), bg_bottom=(0.78, 0.86, 0.94), out=f'{R}/renders/finder-{k}.png'))
json.dump({'shots': shots}, open(f'{R}/scripts/spec.json', 'w'), indent=1)
print(len(shots), 'shots')
