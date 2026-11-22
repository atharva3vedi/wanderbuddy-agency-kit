"""Mix the audio and cut the rendered shots into app-25s.mp4 (system python3 + ffmpeg).

  python3 build/edit.py [--render DIR]

Audio (marketing/music/README.md rules): the bossa bed and the Iowa piano
notes only, notes in G major, piano 4.5 dB under the bed, two-pass loudnorm
to -14 LUFS. Video: each shot's RGBA frames over its ground (grounds/), the
panic's headline layer on top, hard cuts on the downbeats, a 0.3 s crossfade
into the end card.
"""
import json
import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.dirname(HERE)
ROOT = os.path.normpath(os.path.join(AD, "../../.."))
TL_NAME = sys.argv[sys.argv.index("--tl") + 1] if "--tl" in sys.argv else os.environ.get("WB_TL", "timeline.json")
TL = json.load(open(os.path.join(HERE, TL_NAME), encoding="utf-8"))
PREFIX = TL.get("prefix", "")
GROUNDS = TL.get("grounds", {"light": "light.png", "panic": "panic.png"})
FPS = TL["fps"]
RENDER = sys.argv[sys.argv.index("--render") + 1] if "--render" in sys.argv else os.path.join(AD, "render")
PIANO = os.path.join(ROOT, "marketing/music/piano")
MUSIC = os.path.join(ROOT, TL["music"]["file"])
OUT_MP4 = os.path.join(AD, TL.get("out", "app-25s.mp4"))
AUDIO_DIR = os.path.join(AD, "audio")
DUR = TL["total"] / FPS


def run(cmd):
    print(" ".join(cmd[:6]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:])
        raise SystemExit(r.returncode)
    return r.stderr


def shot(sid):
    return next(s for s in TL["shots"] if s["id"] == sid)


# --- the score -----------------------------------------------------------------

def notes():
    """(time s, note, gain dB, group) for every piano note."""
    ev = []
    P = TL["panic"]
    rnd = random.Random(11)
    high = ["D6", "B5", "G5", "D5", "B4", "B5", "D6", "G5"]
    # 5 am: one low G under the first message, and again when the headline lands.
    ev += [(0.0, "G2", -3.0, "panic"), (0.0, "D3", -6.0, "panic")]
    hl = P["headline_in"] / FPS
    ev += [(hl, "G2", -3.0, "panic"), (hl + 0.02, "D3", -6.0, "panic")]
    # Every question that arrives is a note; they pile up into a wash.
    for k, c in enumerate(P["cards"]):
        t = c["f"] / FPS
        g = -13.0 + 5.0 * k / len(P["cards"])
        ev.append((t, rnd.choice(high), g, "panic"))
    # The questions fall back into the phone: a quick run down the keys.
    c0 = P["collapse"][0] / FPS
    for i, nt in enumerate(["D6", "B5", "G5", "D5", "B4", "G4"]):
        ev.append((c0 + 0.12 + i * 0.075, nt, -10.0, "run"))
    # 7.0 s: the logo lands with the bed's downbeat.
    t7 = shot("logo")["start"] / FPS
    ev += [(t7, "G4", -6.5, "app"), (t7, "D5", -6.5, "app"), (t7 + 0.01, "G5", -9.0, "app")]
    # Each ring is a tap: G4 + D5.
    for bid, b in TL["beats"].items():
        t = (shot(bid)["start"] + b.get("ring_in", 18)) / FPS
        ev += [(t, "G4", -9.5, "app"), (t + 0.012, "D5", -9.5, "app")]
    # The end card: a run up the keys as the peaks rise.
    te = (shot("end")["start"] + 6) / FPS
    for i, nt in enumerate(["G4", "B4", "D5", "G5"]):
        ev.append((te + i * 0.085, nt, -8.0, "app"))
    return ev


