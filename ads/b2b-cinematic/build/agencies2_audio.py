"""Three Agencies, second cut: an original score, written and generated here.

The founder's call on 2026-11-11: "you can generate your own music". So this one
is not the bossa bed: strings, a pulse, rain and two low hits are synthesized in
this file with numpy; the piano is still the real Iowa Steinway notes.

  /Applications/Blender.app/Contents/Resources/5.3/python/bin/python3.13 build/agencies2_audio.py

E minor while nobody answers (a low string pad, a soft pulse like a clock, rain on
the street), C major 7 when the listing appears, a held D under the dark office,
G major when the hold lands, back to a thin E minor next door, then C, D, G as
the shutters go up. Output: out/audio/agencies2.wav (32.3 s, 48 kHz stereo,
-14 LUFS) and agencies2.json (every event, and each stem's level).
"""
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio import OUT, SR, convolve, note, place, reverb_ir  # noqa: E402

FPS = 24
CARD = 28.8
DUR = CARD + 84 / FPS
TB, TC, TD, TE, TF = 84 / FPS, 192 / FPS, 348 / FPS, 468 / FPS, 564 / FPS
N = int(DUR * SR)
T = np.arange(N) / SR
rng = np.random.default_rng(7)
db = lambda g: 10 ** (g / 20)  # noqa: E731


def ramp(t0, t1, attack, release):
    e = np.clip((T - t0) / max(attack, 1e-3), 0, 1) * np.clip((t1 - T) / max(release, 1e-3), 0, 1)
    return (e * e * (3 - 2 * e)).astype(np.float32)


def pad(freqs, t0, t1, gain_db, attack=1.2, release=1.2, bright=1.0):
    """A string section: three slightly detuned voices a note, a slow vibrato, soft upper partials."""
    i0, i1 = max(0, int((t0 - 0.05) * SR)), min(N, int((t1 + 0.05) * SR))
    tt = T[i0:i1]
    out = np.zeros((i1 - i0, 2), dtype=np.float64)
    for i, f0 in enumerate(freqs):
        for cents, pan in ((-6, -0.55), (0, 0.0), (6, 0.55)):
            f = f0 * 2 ** (cents / 1200)
            vib = 1 + 0.0028 * np.sin(2 * np.pi * (4.4 + 0.35 * i + 0.2 * pan) * tt + rng.uniform(0, 6.28))
            ph = 2 * np.pi * np.cumsum(f * vib) / SR
            sig = np.zeros_like(tt)
            for h in range(1, 9):
                if f * h > 4200:
                    break
                sig += np.sin(h * ph + rng.uniform(0, 6.28)) / h ** (2.1 / bright)
            out[:, 0] += sig * (1 - pan) / 2
            out[:, 1] += sig * (1 + pan) / 2
    out /= max(1, len(freqs)) * 1.5
    breathe = 0.86 + 0.14 * np.sin(2 * np.pi * 0.11 * tt + 1.0)
    full = np.zeros((N, 2), dtype=np.float32)
    full[i0:i1] = (out * breathe[:, None]).astype(np.float32)
    return full * ramp(t0, t1, attack, release)[:, None] * db(gain_db)


def band_noise(lo, hi, tilt=-3.0, seed=1):
    """Stereo noise between lo and hi Hz, falling tilt dB an octave: rain."""
    r = np.random.default_rng(seed)
    out = np.zeros((N, 2), dtype=np.float32)
    fr = np.fft.rfftfreq(N, 1 / SR)
    g = np.zeros_like(fr)
    m = (fr > lo) & (fr < hi)
    g[m] = (fr[m] / 1000.0) ** (tilt / 6.02)
    g *= np.clip((fr - lo) / (lo * 0.5), 0, 1) * np.clip((hi - fr) / (hi * 0.25), 0, 1)
    for c in (0, 1):
        x = np.fft.irfft(np.fft.rfft(r.standard_normal(N)) * g, N)
        out[:, c] = x / (np.sqrt(np.mean(x ** 2)) + 1e-9)
    slow = np.fft.irfft(np.fft.rfft(r.standard_normal(N)) * (fr < 0.35), N)
    slow = 0.88 + 0.12 * slow / (np.abs(slow).max() + 1e-9)
    return out * slow[:, None].astype(np.float32)


