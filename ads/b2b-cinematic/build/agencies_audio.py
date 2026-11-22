"""Three Agencies: a working score from what we already own (the Iowa Steinway
notes, nothing synthesized, no bed). It is a stand-in until the founder picks a
licensed track from MUSIC_SHORTLIST.md: a low open fifth, a soft clock tick that
stops dead at dawn, a note on each thing that happens.

  /Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13 build/agencies_audio.py
Output: out/audio/agencies.wav (29.6 s, 48 kHz stereo, -14 LUFS) and agencies.json.
"""
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio import OUT, SR, convolve, note, place, reverb_ir  # noqa: E402

FPS = 24
CARD = 26.1
DUR = CARD + 84 / FPS
S4, S5 = 372, 492


def short(x, seconds):
    n = int(seconds * SR)
    y = x[:n].copy()
    y *= np.linspace(1, 0, len(y))[:, None] ** 2
    return y


def main():
    n = int(DUR * SR)
    dry = np.zeros((n, 2), dtype=np.float32)      # the ticks stay dry and close
    keys = np.zeros((n, 2), dtype=np.float32)
    ev, ticks = [], []
    f = lambda fr: fr / FPS  # noqa: E731
    ev += [(0.0, "G2", -7.0), (0.02, "D3", -9.0)]
    for t in (4.0, 8.0, 12.0, 16.0):              # the night, breathing
        ev.append((t, "G2", -13.0))
    t = 0.5
    k = 0
    while t < f(S5) - 0.2:                        # the clock: stops dead when the shutters are due
        ticks.append((t, "D6" if k % 2 else "B5", -23.0 if k % 2 else -21.0))
        t += 0.5
        k += 1
    for fr, nm in ((104, "D4"), (146, "B3")):     # two phones buzz behind two shutters
        ev += [(f(fr), nm, -13.0), (f(fr) + 0.11, nm, -15.0)]
    ev += [(f(188), "B4", -15.0), (f(188) + 0.07, "D5", -15.0), (f(188) + 0.14, "G5", -15.0)]   # the laptop wakes
    ev += [(f(276), "D5", -10.0), (f(292), "G4", -9.5), (f(292) + 0.012, "D5", -9.5)]            # the answer, the ring
    ev += [(f(S4), "D4", -12.0), (f(402), "B3", -11.0), (f(434), "D3", -9.5), (f(462), "G2", -5.5), (f(462) + 0.02, "D3", -8.5)]
    for i, nm in enumerate(["G4", "B4", "D5"]):   # the shutters go up
        ev.append((f(518) + 0.13 * i, nm, -13.0))
    for i, nm in enumerate(["B4", "D5", "G5"]):
        ev.append((f(540) + 0.13 * i, nm, -13.0))
    ev += [(24.3, "G4", -10.0), (24.312, "D5", -10.0)]
    for i, nm in enumerate(["G4", "B4", "D5", "G5"]):                # the end card
        ev.append((CARD + 0.17 + 0.085 * i, nm, -9.0))
    for nm, g in (("G2", -6.0), ("D3", -8.0), ("G4", -10.0), ("B4", -12.0)):
        ev.append((CARD + 1.05, nm, g))
    for t, nm, g in ev:
        place(keys, note(nm), t, g)
    for t, nm, g in ticks:
        place(dry, short(note(nm), 0.16), t, g)
    wet = 0.45
    out = (1 - wet) * keys + wet * 1.6 * convolve(keys, reverb_ir())[:n] + dry
    os.makedirs(OUT, exist_ok=True)
    raw = os.path.join(OUT, "agencies_raw.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", raw],
                   input=out.astype(np.float32).tobytes(), check=True)
    p1 = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True).stderr
    js = json.loads(p1[p1.rindex("{"):p1.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    final = os.path.join(OUT, "agencies.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", ln, "-ar", str(SR), final], check=True)
    json.dump({"notes": [{"t": round(t, 3), "note": nm, "gain_db": g} for t, nm, g in sorted(ev)],
               "ticks": {"from": 0.5, "to": round(f(S5) - 0.2, 2), "every": 0.5, "notes": ["B5", "D6"]},
               "bed": None, "reverb_wet": wet, "loudnorm_pass1": js}, open(os.path.join(OUT, "agencies.json"), "w"), indent=1)
    print("agencies ->", final, "input_i", js["input_i"])


if __name__ == "__main__":
    main()
