#!/usr/bin/env bash
# Prints one size of the poster (run `python -I build.py <size>` first) on a sheet
# with 0.125 in bleed, into out/ (24x36) or out/8x10/:
#   poster-print.pdf  trim + 0.25 in, TrimBox + BleedBox set: send this one to the printer
#   poster.pdf        the same page cropped to the trim, for viewing
#   poster-bleed.png  with bleed, at the size's dpi
#   poster.png        trimmed (also poster.jpg and an 800 px poster-preview.jpg)
#   bash render.sh [24x36|8x10]
set -euo pipefail
FMT="${1:-24x36}"
case "$FMT" in 24x36) DIR=out ;; 8x10) DIR=out/8x10 ;; *) echo "unknown size $FMT" >&2; exit 2 ;; esac
cd "$(dirname "$0")/$DIR"
source ./render.env
CHROME="${CHROME:-/c/Program Files/Google/Chrome/Application/chrome.exe}"
HERE="$(pwd -W 2>/dev/null || pwd)"
PAGE="file:///$HERE/poster.html"
FLAGS=(--headless=new --mute-audio --hide-scrollbars --disable-gpu --allow-file-access-from-files
       --run-all-compositor-stages-before-draw --virtual-time-budget=8000)

# The sheet can be a fraction of a css px wide; the window rounds up and the crop takes it back.
"$CHROME" "${FLAGS[@]}" --window-size="$WIN_W,$WIN_H" --force-device-scale-factor="$DSF" \
  --screenshot="$HERE/sheet.png" "$PAGE" 2>/dev/null
"$CHROME" "${FLAGS[@]}" --no-pdf-header-footer --print-to-pdf="$HERE/sheet.pdf" "$PAGE" 2>/dev/null

python -I - <<'EOF'
import os
import pymupdf
from PIL import Image

e = {k: int(os.environ[k]) for k in ('SHEET_W', 'SHEET_H', 'BLEED_PX', 'DPI', 'PREVIEW_W', 'PREVIEW_H')}
b, dpi = e['BLEED_PX'], (e['DPI'], e['DPI'])
sheet = Image.open('sheet.png').convert('RGB').crop((0, 0, e['SHEET_W'], e['SHEET_H']))
sheet.save('poster-bleed.png', dpi=dpi)
trim = sheet.crop((b, b, e['SHEET_W'] - b, e['SHEET_H'] - b))
trim.save('poster.png', dpi=dpi)
trim.save('poster.jpg', quality=94, subsampling=0, dpi=dpi)
trim.resize((e['PREVIEW_W'], e['PREVIEW_H']), Image.LANCZOS).save('poster-preview.jpg', quality=88)

BLEED_PT = 9                        # 0.125 in
for name, cropped in (('poster-print.pdf', False), ('poster.pdf', True)):
    doc = pymupdf.open('sheet.pdf')
    assert len(doc) == 1, f'expected one page, got {len(doc)}'
    page = doc[0]
    box = page.mediabox
    t = pymupdf.Rect(box.x0 + BLEED_PT, box.y0 + BLEED_PT, box.x1 - BLEED_PT, box.y1 - BLEED_PT)
    page.set_bleedbox(box)
    page.set_trimbox(t)
    if cropped:
        page.set_cropbox(t)
    doc.save(name, garbage=3, deflate=True)
    print(name, 'media', [round(v / 72, 3) for v in (box.width, box.height)], 'in, trim',
          [round(v / 72, 3) for v in (t.width, t.height)], 'in')
print('png', trim.size, 'at', e['DPI'], 'dpi')
EOF