def add(buf, sig, t0):
    i = int(round(t0 * SR))
    if i >= N:
        return
    sig = sig[: N - i]
    buf[i:i + len(sig)] += sig


def pluck(freq, gain_db, pan=0.0):
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.085) + 0.35 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t / 0.04)
    click = rng.standard_normal(n) * np.exp(-t / 0.0025) * 0.22
    s = (s + click) * np.clip(t / 0.002, 0, 1) * db(gain_db)
    return np.stack([s * (1 - pan) / 2 * 2 ** 0.5, s * (1 + pan) / 2 * 2 ** 0.5], axis=1).astype(np.float32)


def thump(f0, f1, decay, gain_db):
    n = int((decay * 4) * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / (decay * 0.35))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay) * np.clip(t / 0.004, 0, 1) * db(gain_db)
    return np.stack([s, s], axis=1).astype(np.float32)


def buzz(gain_db):
    """A phone vibrating on a desk behind a shutter: two short bursts."""
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    car = 0.6 * np.sin(2 * np.pi * 165 * t) + 0.25 * np.sin(2 * np.pi * 330 * t) + 0.1 * np.sin(2 * np.pi * 495 * t)
    am = 0.6 + 0.4 * np.sin(2 * np.pi * 27 * t)
    gate = (np.clip(t / 0.02, 0, 1) * np.clip((0.32 - t) / 0.03, 0, 1)) + (np.clip((t - 0.5) / 0.02, 0, 1) * np.clip((0.82 - t) / 0.03, 0, 1))
    s = car * am * gate * db(gain_db)
    return np.stack([s, s], axis=1).astype(np.float32)


def rms_db(x):
    return round(float(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)), 1)


