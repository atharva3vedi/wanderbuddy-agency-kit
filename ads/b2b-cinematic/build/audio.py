"""The four scores (Brand Codex 06): the Pixabay bossa bed and the Iowa Steinway
notes in G, nothing synthesized. Run with Blender's Python (it has numpy):

  /Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13 build/audio.py [film ...]

Each film: piano notes on what happens on screen, a room reverb on the piano
only (an exponential tail, the notes stay real recordings), the bed coming in on
a downbeat at the film's turn, the end card's run and G chord, then two-pass
loudnorm to -14 LUFS. Output: out/audio/<film>.wav (24.7 s, 48 kHz stereo) and
out/audio/<film>.json (every note, for the record).
"""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.dirname(HERE)
ROOT = os.path.normpath(os.path.join(AD, "../../.."))
PIANO = os.path.join(ROOT, "marketing/music/piano")
BED = os.path.join(ROOT, "marketing/music/musicalmix2020-bossa-nova-summer-instrumental-brazil-7969.mp3")
OUT = os.path.join(AD, "out", "audio")
SR, FPS = 48000, 24
DUR = 24.7                     # 21.5 s of film, the end card from 21.2 s (0.3 s crossfade), 3.5 s long
CARD = 21.2
DOWNBEAT0, BAR = 3.476, 60 / 140 * 4


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


NOTES = {}


def note(name):
    if name not in NOTES:
        shift = {"E": ("D", 2), "A": ("G", 2)}
        base, semis = shift.get(name[0], (name[0], 0))
        x = load(os.path.join(PIANO, base + name[1:] + ".wav"))
        if semis:
            r = 2 ** (semis / 12)
            idx = np.arange(0, len(x) - 1, r)
            x = np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in (0, 1)], axis=1).astype(np.float32)
        NOTES[name] = x
    return NOTES[name]


def reverb_ir(seconds=2.4, seed=1):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    env = np.exp(-6.9 * t / seconds)
    ir = rng.standard_normal((n, 2)).astype(np.float32) * env[:, None]
    ir[: int(0.012 * SR)] = 0                         # a short pre-delay
    # darker tail: a one-pole low-pass
    a = 0.82
    for c in (0, 1):
        y = np.zeros(n, dtype=np.float32)
        acc = 0.0
        col = ir[:, c]
        for i in range(n):
            acc = a * acc + (1 - a) * col[i]
            y[i] = acc
        ir[:, c] = y
    return ir / np.sqrt((ir ** 2).sum(axis=0, keepdims=True))


def convolve(x, ir):
    n = len(x) + len(ir) - 1
    N = 1 << (n - 1).bit_length()
    out = np.zeros((n, 2), dtype=np.float32)
    for c in (0, 1):
        out[:, c] = np.fft.irfft(np.fft.rfft(x[:, c], N) * np.fft.rfft(ir[:, c], N), N)[:n]
    return out


def place(buf, x, t, gain_db):
    i = int(round(t * SR))
    if i >= len(buf):
        return
    x = x[: len(buf) - i] * (10 ** (gain_db / 20))
    buf[i:i + len(x)] += x


# --- the scores ----------------------------------------------------------------

def tau_table():
    """Film 1's board clock (departures.py speed()): slow motion, then real time."""
    def sm(t):
        return t * t * (3 - 2 * t)

    def speed(f):
        return 0.2 + 0.8 * sm(min(1, max(0, (f - 66) / 70)))
    T = [0.0]
    for f in range(1, 700):
        T.append(T[-1] + 0.5 * (speed(f - 1) + speed(f)) / FPS)
    return T


def at_tau(T, tau):
    for f in range(1, len(T)):
        if T[f] >= tau:
            return (f - 1 + (tau - T[f - 1]) / (T[f] - T[f - 1])) / FPS
    return len(T) / FPS


PENTA = ["G4", "A4", "B4", "D5", "E5", "G5", "A5", "B5", "D6"]


def end_card(ev):
    for i, n in enumerate(["G4", "B4", "D5", "G5"]):
        ev.append((CARD + 0.17 + 0.085 * i, n, -9.0))
    for n, g in (("G2", -6.0), ("D3", -8.0), ("G4", -10.0), ("B4", -12.0)):
        ev.append((CARD + 1.05, n, g))


