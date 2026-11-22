"""Cut Monsoon: the Blender frames, a 0.3 s crossfade into the two-line end
card, the words on top (each fades in 0.35 s while rising 14 px), the score.

  python3 build/agencies_compose.py   -> out/v2-monsoon.mp4 and a _share copy
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.dirname(HERE)
R = os.path.join(AD, "render")
OUT = os.path.join(AD, "out")
FPS = 24
FILM, NAME = "monsoon", "v2-monsoon"
CARD_AT, XF = 27.2, 0.3


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-4000:])
        raise SystemExit(r.returncode)


spec = json.load(open(os.path.join(HERE, f"{FILM}.supers.json")))
dur = CARD_AT + 84 / FPS
cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
       "-framerate", str(FPS), "-i", os.path.join(R, FILM, "3d", "%04d.png"),
       "-framerate", str(FPS), "-i", os.path.join(R, "endcard_v2", "%04d.png")]
parts = ["[0:v]format=rgb24,setsar=1[film]",
         f"[1:v]format=rgb24,setsar=1[card];[film][card]xfade=transition=fade:duration={XF}:offset={CARD_AT}[v0]"]
nxt, last = 2, "v0"
for k, s in enumerate(spec["supers"]):
    t0, t1 = s["t"]
    cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", os.path.join(R, FILM, "supers", f"{k}.png")]
    parts.append(f"[{nxt}:v]format=rgba,fade=t=in:st={t0}:d=0.35:alpha=1,fade=t=out:st={t1 - 0.35:.3f}:d=0.35:alpha=1[s{k}]")
    parts.append(f"[{last}][s{k}]overlay=x=0:y='14*max(0\\,1-(t-{t0})/0.6)':eval=frame:enable='between(t\\,{t0}\\,{t1})'[v{k + 1}]")
    last = f"v{k + 1}"
    nxt += 1
cmd += ["-i", os.path.join(OUT, "audio", f"{FILM}.wav")]
parts.append(f"[{last}]format=yuv420p[vout]")
final = os.path.join(OUT, f"{NAME}.mp4")
cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", f"{nxt}:a",
        "-t", f"{dur:.3f}", "-r", str(FPS),
        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final]
run(cmd)
share = os.path.join(OUT, f"{NAME}_share.mp4")
run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", final, "-c:v", "libx264", "-preset", "slow",
     "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", share])
print(FILM, "->", final)
