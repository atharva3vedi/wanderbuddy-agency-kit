#!/usr/bin/env bash
# Builds the finished reel: footage -> picture -> soundtrack -> mux -> loudness.
#   bash build.sh [name]          (default WanderBuddy_HowWeGotToRevenue)
#   SKIP_CUT=1 bash build.sh      reuse footage.mp4
# Voice is already in audio/s1_vo.wav (vo.py + timeline.py), captions in s1_caps.js (words.py + captions.py).
set -e
cd "$(dirname "$0")"
PY=~/.cache/hyperframes/tts/venv/Scripts/python
NAME=${1:-WanderBuddy_HowWeGotToRevenue}; OUT=../out
mkdir -p $OUT
[ -n "$SKIP_CUT" ] || python cut.py
node render.mjs --out silent.mp4
$PY -I audio.py < /dev/null
ffmpeg -v error -y -i silent.mp4 -i audio/s1_mix.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest joined.mkv
# two-pass loudnorm to -14 LUFS (Instagram)
J=$(ffmpeg -hide_banner -i joined.mkv -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$J" | grep "\"$1\"" | grep -oE '[-0-9.]+'; }
ffmpeg -v error -y -i joined.mkv -map 0:v -map 0:a -c:v copy \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 256k -movflags +faststart $OUT/$NAME.mp4
# a lighter copy for sending to a phone
ffmpeg -v error -y -i $OUT/$NAME.mp4 -c:v libx264 -preset slow -crf 24 -c:a aac -b:a 160k -movflags +faststart $OUT/${NAME}_share.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT/$NAME.mp4
echo wrote $OUT/$NAME.mp4