def main():
    f = lambda fr: fr / FPS  # noqa: E731
    E2, G2, B2, C3, D3, E3, G3, A3, B3, C4, D4, E4, FS4, G4 = 82.41, 98.0, 123.47, 130.81, 146.83, 164.81, 196.0, 220.0, 246.94, 261.63, 293.66, 329.63, 369.99, 392.0
    D2, A2 = 73.42, 110.0
    chords = [
        ("Em", [E2, B2, E3, G3], 0.0, 8.6, -21, 2.5, 1.2),
        ("Cmaj7", [C3, G3, B3, E4], 7.6, 15.0, -21, 1.2, 1.0),
        ("D5", [D2, A2, D3, A3], 14.2, 18.4, -23, 0.8, 0.6),
        ("G", [G2, D3, G3, B3, D4], 17.9, 20.1, -18, 0.35, 1.5),
        ("Em thin", [E2, B2], 19.4, 23.8, -24, 0.8, 0.9),
        ("C", [C3, G3, C4, E4], 23.3, 25.7, -20, 0.8, 0.9),
        ("D", [D3, A3, D4, FS4], 25.0, 27.4, -20, 0.8, 0.9),
        ("G", [G2, D3, G3, B3, D4, G4], 26.8, DUR - 0.2, -18, 0.9, 2.6),
    ]
    strings = np.zeros((N, 2), dtype=np.float32)
    for _, fr, t0, t1, g, a, r in chords:
        strings += pad(fr, t0, t1, g, a, r)
    # rain: open on the street, muffled indoors, gone by morning
    street = band_noise(350, 8000, -3.0, seed=3) * db(-31)
    indoors = band_noise(120, 1100, -4.5, seed=4) * db(-33)
    rain = street * ramp(-1, TC + 0.2, 0.01, 0.5)[:, None] + indoors * ramp(TC - 0.3, TE + 0.3, 0.5, 0.7)[:, None]
    rain *= ramp(-1, DUR, 0.01, 0.01)[:, None]
    rain[: int(1.2 * SR)] *= np.linspace(0, 1, int(1.2 * SR))[:, None] ** 2
    # the pulse: a clock nobody is watching, until the hold lands
    pulse = np.zeros((N, 2), dtype=np.float32)
    k, t = 0, 0.5
    while t < f(434) - 0.2:
        g = np.interp(t, [0.5, TC, TC + 0.5, TD, f(434)], [-29, -22, -26, -24, -20])
        pulse_note = [E3, E3, B2, E3][k % 4]
        add(pulse, pluck(pulse_note, g, pan=(-0.25 if k % 2 else 0.25)), t)
        t += 0.5
        k += 1
    hits = np.zeros((N, 2), dtype=np.float32)
    for t0 in (2.0, 4.0, 6.0):
        add(hits, thump(58, 44, 0.22, -21), t0)
    add(hits, thump(72, 42, 1.3, -13), f(434))            # the hold lands
    add(hits, thump(52, 36, 0.9, -15), f(518))            # too late
    add(hits, buzz(-27), f(92))
    add(hits, buzz(-27), f(134))
    # the piano: real notes, a room around them
    ev = [(0.02, "E3", -10.0), (0.04, "B3", -13.0), (f(92), "B3", -16.0), (f(134), "B3", -16.0),
          (TC, "G4", -13.0), (TC + 0.02, "E4", -15.0), (f(252), "A4", -15.0),
          (f(298), "G4", -10.0), (f(298) + 0.012, "D5", -10.0), (f(324), "D5", -11.0), (f(324) + 0.08, "G5", -11.0),
          (f(354), "B4", -16.0), (f(354) + 0.07, "D5", -16.0), (f(354) + 0.14, "G5", -16.0),
          (f(434), "G2", -8.0), (f(434), "G4", -9.0), (f(434) + 0.012, "B4", -10.0), (f(434) + 0.024, "D5", -9.0),
          (TE, "E3", -11.0), (f(518), "E3", -8.0), (f(518) + 0.02, "B3", -12.0)]
    for i, nm in enumerate(["G4", "B4", "D5"]):
        ev.append((f(582) + 0.13 * i, nm, -13.0))
    for i, nm in enumerate(["B4", "D5", "G5"]):
        ev.append((f(604) + 0.13 * i, nm, -13.0))
    ev += [(f(628), "G4", -10.0), (f(628) + 0.012, "D5", -10.0)]
    for i, nm in enumerate(["G4", "B4", "D5", "G5"]):
        ev.append((CARD + 0.17 + 0.085 * i, nm, -9.0))
    for nm, g in (("G2", -6.0), ("D3", -8.0), ("G4", -10.0), ("B4", -12.0)):
        ev.append((CARD + 1.05, nm, g))
    keys = np.zeros((N, 2), dtype=np.float32)
    for t0, nm, g in ev:
        place(keys, note(nm), t0, g)
    ir = reverb_ir()
    wet = 0.42
    keys = (1 - wet) * keys + wet * 1.6 * convolve(keys, ir)[:N]
    strings = 0.72 * strings + 0.28 * 1.6 * convolve(strings, ir)[:N]
    strings *= db(7.0)                                        # balance: the piano sits on the strings, not over them
    pulse *= db(9.0)
    rain *= db(2.0)
    out = strings + rain + pulse + hits + keys
    out *= ramp(-1, DUR, 0.01, 0.35)[:, None]
    out = np.tanh(out * 1.4) / 1.4                              # a soft ceiling before loudnorm
    os.makedirs(OUT, exist_ok=True)
    raw = os.path.join(OUT, "agencies2_raw.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", raw],
                   input=out.astype(np.float32).tobytes(), check=True)
    p1 = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True).stderr
    js = json.loads(p1[p1.rindex("{"):p1.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    final = os.path.join(OUT, "agencies2.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", ln, "-ar", str(SR), final], check=True)
    stems = {"strings": rms_db(strings), "rain": rms_db(rain), "pulse": rms_db(pulse), "hits": rms_db(hits), "piano": rms_db(keys)}
    json.dump({"made": "generated in build/agencies2_audio.py; piano notes are the Iowa Steinway samples",
               "chords": [{"name": c[0], "from": c[2], "to": round(c[3], 2), "gain_db": c[4]} for c in chords],
               "piano": [{"t": round(t0, 3), "note": nm, "gain_db": g} for t0, nm, g in sorted(ev)],
               "stems_rms_db": stems, "peak": round(float(np.abs(out).max()), 3), "loudnorm_pass1": js},
              open(os.path.join(OUT, "agencies2.json"), "w"), indent=1)
    print("agencies2 ->", final, "stems", stems, "peak", round(float(np.abs(out).max()), 3), "input_i", js["input_i"])


if __name__ == "__main__":
    main()
