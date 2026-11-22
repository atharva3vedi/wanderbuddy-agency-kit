# Cuts Reel 1 (Walk-in) from the founder's phone takes.
#   python reel1.py --probe     transcribes every take in ../reel1_takes into ../reel1/takes.json (to write edit.json)
#   python reel1.py             cuts ../reel1/edit.json into ../out/WanderBuddy_B2B_Reel1_WalkIn.mp4
#   options: --takes DIR  --edit FILE  --name NAME  --outdir DIR
# edit.json: {"hook": {"text": "...", "to": 2.2}, "free_word": "Free.", "segments": [
#   {"src": "take.mp4", "in": 0.4, "out": 2.6},
#   {"insert": "insert_card.mp4", "from": 0, "audio": {"src": "take6.mp4", "in": 3.1, "out": 5.0}}]}
# An insert runs as long as the founder's line laid under it (or "dur" seconds of silence).
import json, os, sys, subprocess, time, urllib.request, uuid
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
def arg(k, d):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
TAKES = arg('--takes', os.path.join(ROOT, 'reel1_takes'))
EDIT = arg('--edit', os.path.join(ROOT, 'reel1', 'edit.json'))
NAME = arg('--name', 'WanderBuddy_B2B_Reel1_WalkIn')
OUTDIR = arg('--outdir', os.path.join(ROOT, 'out'))
WORK = os.path.join(ROOT, 'reel1', 'work'); os.makedirs(WORK, exist_ok=True)
KEY = next(l.split('=', 1)[1].strip().strip('"') for l in open(r'C:/Users/PC/Videos/WanderBuddy/.env', encoding='utf8') if l.startswith('GROQ_API_KEY='))
VF = 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,format=yuv420p'
AF = 'aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo'

def ff(*a): subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
def has_audio(f): return bool(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip())

