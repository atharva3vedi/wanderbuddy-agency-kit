# Cuts the footage layer from edl.json: one 1080x1920 30 fps piece per shot, joined into footage.mp4.
# Cards get a flat ink piece (the page paints them); boxes and the triptych get their clips in place.
#   python cut.py            -> clips/NN_<id>.mp4 + footage.mp4
#   python cut.py hook,tri   -> re-cut just those shots, then join
import json, os, sys, subprocess
here = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(here, 'edl.json'), encoding='utf8')); FPS = E['fps']
only = sys.argv[1].split(',') if len(sys.argv) > 1 else None
os.makedirs(os.path.join(here, 'clips'), exist_ok=True)
open(os.path.join(here, 'edl.js'), 'w', encoding='utf8').write('window.EDL=' + json.dumps(E, ensure_ascii=False) + ';')   # the page reads it
INK = '0x0C1622'

def frames(s): return round(s['t1'] * FPS) - round(s['t0'] * FPS)

def run(args): subprocess.run(['ffmpeg', '-v', 'error', '-y'] + args, check=True)

def fill(s, n, out):
    d = n / FPS; z0, z1 = s.get('z', [1, 1])
    zoom = f"{z0}+({z1}-{z0})*min(t/{d:.3f},1)"
    vf = (f"fps={FPS},scale=1080:1920:force_original_aspect_ratio=increase:flags=bicubic,"
          f"scale=w='2*trunc(iw*({zoom})/2)':h=-2:eval=frame:flags=bicubic,crop=1080:1920,setsar=1")
    if s.get('bw'): vf += ',hue=s=0,eq=contrast=1.12:brightness=-0.02'
    else: vf += ',eq=saturation=1.06'
    run(['-ss', str(s['in']), '-i', E['src'][s['clip']], '-vf', vf, '-frames:v', str(n), '-an',
         '-c:v', 'libx264', '-preset', 'fast', '-crf', '15', '-pix_fmt', 'yuv420p', out])

def box(s, n, out):
    x, y, w, h = s['box']
    fc = (f"color=c={INK}:s=1080x1920:r={FPS}[bg];[0:v]setpts=PTS/{s.get('speed', 1)},fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase:flags=bicubic,"
          f"crop={w}:{h},setsar=1,{'hue=s=0,eq=contrast=1.12:brightness=-0.02' if s.get('bw') else 'eq=saturation=1.06'}[fg];[bg][fg]overlay={x}:{y}:shortest=1,format=yuv420p")
    run(['-ss', str(s['in']), '-i', E['src'][s['clip']], '-filter_complex', fc, '-frames:v', str(n), '-an',
         '-c:v', 'libx264', '-preset', 'fast', '-crf', '15', out])

def tri(s, n, out):
    x0, y, w, h = s['box']; ins = []; fc = f"color=c={INK}:s=1080x1920:r={FPS}[b0];"
    for k, (clip, t) in enumerate(s['clips']):
        ins += ['-ss', str(t), '-i', E['src'][clip]]
        fc += f"[{k}:v]fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase:flags=bicubic,crop={w}:{h},setsar=1,eq=saturation=1.08[p{k}];"
    for k in range(3):
        fc += f"[b{k}][p{k}]overlay={x0 + k * (w + x0)}:{y}:shortest=1[b{k + 1}];"
    fc += "[b3]format=yuv420p"
    run(ins + ['-filter_complex', fc, '-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '15', out])

def card(s, n, out):
    run(['-f', 'lavfi', '-i', f'color=c={INK}:s=1080x1920:r={FPS}', '-frames:v', str(n), '-c:v', 'libx264', '-preset', 'fast',
         '-crf', '15', '-pix_fmt', 'yuv420p', out])

lst = []
for k, s in enumerate(E['shots']):
    out = os.path.join(here, 'clips', f"{k:02d}_{s['id']}.mp4"); lst.append(out)
    if only and s['id'] not in only and os.path.exists(out): continue
    n = frames(s); {'fill': fill, 'box': box, 'tri': tri, 'card': card}[s['kind']](s, n, out)
    print(f"{s['id']:8s} {n:4d} frames")
open(os.path.join(here, 'clips', 'list.txt'), 'w').write(''.join(f"file '{p.replace(os.sep, '/')}'\n" for p in lst))
run(['-f', 'concat', '-safe', '0', '-i', os.path.join(here, 'clips', 'list.txt'), '-c', 'copy', os.path.join(here, 'footage.mp4')])
r = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0',
                    os.path.join(here, 'footage.mp4')], capture_output=True, text=True).stdout.strip()
print('footage.mp4 frames', r, 'expected', round(E['duration'] * FPS))
