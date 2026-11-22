"""Cut each film: the Blender frames, a 0.3 s crossfade into the end card, the
words on top (each fades in 0.35 s while rising 14 px), the score. System python3 + ffmpeg.

  python3 build/compose.py [film ...]     -> out/<n>-<film>.mp4 and a smaller _share copy

Film 4 (day2) is two Blender scenes: the land frames dissolve into the phone
frames over 1.25 s at 13.75 s (the match from the karst to the card's photo).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.dirname(HERE)
R = os.path.join(AD, "render")
OUT = os.path.join(AD, "out")
FPS = 24
FILMS = {"departures": "1-departures", "order": "2-order", "night": "3-2348", "day2": "4-day2"}
CARD_AT, XF = 21.2, 0.3


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-4000:])
        raise SystemExit(r.returncode)


def build(film):
    spec = json.load(open(os.path.join(HERE, f"{film}.supers.json")))
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    parts = []
    if film == "day2":
        cmd += ["-framerate", str(FPS), "-i", os.path.join(R, "day2", "land", "%04d.png"),
                "-framerate", str(FPS), "-i", os.path.join(R, "day2", "phone", "%04d.png")]
        parts.append("[0:v]format=rgb24,setsar=1[l];[1:v]format=rgb24,setsar=1[p];"
                     "[l][p]xfade=transition=fade:duration=1.25:offset=13.75[film]")
        nxt = 2
    else:
        cmd += ["-framerate", str(FPS), "-i", os.path.join(R, film, "3d", "%04d.png")]
        parts.append("[0:v]format=rgb24,setsar=1[film]")
        nxt = 1
    cmd += ["-framerate", str(FPS), "-i", os.path.join(R, "endcard", "%04d.png")]
    ci = nxt
    nxt += 1
    parts.append(f"[{ci}:v]format=rgb24,setsar=1[card];[film][card]xfade=transition=fade:duration={XF}:offset={CARD_AT}[v0]")
    dur = CARD_AT + 84 / FPS
    last = "v0"
    for k, s in enumerate(spec["supers"]):
        t0, t1 = s["t"]
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", os.path.join(R, film, "supers", f"{k}.png")]
        parts.append(f"[{nxt}:v]format=rgba,fade=t=in:st={t0}:d=0.35:alpha=1,fade=t=out:st={t1 - 0.35:.3f}:d=0.35:alpha=1[s{k}]")
        parts.append(f"[{last}][s{k}]overlay=x=0:y='14*max(0\\,1-(t-{t0})/0.6)':eval=frame:enable='between(t\\,{t0}\\,{t1})'[v{k + 1}]")
        last = f"v{k + 1}"
        nxt += 1
    cmd += ["-i", os.path.join(OUT, "audio", f"{film}.wav")]
    ai = nxt
    parts.append(f"[{last}]format=yuv420p[vout]")
    name = FILMS[film]
    final = os.path.join(OUT, f"{name}.mp4")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", f"{ai}:a",
            "-t", f"{dur:.3f}", "-r", str(FPS),
            "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final]
    run(cmd)
    share = os.path.join(OUT, f"{name}_share.mp4")
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", final, "-c:v", "libx264", "-preset", "slow",
         "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", share])
    print(film, "->", final)


if __name__ == "__main__":
    for f in (sys.argv[1:] or list(FILMS)):
        build(f)
