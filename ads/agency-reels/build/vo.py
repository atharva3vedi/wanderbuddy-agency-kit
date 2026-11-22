# Narration via Groq Orpheus (voice from lines.json, default troy) (canopylabs/orpheus-v1-english), one request per line.
#   python vo.py r2 [i,j,...]   -> vo/r2/<voice>/lNN.wav (raw takes in vo/r2/<voice>_raw)
import sys, os, json, time, subprocess, urllib.request, urllib.error
sys.stdout.reconfigure(encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__))
reel = sys.argv[1]
key = next(l.split('=', 1)[1].strip().strip('"') for l in open(r'C:/Users/PC/Videos/WanderBuddy/.env', encoding='utf8') if l.startswith('GROQ_API_KEY='))
d = os.path.join(here, 'vo', reel); spec = json.load(open(os.path.join(d, 'lines.json'), encoding='utf8')); voice = spec.get('voice', 'troy')
folder = spec.get('folder', voice)                     # a skit keeps both speakers' lines in one folder
raw, out = os.path.join(d, folder + '_raw'), os.path.join(d, folder)
os.makedirs(raw, exist_ok=True); os.makedirs(out, exist_ok=True)
lines = spec['lines']
only = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else range(len(lines))
# never a pitch change; Troy had the origin-story chain, other voices only a gentle clean-up
chain = 'highpass=f=70,acompressor=threshold=-22dB:ratio=1.8:attack=12:release=180:makeup=1.5' if voice != 'troy' else 'atempo=1.04,highpass=f=60,equalizer=f=140:t=q:w=1:g=2,equalizer=f=4500:t=q:w=1.5:g=-1.5,acompressor=threshold=-24dB:ratio=2:attack=10:release=150:makeup=2'
for i in only:
    say = lines[i].get('say', lines[i]['text']); who = lines[i].get('voice', voice)   # a line can name its own speaker
    body = json.dumps({'model': 'canopylabs/orpheus-v1-english', 'voice': who, 'input': say, 'response_format': 'wav'}).encode()
    data = None
    for attempt in range(6):
        req = urllib.request.Request('https://api.groq.com/openai/v1/audio/speech', data=body, headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json', 'User-Agent': 'curl/8.9'})
        try:
            data = urllib.request.urlopen(req, timeout=60).read(); break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors='replace')
            if e.code == 429 and 'per day' not in msg: time.sleep(10 * (attempt + 1)); continue
            sys.exit(f'line {i}: HTTP {e.code} {msg[:300]}')
    if data is None: sys.exit(f'line {i}: still rate limited')
    open(f'{raw}/l{i:02d}.wav', 'wb').write(data)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{raw}/l{i:02d}.wav', '-af', chain, '-ar', '48000', f'{out}/l{i:02d}.wav'], check=True)
    print(reel, i, who, say)
