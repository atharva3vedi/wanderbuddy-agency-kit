"""4:5 cuts (1080 x 1350) of the second-pass films, for the LinkedIn feed. No Blender:
the 9:16 frames are cropped to a window that follows each shot, and the words are laid
out again inside that window.

  python3 build/compose_45.py [film ...]   -> out/linkedin/<name>_4x5.mp4 (+ _share)

Per film:
  windows   [(from seconds, top of the 1350 px window in the 9:16 frame, or "fit")]. "fit"
            shows the whole 9:16 frame scaled to the window's height, its edge columns carried out to the sides
            (used where the picture is taller than the window: the fourteen pages).
  words     {caption index: {"y": centre in the 4:5 frame, "text": ..., "size": ...}} for the
            captions that cannot simply move with their window.
The end card is cropped around its own content (CARD_Y).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.dirname(HERE)
R = os.path.join(AD, "render")
OUT = os.path.join(AD, "out", "linkedin")
FPS, W, H = 24, 1080, 1350
# A "fit" shot starts as a plain centred crop and pulls back to the whole 9:16 frame between FIT_A and
# FIT_B seconds, so the sides only open up once nothing is touching the frame's edges.
FIT_A, FIT_B = 12.8, 16.7
_ST = f"clip((t-{FIT_A})/{FIT_B - FIT_A}\\,0\\,1)"
_SM = f"({_ST})*({_ST})*(3-2*({_ST}))"
ZOOM = f"1-{1 - 1350 / 1920:.4f}*{_SM}"
CARD_Y = 343                 # the end card's lockup and lines run from 801 to 1235: centred in 1350
XF = 0.3

FILMS = {
    "three-agencies": dict(film="agencies2", name="v3-three-agencies", card="endcard_v3", card_at=28.8, audio="agencies2", windows=[(0, 150)]),
    "monsoon": dict(film="monsoon", name="v2-monsoon", card="endcard_v2", card_at=27.2, audio="monsoon",
                    windows=[(0, 420), (3.5, 150)],                      # the phone: keep the clock and the "113 unread" badge
                    words={0: {"y": 1000}}),                             # "Peak season." moves onto the dark of the phone
    "opened": dict(film="opened", name="v2-opened-3-times", card="endcard_v2", card_at=26.8, audio="opened", windows=[(0, 150)]),
    "day2": dict(film="day2", name="v2-day2", card="endcard_v2", card_at=21.2, audio="day2v2", windows=[(0, 150)], two=True),
    "reel": dict(film="reel", name="v2-the-reel", card="endcard_v2", card_at=31.7, audio="reel",
                 windows=[(0, 150), (6.5, 330), (10.0, "fit"), (18.0, 150)],   # the panel with its whole result card; all fourteen pages
                 words={2: {"y": 54, "size": 46, "text": "Reads it. Prices it. Writes the plan."},
                        3: {"y": 100}}),
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-4000:])
        raise SystemExit(r.returncode)


def window_at(windows, t):
    cur = windows[0][1]
    for t0, y in windows:
        if t >= t0 - 1e-6:
            cur = y
    return cur


def build(key):
    c = FILMS[key]
    film = c["film"]
    spec = json.load(open(os.path.join(HERE, f"{film}.supers.json")))
    # the words, placed inside the 4:5 window
    spec45 = {k: v for k, v in spec.items() if k != "supers"}
    spec45["supers"] = []
    for i, s in enumerate(spec["supers"]):
        s = dict(s)
        over = c.get("words", {}).get(i)
        win = window_at(c["windows"], s["t"][0])
        if over:
            s.update(over)
        elif win == "fit":
            raise SystemExit(f"{key}: caption {i} sits in a 'fit' shot and needs a place in words")
        else:
            s["y"] = s["y"] - win
        spec45["supers"].append(s)
    json.dump(spec45, open(os.path.join(HERE, f"{film}_45.supers.json"), "w"), indent=1)
    run(["node", os.path.join(HERE, "stills.mjs"), "supers", f"{film}_45"])
    dur = c["card_at"] + 84 / FPS
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    parts = []
    if c.get("two"):
        cmd += ["-framerate", str(FPS), "-i", os.path.join(R, "day2", "land", "%04d.png"),
                "-framerate", str(FPS), "-i", os.path.join(R, "day2", "phone", "%04d.png")]
        parts.append("[0:v]format=rgb24,setsar=1[l];[1:v]format=rgb24,setsar=1[p];[l][p]xfade=transition=fade:duration=1.25:offset=13.75[src]")
        nxt = 2
    else:
        cmd += ["-framerate", str(FPS), "-i", os.path.join(R, film, "3d", "%04d.png")]
        parts.append("[0:v]format=rgb24,setsar=1[src]")
        nxt = 1
    crops = [(t0, y) for t0, y in c["windows"]]
    expr = str(next(y for _, y in reversed(crops) if y != "fit") if crops[-1][1] == "fit" else crops[-1][1])
    last_num = None
    for t0, y in reversed(crops):
        if y != "fit":
            last_num = y
    cur = None
    # nested ifs, last window first; a "fit" stretch borrows the window before it (it is covered anyway)
    seq = []
    prev = last_num
    for t0, y in crops:
        if y == "fit":
            y = prev
        seq.append((t0, y))
        prev = y
    expr = str(seq[-1][1])
    for (t0, _), (_, yb) in zip(reversed(seq[1:]), reversed(seq[:-1])):
        expr = f"if(lt(t\\,{t0})\\,{yb}\\,{expr})"
    fits = [(t0, (c["windows"][i + 1][0] if i + 1 < len(c["windows"]) else c["card_at"] + XF)) for i, (t0, y) in enumerate(c["windows"]) if y == "fit"]
    if fits:
        parts.append(f"[src]split=2[fa][fb];[fa]crop={W}:{H}:0:'{expr}'[crop];"
                     f"[fb]split=2[z1][z2];[z1]scale=-2:{H},pad={W}:{H}:(ow-iw)/2:0,fillborders=left=160:right=160:mode=smear[bgf];"   # the desk carries on to the sides
                     f"[z2]scale=w='{W}*({ZOOM})':h='1920*({ZOOM})':eval=frame[zf];[bgf][zf]overlay=x='(W-w)/2':y='(H-h)/2+135*(1-({_SM}))':eval=frame[fit]")   # starts on the same window as the other shots (top 150)
        cur = "crop"
        for k, (a, b) in enumerate(fits):
            parts.append(f"[{cur}][fit]overlay=enable='between(t\\,{a}\\,{b - 0.5 / FPS:.4f})'[f{k}]")
            cur = f"f{k}"
        parts.append(f"[{cur}]null[film]")
    else:
        parts.append(f"[src]crop={W}:{H}:0:'{expr}'[film]")
    cmd += ["-framerate", str(FPS), "-i", os.path.join(R, c["card"], "%04d.png")]
    parts.append(f"[{nxt}:v]format=rgb24,setsar=1,crop={W}:{H}:0:{CARD_Y}[card];[film][card]xfade=transition=fade:duration={XF}:offset={c['card_at']}[v0]")
    nxt += 1
    lastv = "v0"
    for k, s in enumerate(spec45["supers"]):
        t0, t1 = s["t"]
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.3f}", "-i", os.path.join(R, f"{film}_45", "supers", f"{k}.png")]
        parts.append(f"[{nxt}:v]format=rgba,crop={W}:{H}:0:0,fade=t=in:st={t0}:d=0.35:alpha=1,fade=t=out:st={t1 - 0.35:.3f}:d=0.35:alpha=1[s{k}]")
        parts.append(f"[{lastv}][s{k}]overlay=x=0:y='14*max(0\\,1-(t-{t0})/0.6)':eval=frame:enable='between(t\\,{t0}\\,{t1})'[v{k + 1}]")
        lastv = f"v{k + 1}"
        nxt += 1
    cmd += ["-i", os.path.join(AD, "out", "audio", f"{c['audio']}.wav")]
    parts.append(f"[{lastv}]format=yuv420p[vout]")
    os.makedirs(OUT, exist_ok=True)
    final = os.path.join(OUT, f"{c['name']}_4x5.mp4")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", f"{nxt}:a", "-t", f"{dur:.3f}", "-r", str(FPS),
            "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final]
    run(cmd)
    print(key, "->", final)


if __name__ == "__main__":
    for k in (sys.argv[1:] or list(FILMS)):
        build(k)
