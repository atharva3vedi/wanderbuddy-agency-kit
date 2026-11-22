# Lays a reel's narration on its timeline, trims silences, writes audio/<reel>_vo.wav + <reel>_tl.js.
#   python timeline.py r2
import json, os, sys, numpy as np, soundfile as sf
from scipy.signal import resample_poly
sys.stdout.reconfigure(encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__))
reel = sys.argv[1]
spec = json.load(open(os.path.join(here, 'vo', reel, 'lines.json'), encoding='utf8'))
SR = 48000

def load(i):
    x, sr = sf.read(os.path.join(here, 'vo', reel, spec.get('folder', spec.get('voice', 'troy')), f'l{i:02d}.wav'), dtype='float32')
    if x.ndim == 2: x = x.mean(1)
    if sr != SR: x = resample_poly(x, SR, sr).astype('float32')
    env = np.convolve(np.abs(x), np.ones(480) / 480, 'same')
    on = np.where(env > max(env.max() * .05, 1e-3))[0]
    a, b = max(0, on[0] - 960), min(len(x), on[-1] + 2400)
    y = x[a:b].copy()
    cap = spec.get('max_pause')   # optional: shorten long pauses inside a line (a skit needs talking speed)
    if cap:
        on = np.convolve(np.abs(y), np.ones(480) / 480, 'same') > env.max() * .05
        keep = np.ones(len(y), bool); k = 0; lim = int(cap * SR)
        while k < len(y):
            if not on[k]:
                j = k
                while j < len(y) and not on[j]: j += 1
                if j - k > lim: keep[k + lim // 2: j - lim // 2] = False
                k = j
            else: k += 1
        y = y[keep]
    v = y[np.convolve(np.abs(y), np.ones(480) / 480, 'same') > env.max() * .05]
    y *= .1 / (np.sqrt(np.mean(v ** 2)) + 1e-9)
    y[:480] *= np.linspace(0, 1, 480); y[-1200:] *= np.linspace(1, 0, 1200)
    return y

t = spec['lead']; cues = []; clips = []
for i, ln in enumerate(spec['lines']):
    y = load(i); d = len(y) / SR
    t += ln['gap']
    cues.append({'i': i, 'start': round(t, 3), 'end': round(t + d, 3), 'text': ln['text'], **{k: ln[k] for k in ('beat', 'who') if k in ln}})
    clips.append((t, y)); t += d
dur = round(t + spec['tail'], 2)
out = np.zeros(int(dur * SR) + SR, dtype='float32')
for s, y in clips:
    k = int(s * SR); out[k:k + len(y)] += y
sf.write(os.path.join(here, 'audio', f'{reel}_vo.wav'), out[:int(dur * SR)], SR)
tl = {'duration': dur, 'cues': cues}
open(os.path.join(here, f'{reel}_tl.js'), 'w', encoding='utf8').write('window.TL=' + json.dumps(tl, ensure_ascii=False) + ';')
for c in cues: print(f"{c['i']:2d} {c['start']:6.2f}-{c['end']:6.2f}  {c['text']}")
print('duration', dur)