def mix_audio():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    ev = notes()
    names = sorted({n for _, n, _, _ in ev})
    cmd = ["ffmpeg", "-y", "-hide_banner"]
    for nm in names:
        cmd += ["-i", os.path.join(PIANO, nm + ".wav")]
    m = TL["music"]
    trim_from = 3.2
    lands = m["downbeat_lands_at"] - (m["first_downbeat_in_file"] - trim_from)
    cmd += ["-ss", str(trim_from), "-i", MUSIC]
    mi = len(names)
    parts, labels = [], {"panic": [], "run": [], "app": []}
    for nm in names:
        uses = [e for e in ev if e[1] == nm]
        idx = names.index(nm)
        outs = "".join(f"[{nm}_{k}]" for k in range(len(uses)))
        parts.append(f"[{idx}:a]asplit={len(uses)}{outs}" if len(uses) > 1 else f"[{idx}:a]anull{outs}")
        for k, (t, _, g, grp) in enumerate(uses):
            lab = f"n_{nm}_{k}"
            parts.append(f"[{nm}_{k}]volume={g}dB,adelay={int(round(t * 1000))}:all=1,apad=whole_dur={DUR}[{lab}]")
            labels[grp].append(lab)
    for grp in ("panic", "run", "app"):
        ins = "".join(f"[{x}]" for x in labels[grp])
        parts.append(f"{ins}amix=inputs={len(labels[grp])}:normalize=0:duration=longest[{grp}_raw]")
    # The panic's notes clear out before the logo; the run rides through.
    parts.append(f"[panic_raw]afade=t=out:st=6.45:d=0.5[panic]")
    parts.append(f"[run_raw]afade=t=out:st=6.9:d=0.35[run]")
    parts.append(f"[app_raw]anull[app]")
    fo = m["fade_out_from"]
    parts.append(f"[{mi}:a]aresample=48000,volume=4.5dB,adelay={int(round(lands * 1000))}:all=1,"
                 f"afade=t=out:st={fo}:d={DUR - fo:.3f},apad=whole_dur={DUR}[bed]")
    parts.append(f"[panic][run][app][bed]amix=inputs=4:normalize=0:duration=longest,atrim=0:{DUR},"
                 f"aformat=sample_rates=48000:channel_layouts=stereo[mix]")
    raw = os.path.join(AUDIO_DIR, PREFIX + "mix_raw.wav")
    run(cmd + ["-filter_complex", ";".join(parts), "-map", "[mix]", "-c:a", "pcm_s24le", raw])
    # Two-pass loudnorm to -14 LUFS.
    err = run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json", "-f", "null", "-"])
    js = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S).group(0))
    ln = (f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    final = os.path.join(AUDIO_DIR, PREFIX + "mix.wav")
    run(["ffmpeg", "-y", "-hide_banner", "-i", raw, "-af", ln + ",aresample=48000", "-ar", "48000", "-c:a", "pcm_s24le", final])
    json.dump({"notes": [{"t": round(t, 3), "note": n, "gain_db": g, "group": grp} for t, n, g, grp in ev],
               "music_trim_from_s": trim_from, "music_lands_at_s": round(lands, 3), "loudnorm_pass1": js},
              open(os.path.join(AUDIO_DIR, PREFIX + "score.json"), "w"), indent=1)
    return final


# --- picture --------------------------------------------------------------------

def cut(audio):
    g = os.path.join(AD, "grounds")
    cmd = ["ffmpeg", "-y", "-hide_banner"]
    inputs = []

    def add(args):
        inputs.append(args)
        return len(inputs) - 1
    i_pg = add(["-loop", "1", "-framerate", str(FPS), "-i", os.path.join(g, GROUNDS["panic"])])
    i_lg = add(["-loop", "1", "-framerate", str(FPS), "-i", os.path.join(g, GROUNDS["light"])])
    order = [x["id"] for x in TL["shots"]]          # panic, logo, the beats..., end
    light = order[1:-1]
    seq = {}
    for sid in ["panic", "panic_ov"] + order[1:]:
        seq[sid] = add(["-framerate", str(FPS), "-start_number", "0", "-i", os.path.join(RENDER, PREFIX + sid, "%04d.png")])
    i_a = add(["-i", audio])
    for a in inputs:
        cmd += a
    parts = []
    n_light = len(light)
    parts.append(f"[{i_lg}:v]split={n_light}" + "".join(f"[lg{k}]" for k in range(n_light)))
    parts.append(f"[{i_pg}:v][{seq['panic']}:v]overlay=shortest=1:format=auto[p1]")
    parts.append(f"[p1][{seq['panic_ov']}:v]overlay=shortest=1:format=auto,format=gbrp,setsar=1[s_panic]")
    for k, sid in enumerate(light):
        parts.append(f"[lg{k}][{seq[sid]}:v]overlay=shortest=1:format=auto,format=gbrp,setsar=1[s_{sid}]")
    parts.append(f"[{seq['end']}:v]format=gbrp,setsar=1,settb=1/{FPS},setpts=N[s_end]")
    parts.append("".join(f"[s_{x}]" for x in ["panic"] + light) + f"concat=n={1 + len(light)}:v=1:a=0,"
                 f"settb=1/{FPS},setpts=N[pre]")
    xf = TL["xfade"]["frames"] / FPS
    off = shot("end")["start"] / FPS
    parts.append(f"[pre][s_end]xfade=transition=fade:duration={xf:.4f}:offset={off:.4f},"
                 f"scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,trim=end_frame={TL['total']}[v]")
    run(cmd + ["-filter_complex", ";".join(parts), "-map", "[v]", "-map", f"{i_a}:a",
               "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-g", "60",
               "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
               "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{DUR:.3f}",
               "-movflags", "+faststart", OUT_MP4])
    print("WROTE", OUT_MP4)


if __name__ == "__main__":
    a = mix_audio()
    if "--audio-only" not in sys.argv:
        cut(a)
