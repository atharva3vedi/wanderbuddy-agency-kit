#!/usr/bin/env python3
"""
WanderBuddy — 8x10" printable store ad.

Builds a single 8x10 inch poster (2400x3000 px @ 300 DPI) that:
  * carries the WanderBuddy brand + tagline,
  * shows a fanned walkthrough of three real app screens,
  * lists every shipped feature in a compact two-column checklist,
  * ends with two scannable QR codes — one per store — each sitting under a
    faithfully drawn Google Play / App Store badge.

Everything is self-contained: the store badges and the QR codes are generated
at run time, so you only need Pillow + qrcode installed. Nothing is downloaded.

    pip install "qrcode[pil]" pillow
    python make_ad.py

Outputs (next to this script):
    wanderbuddy-store-ad.png   # 2400x3000, 300 DPI, print-ready
    wanderbuddy-store-ad.pdf   # same, as a single 8x10" page
"""

from __future__ import annotations

import math
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# --------------------------------------------------------------------------- #
# Paths & canvas
# --------------------------------------------------------------------------- #
SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parent.parent
SHOTS_DIR = REPO / "marketing" / "output" / "play-store"

DPI = 300
W, H = 8 * DPI, 10 * DPI          # 2400 x 3000
MARGIN = 130

OUT_PNG = SCRIPT_DIR / "wanderbuddy-store-ad.png"
OUT_PDF = SCRIPT_DIR / "wanderbuddy-store-ad.pdf"

# --------------------------------------------------------------------------- #
# Store links (single source of truth: website/src/lib/site.ts)
# --------------------------------------------------------------------------- #
PLAY_URL = "https://play.google.com/store/apps/details?id=com.wanderbuddy.wanderbuddy"
IOS_URL = "https://apps.apple.com/app/id6795848498"
SITE_URL = "wanderbuddyapp.com"

# --------------------------------------------------------------------------- #
# Brand palette (from lib/theme/app_colors.dart, dark scheme)
# --------------------------------------------------------------------------- #
INK = (11, 20, 31)          # #0B141F  bgPage
INK_2 = (18, 32, 46)        # #12202E  bgSubtle
SURFACE = (23, 41, 59)      # #17293B
AZURE = (63, 167, 230)      # #3FA7E6  primary
TEAL = (53, 201, 188)       # #35C9BC
AMBER = (240, 164, 49)      # #F0A431  accent
TEXT = (231, 241, 250)      # #E7F1FA
MUTED = (141, 167, 188)     # #8DA7BC
WHITE = (255, 255, 255)

# --------------------------------------------------------------------------- #
# Fonts
# --------------------------------------------------------------------------- #
FONT_DIR = Path("C:/Windows/Fonts")
_FONT_FILES = {
    "black": "seguibl.ttf",
    "bold": "segoeuib.ttf",
    "semibold": "seguisb.ttf",
    "regular": "segoeui.ttf",
}


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_DIR / _FONT_FILES[weight]
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


# --------------------------------------------------------------------------- #
# Small drawing helpers
# --------------------------------------------------------------------------- #
def text_w(draw: ImageDraw.ImageDraw, s: str, f: ImageFont.FreeTypeFont) -> int:
    l, t, r, b = draw.textbbox((0, 0), s, font=f)
    return r - l


