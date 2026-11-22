"""Pieces for the generated scores of the second-pass films (numpy only).

The founder's call on 2026-11-11: the films may carry music generated here.
Everything in this file is synthesized except the piano, which is the real Iowa
Steinway notes through audio.py. Run with Blender's Python (it has numpy).

  s = Score(seconds)          a stereo buffer per stem, mixed and normalised by s.write(name)
"""
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio import OUT, SR, convolve, note, place, reverb_ir  # noqa: E402

HZ = {"C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13, "E": 329.63, "F": 349.23, "F#": 369.99,
      "G": 392.0, "G#": 415.3, "A": 440.0, "A#": 466.16, "B": 493.88}


def hz(name):
    """'E2', 'F#4' -> Hz."""
    return HZ[name[:-1]] * 2 ** (int(name[-1]) - 4)


def db(g):
    return 10 ** (g / 20)


class Score:
    def __init__(self, seconds, seed=7):
        self.dur = seconds
        self.n = int(seconds * SR)
        self.t = np.arange(self.n) / SR
        self.rng = np.random.default_rng(seed)
        self.stems = {}
        self.log = []

    def stem(self, name):
        if name not in self.stems:
            self.stems[name] = np.zeros((self.n, 2), dtype=np.float32)
        return self.stems[name]

    def ramp(self, t0, t1, attack, release):
        e = np.clip((self.t - t0) / max(attack, 1e-3), 0, 1) * np.clip((t1 - self.t) / max(release, 1e-3), 0, 1)
        return (e * e * (3 - 2 * e)).astype(np.float32)

    def add(self, stem, sig, t0):
        buf = self.stem(stem)
        i = int(round(t0 * SR))
        if i >= self.n or i < 0:
            return
        sig = sig[: self.n - i]
        buf[i:i + len(sig)] += sig

    # --- sustained -------------------------------------------------------------
    def pad(self, stem, notes, t0, t1, gain_db, attack=1.2, release=1.2, bright=1.0):
        """Strings: three slightly detuned voices a note, slow vibrato, soft upper partials."""
        i0, i1 = max(0, int((t0 - 0.05) * SR)), min(self.n, int((t1 + 0.05) * SR))
        tt = self.t[i0:i1]
        out = np.zeros((i1 - i0, 2), dtype=np.float64)
        for i, nm in enumerate(notes):
            f0 = hz(nm) if isinstance(nm, str) else nm
            for cents, pan in ((-6, -0.55), (0, 0.0), (6, 0.55)):
                f = f0 * 2 ** (cents / 1200)
                vib = 1 + 0.0028 * np.sin(2 * np.pi * (4.4 + 0.35 * i + 0.2 * pan) * tt + self.rng.uniform(0, 6.28))
                ph = 2 * np.pi * np.cumsum(f * vib) / SR
                sig = np.zeros_like(tt)
                for h in range(1, 9):
                    if f * h > 4200:
                        break
                    sig += np.sin(h * ph + self.rng.uniform(0, 6.28)) / h ** (2.1 / bright)
                out[:, 0] += sig * (1 - pan) / 2
                out[:, 1] += sig * (1 + pan) / 2
        out /= max(1, len(notes)) * 1.5
        breathe = 0.86 + 0.14 * np.sin(2 * np.pi * 0.11 * tt + 1.0)
        env = self.ramp(t0, t1, attack, release)[i0:i1]
        self.stem(stem)[i0:i1] += (out * (breathe * env)[:, None] * db(gain_db)).astype(np.float32)
        self.log.append({"pad": notes, "from": round(t0, 2), "to": round(t1, 2), "gain_db": gain_db})

    def noise(self, stem, lo, hi, t0, t1, gain_db, tilt=-3.0, attack=0.5, release=0.5, seed=1):
        """Stereo noise between lo and hi Hz: rain, air, paper."""
        r = np.random.default_rng(seed)
        fr = np.fft.rfftfreq(self.n, 1 / SR)
        g = np.zeros_like(fr)
        m = (fr > lo) & (fr < hi)
        g[m] = (fr[m] / 1000.0) ** (tilt / 6.02)
        g *= np.clip((fr - lo) / (lo * 0.5), 0, 1) * np.clip((hi - fr) / (hi * 0.25), 0, 1)
        slow = np.fft.irfft(np.fft.rfft(r.standard_normal(self.n)) * (fr < 0.35), self.n)
        slow = 0.88 + 0.12 * slow / (np.abs(slow).max() + 1e-9)
        env = self.ramp(t0, t1, attack, release) * slow.astype(np.float32) * db(gain_db)
        buf = self.stem(stem)
        for c in (0, 1):
            x = np.fft.irfft(np.fft.rfft(r.standard_normal(self.n)) * g, self.n)
            buf[:, c] += (x / (np.sqrt(np.mean(x ** 2)) + 1e-9)).astype(np.float32) * env

    def hum(self, stem, t0, t1, gain_db, stop_from=None, blades=6.15):
        """A ceiling fan: a low hum and air, beating at the blade rate; it can wind down."""
        tt = self.t
        speed = np.ones(self.n)
        if stop_from is not None:
            speed = 1 - np.clip((tt - stop_from) / max(t1 - stop_from, 1e-3), 0, 1) ** 1.5
        ph = 2 * np.pi * np.cumsum(48 * (0.6 + 0.4 * speed)) / SR
        beat = 0.7 + 0.3 * np.sin(2 * np.pi * np.cumsum(blades * speed) / SR)
        r = np.random.default_rng(11)
        fr = np.fft.rfftfreq(self.n, 1 / SR)
        air = np.fft.irfft(np.fft.rfft(r.standard_normal(self.n)) * ((fr > 180) & (fr < 900)), self.n)
        air /= np.sqrt(np.mean(air ** 2)) + 1e-9
        sig = (0.7 * np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.5 * air) * beat * np.sqrt(speed)
        sig = (sig * self.ramp(t0, t1, 0.4, 0.05) * db(gain_db)).astype(np.float32)
        self.stem(stem)[:] += np.stack([sig, sig], axis=1)

    # --- struck ----------------------------------------------------------------
    def pluck(self, stem, t0, freq, gain_db, pan=0.0, decay=0.085, click=0.22):
        n = int(0.5 * SR)
        t = np.arange(n) / SR
        s = np.sin(2 * np.pi * freq * t) * np.exp(-t / decay) + 0.35 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t / (decay * 0.5))
        s = (s + self.rng.standard_normal(n) * np.exp(-t / 0.0025) * click) * np.clip(t / 0.002, 0, 1) * db(gain_db)
        self.add(stem, np.stack([s * (1 - pan), s * (1 + pan)], axis=1).astype(np.float32) * 0.7071, t0)

    def string(self, stem, t0, freq, gain_db, pan=0.0, seconds=3.0, damp=0.9965, bright=0.5):
        """A plucked string (Karplus-Strong): a harp or zither note."""
        L = max(2, int(round(SR / freq)))
        periods = int(seconds * SR / L)
        cur = self.rng.uniform(-1, 1, L)
        for _ in range(int(4 * (1 - bright)) + 1):          # soften the pluck
            cur = 0.5 * (cur + np.roll(cur, 1))
        out = np.empty(periods * L)
        for k in range(periods):
            out[k * L:(k + 1) * L] = cur
            cur = damp * 0.5 * (cur + np.roll(cur, 1))
        out *= np.clip(np.arange(len(out)) / (0.003 * SR), 0, 1)
        out *= db(gain_db) / (np.abs(out).max() + 1e-9)
        self.add(stem, np.stack([out * (1 - pan), out * (1 + pan)], axis=1).astype(np.float32) * 0.7071, t0)
        self.log.append({"string": round(freq, 1), "t": round(t0, 3), "gain_db": gain_db})

    def thump(self, stem, t0, f0, f1, decay, gain_db):
        n = int(decay * 4 * SR)
        t = np.arange(n) / SR
        f = f1 + (f0 - f1) * np.exp(-t / (decay * 0.35))
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay) * np.clip(t / 0.004, 0, 1) * db(gain_db)
        self.add(stem, np.stack([s, s], axis=1).astype(np.float32), t0)

    def dum(self, stem, t0, gain_db, pan=0.0):
        """The low stroke of a hand drum."""
        n = int(0.5 * SR)
        t = np.arange(n) / SR
        f = 72 + 46 * np.exp(-t / 0.03)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.15) + 0.25 * self.rng.standard_normal(n) * np.exp(-t / 0.006)
        s *= np.clip(t / 0.0015, 0, 1) * db(gain_db)
        self.add(stem, np.stack([s * (1 - pan), s * (1 + pan)], axis=1).astype(np.float32) * 0.7071, t0)

    def tak(self, stem, t0, gain_db, pan=0.0, tone=430.0):
        """The high, dry stroke."""
        n = int(0.2 * SR)
        t = np.arange(n) / SR
        nz = self.rng.standard_normal(n)
        nz = nz - np.concatenate([[0], nz[:-1]]) * 0.92          # tilt it up
        s = 0.55 * nz * np.exp(-t / 0.018) + np.sin(2 * np.pi * tone * t) * np.exp(-t / 0.045)
        s *= np.clip(t / 0.001, 0, 1) * db(gain_db) * 0.6
        self.add(stem, np.stack([s * (1 - pan), s * (1 + pan)], axis=1).astype(np.float32) * 0.7071, t0)

    def buzz(self, stem, t0, gain_db):
        """A phone vibrating on a desk: two short bursts."""
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        car = 0.6 * np.sin(2 * np.pi * 165 * t) + 0.25 * np.sin(2 * np.pi * 330 * t) + 0.1 * np.sin(2 * np.pi * 495 * t)
        gate = (np.clip(t / 0.02, 0, 1) * np.clip((0.32 - t) / 0.03, 0, 1)) + (np.clip((t - 0.5) / 0.02, 0, 1) * np.clip((0.82 - t) / 0.03, 0, 1))
        s = car * (0.6 + 0.4 * np.sin(2 * np.pi * 27 * t)) * gate * db(gain_db)
        self.add(stem, np.stack([s, s], axis=1).astype(np.float32), t0)

    def piano(self, events, wet=0.42):
        """events: (t, 'G4', gain_db). The real notes, with a room."""
        keys = np.zeros((self.n, 2), dtype=np.float32)
        for t0, nm, g in events:
            place(keys, note(nm), t0, g)
        self.stem("piano")[:] += (1 - wet) * keys + wet * 1.6 * convolve(keys, reverb_ir())[: self.n]
        self.log.append({"piano": [{"t": round(t0, 3), "note": nm, "gain_db": g} for t0, nm, g in sorted(events)]})

    def room(self, stem, wet=0.28):
        x = self.stem(stem)
        x[:] = (1 - wet) * x + wet * 1.6 * convolve(x, reverb_ir())[: self.n]

    def end_card(self, card):
        """The same four notes and G chord every film ends on."""
        ev = [(card + 0.17 + 0.085 * i, nm, -9.0) for i, nm in enumerate(["G4", "B4", "D5", "G5"])]
        ev += [(card + 1.05, nm, g) for nm, g in (("G2", -6.0), ("D3", -8.0), ("G4", -10.0), ("B4", -12.0))]
        return ev

    # --- out ---------------------------------------------------------------------
    def write(self, name, gains=None, note_="generated in build; the piano is the Iowa Steinway samples"):
        gains = gains or {}
        out = np.zeros((self.n, 2), dtype=np.float32)
        levels = {}
        for k, x in self.stems.items():
            x = x * db(gains.get(k, 0.0))
            levels[k] = round(float(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)), 1)
            out += x
        out *= self.ramp(-1, self.dur, 0.01, 0.35)[:, None]
        out = np.tanh(out * 1.4) / 1.4
        os.makedirs(OUT, exist_ok=True)
        raw = os.path.join(OUT, f"{name}_raw.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", raw],
                       input=out.astype(np.float32).tobytes(), check=True)
        p1 = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json",
                             "-f", "null", "-"], capture_output=True, text=True).stderr
        js = json.loads(p1[p1.rindex("{"):p1.rindex("}") + 1])
        ln = (f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
              f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
        final = os.path.join(OUT, f"{name}.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", ln, "-ar", str(SR), final], check=True)
        json.dump({"made": note_, "stems_rms_db": levels, "peak": round(float(np.abs(out).max()), 3), "events": self.log, "loudnorm_pass1": js},
                  open(os.path.join(OUT, f"{name}.json"), "w"), indent=1)
        print(name, "->", final, "stems", levels, "peak", round(float(np.abs(out).max()), 3), "input_i", js["input_i"])
