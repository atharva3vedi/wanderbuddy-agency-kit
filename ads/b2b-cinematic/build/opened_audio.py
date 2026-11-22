"""Opened 3 Times: an original score generated here (score_lib.py). Close and quiet.

  /Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13 build/opened_audio.py

A slow heartbeat and warm strings in A minor while she reads; each time she opens
the plan the piano steps up one note; a ringing tone when Lantern Trips calls, and
C major when she books; a bare clock next door; F, G, C as the shutters go up.
(A minor and C major so this film does not sit in the same key as the others.
The piano notes are the real Steinway samples, shifted where the set has no note.)
Output: out/audio/opened.wav (30.3 s) and opened.json.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio import SR  # noqa: E402
from score_lib import Score, db, hz  # noqa: E402

FPS = 24
CARD = 26.8
DUR = CARD + 84 / FPS
f = lambda fr: fr / FPS  # noqa: E731
TD, TE, TF = f(240), f(420), f(516)


def ringback(s, t0, seconds, gain_db):
    """A phone ringing at the other end: two tones, on and off."""
    n = int(seconds * SR)
    t = np.arange(n) / SR
    tone = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.5 * np.sin(2 * np.pi * 480 * t)
    gate = ((t % 0.9) < 0.42).astype(float)
    gate = np.convolve(gate, np.ones(400) / 400, mode="same")
    sig = (tone * gate * np.clip(t / 0.02, 0, 1) * np.clip((seconds - t) / 0.05, 0, 1) * db(gain_db)).astype(np.float32)
    s.add("hits", np.stack([sig, sig], axis=1), t0)


def main():
    s = Score(DUR, seed=11)
    # she reads: a heartbeat, warm strings
    t = 0.4
    while t < TD - 0.3:
        s.thump("pulse", t, 62, 44, 0.16, -22)
        s.thump("pulse", t + 0.28, 56, 42, 0.12, -27)
        t += 1.15
    s.pad("strings", ["A2", "E3", "A3", "C4"], 0.0, 6.4, -22, attack=2.5, release=1.4)
    s.pad("strings", ["F2", "C3", "F3", "A3"], 5.4, TD + 0.4, -22, attack=1.4, release=1.2)
    ev = [(0.05, "A2", -10.0), (0.07, "E4", -15.0)]
    for k, (fr, nm) in enumerate(((76, "A4"), (140, "B4"), (196, "D5"))):      # opened once, twice, three times
        ev += [(f(fr), nm, -11.0 + k), (f(fr) + 0.012, "E5" if k < 2 else "G5", -15.0)]
    # Lantern Trips: the prompt, the call, the booking
    s.noise("rain", 120, 1100, TD - 0.3, TE + 0.3, -34, tilt=-4.5, attack=0.6, release=0.6, seed=4)
    s.pad("strings", ["G2", "D3", "G3", "B3"], TD - 0.2, f(356) + 0.3, -22, attack=1.0, release=0.8)
    ev += [(f(326), "G4", -10.0), (f(326) + 0.012, "D5", -10.0)]
    ringback(s, f(326) + 0.5, 1.1, -27)
    s.pad("strings", ["C3", "G3", "C4", "E4", "G4"], f(356) - 0.3, TE + 0.4, -19, attack=0.5, release=1.2)
    s.thump("hits", f(384), 72, 42, 1.2, -14)
    ev += [(f(384), "G2", -9.0), (f(384), "G4", -9.0), (f(384) + 0.012, "B4", -10.0), (f(384) + 0.024, "E5", -9.0)]
    # next door: a clock, and nothing else
    t = TE + 0.4
    k = 0
    while t < TF - 0.3:
        s.pluck("pulse", t, hz("E3") if k % 2 else hz("A3"), -24, pan=(-0.2 if k % 2 else 0.2))
        t += 0.5
        k += 1
    s.pad("strings", ["A2", "E3"], TE - 0.1, TF + 0.2, -25, attack=0.8, release=0.8)
    ev += [(TE + 0.05, "A2", -10.0), (f(472), "E3", -10.0)]
    # the street at dawn
    s.pad("strings", ["F2", "C3", "F3", "A3"], TF - 0.2, f(556) + 0.5, -20, attack=0.8, release=0.9)
    s.pad("strings", ["G2", "D3", "G3", "B3"], f(556) - 0.3, f(580) + 0.4, -20, attack=0.7, release=0.8)
    s.pad("strings", ["C3", "G3", "C4", "E4", "G4"], f(580) - 0.2, DUR - 0.2, -18, attack=0.5, release=2.6)
    for i, nm in enumerate(["A4", "B4", "D5"]):
        ev.append((f(534) + 0.13 * i, nm, -13.0))
    for i, nm in enumerate(["B4", "D5", "E5"]):
        ev.append((f(556) + 0.13 * i, nm, -13.0))
    ev += [(f(580), "G4", -10.0), (f(580) + 0.012, "E5", -10.0)]
    ev += s.end_card(CARD)
    s.piano(ev)
    s.room("strings")
    s.write("opened", gains={"strings": 7.0, "pulse": 5.0, "rain": 2.0})


if __name__ == "__main__":
    main()
