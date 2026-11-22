"""Documentary cut (v2) of Pt 1/2/3: narrator + captions on the narrator only, no labels or
black cards. Holds (slow pull-out on a frame) make room for the narrator; real app frames
dissolve in and out; dialogue ducks under the voice; music bed + plug swell; brand outro.

    python doc.py 1 2 3
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

import overlays as ov
from narration import PARTS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[2]
CLIPS, VO, TMP = ROOT / "clips", HERE / "vo", HERE / "tmp2"
TMP.mkdir(exist_ok=True)
PLAY = REPO / "store/graphics/appstore/play"
OUTRO = REPO / "marketing/outro/outro.mp4"
OUTRO_WAVE = REPO / "marketing/outro/audio/beach2.mp4"
CHIME = REPO / "marketing/outro/audio/chime_soft.wav"
FPS, SR = 30, 48000
VOX = json.loads((VO / "index.json").read_text())
GAP = 0.25  # between consecutive narrator lines


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2500:])
        raise SystemExit("ffmpeg failed: " + " ".join(cmd[:8]))


def dur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                 "csv=p=0", str(p)], capture_output=True, text=True).stdout)


def load_audio(p: Path, start: float = 0.0, length: float | None = None) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}"]
    if length is not None:
        cmd += ["-t", f"{length:.3f}"]
    cmd += ["-i", str(p), "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def frames(sec: float) -> int:
    return max(1, round(sec * FPS))


# ---------- sources ----------
def norm_clip(cid: str) -> Path:
    """1080x1920/30fps video + loudness-normalised dialogue audio for one clip."""
    out = TMP / f"n_{cid}.mov"
    if not out.exists():
        run(["ffmpeg", "-y", "-i", str(CLIPS / f"{cid}.mp4"), "-vf",
             "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1",
             "-af", "loudnorm=I=-17:TP=-2:LRA=11,aresample=48000,aformat=channel_layouts=stereo",
             "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-c:a", "pcm_s16le", str(out)])
    return out


def still(src: Path, t: float, out: Path) -> Path:
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(0.0, t):.3f}", "-i", str(src), "-frames:v", "1", str(out)])
    return out


def last_word_end(cid: str, t0: float, t1: float) -> float:
    words = json.loads((HERE / "transcripts" / f"{cid}.json").read_text())
    ends = [w["e"] for w in words if t0 <= w["s"] < t1]
    return max(ends) if ends else t0


# ---------- video pieces ----------
def hold_piece(img: Path, n: int, out: Path, z0: float, z1: float) -> Path:
    """A held frame with a slow zoom (pull-out ending exactly on the clip framing, or push-in)."""
    z = f"{z0}+({z1}-{z0})*on/{max(1, n - 1)}"
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(img), "-vf",
         f"scale=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps=30,"
         "format=yuv420p", "-frames:v", str(n), "-c:v", "libx264", "-crf", "16", "-preset", "fast", str(out)])
    return out


def clip_piece(src: Path, t0: float, n: int, out: Path) -> Path:
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t0:.3f}", "-i", str(src), "-frames:v", str(n), "-an",
         "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "fast", str(out)])
    return out


def app_piece(png: Path, prev_img: Path, next_img: Path, n: int, out: Path) -> Path:
    """Real app frame: dissolve in from the previous shot's last frame, slow push-in, dissolve out."""
    xf = 0.35
    d = n / FPS
    run(["ffmpeg", "-y", "-v", "error",
         "-loop", "1", "-t", f"{xf:.3f}", "-i", str(prev_img),
         "-loop", "1", "-t", f"{d:.3f}", "-i", str(png),
         "-loop", "1", "-t", f"{xf + 0.1:.3f}", "-i", str(next_img),
         "-filter_complex",
         "[0:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[a];"
         f"[1:v]scale=2160:3840,zoompan=z='1.0+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
         f":d={n + 30}:s=1080x1920:fps=30,format=yuv420p,setsar=1[b];"
         "[2:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[c];"
         f"[a][b]xfade=transition=fade:duration={xf}:offset=0.001[ab];"
         f"[ab][c]xfade=transition=fade:duration={xf}:offset={d - xf:.3f}[v]",
         "-map", "[v]", "-frames:v", str(n), "-c:v", "libx264", "-crf", "16", "-preset", "fast", str(out)])
    return out


def outro_piece(prev_img: Path, out: Path) -> Path:
    od = dur(OUTRO)
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", "0.6", "-i", str(prev_img), "-i", str(OUTRO),
         "-filter_complex",
         "[0:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[a];"
         "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p,setsar=1[b];"
         "[a][b]xfade=transition=fade:duration=0.45:offset=0.001[v]",
         "-map", "[v]", "-frames:v", str(frames(od)), "-c:v", "libx264", "-crf", "16", "-preset", "fast", str(out)])
    return out


