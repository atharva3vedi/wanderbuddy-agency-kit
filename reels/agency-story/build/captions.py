# Word times for the captions: the script's own words (lines.json), timed from Whisper (audio/<reel>_words.json).
#   python captions.py s1   -> <reel>_caps.js  (window.WORDS = per-word times, window.CAPS = 1 to 3 word chunks)
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__)); reel = sys.argv[1]
cues = json.loads(open(os.path.join(here, f'{reel}_tl.js'), encoding='utf8').read()[len('window.TL='):-1])['cues']
heard = json.load(open(os.path.join(here, 'audio', f'{reel}_words.json'), encoding='utf8'))
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())

import difflib
# align every written word to the heard words over the whole narration; unmatched runs share the gap between matches
mine = [(c, w) for c in cues for w in c['text'].split()]
A = [norm(w) for _, w in mine]; B = [norm(w['word']) for w in heard]
T = [None] * len(mine)
for a, b, n in difflib.SequenceMatcher(None, A, B, autojunk=False).get_matching_blocks():
    for k in range(n): T[a + k] = (heard[b + k]['start'], heard[b + k]['end'])
j = 0
while j < len(mine):
    if T[j]: j += 1; continue
    k = j
    while k < len(mine) and not T[k]: k += 1
    c = mine[j][0]
    lo = T[j - 1][1] if j and mine[j - 1][0] is c else c['start']
    hi = T[k][0] if k < len(mine) and mine[k][0] is c else c['end']
    n = [len(A[x]) + 2 for x in range(j, k)]; tot = sum(n); t = lo
    for x, m in zip(range(j, k), n):
        d = (hi - lo) * m / tot; T[x] = (t, t + d); t += d
    print('spread:', ' '.join(mine[x][1] for x in range(j, k)))
    j = k
words, caps = [], []
for (c, w), (a, b) in zip(mine, T):
    words.append({'i': c['i'], 'w': w, 'k': norm(w), 't0': round(a, 3), 't1': round(b, 3)})
for c in cues:
    # chunks: up to 3 words / 17 characters, a new chunk after a comma or full stop
    ln = [w for w in words if w['i'] == c['i']]; cur = []
    for j, w in enumerate(ln):
        if cur and (len(cur) >= 3 or len(' '.join(x['w'] for x in cur + [w])) > 17):
            caps.append(cur); cur = []
        cur.append(w)
        if re.search(r'[,.?]$', w['w']) and j < len(ln) - 1:
            caps.append(cur); cur = []
    if cur: caps.append(cur)

out = []
for j, ch in enumerate(caps):
    nxt = caps[j + 1][0]['t0'] if j + 1 < len(caps) else ch[-1]['t1'] + .4
    end = nxt if nxt - ch[-1]['t1'] < .6 else ch[-1]['t1'] + .35       # hold through short gaps only
    out.append({'i': ch[0]['i'], 't0': ch[0]['t0'], 't1': round(end, 3), 'text': ' '.join(x['w'] for x in ch)})
open(os.path.join(here, f'{reel}_caps.js'), 'w', encoding='utf8').write(
    'window.WORDS=' + json.dumps(words, ensure_ascii=False) + ';\nwindow.CAPS=' + json.dumps(out, ensure_ascii=False) + ';')
print(len(words), 'words,', len(out), 'chunks')
for c in out[:8]: print(c)
