"""v5 "The Kinds of Travellers" cuts (edit list in narration5.py).

Title card on each part's establishing shot; scene-setting narrator lines are placed
automatically ("SETUP" lands just before the first spoken word, "END" just after the last,
"TAIL" at the end of a shot); slow motion via motion interpolation; dialogue ducks under the
narrator; captions follow the narrator.

    python cut5.py 1 2 3
"""

from __future__ import annotations

import json
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import doc as D  # run, dur, frames, norm_clip, still, hold_piece, app_piece, outro_piece, load_audio, caption_chunks
import overlays as ov
from narration5 import PARTS

FPS, SR = D.FPS, D.SR
TMP = D.HERE / "tmp5"
TMP.mkdir(exist_ok=True)
MAX_HOLD = 2.0
SERIF = str(D.REPO / "assets/fonts/InstrumentSerif-Regular.ttf")
SERIF_I = str(D.REPO / "assets/fonts/InstrumentSerif-Italic.ttf")


def words(cid: str) -> list[dict]:
    p = D.HERE / "transcripts" / f"{cid}.json"
    return json.loads(p.read_text()) if p.exists() else []


def title_png(main: str, sub: str, out):
    """Documentary title: big serif title + italic part line over a soft dark band, centred."""
    W, H = 1080, 1920
    band = Image.new("L", (W, H), 0)
    bd = ImageDraw.Draw(band)
    for y in range(560, 1180):  # vertical fade in and out around the title block
        a = 1 - abs(y - 870) / 310
        bd.line([(0, y), (W, y)], fill=int(150 * max(0.0, a) ** 0.8))
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    im.putalpha(band)
    d = ImageDraw.Draw(im)
    f1, f2 = ImageFont.truetype(SERIF, 132), ImageFont.truetype(SERIF_I, 70)
    lines = ["The Kinds of", "Travellers"] if main.startswith("The Kinds") else [main]
    y = 690
    for ln in lines:
        d.text((W / 2, y), ln, font=f1, fill=(255, 255, 255, 255), anchor="ma", stroke_width=2,
               stroke_fill=(0, 0, 0, 200))
        y += 140
    y += 22
    d.text((W / 2, y), sub, font=f2, fill=(255, 196, 64, 255), anchor="ma", stroke_width=2,
           stroke_fill=(0, 0, 0, 200))
    im.save(out)


def clip_piece(src, t0, length, speed, n, out):
    vf = f"setpts=PTS/{speed}"
    if speed < 1:  # smooth slow motion
        vf += ",minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
    D.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{length + 0.2:.3f}", "-i", str(src), "-an",
           "-vf", vf + ",fps=30,format=yuv420p", "-frames:v", str(n), "-c:v", "libx264", "-crf", "16",
           "-preset", "fast", str(out)])
    return out


