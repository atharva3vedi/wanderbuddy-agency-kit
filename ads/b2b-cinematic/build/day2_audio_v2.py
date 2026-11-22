"""Day 2, new score: so it no longer shares the bossa bed with anything.

  /Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13 build/day2_audio_v2.py

Generated here (score_lib.py): plucked strings in G pentatonic, slow, like a zither
heard across water; a low drone of strings in G and D that opens to C and back;
air over water. Seven plucks climb for the seven boat lights. The real piano
marks the two rings and the end card. Same picture and timing as out/4-day2.mp4.
Output: out/audio/day2v2.wav (24.7 s) and day2v2.json.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_lib import Score, hz  # noqa: E402

FPS = 24
CARD = 21.2
DUR = 24.7
f = lambda fr: fr / FPS  # noqa: E731


def main():
    s = Score(DUR, seed=3)
    s.noise("air", 150, 2400, 0.0, 15.5, -36, tilt=-4.0, attack=2.0, release=2.5, seed=8)
    s.pad("strings", ["G2", "D3", "G3"], 0.0, 9.6, -22, attack=3.0, release=1.6)
    s.pad("strings", ["E2", "B2", "E3", "G3"], 8.6, 14.2, -22, attack=1.4, release=1.4)
    s.pad("strings", ["C3", "G3", "C4", "E4"], 13.4, 18.9, -21, attack=1.2, release=1.2)
    s.pad("strings", ["G2", "D3", "G3", "B3", "D4"], 18.2, DUR - 0.2, -19, attack=1.0, release=2.2)
    # the zither: a slow figure, each note left to ring
    motif = [(0.6, "D5"), (1.5, "B4"), (2.4, "G4"), (3.6, "A4"), (4.5, "D5"), (5.7, "E5"), (6.6, "D5"), (7.8, "B4")]
    for k, (t, nm) in enumerate(motif):
        s.string("zither", t, hz(nm), -15, pan=(-0.3 if k % 2 else 0.3), seconds=3.2)
        if k % 4 == 0:
            s.string("zither", t + 0.02, hz(nm) / 2, -20, pan=0.0, seconds=3.2)
    for k, nm in enumerate(["G4", "A4", "B4", "D5", "E5", "G5", "A5"]):      # seven boat lights
        s.string("zither", f(222) + 0.13 * k, hz(nm), -13 + 0.4 * k, pan=-0.45 + 0.15 * k, seconds=3.0)
    for t, nm in ((11.6, "E5"), (12.5, "D5"), (14.2, "G4"), (15.1, "B4"), (17.4, "D5"), (19.6, "G5"), (20.4, "D5")):
        s.string("zither", t, hz(nm), -17, pan=0.2, seconds=2.6)
    s.room("zither", wet=0.34)
    s.room("strings")
    ev = [(f(392), "G4", -10.0), (f(392) + 0.012, "D5", -10.0), (f(452), "G4", -10.0), (f(452) + 0.012, "D5", -10.0)]
    ev += s.end_card(CARD)
    s.piano(ev)
    s.write("day2v2", gains={"strings": 6.0, "zither": 3.0, "air": 2.0})


if __name__ == "__main__":
    main()