def rounded(size, radius, fill) -> Image.Image:
    """A solid rounded-rectangle RGBA tile."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=fill)
    return img


def drop_shadow(tile: Image.Image, blur=28, alpha=150, offset=(0, 18)) -> Image.Image:
    """Return a shadow layer sized to fit `tile` + blur padding, and the paste
    offset. Used to place a soft shadow behind rounded tiles/phones."""
    pad = blur * 3
    shadow = Image.new("RGBA", (tile.width + pad * 2, tile.height + pad * 2), (0, 0, 0, 0))
    a = tile.split()[-1].point(lambda v: int(v * (alpha / 255)))
    black = Image.new("RGBA", tile.size, (0, 0, 0, 255))
    black.putalpha(a)
    shadow.paste(black, (pad + offset[0], pad + offset[1]), black)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    return shadow, pad


# --------------------------------------------------------------------------- #
# Background
# --------------------------------------------------------------------------- #
def make_background() -> Image.Image:
    """Ink-navy vertical gradient + a soft azure glow + faint skyline."""
    bg = Image.new("RGB", (W, H), INK)
    top = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / H
        # ease toward a slightly lighter navy at the middle, dark at edges
        k = math.sin(t * math.pi) * 0.5
        c = tuple(int(INK[i] + (INK_2[i] - INK[i]) * (0.25 + k)) for i in range(3))
        top.putpixel((0, y), c)
    bg = top.resize((W, H))

    # radial azure glow, upper area (behind the phones)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gx, gy, gr = W // 2, int(H * 0.34), int(W * 0.62)
    for i in range(gr, 0, -8):
        a = int(42 * (1 - i / gr))
        gd.ellipse([gx - i, gy - int(i * 0.72), gx + i, gy + int(i * 0.72)],
                   fill=(AZURE[0], AZURE[1], AZURE[2], a))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    bg = Image.alpha_composite(bg.convert("RGBA"), glow)

    # faint city skyline along the very bottom
    sky = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sky)
    base = H - 40
    x = -20
    rng = _prng(7)
    while x < W + 40:
        bw = 60 + int(next(rng) * 130)
        bh = 90 + int(next(rng) * 360)
        col = (255, 255, 255, 12)
        sd.rectangle([x, base - bh, x + bw, base], fill=col)
        # a couple of lit windows
        for _ in range(int(bh / 70)):
            wx = x + 12 + int(next(rng) * max(1, bw - 24))
            wy = base - bh + 14 + int(next(rng) * max(1, bh - 28))
            sd.rectangle([wx, wy, wx + 6, wy + 6], fill=(AZURE[0], AZURE[1], AZURE[2], 40))
        x += bw + 14
    bg = Image.alpha_composite(bg, sky)
    return bg.convert("RGB")


def _prng(seed: int):
    """Tiny deterministic 0..1 generator so the skyline is stable across runs."""
    s = seed
    while True:
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        yield s / 0x7FFFFFFF


# --------------------------------------------------------------------------- #
# Phone rendering (rounded screenshot with a thin device edge)
# --------------------------------------------------------------------------- #
def phone(shot_path: Path, target_w: int, angle: float = 0.0) -> Image.Image:
    src = Image.open(shot_path).convert("RGB")
    ratio = src.height / src.width
    target_h = int(target_w * ratio)
    src = src.resize((target_w, target_h), Image.LANCZOS)

    radius = int(target_w * 0.085)
    # rounded mask
    mask = Image.new("L", (target_w, target_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, target_w - 1, target_h - 1], radius=radius, fill=255)

    tile = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    tile.paste(src, (0, 0), mask)

    # thin bright edge for a "glass" device feel
    edge = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    ImageDraw.Draw(edge).rounded_rectangle(
        [1, 1, target_w - 2, target_h - 2], radius=radius,
        outline=(255, 255, 255, 60), width=3)
    tile = Image.alpha_composite(tile, edge)

    if angle:
        tile = tile.rotate(angle, expand=True, resample=Image.BICUBIC)
    return tile


def paste_phone(base: Image.Image, shot: str, target_w: int, center_x: int,
                top_y: int, angle: float = 0.0):
    tile = phone(SHOTS_DIR / shot, target_w, angle)
    shadow, pad = drop_shadow(tile, blur=30, alpha=130, offset=(0, 22))
    x = center_x - tile.width // 2
    base.alpha_composite(shadow, (x - pad, top_y - pad))
    base.alpha_composite(tile, (x, top_y))
    return top_y + tile.height


# --------------------------------------------------------------------------- #
# Store badges (drawn from scratch — no external image files needed)
# --------------------------------------------------------------------------- #
def _badge_shell(w: int, h: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(h * 0.22)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=(0, 0, 0, 255))
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r,
                        outline=(255, 255, 255, 120), width=3)
    return img, d


def google_play_badge(w: int, h: int) -> Image.Image:
    img, d = _badge_shell(w, h)

    # --- colored play triangle ---
    ih = int(h * 0.46)
    iw = int(ih * 0.9)
    ix = int(w * 0.10)
    iy = (h - ih) // 2
    A = (ix, iy)                      # top-left
    B = (ix, iy + ih)                # bottom-left
    O = (ix + int(iw * 0.30), iy + ih / 2)   # interior seam
    Tu = (ix + iw, iy + ih * 0.42)   # upper tip
    Tl = (ix + iw, iy + ih * 0.58)   # lower tip
    d.polygon([A, B, O], fill=(0, 181, 255))       # blue  (left)
    d.polygon([A, O, Tu], fill=(0, 214, 103))      # green (top)
    d.polygon([Tu, O, Tl], fill=(255, 206, 0))     # yellow(tip)
    d.polygon([Tl, O, B], fill=(255, 66, 77))      # red   (bottom)

    # --- text ---
    tx = ix + iw + int(w * 0.055)
    f_small = font("semibold", int(h * 0.15))
    f_big = font("bold", int(h * 0.315))
    d.text((tx, int(h * 0.21)), "GET IT ON", font=f_small, fill=(210, 214, 218))
    d.text((tx, int(h * 0.41)), "Google Play", font=f_big, fill=WHITE)
    return img


def _apple_mark(size: int) -> Image.Image:
    """A recognizable white Apple silhouette built from ellipses + a bite."""
    S = size * 4  # supersample
    mask = Image.new("L", (S, S), 0)
    m = ImageDraw.Draw(mask)

    cy = int(S * 0.62)
    r = int(S * 0.29)
    lx, rx = int(S * 0.37), int(S * 0.63)
    # two lobes + a bridge = rounded apple body
    m.ellipse([lx - r, cy - r, lx + r, cy + r], fill=255)
    m.ellipse([rx - r, cy - r, rx + r, cy + r], fill=255)
    m.rectangle([lx, cy - r, rx, cy + r], fill=255)
    # pull the bottom to a gentle point
    m.polygon([(lx - int(r * 0.55), cy), (rx + int(r * 0.55), cy),
               (int(S * 0.5), int(S * 0.94))], fill=255)
    # shallow top dimple between the humps (small, so it stays an apple)
    m.ellipse([int(S * 0.455), int(S * 0.28), int(S * 0.545), int(S * 0.40)], fill=0)

    # bite out of the right side
    bite_r = int(S * 0.155)
    m.ellipse([rx + int(r * 0.38) - bite_r, cy - bite_r,
               rx + int(r * 0.38) + bite_r, cy + bite_r], fill=0)

    # small leaf, angled off the top-right of the stem
    leaf = Image.new("L", (S, S), 0)
    ld = ImageDraw.Draw(leaf)
    lw, lh = int(S * 0.055), int(S * 0.11)
    lcx, lcy = int(S * 0.555), int(S * 0.17)
    ld.ellipse([lcx - lw, lcy - lh, lcx + lw, lcy + lh], fill=255)
    leaf = leaf.rotate(-40, center=(lcx, lcy), resample=Image.BICUBIC)
    mask = Image.composite(Image.new("L", (S, S), 255), mask, leaf)

    white = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    white.paste(WHITE + (255,), (0, 0), mask)
    return white.resize((size, size), Image.LANCZOS)


def app_store_badge(w: int, h: int) -> Image.Image:
    img, d = _badge_shell(w, h)

    mark = _apple_mark(int(h * 0.56))
    mx = int(w * 0.09)
    img.alpha_composite(mark, (mx, (h - mark.height) // 2 - int(h * 0.02)))

    tx = mx + mark.width + int(w * 0.05)
    f_small = font("semibold", int(h * 0.155))
    f_big = font("bold", int(h * 0.34))
    d.text((tx, int(h * 0.21)), "Download on the", font=f_small, fill=(210, 214, 218))
    d.text((tx, int(h * 0.40)), "App Store", font=f_big, fill=WHITE)
    return img


# --------------------------------------------------------------------------- #
# QR code (dark modules on a white rounded card)
# --------------------------------------------------------------------------- #
def qr_card(url: str, card: int) -> Image.Image:
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_M, border=0)
    qr.add_data(url)
    qr.make(fit=True)
    modules = qr.modules_count

    # Integer pixels-per-module so every module is exactly equal width -> crisp,
    # reliably scannable. Target ~80% of the card, snapped down to a whole scale.
    target = int(card * 0.80)
    box = max(1, target // modules)
    qr.box_size = box
    code = qr.make_image(fill_color=(12, 22, 34), back_color="white").convert("RGBA")

    tile = rounded((card, card), int(card * 0.12), WHITE + (255,))
    off = (card - code.width) // 2      # >= card*0.10 quiet zone on every side
    tile.alpha_composite(code, (off, off))
    return tile


# --------------------------------------------------------------------------- #
# Compose
# --------------------------------------------------------------------------- #
def main():
    canvas = make_background().convert("RGBA")
    d = ImageDraw.Draw(canvas)

    # ---- header ------------------------------------------------------------
    y = MARGIN - 20
    f_brand = font("black", 118)
    wander = "Wander"
    buddy = "Buddy"
    ww = text_w(d, wander, f_brand)
    bw = text_w(d, buddy, f_brand)
    bx = (W - (ww + bw)) // 2
    d.text((bx, y), wander, font=f_brand, fill=WHITE)
    d.text((bx + ww, y), buddy, font=f_brand, fill=AZURE)

    y += 150
    f_tag = font("semibold", 50)
    tag = "Travel together, perfectly in sync."
    d.text(((W - text_w(d, tag, f_tag)) // 2, y), tag, font=f_tag, fill=MUTED)

    # ---- fanned phones -----------------------------------------------------
    phones_top = y + 110
    # side phones first (behind), then center on top
    paste_phone(canvas, "screenshot-3-trip-vibe.png", 470,
                center_x=int(W * 0.235), top_y=phones_top + 120, angle=9)
    paste_phone(canvas, "screenshot-4-meet-travelers.png", 470,
                center_x=int(W * 0.765), top_y=phones_top + 120, angle=-9)
    paste_phone(canvas, "screenshot-community-live.png", 540,
                center_x=W // 2, top_y=phones_top)

    # ---- feature checklist -------------------------------------------------
    sec_y = phones_top + 1230
    f_sec = font("bold", 58)
    sec = "Everything your trip needs — in one app"
    d.text(((W - text_w(d, sec, f_sec)) // 2, sec_y), sec, font=f_sec, fill=TEXT)

    features = [
        "AI trip planner in seconds",
        "Trip Vibe personality radar",
        "Shared maps & live location",
        "Group chat + voice rooms",
        "Expenses that settle themselves",
        "Currency, visa & travel tips",
        "One-tap SOS safety",
        "Meet fellow travelers",
    ]
    f_feat = font("semibold", 43)
    col_x = [MARGIN + 40, W // 2 + 40]
    row_h = 92
    list_top = sec_y + 105
    for i, feat in enumerate(features):
        cx = col_x[i % 2]
        ry = list_top + (i // 2) * row_h
        # azure check chip
        chip = 46
        d.ellipse([cx, ry, cx + chip, ry + chip], fill=(AZURE[0], AZURE[1], AZURE[2], 45))
        d.line([(cx + 13, ry + 24), (cx + 21, ry + 33)], fill=AZURE, width=6)
        d.line([(cx + 21, ry + 33), (cx + 35, ry + 14)], fill=AZURE, width=6)
        d.text((cx + chip + 26, ry + 2), feat, font=f_feat, fill=TEXT)

    # ---- download section --------------------------------------------------
    dl_y = list_top + 4 * row_h + 55
    # divider
    d.line([(MARGIN, dl_y), (W - MARGIN, dl_y)], fill=(255, 255, 255, 30), width=2)
    dl_y += 48

    f_dl = font("black", 64)
    dl = "Download free today"
    d.text(((W - text_w(d, dl, f_dl)) // 2, dl_y), dl, font=f_dl, fill=WHITE)

    f_scan = font("semibold", 40)
    scan = "Scan a code to get WanderBuddy on your phone"
    d.text(((W - text_w(d, scan, f_scan)) // 2, dl_y + 82), scan,
           font=f_scan, fill=MUTED)

    # two QR + badge blocks
    block_top = dl_y + 165
    card = 380
    badge_w, badge_h = 400, 118
    gap_between_qr_badge = 26
    # horizontal placement: two blocks centered with a gap
    block_gap = 220
    total = card * 2 + block_gap
    left_x = (W - total) // 2
    centers = [left_x + card // 2, left_x + card + block_gap + card // 2]

    blocks = [
        (PLAY_URL, google_play_badge(badge_w, badge_h)),
        (IOS_URL, app_store_badge(badge_w, badge_h)),
    ]
    for cx, (url, badge) in zip(centers, blocks):
        qc = qr_card(url, card)
        shadow, pad = drop_shadow(qc, blur=26, alpha=90, offset=(0, 14))
        qx = cx - card // 2
        canvas.alpha_composite(shadow, (qx - pad, block_top - pad))
        canvas.alpha_composite(qc, (qx, block_top))
        by = block_top + card + gap_between_qr_badge
        canvas.alpha_composite(badge, (cx - badge_w // 2, by))

    badges_bottom = block_top + card + gap_between_qr_badge + badge_h

    # ---- footer ------------------------------------------------------------
    f_foot = font("semibold", 42)
    foot_y = badges_bottom + 48
    fw = text_w(d, SITE_URL, f_foot)
    # small azure dot before the url
    d.ellipse([(W - fw) // 2 - 44, foot_y + 12, (W - fw) // 2 - 22, foot_y + 34],
              fill=AZURE)
    d.text(((W - fw) // 2, foot_y), SITE_URL, font=f_foot, fill=TEXT)

    # ---- save --------------------------------------------------------------
    out = canvas.convert("RGB")
    out.save(OUT_PNG, "PNG", dpi=(DPI, DPI))
    out.save(OUT_PDF, "PDF", resolution=DPI)
    print(f"Wrote {OUT_PNG}  ({out.width}x{out.height} px, {DPI} DPI)")
    print(f"Wrote {OUT_PDF}  (8x10 in)")


if __name__ == "__main__":
    main()
