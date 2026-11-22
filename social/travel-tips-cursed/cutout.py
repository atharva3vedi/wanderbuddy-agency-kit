"""Knock the background off a cutout image and write a clean transparent PNG.

    python cutout.py sources/gun-src.png sources/gun.png

Used for the final slide, which composites a subject over the brand navy field
rather than over a photograph. Handles the two cases you actually get from stock
sites and screenshots:

  1. The file already has real transparency. Then we only trim the empty margin,
     because most "transparent PNG" downloads carry a lot of dead space that
     throws off the composition.
  2. The file has a flat background (white, black, checkerboard, whatever). Then
     we flood fill inward from every edge with a tolerance, which removes the
     surround without eating holes out of the subject the way a global colour
     key does.

The alpha edge gets a half pixel of feather so it does not read as a sticker
against the navy.
"""
import sys
from PIL import Image, ImageDraw, ImageFilter

TOL = 42          # per channel flood fill tolerance
FEATHER = 1.1     # gaussian radius on the alpha edge
PAD = 8           # transparent margin kept around the trimmed subject


def has_real_alpha(im):
    """True if the image carries transparency worth trusting."""
    if im.mode != "RGBA":
        return False
    alpha = im.getchannel("A")
    lo, hi = alpha.getextrema()
    if lo > 250:                       # fully opaque, the alpha is decorative
        return False
    # A real cutout has a meaningful share of fully transparent pixels.
    transparent = sum(c for v, c in enumerate(alpha.histogram()) if v < 8)
    return transparent > 0.02 * im.width * im.height


def strip_background(im):
    """Flood fill the surround from every border pixel and return an alpha mask."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    # Work on a paletted sentinel copy: flood fill marks background as magenta.
    marker = (255, 0, 255)
    work = rgb.copy()
    seeds = ([(x, 0) for x in range(0, w, 4)] + [(x, h - 1) for x in range(0, w, 4)] +
             [(0, y) for y in range(0, h, 4)] + [(w - 1, y) for y in range(0, h, 4)])
    for seed in seeds:
        if work.getpixel(seed) == marker:
            continue
        ImageDraw.floodfill(work, seed, marker, thresh=TOL)

    px_work, px_rgb = work.load(), rgb.load()
    alpha = Image.new("L", (w, h), 255)
    px_a = alpha.load()
    for y in range(h):
        for x in range(w):
            # Only treat it as background if the fill reached it AND the source
            # pixel was not already that magenta, so a genuinely magenta subject
            # survives.
            if px_work[x, y] == marker and px_rgb[x, y] != marker:
                px_a[x, y] = 0
    return alpha


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python cutout.py <in> <out.png>")
    src, dst = sys.argv[1], sys.argv[2]
    im = Image.open(src)
    im = im.convert("RGBA")

    if has_real_alpha(im):
        print("source already has transparency, trimming only")
    else:
        print("flat background detected, flood filling from the edges")
        im.putalpha(strip_background(im))

    im.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(FEATHER)))

    box = im.getchannel("A").getbbox()
    if box:
        l, t, r, b = box
        im = im.crop((max(0, l - PAD), max(0, t - PAD),
                      min(im.width, r + PAD), min(im.height, b + PAD)))

    im.save(dst)
    print(f"wrote {dst}  {im.width}x{im.height}")


if __name__ == "__main__":
    main()
