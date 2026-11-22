# Soundtrack for "How we got to revenue", from real recordings (same recipe as the B2B reels):
#   music  "Bossa Nova - Summer - Instrumental Brazil" by Musicalmix2020 (Pixabay Content License)
#   piano  single Steinway notes, University of Iowa Musical Instrument Samples (free for any use)
#   voice  audio/s1_vo.wav (vo.py + timeline.py), Troy on Groq Orpheus
# Piano notes land on the page's cues (audio/s1_sfx.json from render.mjs), in G major pentatonic.
#   python audio.py   -> audio/s1_mix.wav
import json, os
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, '..', 'assets'))
SR = 48000
cues = json.load(open(os.path.join(HERE, 'audio', 's1_sfx.json')))
TOTAL = cues['duration']; N = int(TOTAL * SR)

def bus(): return np.zeros((N, 2))
def add(b, t, y, gain=1.0):
    k = int(t * SR)
    if k >= N or k < 0: return
    y = y[:N - k]; b[k:k + len(y)] += y * gain
def filt(x, kind, f, order=2): return sosfilt(butter(order, f, btype=kind, fs=SR, output='sos'), x, axis=0)
def fades(y, a=.005, b=.3):
    y = y.copy(); na, nb = int(a * SR), min(int(b * SR), len(y))
    y[:na] *= np.linspace(0, 1, na)[:, None]; y[-nb:] *= np.linspace(1, 0, nb)[:, None]; return y
def rms_db(x):
    a = x[np.abs(x) > 1e-3]; return 20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-12) if len(a) else -120
def to_db(x, target): return x * 10 ** ((target - rms_db(x.mean(1))) / 20)

# ---------------- piano: recorded notes, E and A made from D and G a whole tone up ----------------
NOTES = {}
for f in os.listdir(os.path.join(ASSETS, 'piano', 'wav')):
    NOTES[f[:-4]] = sf.read(os.path.join(ASSETS, 'piano', 'wav', f), dtype='float64')[0]
for src, dst in (('D4', 'E4'), ('D5', 'E5'), ('G4', 'A4'), ('G5', 'A5'), ('D6', 'E6')):
    NOTES[dst] = resample_poly(NOTES[src], 89, 100, axis=0)          # x1.124 = +2 semitones
def key(n, d=1.2, vel=1.0, bright=True):
    y = fades(NOTES[n][:int(d * SR)], .002, min(.6, d * .6)) * vel
    return y if bright else filt(y, 'low', 2600)
RUN = ['D4', 'E4', 'G4', 'A4', 'B4', 'D5', 'E5', 'G5', 'A5', 'B5', 'D6']
fx = bus(); k_pop = 0; k_tick = 0
for c in cues['sfx']:
    t, kind, g = c['t'], c['kind'], c['gain']
    if kind == 'whoosh':                     # pixels / weeks filling: a run up the keys
        for i, n in enumerate(RUN): add(fx, t + i * .06, key(n, .9, .3 + .35 * i / len(RUN)), g)
    elif kind == 'tick':
        n = ['G5', 'A5', 'B5', 'D6', 'E6', 'D6', 'B5'][k_tick % 7]; k_tick += 1
        add(fx, t, key(n, 1.0, .55), g)
    elif kind == 'glow':
        for i, n in enumerate(['D5', 'G5', 'B5', 'D6']): add(fx, t + i * .09, key(n, 1.6, .5), g)
    elif kind == 'lift':
        add(fx, t, key('G4', 1.2, .6), g); add(fx, t + .14, key('D5', 1.4, .6), g)
    elif kind == 'swish':
        add(fx, t, key('B4', .8, .35, False), g); add(fx, t, key('D5', .8, .3, False), g)
    elif kind == 'pop':
        n = ['D5', 'E5', 'G5', 'A5', 'B5', 'G5'][k_pop % 6]; k_pop += 1
        add(fx, t, key(n, .7, .5, False), g)
    elif kind == 'msg':
        add(fx, t, key('B5', .8, .45), g); add(fx, t + .08, key('E6', .9, .4), g)
    elif kind == 'thud':                     # the hard truth: a low, full chord
        for n, v in (('G2', 1.0), ('D3', .8), ('B3', .7), ('D4', .6), ('G4', .5)): add(fx, t, key(n, 2.4, v), g)
    elif kind == 'slide':
        for i, n in enumerate(['D6', 'B5', 'A5', 'G5', 'E5', 'D5']): add(fx, t + i * .04, key(n, .7, .4), g)

# ---------------- music: the track from its own start; it dips under the B&W beat, then comes back ----------------
song, ssr = sf.read(os.path.join(ASSETS, 'music', 'bossa48k.wav'), dtype='float64')
music = np.zeros((N, 2)); music[:min(N, len(song))] = song[:N]
music = fades(music, .02, 2.2)
tt = np.arange(N) / SR
dip = 1 - .55 * np.clip((tt - 30.0) / .4, 0, 1) * np.clip((34.7 - tt) / .5, 0, 1)    # "a hard business to make work"
music *= dip[:, None]

# ---------------- voice + mix ----------------
vo, vsr = sf.read(os.path.join(HERE, 'audio', 's1_vo.wav'), dtype='float64')
if vo.ndim == 1: vo = np.stack([vo, vo], 1)
vo = resample_poly(vo, SR, vsr, axis=0) if vsr != SR else vo
vbus = bus(); add(vbus, 0, filt(to_db(vo, -17), 'high', 70))
ve = np.convolve(np.abs(vbus[:, 0]), np.ones(2400) / 2400, 'same')
duck = 1 - .45 * np.clip(ve / .02, 0, 1); duck = np.convolve(duck, np.ones(9600) / 9600, 'same')
music = to_db(music, -26.5) * duck[:, None]
fx = to_db(fx, -31)
print('stems dB  vo', round(rms_db(vbus[:, 0]), 1), ' music', round(rms_db(music[:, 0]), 1), ' piano', round(rms_db(fx[:, 0]), 1))
mix = vbus + music + fx
mix = np.tanh(mix * 1.4) / 1.4
sf.write(os.path.join(HERE, 'audio', 's1_mix.wav'), mix.astype(np.float32), SR)
print('mix', round(len(mix) / SR, 2), 's')
