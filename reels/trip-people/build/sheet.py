"""Contact sheet: 4 frames per clip, one row per clip. python sheet.py OUT.jpg ID..."""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent.parent
out, ids = sys.argv[1], sys.argv[2:]
tw, th = 180, 320
rows = []
for sid in ids:
    clip = ROOT / "clips" / f"{sid}.mp4"
    d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(clip)],capture_output=True,text=True).stdout)
    row = Image.new("RGB", (tw*4+120, th), "white")
    ImageDraw.Draw(row).text((5, 5), sid, fill="black")
    for i, f in enumerate([0.1, 0.35, 0.65, 0.92]):
        tmp = ROOT / "build" / "tmp_frame.jpg"
        subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{d*f:.2f}","-i",str(clip),"-frames:v","1",str(tmp)])
        row.paste(Image.open(tmp).resize((tw, th)), (120 + i*tw, 0))
    rows.append(row)
sheet = Image.new("RGB", (tw*4+120, th*len(rows)), "white")
for i, r in enumerate(rows): sheet.paste(r, (0, i*th))
sheet.save(out, quality=80)