def whisper(path):
    """Groq whisper-large-v3 with word timestamps."""
    mp3 = os.path.join(WORK, 'whisper.mp3')
    ff('-i', path, '-vn', '-ac', '1', '-b:a', '64k', mp3)
    bd = uuid.uuid4().hex
    fields = [('model', 'whisper-large-v3'), ('language', 'en'), ('response_format', 'verbose_json'), ('timestamp_granularities[]', 'word'), ('timestamp_granularities[]', 'segment')]
    body = b''.join(f'--{bd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in fields)
    body += f'--{bd}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode() + open(mp3, 'rb').read() + f'\r\n--{bd}--\r\n'.encode()
    for attempt in range(5):
        req = urllib.request.Request('https://api.groq.com/openai/v1/audio/transcriptions', data=body,
                                     headers={'Authorization': 'Bearer ' + KEY, 'Content-Type': f'multipart/form-data; boundary={bd}', 'User-Agent': 'curl/8.9'})
        try: return json.loads(urllib.request.urlopen(req, timeout=180).read())
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(15 * (attempt + 1)); continue
            raise
    sys.exit('whisper: still rate limited')

if '--probe' in sys.argv:
    out = []
    for f in sorted(os.listdir(TAKES)):
        p = os.path.join(TAKES, f)
        if os.path.splitext(f)[1].lower() not in ('.mp4', '.mov', '.m4v', '.3gp', '.mkv', '.webm'): continue
        d = dur(p); w = whisper(p) if has_audio(p) else {'segments': []}
        segs = [{'start': round(s['start'], 2), 'end': round(s['end'], 2), 'text': s['text'].strip()} for s in w.get('segments', [])]
        out.append({'file': f, 'duration': round(d, 2), 'segments': segs})
        print(f'{f}  {d:.1f}s'); [print(f"   {s['start']:6.2f}-{s['end']:6.2f}  {s['text']}") for s in segs]
        time.sleep(3.5)   # Whisper free tier: 20 requests a minute
    json.dump(out, open(os.path.join(ROOT, 'reel1', 'takes.json'), 'w', encoding='utf8'), indent=1, ensure_ascii=False)
    sys.exit(0)

# ---------------- cut ----------------
E = json.load(open(EDIT, encoding='utf8'))
parts = []
for i, s in enumerate(E['segments']):
    o = os.path.join(WORK, f'seg_{i:02d}.mkv')
    if 'insert' in s:
        ins = os.path.join(ROOT, 'reel1', s['insert'])
        if 'audio' in s:
            a = s['audio']; src = os.path.join(TAKES, a['src']); d = a['out'] - a['in']
            ff('-ss', str(s.get('from', 0)), '-i', ins, '-ss', str(a['in']), '-t', str(d), '-i', src,
               '-filter_complex', f"[0:v]{VF},tpad=stop_mode=clone:stop_duration={d}[v];[1:a]{AF}[a]", '-map', '[v]', '-map', '[a]',
               '-t', str(d), '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-c:a', 'pcm_s16le', o)
        else:
            d = s['dur']
            ff('-ss', str(s.get('from', 0)), '-i', ins, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
               '-filter_complex', f"[0:v]{VF},tpad=stop_mode=clone:stop_duration={d}[v]", '-map', '[v]', '-map', '1:a',
               '-t', str(d), '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-c:a', 'pcm_s16le', o)
    else:
        src = os.path.join(TAKES, s['src']); d = s['out'] - s['in']
        enc = ['-t', str(d), '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-c:a', 'pcm_s16le', o]
        if has_audio(src):
            ff('-ss', str(s['in']), '-t', str(d), '-i', src, '-map', '0:v', '-map', '0:a', '-vf', VF, '-af', AF, *enc)
        else:
            ff('-ss', str(s['in']), '-t', str(d), '-i', src, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-map', '0:v', '-map', '1:a', '-vf', VF, *enc)
    parts.append(o); print('segment', i, round(dur(o), 2))
lst = os.path.join(WORK, 'parts.txt')
open(lst, 'w').write(''.join(f"file '{p.replace(os.sep, '/')}'\n" for p in parts))
body = os.path.join(WORK, 'body.mkv')
# light voice cleanup for phone audio: rumble, hiss, a gentle compressor
ff('-f', 'concat', '-safe', '0', '-i', lst, '-c:v', 'copy', '-af', 'highpass=f=80,afftdn=nf=-28,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=160:makeup=2', '-c:a', 'pcm_s16le', body)
D = dur(body)

# ---------------- captions from the founder's own words ----------------
w = whisper(body)
words = [{'w': x['word'].strip(), 'a': x['start'], 'b': x['end']} for x in w.get('words', []) if x['word'].strip()]
text_all = ' '.join(x['w'] for x in words)
for a, b in (('Wander Buddy', 'WanderBuddy'), ('Wonder Buddy', 'WanderBuddy'), ('Wonderbuddy', 'WanderBuddy'), ('Wanderbuddy', 'WanderBuddy')):
    text_all = text_all.replace(a, b)
# re-split the fixed text back onto the word timings (merged names take the first word's start, last word's end)
fixed = []; k = 0
for tok in text_all.split(' '):
    if k >= len(words): break
    n = 2 if tok.startswith('WanderBuddy') and k + 1 < len(words) and words[k]['w'].lower().startswith(('wander', 'wonder')) and not words[k]['w'].lower().startswith(('wanderbuddy', 'wonderbuddy')) else 1
    fixed.append({'w': tok, 'a': words[k]['a'], 'b': words[k + n - 1]['b']}); k += n
# one sentence per caption; a long one splits into even parts, so no word is left on its own (as in reel.html)
CCMAX = 30; sents = []; cur = []
for x in fixed:
    cur.append(x)
    if x['w'][-1:] in '.?!': sents.append(cur); cur = []
if cur: sents.append(cur)
chunks = []
for st in sents:
    ws = [y['w'] for y in st]; n = -(-len(' '.join(ws)) // CCMAX); part = []; start = 0
    for j, x in enumerate(st):
        if part and n > 1 and len(' '.join(ws[start:j + 1])) > len(' '.join(ws[start:])) / n + 4:
            chunks.append(part); part = []; start = j; n -= 1
        part.append(x)
    chunks.append(part)
hook = E.get('hook'); free = E.get('free_word', 'Free.')
items = []; spans = []
if hook:
    items.append({'name': 'hook', 'kind': 'head', 'text': hook['text'], 'size': hook.get('size')}); spans.append(('hook', hook.get('from', 0), hook['to']))
for i, c in enumerate(chunks):
    t = ' '.join(y['w'] for y in c).rstrip(',')
    nxt = chunks[i + 1][0]['a'] - .06 if i + 1 < len(chunks) else D
    a, b = max(0, c[0]['a'] - .06), min(D, c[-1]['b'] + .3, nxt)
    if hook and a < hook['to']: a = hook['to']
    if a >= b: continue
    kind = 'free' if t.strip().lower() == free.lower() else 'cc'
    if kind == 'free': b = min(D, b + .6)
    items.append({'name': f'c{i:02d}', 'kind': kind, 'text': t}); spans.append((f'c{i:02d}', a, b))
for s in spans: print(f'  {s[1]:6.2f}-{s[2]:6.2f}  ' + next(it['text'] for it in items if it['name'] == s[0]))
ov = os.path.join(WORK, 'overlays'); json.dump(items, open(os.path.join(WORK, 'overlays.json'), 'w', encoding='utf8'), ensure_ascii=False)
subprocess.run(['node', os.path.join(HERE, 'overlay.mjs'), os.path.join(WORK, 'overlays.json'), ov], check=True)
inputs = sum((['-i', os.path.join(ov, n + '.png')] for n, _, _ in spans), [])
chain = []; last = '0:v'
for j, (n, a, b) in enumerate(spans):
    chain.append(f"[{last}][{j + 1}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[o{j}]"); last = f'o{j}'
captioned = os.path.join(WORK, 'captioned.mkv')
ff('-i', body, *inputs, '-filter_complex', ';'.join(chain), '-map', f'[{last}]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-c:a', 'copy', captioned)

# ---------------- end card + loudness (same as build.sh) ----------------
joined = os.path.join(WORK, 'joined.mkv')
ff('-i', captioned, '-i', os.path.join(ROOT, 'endcard', 'endcard_piano.mp4'), '-filter_complex',
   f"[0:v]fps=30,format=yuv420p,setsar=1[v0];[0:a]{AF}[a0];[1:v]fps=30,format=yuv420p,setsar=1[v1];[1:a]{AF}[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
   '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-c:a', 'pcm_s16le', joined)
m = subprocess.run(['ffmpeg', '-hide_banner', '-i', joined, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex('{'):m.rindex('}') + 1])
out = os.path.join(OUTDIR, NAME + '.mp4')
ff('-i', joined, '-map', '0:v', '-map', '0:a', '-c:v', 'copy', '-af',
   f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000",
   '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', out)
print('wrote', out, round(dur(out), 2), 's')