# ---------- captions ----------
def caption_chunks(line: str, start: float) -> list[tuple[str, float, float]]:
    """Split a narrator line into short caption chunks, timed across its spoken span."""
    meta = VOX[line]
    words = meta.get("words") or []
    s0 = words[0]["s"] if words else 0.0
    s1 = words[-1]["e"] if words else meta["dur"]
    toks = line.split()
    chunks, cur = [], []
    for t in toks:
        cur.append(t)
        txt = " ".join(cur)
        if len(txt) >= 22 or (re.search(r"[.,?!]$", t) and len(txt) > 9):
            chunks.append(txt)
            cur = []
    if cur:
        if chunks and len(" ".join(cur)) < 8:
            chunks[-1] += " " + " ".join(cur)
        else:
            chunks.append(" ".join(cur))
    total = sum(len(c) for c in chunks)
    out, t = [], s0
    for c in chunks:
        d = (s1 - s0) * len(c) / total
        out.append((c, start + t, start + t + d))
        t += d
    # stretch each chunk to the next one's start so captions don't flicker off between words
    return [(c, a, (out[i + 1][1] if i + 1 < len(out) else b + 0.25)) for i, (c, a, b) in enumerate(out)]


# ---------- part ----------
def build(part: int) -> Path:
    beats = PARTS[part]
    pieces: list[Path] = []
    vo_events: list[tuple[str, float]] = []
    dia_events: list[tuple[Path, float, float, float]] = []  # src, clip_t0, length, timeline_start
    plug_start = None
    T = 0  # timeline in frames
    prev_last_img = None

    for bi, b in enumerate(beats):
        tag = f"p{part}_{bi:02d}"
        if b.get("clip") and b["clip"].startswith("PL") and plug_start is None:
            plug_start = T / FPS
        if "clip" in b:
            cid = b["clip"]
            src = norm_clip(cid)
            t0 = b.get("t0", 0.0)
            t1 = min(b.get("t1", 999.0), dur(src) - 0.05)
            n_clip = frames(t1 - t0)
            # intro lines over a held first frame
            t_cursor, pre = 0.2, 0.0
            for line in b.get("intro", []):
                vo_events.append((line, T / FPS + t_cursor))
                t_cursor += VOX[line]["dur"] + GAP
            if b.get("intro"):
                pre = t_cursor + 0.15
            n_pre = frames(pre) if pre else 0
            base = (T + n_pre) / FPS  # timeline time of clip t0
            last_end = (T / FPS + t_cursor - GAP) if b.get("intro") else -1.0
            for line, at in b.get("vo", []):
                if at == "END":
                    at = last_word_end(cid, t0, t1) + 0.25
                st = base + (at - t0) if at is not None else last_end + GAP
                st = max(st, last_end + 0.15)
                vo_events.append((line, st))
                last_end = st + VOX[line]["dur"]
            post = max(0.0, last_end + 0.45 - (base + n_clip / FPS))
            n_post = frames(post) if post > 0.05 else 0
            first = still(src, t0 + 0.02, TMP / f"{tag}_first.png")
            last = still(src, t0 + (n_clip - 1) / FPS, TMP / f"{tag}_last.png")
            if n_pre:
                pieces.append(hold_piece(first, n_pre, TMP / f"{tag}_a.mp4", 1.045, 1.0))
            pieces.append(clip_piece(src, t0, n_clip, TMP / f"{tag}_b.mp4"))
            dia_events.append((src, t0, n_clip / FPS, base))
            if n_post:
                pieces.append(hold_piece(last, n_post, TMP / f"{tag}_c.mp4", 1.0, 1.035))
            T += n_pre + n_clip + n_post
            prev_last_img = last
        elif "app" in b:
            if plug_start is None:
                plug_start = T / FPS
            t_cursor = 0.5
            for line in b["vo"]:
                vo_events.append((line, T / FPS + t_cursor))
                t_cursor += VOX[line]["dur"] + GAP
            n = frames(t_cursor + 0.35)
            nxt = beats[bi + 1]
            nxt_first = still(norm_clip(nxt["clip"]), nxt.get("t0", 0.0) + 0.02, TMP / f"{tag}_next.png")
            pieces.append(app_piece(PLAY / b["app"], prev_last_img, nxt_first, n, TMP / f"{tag}_app.mp4"))
            T += n
        elif "outro" in b:
            outro_start = T / FPS
            pieces.append(outro_piece(prev_last_img, TMP / f"{tag}_outro.mp4"))
            vo_events.append((b["outro"], outro_start + 0.9))
            T += frames(dur(OUTRO))

    total = T / FPS
    # ---------- video: concat pieces, then burn narrator captions ----------
    lst = TMP / f"p{part}_list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in pieces))
    body = TMP / f"p{part}_body.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(body)])

    caps = []
    outro_lines = {b["outro"] for b in beats if "outro" in b}
    for line, st in vo_events:
        cy = 330 if line in outro_lines else 1490  # above the logo, clear of the store badges
        caps += [(c, s0, e0, cy) for c, s0, e0 in caption_chunks(line, st)]
    inputs, fc, last = [], [], "0:v"
    for i, (text, a, e, cy) in enumerate(caps):
        png = TMP / f"p{part}_cap{i:03d}.png"
        ov.stroke_text(text, png, size=62, cy=cy)
        inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", str(png)]
        fc.append(f"[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{a:.3f},{e:.3f})'[c{i}]")
        last = f"c{i}"
    fc.append(f"[{last}]format=yuv420p[vout]")
    (TMP / f"p{part}_caps.txt").write_text(";\n".join(fc))
    video = TMP / f"p{part}_video.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(body), *inputs, "-filter_complex_script",
         str(TMP / f"p{part}_caps.txt"), "-map", "[vout]", "-t", f"{total:.3f}", "-c:v", "libx264",
         "-crf", "18", "-preset", "medium", str(video)])

    # ---------- audio ----------
    N = int(total * SR) + SR
    dia, vo, mus = (np.zeros((N, 2), np.float32) for _ in range(3))
    for src, t0, length, at in dia_events:
        a = load_audio(src, t0, length)
        f = min(len(a), int(0.02 * SR))
        if f:
            a[:f] *= np.linspace(0, 1, f)[:, None]
            a[-f:] *= np.linspace(1, 0, f)[:, None]
        i = int(at * SR)
        dia[i:i + len(a)] += a[: N - i]
    duck = np.ones(N, np.float32)
    for line, st in vo_events:
        a = load_audio(VO / VOX[line]["file"])
        i = int(st * SR)
        vo[i:i + len(a)] += a[: N - i]
        s, e = max(0, int((st - 0.12) * SR)), min(N, int((st + VOX[line]["dur"] + 0.1) * SR))
        duck[s:e] = 0.22
    # smooth the duck envelope (~120 ms)
    k = int(0.12 * SR)
    duck = np.convolve(duck, np.ones(k) / k, mode="same").astype(np.float32)

    plug_t = plug_start if plug_start is not None else total
    outro_t = total - dur(OUTRO)
    bed_p, swell_p = CLIPS / "MUSIC_A.mp4", CLIPS / "MUSIC_B.mp4"
    if bed_p.exists():  # playful bed under the comedy, looped with 1 s crossfades
        bed = load_audio(bed_p)
        bed /= max(1e-6, float(np.sqrt((bed ** 2).mean()))) / 0.035
        x = int(1.0 * SR)
        t = 0
        while t < int(plug_t * SR):
            seg = bed.copy()
            seg[:x] *= np.linspace(0, 1, x)[:, None]
            seg[-x:] *= np.linspace(1, 0, x)[:, None]
            mus[t:t + len(seg)] += seg[: N - t]
            t += len(seg) - x
        fade_end = int(plug_t * SR)
        mus[fade_end:] = 0
        f = int(0.8 * SR)
        mus[max(0, fade_end - f):fade_end] *= np.linspace(1, 0, min(f, fade_end))[:, None]
    if swell_p.exists() and plug_start is not None:  # the plug gets the big hopeful swell
        sw = load_audio(swell_p)
        sw /= max(1e-6, float(np.sqrt((sw ** 2).mean()))) / 0.06
        i = int(plug_t * SR)
        L = min(len(sw), int((outro_t + 1.2 - plug_t) * SR), N - i)
        seg = sw[:L].copy()
        seg[: int(0.6 * SR)] *= np.linspace(0, 1, int(0.6 * SR))[:, None]
        seg[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))[:, None]
        mus[i:i + L] += seg
    mus *= (0.55 + 0.45 * duck)[:, None]  # music dips a little under the narrator

    # outro: its wave wash + chime (no second announcer; the narrator closes)
    o = int(outro_t * SR)
    wave = load_audio(OUTRO_WAVE, 0, dur(OUTRO)) * 0.5
    dia[o:o + len(wave)] += wave[: N - o]
    ch = load_audio(CHIME) * 0.8
    c = int((outro_t + 3.15) * SR)
    dia[c:c + len(ch)] += ch[: N - c]

    mix = dia * duck[:, None] + vo + mus
    mix = mix[: int(total * SR)]
    wav = TMP / f"p{part}_mix.f32"
    wav.write_bytes(mix.astype(np.float32).tobytes())

    final = ROOT / f"Trip_People_Pt{part}_doc.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(wav),
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af",
         "alimiter=limit=0.89:attack=5:release=60,loudnorm=I=-14:TP=-1.2:LRA=11,aresample=48000",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(final)])
    print(f"Pt {part}: {final.name} {dur(final):.1f}s, {len(vo_events)} narrator lines, {len(caps)} captions",
          flush=True)
    return final


if __name__ == "__main__":
    for p in sys.argv[1:] or ["1", "2", "3"]:
        build(int(p))