def clip_audio(src, t0, length, speed) -> np.ndarray:
    tempo = f"atempo={speed}" if speed >= 0.5 else "atempo=0.5"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{length:.3f}", "-i", str(src), "-vn",
                          "-af", tempo, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def build(part: int):
    VOX = D.VOX
    beats = PARTS[part]
    pieces, vo_events, dia_events, titles = [], [], [], []
    T, prev_last, plug_t = 0, None, None
    for bi, b in enumerate(beats):
        tag = f"p{part}_{bi:02d}"
        if (b.get("clip", "").startswith("PL") or "app" in b) and plug_t is None:
            plug_t = T / FPS
        if "clip" in b:
            cid, sp = b["clip"], b.get("speed", 1.0)
            src = D.norm_clip(cid)
            t0, t1 = b.get("t0", 0.0), min(b.get("t1", 99.0), D.dur(src) - 0.05)
            if b.get("fit"):  # establishing B-roll: exactly as long as its narrator lines
                need = 0.2 + sum(VOX[ln]["dur"] for ln, _ in b["vo"]) + 0.25 * (len(b["vo"]) - 1) + 0.35
                t1 = min(t1, t0 + need * sp)
            ws = [w for w in words(cid) if t0 <= w["s"] < t1]
            first_w = ws[0]["s"] if ws else t1
            last_w = ws[-1]["e"] if ws else t0
            n = D.frames((t1 - t0) / sp)
            # SETUP lines may need a short lead-in hold before the clip
            pre = 0.0
            for line, at in b.get("vo", []):
                if at == "SETUP":
                    start_clip = first_w - (0.15 + VOX[line]["dur"]) * sp
                    if start_clip < t0 + 0.05 * sp:
                        pre = max(pre, (t0 + 0.05 * sp - start_clip) / sp)
            n_pre = D.frames(pre) if pre > 0.04 else 0
            if n_pre:
                first = D.still(src, t0 + 0.02, TMP / f"{tag}_first.png")
                pieces.append(D.hold_piece(first, n_pre, TMP / f"{tag}_a.mp4", 1.03, 1.0))
            base = (T + n_pre) / FPS
            L = n / FPS
            last_end = -1.0
            for line, at in b.get("vo", []):
                d = VOX[line]["dur"]
                if at == "SETUP":
                    st = base + (first_w - t0) / sp - 0.15 - d
                elif at == "END":
                    st = base + (last_w - t0) / sp + 0.2
                elif at == "TAIL":
                    st = base + L - d - 0.1
                elif at is None:
                    st = last_end + 0.25
                else:
                    st = base + (at - t0) / sp
                st = max(st, last_end + 0.15, T / FPS + 0.05)
                vo_events.append((line, st))
                last_end = st + d
            hold = max(0.0, last_end + 0.25 - (base + L))
            cap = b.get("max_hold", MAX_HOLD)
            if hold > cap:
                print(f"  ! {cid}: line needs {hold:.2f}s hold, capped at {cap}")
                hold = cap
            pieces.append(clip_piece(src, t0, t1 - t0, sp, n, TMP / f"{tag}_b.mp4"))
            dia_events.append((src, t0, t1 - t0, sp, base))
            last = TMP / f"{tag}_last.png"
            D.run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.3", "-i", str(pieces[-1]), "-update", "1", str(last)])
            n_post = D.frames(hold) if hold > 0.05 else 0
            if n_post:
                pieces.append(D.hold_piece(last, n_post, TMP / f"{tag}_c.mp4", 1.0, 1.02))
            if b.get("title"):
                png = TMP / f"{tag}_title.png"
                title_png(*b["title"], png)
                titles.append((png, base + 0.7, base + L + n_post / FPS - 0.15))
            T += n_pre + n + n_post
            prev_last = last
        elif "app" in b:
            n = D.frames(b["d"])
            for line, at in b.get("vo", []):
                vo_events.append((line, T / FPS + at))
            nxt = beats[bi + 1]
            nxt_first = D.still(D.norm_clip(nxt["clip"]), nxt.get("t0", 0.0) + 0.02, TMP / f"{tag}_next.png") \
                if "clip" in nxt else prev_last
            pieces.append(D.app_piece(D.PLAY / b["app"], prev_last, nxt_first, n, TMP / f"{tag}_app.mp4"))
            last = TMP / f"{tag}_last.png"
            D.run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.3", "-i", str(pieces[-1]), "-update", "1", str(last)])
            prev_last = last
            T += n
        elif "outro" in b:
            outro_t = T / FPS
            pieces.append(D.outro_piece(prev_last, TMP / f"{tag}_outro.mp4"))
            vo_events.append((b["outro"], outro_t + 0.8))
            T += D.frames(D.dur(D.OUTRO))
    total = T / FPS

    # ---- video: concat, then title cards + narrator captions ----
    lst = TMP / f"p{part}_list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in pieces))
    body = TMP / f"p{part}_body.mp4"
    D.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(body)])
    outro_lines = {b["outro"] for b in beats if "outro" in b}
    caps = []
    for line, st in vo_events:
        cy = 330 if line in outro_lines else 1490
        caps += [(c, a, e, cy) for c, a, e in D.caption_chunks(line, st)]
    inputs, fc, lastv, k = [], [], "0:v", 1
    for png, a, e in titles:
        inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(png)]
        fc.append(f"[{k}:v]format=rgba,fade=in:st={a:.2f}:d=0.5:alpha=1,fade=out:st={e - 0.5:.2f}:d=0.5:alpha=1[t{k}]")
        fc.append(f"[{lastv}][t{k}]overlay=0:0:enable='between(t,{a:.3f},{e:.3f})'[v{k}]")
        lastv, k = f"v{k}", k + 1
    for i, (text, a, e, cy) in enumerate(caps):
        png = TMP / f"p{part}_cap{i:03d}.png"
        ov.stroke_text(text, png, size=64, cy=cy)
        inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(png)]
        fc.append(f"[{lastv}][{k}:v]overlay=0:0:enable='between(t,{a:.3f},{e:.3f})'[v{k}]")
        lastv, k = f"v{k}", k + 1
    fc.append(f"[{lastv}]format=yuv420p[vout]")
    (TMP / f"p{part}_fc.txt").write_text(";\n".join(fc))
    video = TMP / f"p{part}_video.mp4"
    D.run(["ffmpeg", "-y", "-v", "error", "-i", str(body), *inputs, "-filter_complex_script",
           str(TMP / f"p{part}_fc.txt"), "-map", "[vout]", "-t", f"{total:.3f}", "-c:v", "libx264",
           "-crf", "18", "-preset", "medium", str(video)])

    # ---- audio ----
    N = int(total * SR) + SR
    dia, vo, mus = (np.zeros((N, 2), np.float32) for _ in range(3))
    for src, t0, length, sp, at in dia_events:
        a = clip_audio(src, t0, length, sp)
        f = min(len(a), int(0.015 * SR))
        if f:
            a[:f] *= np.linspace(0, 1, f)[:, None]
            a[-f:] *= np.linspace(1, 0, f)[:, None]
        i = int(at * SR)
        dia[i:i + len(a)] += a[: N - i]
    duck = np.ones(N, np.float32)
    for line, st in vo_events:
        a = D.load_audio(D.VO / VOX[line]["file"])
        i = max(0, int(st * SR))
        vo[i:i + len(a)] += a[: N - i]
        duck[max(0, int((st - 0.08) * SR)):min(N, int((st + VOX[line]["dur"] + 0.06) * SR))] = 0.25
    kk = int(0.08 * SR)
    duck = np.convolve(duck, np.ones(kk) / kk, mode="same").astype(np.float32)
    plug_t = plug_t if plug_t is not None else total
    outro_t = total - D.dur(D.OUTRO)
    bed_p, swell_p = D.CLIPS / "MUSIC_A.mp4", D.CLIPS / "MUSIC_B.mp4"
    if bed_p.exists():
        bed = D.load_audio(bed_p)
        bed /= max(1e-6, float(np.sqrt((bed ** 2).mean()))) / 0.03
        x, t = int(1.0 * SR), 0
        while t < int(plug_t * SR):
            seg = bed.copy()
            seg[:x] *= np.linspace(0, 1, x)[:, None]
            seg[-x:] *= np.linspace(1, 0, x)[:, None]
            mus[t:t + len(seg)] += seg[: N - t]
            t += len(seg) - x
        e = int(plug_t * SR)
        mus[e:] = 0
        f = min(int(0.6 * SR), e)
        mus[e - f:e] *= np.linspace(1, 0, f)[:, None]
    if swell_p.exists():
        sw = D.load_audio(swell_p)
        sw /= max(1e-6, float(np.sqrt((sw ** 2).mean()))) / 0.06
        i = int(plug_t * SR)
        L = min(len(sw), int((outro_t + 1.2 - plug_t) * SR), N - i)
        seg = sw[:L].copy()
        seg[: int(0.4 * SR)] *= np.linspace(0, 1, int(0.4 * SR))[:, None]
        seg[-int(1.0 * SR):] *= np.linspace(1, 0, int(1.0 * SR))[:, None]
        mus[i:i + L] += seg
    mus *= (0.55 + 0.45 * duck)[:, None]
    o = int(outro_t * SR)
    wave = D.load_audio(D.OUTRO_WAVE, 0, D.dur(D.OUTRO)) * 0.5
    dia[o:o + len(wave)] += wave[: N - o]
    ch = D.load_audio(D.CHIME) * 0.8
    c = int((outro_t + 3.15) * SR)
    dia[c:c + len(ch)] += ch[: N - c]
    mix = (dia * duck[:, None] + vo + mus)[: int(total * SR)]
    raw = TMP / f"p{part}_mix.f32"
    raw.write_bytes(mix.astype(np.float32).tobytes())
    final = D.ROOT / f"Kinds_of_Travellers_Pt{part}.mp4"
    D.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw),
           "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af",
           "alimiter=limit=0.89:attack=5:release=60,loudnorm=I=-14:TP=-1.2:LRA=11,aresample=48000",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(final)])
    print(f"Pt {part}: {final.name} {D.dur(final):.1f}s, {len(vo_events)} narrator lines", flush=True)


if __name__ == "__main__":
    for p in sys.argv[1:] or ["1", "2", "3"]:
        build(int(p))
