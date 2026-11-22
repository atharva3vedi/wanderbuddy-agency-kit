"""Word-level transcripts of each generated clip (faster-whisper), so burned-in captions
match what the model actually said. Usage: python transcribe.py [IDS...]"""

import json
import sys
from pathlib import Path

from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "transcripts"
OUT.mkdir(exist_ok=True)

ids = sys.argv[1:] or [p.stem for p in sorted((ROOT / "clips").glob("*.mp4"))]
model = WhisperModel("small.en", device="cpu", compute_type="int8")
for sid in ids:
    clip = ROOT / "clips" / f"{sid}.mp4"
    if not clip.exists():
        continue
    segs, _ = model.transcribe(str(clip), word_timestamps=True, vad_filter=False, language="en")
    words = [
        {"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)}
        for s in segs
        for w in (s.words or [])
    ]
    (OUT / f"{sid}.json").write_text(json.dumps(words, indent=1))
    print(sid, "|", " ".join(w["w"] for w in words), flush=True)
