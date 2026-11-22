"""Narrator lines -> vo/NNN.wav (Kokoro bm_george, slowed, pitched down a touch, warm room).
Run with the kokoro venv python:  python tts.py [voice] [speed]
An original British documentary-style voice, not a clone of any real narrator."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import soundfile as sf
from kokoro_onnx import Kokoro

import importlib
import os

_n = importlib.import_module(os.environ.get("NARR", "narration"))
all_lines, tts_text = _n.all_lines, _n.tts_text

HERE = Path(__file__).resolve().parent
VO = HERE / "vo"
VO.mkdir(exist_ok=True)
CACHE = Path.home() / ".cache/hyperframes/tts"
voice = sys.argv[1] if len(sys.argv) > 1 else "bm_george"
speed = float(sys.argv[2]) if len(sys.argv) > 2 else 0.88

k = Kokoro(str(CACHE / "models/kokoro-v1.0.onnx"), str(CACHE / "voices/voices-v1.0.bin"))
index = {}
for line in all_lines():
    key = hashlib.sha1(f"{voice}|{speed}|{line}".encode()).hexdigest()[:10]
    raw, out = VO / f"{key}_raw.wav", VO / f"{key}.wav"
    if not out.exists():
        samples, sr = k.create(tts_text(line), voice=voice, speed=speed, lang="en-gb")
        sf.write(raw, samples, sr)
        # pitch down ~4% (keeps length), gentle warmth + a small room, then -16 LUFS, 48k stereo
        af = (f"asetrate={sr}*0.96,aresample={sr},atempo=1.0417,"
              "equalizer=f=180:t=q:w=1:g=2.5,equalizer=f=6500:t=q:w=1:g=-2,"
              "aecho=0.8:0.5:28:0.10,silenceremove=start_periods=1:start_threshold=-50dB,"
              "areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
              "loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000,aformat=channel_layouts=stereo")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", af, str(out)], check=True)
        raw.unlink()
    info = sf.info(str(out))
    index[line] = {"file": out.name, "dur": round(info.frames / info.samplerate, 3)}
    print(f"{index[line]['dur']:5.2f}s  {line}", flush=True)
(VO / "index.json").write_text(json.dumps(index, indent=1))
