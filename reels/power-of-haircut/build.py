"""Power-of-haircut reel stills: before (old July UI), after (current redesign),
side-by-side pairs, and pairs of the 3 badly designed mockups (bad/) vs now.

Run from repo root:  python marketing/Reels/power-of-haircut/build.py
Inputs: assets/Screenshots (old UI, Jul 2026) and
store/graphics/appstore/build/screens_v2 (current UI, re-shot by the flutter harness).
"""
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
OLD = ROOT / "assets" / "Screenshots"
NEW = ROOT / "store" / "graphics" / "appstore" / "build" / "screens_v2"


def old(n):
    return Image.open(next(OLD.glob(f"Screenshot_{n}_*.png"))).convert("RGB")


# (label, old screenshot number, new capture name): same job, before vs after.
PAIRS = [
    ("01_home", 9, "home"),
    ("02_itinerary", 15, "plan"),
    ("03_budget", 16, "budget"),
    ("04_visa_vs_prepare", 1, "prepare"),
    ("05_translate", 22, "translate"),
    ("06_ai_chat_vs_reels", 20, "reels"),
    ("07_members_vs_vote", 17, "vote"),
    ("08_light_home_vs_map", 36, "map"),
]
AFTER_EXTRA = ["plan_more", "ideas", "dates", "live", "map_overlay"]


def copy_raw():
    for d in ("before", "after", "pairs", "broken"):
        (OUT / d).mkdir(exist_ok=True)
    for label, n, name in PAIRS:
        old(n).save(OUT / "before" / f"{label}.png")
        shutil.copy(NEW / f"{name}.png", OUT / "after" / f"{label}.png")
    for i, name in enumerate(AFTER_EXTRA, start=len(PAIRS) + 1):
        shutil.copy(NEW / f"{name}.png", OUT / "after" / f"{i:02d}_{name}.png")


def rounded(im, r):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *im.size), r, fill=255)
    out = Image.new("RGBA", im.size)
    out.paste(im, (0, 0), mask)
    return out


def pair_frame(a, b):
    """1080x1920 split frame: before on the left, after on the right, no text."""
    W, H = 1080, 1920
    canvas = Image.new("RGB", (W, H), (11, 18, 28))
    pw = 500
    for i, im in enumerate((a, b)):
        ph = int(im.height * pw / im.width)
        if ph > H - 80:
            ph = H - 80
            im = im.crop((0, 0, im.width, int(ph * im.width / pw)))
        p = rounded(im.resize((pw, ph), Image.LANCZOS), 36)
        canvas.paste(p, (27 + i * (pw + 26), (H - ph) // 2), p)
    return canvas


def build_pairs():
    for label, n, name in PAIRS:
        pair_frame(old(n), Image.open(NEW / f"{name}.png").convert("RGB")).save(
            OUT / "pairs" / f"{label}.png")


def main():
    copy_raw()
    build_pairs()
    # broken/ = plain badly designed mockups, rendered first by bad/render.mjs
    for name, new in (("01_home", "home"), ("02_plan", "plan"), ("03_budget", "budget")):
        bad = OUT / "broken" / f"{name}.png"
        if bad.exists():
            pair_frame(Image.open(bad).convert("RGB"), Image.open(NEW / f"{new}.png").convert("RGB")).save(
                OUT / "pairs" / f"bad_vs_new_{name}.png")
    print("done ->", OUT)


if __name__ == "__main__":
    main()
