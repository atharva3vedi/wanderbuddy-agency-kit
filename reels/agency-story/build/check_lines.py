# Transcribes single takes: python check_lines.py s1 0,3,12
import sys, os, json, subprocess, urllib.request, uuid
sys.stdout.reconfigure(encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__)); reel = sys.argv[1]
spec = json.load(open(os.path.join(here, 'vo', reel, 'lines.json'), encoding='utf8')); folder = spec.get('folder', spec.get('voice', 'troy'))
key = next(l.split('=', 1)[1].strip().strip('"') for l in open(r'C:/Users/PC/Videos/WanderBuddy/.env', encoding='utf8') if l.startswith('GROQ_API_KEY='))
for i in [int(x) for x in sys.argv[2].split(',')]:
    mp3 = os.path.join(here, 'audio', f'_l{i:02d}.mp3')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(here, 'vo', reel, folder, f'l{i:02d}.wav'), '-ac', '1', '-b:a', '64k', mp3], check=True)
    bd = uuid.uuid4().hex
    body = (f'--{bd}\r\nContent-Disposition: form-data; name="model"\r\n\r\nwhisper-large-v3\r\n--{bd}\r\nContent-Disposition: form-data; name="language"\r\n\r\nen\r\n'
            f'--{bd}\r\nContent-Disposition: form-data; name="file"; filename="l.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n').encode() + open(mp3, 'rb').read() + f'\r\n--{bd}--\r\n'.encode()
    req = urllib.request.Request('https://api.groq.com/openai/v1/audio/transcriptions', data=body, headers={'Authorization': 'Bearer ' + key, 'Content-Type': f'multipart/form-data; boundary={bd}', 'User-Agent': 'curl/8.9'})
    print(i, json.loads(urllib.request.urlopen(req, timeout=120).read())['text'])
