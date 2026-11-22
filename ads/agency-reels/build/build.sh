#!/usr/bin/env bash
# Builds one finished reel: frames -> soundtrack -> mux -> end card -> loudness.
#   bash build.sh r2 WanderBuddy_B2B_Reel2_Post214
# Voice is already in audio/<reel>_vo.wav (vo.py + timeline.py). One render at a time.
set -e
cd "$(dirname "$0")"
PY=~/.cache/hyperframes/tts/venv/Scripts/python
R=$1; NAME=$2; OUT=../out
mkdir -p $OUT
node render.mjs $R --out ${R}_silent.mp4
$PY -I audio.py $R < /dev/null
# reel + end card pictures, crossfading over 0.3 s; the soundtrack (audio/<reel>_mix.wav) already runs across both
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ${R}_silent.mp4)
ffmpeg -v error -y -i ${R}_silent.mp4 -i ../endcard/endcard_silent.mp4 -i audio/${R}_mix.wav -filter_complex   "[0:v]fps=30,format=yuv420p,setsar=1[v0];[1:v]fps=30,format=yuv420p,setsar=1[v1];[v0][v1]xfade=transition=fade:duration=0.3:offset=$(python -c "print(round($D - 0.3, 3))")[v]"   -map "[v]" -map 2:a -c:v libx264 -preset medium -crf 16 -c:a pcm_s16le -shortest ${R}_joined.mkv
# two-pass loudnorm to -14 LUFS (Instagram)
J=$(ffmpeg -hide_banner -i ${R}_joined.mkv -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$J" | grep "\"$1\"" | grep -oE '[-0-9.]+'; }
ffmpeg -v error -y -i ${R}_joined.mkv -map 0:v -map 0:a -c:v copy \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 256k -movflags +faststart $OUT/$NAME.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT/$NAME.mp4
echo wrote $OUT/$NAME.mp4