def score(film):
    ev = []
    f = lambda fr: fr / FPS  # noqa: E731
    if film == "departures":
        T = tau_table()
        hi = ["D6", "B5", "G5", "D5"]
        for i in range(9):                        # the K flipping through the drum, in slow motion
            ev.append((at_tau(T, 0.05 + 0.062 * i), hi[i % 4], -17.0 + i * 0.4))
        ev.append((at_tau(T, 0.05 + 0.062 * 10), "G4", -11.0))
        for r in range(10):                       # each row starting its cascade: a run up the keys
            ev.append((at_tau(T, 1.55 + 0.16 * r), PENTA[min(r, 8)], -14.0))
        ev += [(f(330), "D5", -9.0), (f(336), "G4", -9.5), (f(336) + 0.012, "D5", -9.5)]
        ev += [(f(466), "G4", -9.5), (f(466) + 0.012, "D5", -9.5)]
        bed = dict(lands=f(150), gain=4.5, bar=0)
        wet = 0.3
    elif film == "order":
        mids = ["D4", "B3", "G4", "D4", "B4", "G4"]
        drops = [4, 12, 20, 27, 34, 40, 46, 52, 58, 63, 70, 78]
        for i, d in enumerate(drops):             # the paper landing
            ev.append((f(d + 6), mids[i % len(mids)], -15.0))
        for b0 in (88, 104):                      # the phone buzzing face down
            for k in range(3):
                ev.append((f(b0) + 0.07 * k, "D5", -19.0))
        for k in range(12):                       # squared up, one note each, climbing
            fk = 118 + 9 * k + 15
            ev.append((f(fk), (PENTA + ["B5", "D6", "D6"])[k], -13.0))
        for i, n in enumerate(["D6", "B5", "G5", "D5", "B4", "G4"]):   # swept away
            ev.append((f(236) + 0.07 * i, n, -12.0))
        for k in range(6):                        # the pages, dealt
            ev.append((f(276 + 11 * k + 10), ["G5", "A5", "B5", "D6", "B5", "D6"][k], -12.5))
        ev += [(f(372), "B4", -13.0), (f(410), "G2", -7.0), (f(410), "D3", -9.0)]
        ev += [(f(446), "G4", -9.5), (f(446) + 0.012, "D5", -9.5)]
        bed = dict(lands=f(118), gain=4.5, bar=0)
        wet = 0.28
    elif film == "night":
        ev += [(0.0, "G2", -7.0), (0.02, "D3", -9.0)]
        ev += [(f(26), "B4", -14.0), (f(26) + 0.02, "D5", -14.0), (f(26) + 0.04, "G5", -15.0)]
        ev += [(f(150), "G4", -13.0)]
        ev += [(f(286), "D5", -10.0), (f(300), "G4", -9.5), (f(300) + 0.012, "D5", -9.5), (f(392), "B4", -16.0)]
        for i, n in enumerate(["G4", "B4", "D5", "G5", "B5", "D6"]):   # the clock running to dawn
            ev.append((f(400) + 0.42 * i, n, -15.0))
        ev += [(f(418), "D6", -15.0), (f(452), "D6", -15.0)]
        bed = dict(lands=f(150), gain=4.5, bar=0, quiet_until=f(400), quiet_db=-7.0)
        wet = 0.45
    elif film == "day2":
        ev += [(0.0, "G2", -6.0), (0.02, "D3", -8.0)]
        ev += [(1.5, "D6", -16.0), (4.0, "B5", -16.0), (6.5, "G5", -16.0)]
        for k, n in enumerate(["G4", "B4", "D5", "G5", "B5", "D6", "B5"]):   # seven lights
            ev.append((f(222) + 0.13 * k, n, -14.0))
        ev += [(f(392), "G4", -9.5), (f(392) + 0.012, "D5", -9.5), (f(432), "B4", -14.0)]
        ev += [(f(452), "G4", -9.5), (f(452) + 0.012, "D5", -9.5)]
        bed = dict(lands=f(240), gain=4.5, bar=0)
        wet = 0.38
    end_card(ev)
    return ev, bed, wet


def mix(film):
    n = int(DUR * SR)
    keys = np.zeros((n, 2), dtype=np.float32)
    ev, bed, wet = score(film)
    for t, nm, g in ev:
        place(keys, note(nm), t, g)
    ir = reverb_ir()
    keys = (1 - wet) * keys + wet * 1.6 * convolve(keys, ir)[:n]
    b = load(BED)
    db = DOWNBEAT0 + BAR * bed["bar"]
    lead = min(bed["lands"], BAR)
    start = int(round((db - lead) * SR))
    seg = b[start:start + int((DUR - (bed["lands"] - lead)) * SR) + 1].copy()
    m = len(seg)
    env = np.ones(m, dtype=np.float32)
    fi = int(lead * SR)
    env[:fi] = np.linspace(0, 1, fi) ** 2
    if "quiet_until" in bed:      # under the night, then up with the dawn
        q = 10 ** (bed["quiet_db"] / 20)
        t_rel = np.arange(m) / SR + (bed["lands"] - lead)
        ramp = np.clip((t_rel - bed["quiet_until"]) / 2.5, 0, 1)
        env *= q + (1 - q) * ramp
    fo_from = DUR - 1.6 - (bed["lands"] - lead)
    k0 = int(fo_from * SR)
    if k0 < m:
        env[k0:] *= np.linspace(1, 0, m - k0)
    seg = seg * env[:, None] * (10 ** (bed["gain"] / 20))
    out = keys.copy()
    i0 = int(round((bed["lands"] - lead) * SR))
    out[i0:i0 + len(seg)] += seg[: n - i0]
    os.makedirs(OUT, exist_ok=True)
    raw = os.path.join(OUT, f"{film}_raw.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", raw],
                   input=out.astype(np.float32).tobytes(), check=True)
    p1 = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True).stderr
    js = json.loads(p1[p1.rindex("{"):p1.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    final = os.path.join(OUT, f"{film}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", ln, "-ar", str(SR), final], check=True)
    json.dump({"notes": [{"t": round(t, 3), "note": nm, "gain_db": g} for t, nm, g in sorted(ev)],
               "bed": {"file": os.path.basename(BED), **{k: round(v, 3) if isinstance(v, float) else v for k, v in bed.items()}},
               "reverb_wet": wet, "loudnorm_pass1": js}, open(os.path.join(OUT, f"{film}.json"), "w"), indent=1)
    print(film, "->", final, "input_i", js["input_i"])


if __name__ == "__main__":
    for film in (sys.argv[1:] or ["departures", "order", "night", "day2"]):
        mix(film)
