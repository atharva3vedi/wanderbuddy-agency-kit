"""Word timings for every narrator line (faster-whisper), for caption chunking + a pronunciation check."""
import json
from pathlib import Path

from faster_whisper import WhisperModel

VO = Path(__file__).resolve().parent / "vo"
index = json.loads((VO / "index.json").read_text())
model = WhisperModel("small.en", device="cpu", compute_type="int8")
for line, meta in index.items():
    segs, _ = model.transcribe(str(VO / meta["file"]), word_timings=True) if False else \
        model.transcribe(str(VO / meta["file"]), word_timestamps=True, language="en")
    words = [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)} for s in segs for w in s.words]
    meta["words"] = words
    heard = " ".join(w["w"] for w in words)
    print(("OK  " if heard.lower().replace(",", "").replace(".", "")[:12] == line.lower().replace(",", "").replace(".", "")[:12] else "??  ") + heard)
(VO / "index.json").write_text(json.dumps(index, indent=1))
