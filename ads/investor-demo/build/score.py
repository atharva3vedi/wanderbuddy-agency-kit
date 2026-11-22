"""The investor demo's music: the bossa nova bed with piano accents.

  /Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13 build/score.py

The founder asked on 2026-11-12 for "more lively bossa nova". The bed is the real
recording every reel uses, marketing/music/musicalmix2020-bossa-nova-summer-instrumental-
brazil-7969.mp3 (Pixabay, human-made; usable in our videos, never shared as a file). It
plays from 56.2 s of the track, its fullest stretch, placed so a downbeat lands as the
laptop opens (7.25 s; the track is 140 BPM with its first downbeat at 3.476 s). For 23:47
it drops 8 dB and goes muffled, as if through a wall, with a clock ticking over it; it
comes back full for the morning and fades under the end card. On top: the real Iowa
Steinway notes (G major, as the reels use them) on the lid, each hop of the arc, the
ring, the 23:48 answer and the model lines, then the end card's four notes and G chord.
Output: out/score.wav (86 s, 48 kHz, -14 LUFS) and out/score.json (every note).
"""
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "../../b2b-cinematic/build")))
import score_lib  # noqa: E402
from audio import BED, SR  # noqa: E402
from score_lib import Score, db  # noqa: E402

score_lib.OUT = os.path.normpath(os.path.join(HERE, "..", "out"))

# The film is 119 s: the friends' act (B2C) sits at 7 to 40 s, and the agency film after it is
# the old one moved D = 33 s later. The bed's offset into the track is chosen so a downbeat
# lands on the laptop opening (LID), which is what the beat has to line up with.
D = 33.0
DUR = 86.0 + D
CARD = 79.4 + D
DOWNBEAT0, BAR = 3.476, 60 / 140 * 4
LID = 7.25 + D
# the track's downbeat nearest 56 s in, moved to the lid
K = round((56.0 + LID - DOWNBEAT0) / BAR)   # whole bars into the track, so a downbeat lands on LID
OFFSET = DOWNBEAT0 + K * BAR - LID          # 56.226 s into the track
NIGHT = (57.6 + D, 69.4 + D)

HITS = [
    # the friends' act: the phone wakes on the group chat, then a note for each card that lifts
    (7.3, "G4", -14.0), (11.0, "B4", -12.0), (15.4, "D5", -12.0), (19.8, "G4", -12.0), (23.5, "D5", -12.0),
    (27.6, "G4", -12.0), (32.0, "B4", -12.0), (36.0, "D5", -12.0), (38.7, "G5", -14.0),
    # the agency film, 33 s later than in the first cut; the add-on card first
    (9.0 + D, "B4", -13.0),
    (LID, "G2", -10.0), (LID + 0.01, "G4", -11.0), (LID + 0.02, "B4", -12.0),  # the lid opens
    (12.0 + D, "G4", -13.0),                                                # the listing lifts
    (18.6 + D, "D5", -12.0),                                                # the arc reaches the phone
    (24.9 + D, "D5", -11.0), (24.912 + D, "G5", -13.0),                     # the ring on the fee
    (31.8 + D, "B4", -12.0),                                                # the hold reaches the inbox
    (39.0 + D, "G4", -15.0), (39.42 + D, "B4", -15.0), (39.84 + D, "D5", -15.0), (40.26 + D, "G5", -16.0),  # the pages
    (46.6 + D, "G5", -12.0),                                                # the plan reaches her phone
    (58.0 + D, "B3", -11.0),                                                # 23:47
    (61.6 + D, "D4", -11.0), (62.9 + D, "B4", -11.0),                       # the question, the answer
    (67.45 + D, "G4", -10.0), (67.46 + D, "D5", -12.0),                     # the answer on her phone
    (71.4 + D, "G4", -12.0), (72.6 + D, "B4", -12.0), (73.8 + D, "D5", -12.0),  # the model lines
]


def bed(lowpass=None):
    af = ["aresample=48000"] + ([f"lowpass=f={lowpass}", f"lowpass=f={lowpass}"] if lowpass else [])
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{OFFSET:.4f}", "-t", f"{DUR + 0.5:.3f}", "-i", BED,
                          "-af", ",".join(af), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
    n = int(DUR * SR)
    return np.pad(x, ((0, max(0, n - len(x))), (0, 0)))[:n]


def main():
    s = Score(DUR, seed=23)
    full, muffled = bed(), bed(lowpass=850)
    t = s.t
    night = s.ramp(NIGHT[0], NIGHT[1], 1.2, 1.0)                      # 0 by day, 1 at night
    edge = s.ramp(0.0, DUR, 1.2, 3.2)                                # fade in, fade under the end card
    mix = full * ((1 - night) * edge)[:, None] + muffled * (night * db(-8.0) * edge)[:, None]
    s.stem("bed")[:] = mix.astype(np.float32)
    s.log.append({"bed": os.path.basename(BED), "from_s": round(OFFSET, 3), "night_db": -8.0, "night_lowpass_hz": 850})
    # 23:47: a clock next to the laptop
    c = NIGHT[0] + 0.8
    while c < NIGHT[1] - 0.6:
        s.tak("clock", c, -30, pan=-0.35, tone=900.0)
        c += 1.0
    s.piano(HITS + s.end_card(CARD))
    s.room("clock", wet=0.35)
    s.write("score", gains={"bed": -4.0, "piano": -2.0, "clock": 14.0},
            note_="investor-demo/build/score.py: the Pixabay bossa bed, the Iowa Steinway notes, a synthesized clock tick")
    del t


main()
