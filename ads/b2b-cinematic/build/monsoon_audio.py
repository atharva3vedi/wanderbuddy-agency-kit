"""Monsoon: an original score generated here (score_lib.py), nothing like film 1's.

  /Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13 build/monsoon_audio.py

A ceiling fan and messages arriving faster and faster; hand drums that speed up
with the paper storm (100 to 180 beats a minute); a dead stop when the fan does,
with only paper landing; then next door: quiet strings in C and G, rain, the
piano on each ring; the street, and G major when the ring lands on the winner.
Output: out/audio/monsoon.wav (30.7 s) and monsoon.json.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_lib import Score, hz  # noqa: E402

FPS = 24
CARD = 27.2
DUR = CARD + 84 / FPS
f = lambda fr: fr / FPS  # noqa: E731
MB, MC, MD, ME = f(84), f(252), f(324), f(516)


def main():
    s = Score(DUR, seed=5)
    rng = np.random.default_rng(9)
    # the fan, until it stops
    s.hum("fan", 0.0, MC + 1.9, -27, stop_from=MC - 0.2)
    # messages arriving: faster and faster, then swallowed by the drums
    ev = []
    t, gap, k = 0.35, 0.62, 0
    while t < MC - 0.3:
        ev.append((t, ["D6", "B5", "G5", "E6", "A5"][k % 5], -17.0 - (3.0 if t > MB + 2 else 0.0)))
        t += gap
        gap = max(0.13, gap * 0.86)
        k += 1
    s.buzz("hits", 0.9, -24)
    s.buzz("hits", 2.3, -24)
    # the drums: one bar pattern, the tempo climbing
    t, beat = MB, 0
    while t < MC - 0.05:
        u = (t - MB) / (MC - MB)
        bpm = 100 + 80 * u ** 1.3
        six = 60 / bpm / 4
        g = -21 + 9 * u
        fill = beat % 4 == 3 or u > 0.8
        s.dum("drums", t, g + 2, pan=-0.15)
        s.tak("drums", t + six, g - 8, pan=0.3, tone=380)
        s.tak("drums", t + 2 * six, g - 1, pan=0.25)
        (s.dum if fill else s.tak)("drums", t + 3 * six, g - (3 if fill else 7), pan=(-0.2 if fill else 0.35))
        if u > 0.45:
            s.tak("drums", t + 2.5 * six, g - 9, pan=-0.3, tone=520)
        t += 4 * six
        beat += 1
    s.room("drums", wet=0.18)
    # paper in the air: a swell of air that rises with the storm
    s.noise("paper", 900, 6500, MB + 0.5, MC + 0.1, -31, tilt=-1.5, attack=5.5, release=0.12, seed=21)
    # tension under the drums
    s.pad("strings", ["E2", "B2", "E3"], MB, MC + 0.05, -24, attack=3.0, release=0.08)
    s.pad("strings", ["G3", "B3"], MB + 3.2, MC + 0.05, -26, attack=2.5, release=0.08)
    # it all comes down: paper landing, one low note for what is lost
    for k in range(9):
        s.thump("hits", MC + 0.35 + 0.17 * k + rng.uniform(-0.04, 0.04), 150, 90, 0.035, -27 + rng.uniform(-3, 2))
    s.thump("hits", f(252 + 42), 120, 70, 0.07, -19)          # the passport copy on the floor
    ev += [(f(252 + 44), "E3", -9.0), (f(252 + 44) + 0.02, "B3", -13.0)]
    # next door
    s.noise("rain", 120, 1100, MD - 0.3, ME + 0.3, -33, tilt=-4.5, attack=0.6, release=0.6, seed=4)
    s.noise("rain", 350, 8000, ME - 0.2, DUR, -31, tilt=-3.0, attack=0.5, release=1.5, seed=3)
    s.pad("strings", ["C3", "G3", "C4", "E4"], MD - 0.2, f(444) + 0.4, -21, attack=1.2, release=1.0)
    s.pad("strings", ["G2", "D3", "G3", "B3", "D4"], f(444) - 0.4, ME + 0.3, -20, attack=1.0, release=1.0)
    ev += [(MD + 0.1, "G4", -13.0), (MD + 0.12, "E4", -15.0),
           (f(410), "G4", -10.0), (f(410) + 0.012, "D5", -10.0), (f(444), "A4", -14.0),
           (f(474), "G4", -10.0), (f(474) + 0.012, "B4", -11.0), (f(474) + 0.024, "D5", -10.0)]
    # the street at 23:30
    s.pad("strings", ["E2", "B2", "E3"], ME - 0.2, f(586) + 0.3, -23, attack=0.9, release=0.8)
    s.pad("strings", ["G2", "D3", "G3", "B3", "D4", "G4"], f(586) - 0.15, DUR - 0.2, -18, attack=0.4, release=2.6)
    s.thump("hits", f(586), 72, 42, 1.3, -13)
    ev += [(ME, "E3", -11.0), (f(586), "G2", -8.0), (f(586), "G4", -9.0), (f(586) + 0.012, "B4", -10.0), (f(586) + 0.024, "D5", -9.0)]
    ev += s.end_card(CARD)
    s.piano(ev)
    s.room("strings")
    s.write("monsoon", gains={"strings": 7.0, "drums": 4.0, "rain": 2.0, "fan": 0.0, "paper": 0.0})


if __name__ == "__main__":
    main()
