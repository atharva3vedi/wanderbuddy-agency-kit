"""Cut Pt 1/2/3: normalize each Seedance clip to 1080x1920/30fps/48k, burn labels, captions
(timed from transcripts/) and supers, then concat with the shared plug and the brand outro.

    python assemble.py 1 2 3
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import overlays as ov
from parts import PARTS, CAPTION_FIXES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[2]
TMP = HERE / "tmp"
TMP.mkdir(exist_ok=True)
OUTRO = REPO / "marketing/outro/outro.mp4"
NORM_V = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
NORM_A = "aresample=48000,aformat=channel_layouts=stereo"


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2500:])
        raise SystemExit(f"ffmpeg failed: {' '.join(cmd[:6])}")


def duration(p: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
        capture_output=True, text=True,
    ).stdout
    return float(out.strip())


def chunks(sid: str, t0: float, t1: float) -> list[tuple[str, float, float]]:
    """Group transcript words into short caption lines inside the [t0, t1] trim window."""
    tp = HERE / "transcripts" / f"{sid}.json"
    if not tp.exists():
        return []
    words = [w for w in json.loads(tp.read_text()) if w["s"] >= t0 - 0.05 and w["s"] < t1]
    out, cur = [], []
    for w in words:
        cur.append(w)
        text = " ".join(x["w"] for x in cur)
        if len(cur) >= 5 or len(text) > 24 or w["w"][-1:] in ".?!,":
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    lines = []
    for i, c in enumerate(out):
        s = c[0]["s"] - t0
        e = (out[i + 1][0]["s"] - t0) if i + 1 < len(out) else c[-1]["e"] - t0 + 0.35
        e = min(e, c[-1]["e"] - t0 + 0.6)
        text = " ".join(x["w"] for x in c)
        for bad, good in CAPTION_FIXES.get(sid, []):
            text = text.replace(bad, good)
        lines.append((text, max(0.0, s), e))
    return lines


def segment(seg: dict, idx: int, part: int) -> Path:
    out = TMP / f"p{part}_{idx:02d}.mp4"
    tag = f"p{part}_{idx:02d}"
    if "card" in seg:
        png = TMP / f"{tag}_card.png"
        ov.card(seg["card"], png, seg.get("card_sub"))
        d = seg.get("dur", 1.8)
        run(["ffmpeg", "-y", "-loop", "1", "-t", str(d), "-i", str(png), "-f", "lavfi", "-t", str(d),
             "-i", "anullsrc=r=48000:cl=stereo", "-vf", f"{NORM_V},format=yuv420p", "-c:v", "libx264",
             "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)])
        return out
    if "file" in seg:
        src = Path(seg["file"])
        run(["ffmpeg", "-y", "-i", str(src), "-vf", f"{NORM_V},format=yuv420p", "-af", NORM_A,
             "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k", str(out)])
        return out

    sid = seg["clip"]
    src = ROOT / "clips" / f"{sid}.mp4"
    full = duration(src)
    t0, t1 = seg.get("trim", (0.0, None))
    t1 = full if t1 is None else min(t1, full)
    d = t1 - t0
    layers: list[tuple[Path, float, float, bool]] = []  # png, start, end, fade-in
    if seg.get("hook"):
        png = TMP / f"{tag}_hook.png"
        ov.hook(seg["hook"], seg["tag"], png)
        layers.append((png, 0.0, d, True))
    if seg.get("label"):
        png = TMP / f"{tag}_label.png"
        ov.label(seg["label"], seg.get("sub"), png)
        layers.append((png, 0.0, seg.get("label_until", d), True))
    if seg.get("caps", True):
        for j, (text, s, e) in enumerate(seg.get("lines") or chunks(sid, t0, t1)):
            png = TMP / f"{tag}_cap{j:02d}.png"
            ov.stroke_text(text, png, size=62, cy=seg.get("cap_y", 1450))
            layers.append((png, s, min(e, d), False))
    for j, (text, s, e, size, cy) in enumerate(seg.get("supers", [])):
        png = TMP / f"{tag}_sup{j:02d}.png"
        ov.stroke_text(text, png, size=size, cy=cy, color=(255, 255, 255))
        layers.append((png, s, min(e, d), True))
    for j, (src_png, s, e) in enumerate(seg.get("pops", [])):
        png = TMP / f"{tag}_pop{j:02d}.png"
        ov.app_card(Path(src_png), png)
        layers.append((png, s, min(e, d), True))

    cmd = ["ffmpeg", "-y", "-ss", f"{t0:.3f}", "-t", f"{d:.3f}", "-i", str(src)]
    for png, *_ in layers:
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", str(png)]
    fc = [f"[0:v]{NORM_V}[b0]"]
    last = "b0"
    for k, (png, s, e, fade) in enumerate(layers, start=1):
        f = f"[{k}:v]format=rgba"
        if fade:
            f += f",fade=in:st={s:.2f}:d=0.18:alpha=1"
        fc.append(f + f"[o{k}]")
        fc.append(f"[{last}][o{k}]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[b{k}]")
        last = f"b{k}"
    fc.append(f"[{last}]format=yuv420p[vout]")
    lufs = -15 if seg.get("caps", True) else -24
    af = NORM_A + f",loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample=48000"
    if seg.get("afade"):
        af += f",afade=t=out:st={d - 0.25:.2f}:d=0.25"
    (TMP / f"{tag}_fc.txt").write_text(";\n".join(fc))
    cmd += ["-filter_complex_script", str(TMP / f"{tag}_fc.txt"), "-map", "[vout]", "-map", "0:a",
            "-af", af, "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac",
            "-b:a", "192k", "-t", f"{d:.3f}", str(out)]
    run(cmd)
    return out


def build(part: int) -> Path:
    segs = [segment(s, i, part) for i, s in enumerate(PARTS[part])]
    segs.append(segment({"file": str(OUTRO)}, 99, part))
    inputs, fc = [], []
    for i, p in enumerate(segs):
        inputs += ["-i", str(p)]
        fc.append(f"[{i}:v][{i}:a]")
    final = ROOT / f"Trip_People_Pt{part}.mp4"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", "".join(fc) + f"concat=n={len(segs)}:v=1:a=1[v][a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "19", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final)])
    print(f"Pt {part}: {final.name} {duration(final):.1f}s", flush=True)
    return final


if __name__ == "__main__":
    for p in sys.argv[1:] or ["1", "2", "3"]:
        build(int(p))
