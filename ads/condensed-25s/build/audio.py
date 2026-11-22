"""The 30 s ad's sound.

  python3 build/audio.py      -> ../out/audio30.wav (30.000 s, -14 LUFS, two-pass)

0-6.4 s  the panic: WhatsApp's own incoming-message tone for every bubble or
         banner that lands (audio/whatsapp_incoming.m4a, copied from the Mac
         WhatsApp app at the founder's choice on 11-10, knowing it is Meta's
         sound), over a low piano pulse that speeds up; then a run down the
         keys as everything is pulled in.
7.0 s    a G major chord and the bossa bed (from 8 s into the track).
         Notes for each line, a run up for each hand-off, the travellers
         lifting off the map, the thread.
26 s     the end card's own piano (marketing/music/endcard_piano.mp4).
Everything except the WhatsApp tone is from marketing/music.
"""
import json
import os
import random
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.dirname(HERE)
MUSIC = os.path.normpath(os.path.join(AD, "../../music"))
PIANO = os.path.join(MUSIC, "piano")
BED = os.path.join(MUSIC, "musicalmix2020-bossa-nova-summer-instrumental-brazil-7969.mp3")
ENDCARD = os.path.join(MUSIC, "endcard_piano.mp4")
OUT = os.path.join(AD, "out")
os.makedirs(OUT, exist_ok=True)
DUR = 30.0
WA = os.path.join(AD, "audio", "whatsapp_incoming.m4a")

random.seed(11)
ev = []  # (time, source, gain dB, semitones, keep seconds)


def note(t, n, db, semi=0, keep=1.4):
    ev.append((t, os.path.join(PIANO, f"{n}.wav"), db, semi, keep))


def ping(t, db, semi=0.0, keep=1.0):
    ev.append((t, WA, db, semi, keep))


# the pulse
t = 0.0
while t < 6.3:
    p = t / 6.3
    note(t, "G2", -22 + 3 * p, keep=0.9)
    note(t + 0.01, "D3", -27 + 3 * p, keep=0.9)
    t += 0.85 - 0.58 * p

# a WhatsApp ping for each card that lands (same times as build.py): the
# first ones whole and clear, then shorter, quieter and slightly detuned as
# they pile up on top of each other
ping(0.05, -7, keep=1.6)
n, pre = 36, 3
for i in range(pre, n):
    tc = 0.35 + 5.85 * ((i - pre) / (n - 1 - pre)) ** 0.7
    k = (i - pre) / (n - 1 - pre)
    semi = 0.0 if i < pre + 7 else random.uniform(-0.35, 0.35)
    ping(tc + 0.02, -8 - 6 * k, semi, keep=1.2 - 0.6 * k)

# pulled in: a run down
for k, nn in enumerate(["D6", "B5", "G5", "D5", "B4", "G4", "D4", "B3"]):
    note(6.36 + k * 0.05, nn, -18, keep=0.6)

# the brand: G major
for nn, db in (("G2", -12), ("G4", -10), ("B4", -12), ("D5", -12)):
    note(7.02, nn, db, keep=3.5)

# labels, hand-offs, the thread
for tl in (9.35, 12.95, 14.65, 18.15, 20.6, 24.5):
    note(tl, "G4", -17, keep=1.2)
    note(tl + 0.01, "D5", -18, keep=1.2)
for tr in (12.0, 17.2):
    note(tr - 0.45, "D5", -17, keep=1.0)   # the chip pops up
    note(tr - 0.44, "G5", -19, keep=1.0)
    for k, nn in enumerate(["G4", "B4", "D5", "G5"]):
        note(tr + k * 0.06, nn, -18, keep=0.8)
for tu, nn in ((20.75, "B4"), (20.92, "D5"), (21.09, "G5")):   # travellers lift off the map
    note(tu, nn, -18, keep=1.0)
for k, nn in enumerate(["B4", "D5", "G5", "B5", "D6"]):          # the thread
    note(24.2 + k * 0.08, nn, -17, keep=1.0)


def build(filters_tail, out, extra=(), level="error"):
    inputs, parts, labels = [], [], []
    for i, (t, src, db, semi, keep) in enumerate(ev):
        inputs += ["-i", src]
        rate = "" if not semi else f"asetrate={int(48000 * 2 ** (semi / 12))},aresample=48000,"
        parts.append(f"[{i}:a]aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo,{rate}atrim=0:{keep},"
                     f"afade=t=out:st={max(0.05, keep - 0.4):.3f}:d=0.4,volume={db}dB,adelay={int(t * 1000)}:all=1[e{i}]")
        labels.append(f"[e{i}]")
    b = len(ev)
    inputs += ["-ss", "8", "-t", "19.6", "-i", BED]
    parts.append(f"[{b}:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.25,"
                 f"afade=t=out:st=18.7:d=0.9,volume=-5dB,adelay=7000:all=1[bed]")
    labels.append("[bed]")
    inputs += ["-i", ENDCARD]
    parts.append(f"[{b + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:4.05,"
                 f"afade=t=out:st=3.35:d=0.7,volume=2dB,adelay=25950:all=1[end]")
    labels.append("[end]")
    graph = ";".join(parts) + ";" + "".join(labels) + \
        f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0,apad=whole_dur={DUR},atrim=0:{DUR}" + filters_tail
    cmd = ["ffmpeg", "-y", "-hide_banner", "-nostats", "-loglevel", level, *inputs, "-filter_complex", graph, *extra, out]
    return subprocess.run(cmd, capture_output=True, text=True)


# pass 1: measure
r = build(",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-", ("-f", "null"), level="info")
if r.returncode:
    raise SystemExit(r.stderr)
j = r.stderr[r.stderr.rindex("{"):]
m = json.loads(j[:j.index("}") + 1])
# pass 2: apply
tail = (",loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:"
        f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
        f"measured_thresh={m['input_thresh']}:offset={m['target_offset']},aresample=48000,atrim=0:{DUR}")
r = build(tail, os.path.join(OUT, "audio30.wav"), ("-c:a", "pcm_s16le"))
if r.returncode:
    raise SystemExit(r.stderr)
print("audio30.wav written; measured", m["input_i"], "LUFS in, events:", len(ev))
