"""Deterministic 1080x1920 transparent overlays (never let the video model render text):
type labels, dialogue captions, supers, and the plug's real-app pop-in cards."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
REPO = Path(__file__).resolve().parents[4]
FONT_B = str(REPO / "assets/fonts/Inter-Bold.ttf")
FONT_R = str(REPO / "assets/fonts/Inter-Regular.ttf")
AMBER = (255, 184, 28)
NAVY = (12, 27, 51)


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def _wrap(draw: ImageDraw.ImageDraw, text: str, f, max_w: int) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split():
            trial = f"{cur} {word}".strip()
            if draw.textlength(trial, font=f) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def label(text: str, sub: str | None, out: Path, y: int = 210) -> None:
    """White pill with black type at the top: the stereotype's name."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f1, f2 = font(66), font(40, bold=False)
    l1 = _wrap(d, text, f1, 900)
    l2 = _wrap(d, sub, f2, 880) if sub else []
    h1, h2 = 80, 52
    box_w = max([d.textlength(s, font=f1) for s in l1] + [d.textlength(s, font=f2) for s in l2]) + 80
    box_h = len(l1) * h1 + len(l2) * h2 + (14 if l2 else 0) + 52
    x0 = (W - box_w) / 2
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([x0, y + 8, x0 + box_w, y + 8 + box_h], 34, fill=(0, 0, 0, 110))
    im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y, x0 + box_w, y + box_h], 34, fill=(255, 255, 255, 255))
    cy = y + 26
    for s in l1:
        d.text((W / 2, cy), s, font=f1, fill=(0, 0, 0), anchor="ma")
        cy += h1
    cy += 14 if l2 else 0
    for s in l2:
        d.text((W / 2, cy), s, font=f2, fill=(0, 0, 0), anchor="ma")
        cy += h2
    im.save(out)


def stroke_text(text: str, out: Path, size: int = 64, cy: int = 1440, color=(255, 255, 255), max_w: int = 940) -> None:
    """Centered white text with a heavy black stroke (dialogue captions and supers)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font(size)
    lines = _wrap(d, text, f, max_w)
    lh = int(size * 1.22)
    y = cy - (len(lines) * lh) / 2
    for s in lines:
        d.text((W / 2, y), s, font=f, fill=color, anchor="ma", stroke_width=max(6, size // 9), stroke_fill=(0, 0, 0))
        y += lh
    im.save(out)


def hook(title: str, tag: str, out: Path) -> None:
    """Cold-open hook: big headline + amber part tag."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font(86)
    lines = _wrap(d, title, f, 960)
    y = 1230
    for s in lines:
        d.text((W / 2, y), s, font=f, fill=(255, 255, 255), anchor="ma", stroke_width=9, stroke_fill=(0, 0, 0))
        y += 104
    ft = font(54)
    tw = d.textlength(tag, font=ft) + 64
    d.rounded_rectangle([(W - tw) / 2, y + 24, (W + tw) / 2, y + 24 + 84], 42, fill=AMBER + (255,))
    d.text((W / 2, y + 24 + 42), tag, font=ft, fill=NAVY, anchor="mm")
    im.save(out)


def card(text: str, out: Path, sub: str | None = None) -> None:
    """Full-screen black card (the '2041' flash-forward)."""
    im = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font(78)
    lines = _wrap(d, text, f, 900)
    y = H / 2 - len(lines) * 50 - (60 if sub else 0)
    if sub:
        d.text((W / 2, y), sub, font=font(56), fill=AMBER, anchor="ma")
        y += 110
    for s in lines:
        d.text((W / 2, y), s, font=f, fill=(255, 255, 255), anchor="ma")
        y += 100
    im.save(out)


def app_card(src: Path, out: Path, scale: float = 0.5, x: int = 500, y: int = 330) -> None:
    """A real Play-store frame as a rounded floating card with a shadow (plug pop-ins)."""
    shot = Image.open(src).convert("RGB")
    w, h = int(W * scale), int(H * scale)
    shot = shot.resize((w, h), Image.LANCZOS)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], 36, fill=255)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x, y + 14, x + w, y + h + 14], 36, fill=(0, 0, 0, 140))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(18)))
    border = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0))
    ImageDraw.Draw(border).rounded_rectangle([0, 0, w + 11, h + 11], 42, fill=(255, 255, 255, 255))
    im.alpha_composite(border, (x - 6, y - 6))
    im.paste(shot, (x, y), mask)
    im.save(out)
