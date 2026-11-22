"""The Reel: an original score generated here (score_lib.py).

  /Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13 build/reel_audio.py

D major, so it sits apart from the other films. A quiet night (rain indoors, low strings);
plucked strings count the steps as the plan is written; when the pages slide out the strings
open up and a plucked figure runs with them, one note a page; a warm chord on Book; the same
quiet for the question on the trip; and a full D chord for the stack at dawn.
The piano is the real Steinway notes (D, B, G and the E and A made from them).
Output: out/audio/reel.wav (35.2 s) and reel.json.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_lib import Score, hz  # noqa: E402

FPS = 24
CARD = 31.7
DUR = CARD + 84 / FPS
f = lambda fr: fr / FPS  # noqa: E731
RB, RB2, RC, RD, RE, RF = f(96), f(156), f(240), f(432), f(552), f(672)


def main():
    s = Score(DUR, seed=21)
    # night: rain behind glass, low strings
    s.noise("rain", 120, 1100, 0.0, RC + 0.3, -33, tilt=-4.5, attack=1.5, release=0.8, seed=4)
    s.noise("rain", 120, 1100, RD - 0.3, RF + 0.3, -34, tilt=-4.5, attack=0.6, release=0.8, seed=5)
    s.pad("strings", ["B2", "F#3", "B3"], 0.0, RB + 0.5, -23, attack=2.5, release=1.0)
    s.pad("strings", ["G2", "D3", "G3", "B3"], RB - 0.4, RB2 + 0.5, -22, attack=1.0, release=0.9)
    s.pad("strings", ["A2", "E3", "A3", "C#4"], RB2 - 0.3, RC + 0.3, -21, attack=0.9, release=0.7)
    ev = [(0.05, "B3", -12.0), (0.07, "D4", -15.0), (2.6, "D5", -14.0)]
    ev += [(f(112), "D5", -10.0), (f(112) + 0.012, "A4", -11.0)]                    # one button
    for k, nm in enumerate(["D4", "E4", "F#4", "A4", "B4"]):                          # the five steps, ticked off
        s.string("plucks", RB2 + 0.25 + 0.2 * k, hz(nm), -14, pan=-0.3 + 0.15 * k, seconds=1.6)
    ev += [(f(196), "D5", -10.0), (f(196) + 0.012, "A4", -11.0), (f(196) + 0.024, "G5", -12.0)]   # the plan is ready
    # the pages: the strings open, one plucked note a page
    s.pad("strings", ["D3", "A3", "D4", "F#4"], RC - 0.2, RC + 4.2, -19, attack=0.8, release=1.0, bright=1.2)
    s.pad("strings", ["G2", "D3", "G3", "B3", "D4"], RC + 3.6, RC + 6.4, -19, attack=0.9, release=1.0, bright=1.2)
    s.pad("strings", ["A2", "E3", "A3", "C#4", "E4"], RC + 5.8, RD + 0.2, -19, attack=0.8, release=0.5, bright=1.2)
    run = ["D5", "F#5", "A5", "D5", "E5", "G5", "B5", "A5", "F#5", "D5", "E5", "A5", "D6"]
    for k, nm in enumerate(run):
        s.string("plucks", f(240 + 14 + 7 * k), hz(nm), -13, pan=(-0.4 if k % 2 == 0 else 0.4), seconds=2.2)
    s.thump("hits", RC + 0.02, 70, 42, 1.0, -16)
    ev += [(RC + 0.03, "D3", -9.0), (f(240 + 124), "D5", -11.0), (f(240 + 124) + 0.012, "A4", -12.0)]
    # Book
    s.pad("strings", ["G2", "D3", "G3", "B3"], RD - 0.2, f(452) + 0.4, -22, attack=0.6, release=0.6)
    s.pad("strings", ["D3", "A3", "D4", "F#4", "A4"], f(452) - 0.2, RE + 0.3, -19, attack=0.4, release=1.2)
    s.thump("hits", f(452), 72, 42, 1.2, -14)
    ev += [(f(452), "D3", -9.0), (f(452), "D5", -9.0), (f(452) + 0.012, "A4", -10.0)]
    # on the trip, 23:47
    s.pad("strings", ["B2", "F#3", "B3"], RE - 0.2, f(596) + 0.3, -24, attack=0.8, release=0.8)
    s.pad("strings", ["G2", "D3", "G3", "B3", "D4"], f(596) - 0.2, RF + 0.3, -20, attack=0.5, release=1.0)
    ev += [(RE + 0.1, "B3", -12.0), (f(580), "D5", -10.0), (f(596), "G4", -9.5), (f(596) + 0.012, "D5", -9.5)]
    # dawn: the stack
    s.pad("strings", ["D3", "A3", "D4", "F#4", "A4"], RF - 0.2, DUR - 0.2, -18, attack=0.8, release=2.6, bright=1.2)
    for k, nm in enumerate(["D5", "A5", "D6"]):
        s.string("plucks", RF + 0.3 + 0.35 * k, hz(nm), -14, pan=0.0, seconds=2.6)
    ev += [(RF + 0.05, "D3", -9.0), (RF + 0.07, "D4", -11.0)]
    ev += s.end_card(CARD)
    s.piano(ev)
    s.room("plucks", wet=0.3)
    s.room("strings")
    s.write("reel", gains={"strings": 7.0, "plucks": 3.0, "rain": 2.0})


if __name__ == "__main__":
    main()
