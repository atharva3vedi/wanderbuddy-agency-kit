"""Day 2 with its own score: the same frames and words as compose.py's day2, the
audio from build/day2_audio_v2.py.   python3 build/day2_compose_v2.py -> out/v2-day2.mp4
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.dirname(HERE)
R, OUT, FPS = os.path.join(AD, "render"), os.path.join(AD, "out"), 24
CARD_AT, XF = 21.2, 0.3
spec = json.load(open(os.path.join(HERE, "day2.supers.json")))
dur = CARD_AT + 84 / FPS
cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
       "-framerate", str(FPS), "-i", os.path.join(R, "day2", "land", "%04d.png"),
       "-framerate", str(FPS), "-i", os.path.join(R, "day2", "phone", "%04d.png"),
       "-framerate", str(FPS), "-i", os.path.join(R, "endcard_v2", "%04d.png")]
parts = ["[0:v]format=rgb24,setsar=1[l];[1:v]format=rgb24,setsar=1[p];[l][p]xfade=transition=fade:duration=1.25:offset=13.75[film]",
         f"[2:v]format=rgb24,setsar=1[card];[film][card]xfade=transition=fade:duration={XF}:offset={CARD_AT}[v0]"]
nxt, last = 3, "v0"
for k, s in enumerate(spec["supers"]):
    t0, t1 = s["t"]
    cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", os.path.join(R, "day2", "supers", f"{k}.png")]
    parts.append(f"[{nxt}:v]format=rgba,fade=t=in:st={t0}:d=0.35:alpha=1,fade=t=out:st={t1 - 0.35:.3f}:d=0.35:alpha=1[s{k}]")
    parts.append(f"[{last}][s{k}]overlay=x=0:y='14*max(0\\,1-(t-{t0})/0.6)':eval=frame:enable='between(t\\,{t0}\\,{t1})'[v{k + 1}]")
    last = f"v{k + 1}"
    nxt += 1
cmd += ["-i", os.path.join(OUT, "audio", "day2v2.wav")]
parts.append(f"[{last}]format=yuv420p[vout]")
final = os.path.join(OUT, "v2-day2.mp4")
cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", f"{nxt}:a", "-t", f"{dur:.3f}", "-r", str(FPS),
        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final]
subprocess.run(cmd, check=True)
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", final, "-c:v", "libx264", "-preset", "slow",
                "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", os.path.join(OUT, "v2-day2_share.mp4")], check=True)
print("day2 ->", final)
