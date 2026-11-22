# Transcribes the whole narration in one Groq whisper-large-v3 request, with word times, for the captions.
#   python words.py s1   -> audio/s1_words.json, prints the transcript
import sys, os, json, subprocess, urllib.request, uuid
sys.stdout.reconfigure(encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__)); reel = sys.argv[1]
key = next(l.split('=', 1)[1].strip().strip('"') for l in open(r'C:/Users/PC/Videos/WanderBuddy/.env', encoding='utf8') if l.startswith('GROQ_API_KEY='))
mp3 = os.path.join(here, 'audio', f'{reel}_vo_check.mp3')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(here, 'audio', f'{reel}_vo.wav'), '-ac', '1', '-b:a', '64k', mp3], check=True)
bd = uuid.uuid4().hex
def field(n, v): return f'--{bd}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{v}\r\n'
body = (field('model', 'whisper-large-v3') + field('language', 'en') + field('response_format', 'verbose_json')
        + field('timestamp_granularities[]', 'word') + field('timestamp_granularities[]', 'segment')
        + f'--{bd}\r\nContent-Disposition: form-data; name="file"; filename="vo.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n').encode() + open(mp3, 'rb').read() + f'\r\n--{bd}--\r\n'.encode()
req = urllib.request.Request('https://api.groq.com/openai/v1/audio/transcriptions', data=body, headers={'Authorization': 'Bearer ' + key, 'Content-Type': f'multipart/form-data; boundary={bd}', 'User-Agent': 'curl/8.9'})
r = json.loads(urllib.request.urlopen(req, timeout=120).read())
json.dump(r.get('words', []), open(os.path.join(here, 'audio', f'{reel}_words.json'), 'w', encoding='utf8'), indent=0)
print(r['text']); print(len(r.get('words', [])), 'words')
