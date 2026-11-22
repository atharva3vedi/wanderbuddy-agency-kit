"""Dense QA strip of a final: one frame every STEP seconds, 10 per row, with timestamps."""
import subprocess, sys
from PIL import Image, ImageDraw
f, out, step = sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1.5
d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
ts = [round(0.3 + i * step, 2) for i in range(int((d - 0.4) / step) + 1)]
tw, th, cols = 162, 288, 10
s = Image.new("RGB", (tw*cols, (th+18)*((len(ts)+cols-1)//cols)), "white")
for i, t in enumerate(ts):
    subprocess.run(["ffmpeg","-y","-v","error","-ss",str(t),"-i",f,"-frames:v","1","build/tmp_q.jpg"])
    x, y = (i%cols)*tw, (i//cols)*(th+18)
    s.paste(Image.open("build/tmp_q.jpg").resize((tw, th)), (x, y+18))
    ImageDraw.Draw(s).text((x+4, y+3), f"{t:.1f}s", fill="black")
s.save(out, quality=80)
